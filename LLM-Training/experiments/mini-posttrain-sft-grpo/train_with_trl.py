"""Optional REAL small-model SFT -> GRPO training; NOT executed by CI.

Requires a user-installed, compatible CUDA/TRL/PyTorch stack and model download.
The dataset/reward code runs independently using only the Python standard library.
"""
from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import sys
from data_and_reward import exact_reward, samples, validate_splits, parse_answer

PACKAGE_NAMES = ("torch", "transformers", "trl", "peft", "datasets", "accelerate")


def package_versions() -> dict[str, str]:
    versions = {}
    for package in PACKAGE_NAMES:
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "MISSING"
    return versions


def ensure_runtime(require_gpu: bool):
    missing = [key for key, value in package_versions().items() if value == "MISSING"]
    if missing:
        raise RuntimeError(f"Missing packages: {missing}; see README for compatible installs")
    import torch
    if require_gpu and not torch.cuda.is_available():
        raise RuntimeError("No CUDA GPU visible; do not claim real training has run")
    from datasets import Dataset
    from peft import AutoPeftModelForCausalLM, LoraConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer, SFTConfig, SFTTrainer
    return torch, Dataset, AutoPeftModelForCausalLM, LoraConfig, AutoModelForCausalLM, AutoTokenizer, GRPOConfig, GRPOTrainer, SFTConfig, SFTTrainer


def write_manifest(output: Path, config: dict):
    output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "status": "STARTED_NOT_VERIFIED",
        "kind": "REAL_MODEL_RUN_REQUIRES_LOG_EVIDENCE",
        "config": config,
        "versions": package_versions(),
        "data": validate_splits(),
    }
    (output / "run-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def run_sft(args):
    (torch, Dataset, _, LoraConfig, AutoModel, Tokenizer, _, _, SFTConfig, SFTTrainer) = ensure_runtime(True)
    save_dir = Path(args.output) / "sft"
    write_manifest(save_dir, vars(args))
    tokenizer = Tokenizer.from_pretrained(args.model, revision=args.revision)
    model = AutoModel.from_pretrained(args.model, revision=args.revision, dtype="auto")
    train = Dataset.from_list([{"prompt": r["prompt"], "completion": r["completion"]} for r in samples("train")])
    dev = Dataset.from_list([{"prompt": r["prompt"], "completion": r["completion"]} for r in samples("dev")])
    config = SFTConfig(
        output_dir=str(save_dir),
        max_steps=args.steps,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=1e-4,
        max_length=128,
        completion_only_loss=True,
        logging_steps=1,
        save_strategy="no",
        report_to="none",
        seed=args.seed,
        bf16=torch.cuda.is_bf16_supported(),
    )
    trainer = SFTTrainer(
        model=model, args=config, train_dataset=train, eval_dataset=dev,
        processing_class=tokenizer,
        peft_config=LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM"),
    )
    trainer.train()
    trainer.save_model(str(save_dir))
    trainer.processing_class.save_pretrained(str(save_dir))
    print(json.dumps({"stage": "SFT_FINISHED_REQUIRES_HELDOUT_EVAL", "adapter": str(save_dir), "steps": args.steps}))


def run_grpo(args):
    (torch, Dataset, AutoPeft, _, _, _, GRPOConfig, GRPOTrainer, _, _) = ensure_runtime(True)
    sft_dir = Path(args.output) / "sft"
    if not (sft_dir / "adapter_config.json").is_file():
        raise RuntimeError(f"Missing SFT adapter: {sft_dir}; run --mode sft first")
    save_dir = Path(args.output) / "grpo"
    write_manifest(save_dir, vars(args))
    model = AutoPeft.from_pretrained(str(sft_dir), is_trainable=True)
    train = Dataset.from_list([{"prompt": r["prompt"], "answer": r["answer"]} for r in samples("train")])
    config = GRPOConfig(
        output_dir=str(save_dir),
        max_steps=args.steps,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=2,
        num_generations=2,
        max_completion_length=48,
        learning_rate=1e-5,
        logging_steps=1,
        save_strategy="no",
        report_to="none",
        seed=args.seed,
        use_vllm=False,
        bf16=torch.cuda.is_bf16_supported(),
        beta=0.0,  # Explicitly no reference-model KL in this first micro experiment
    )
    trainer = GRPOTrainer(model=model, args=config, train_dataset=train, reward_funcs=exact_reward)
    trainer.train()
    trainer.save_model(str(save_dir))
    print(json.dumps({"stage": "GRPO_FINISHED_REQUIRES_HELDOUT_EVAL", "adapter": str(save_dir), "steps": args.steps}))


def evaluate(args):
    (torch, _, AutoPeft, _, AutoModel, Tokenizer, _, _, _, _) = ensure_runtime(False)
    checkpoint = args.checkpoint
    if checkpoint == "base":
        model = AutoModel.from_pretrained(args.model, revision=args.revision, dtype="auto")
    else:
        save_dir = Path(args.output) / checkpoint
        if not (save_dir / "adapter_config.json").is_file():
            raise RuntimeError(f"Missing adapter: {save_dir}")
        model = AutoPeft.from_pretrained(str(save_dir), is_trainable=False)
    tokenizer = Tokenizer.from_pretrained(args.model, revision=args.revision)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    success, errors = 0, []
    # Dev is repeatable; final test is to be used once after tuning is frozen.
    for row in samples(args.split):
        inputs = tokenizer(row["prompt"], return_tensors="pt").to(device)
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=48, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        completion = tokenizer.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        ok = parse_answer(completion) == int(row["answer"])
        success += int(ok)
        if not ok:
            errors.append({"task_id": row["task_id"], "expected": row["answer"], "output": completion})
    result = {
        "checkpoint": checkpoint, "split": args.split,
        "n": len(samples(args.split)), "correct": success,
        "accuracy": round(success / len(samples(args.split)), 4),
        "first_10_failures": errors[:10], "data_sha256": validate_splits()[args.split]["sha256"],
        "status": "OBSERVED_IF_RUN_AND_LOG_SAVED_NOT_A_PREDECLARED_RESULT",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["data-check", "preflight", "sft", "grpo", "eval"], required=True)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--revision", default="main", help="Replace with pinned model commit SHA for formal runs")
    parser.add_argument("--output", default="runs/mini-sft-grpo")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--checkpoint", choices=["base", "sft", "grpo"], default="base")
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be >= 1")
    if args.mode == "data-check":
        print(json.dumps(validate_splits(), indent=2))
    elif args.mode == "preflight":
        print(json.dumps({"packages": package_versions(), "splits": validate_splits(), "status": "DEPENDENCY_CHECK_NOT_TRAINING"}, indent=2))
    elif args.mode == "sft":
        run_sft(args)
    elif args.mode == "grpo":
        run_grpo(args)
    elif args.mode == "eval":
        evaluate(args)


if __name__ == "__main__":
    main()
