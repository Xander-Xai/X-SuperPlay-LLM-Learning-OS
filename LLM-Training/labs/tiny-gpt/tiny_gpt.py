"""CPU teaching GPT: synthetic character vocabulary, not MiniMind/Qwen or a benchmark."""
from __future__ import annotations
import math
import tempfile
from pathlib import Path
import torch
from torch import nn
from torch.nn import functional as F

class CausalAttention(nn.Module):
    def __init__(self, width=32, heads=4, context=12):
        super().__init__()
        if width % heads or width <= 0:
            raise ValueError("width must be divisible by heads")
        self.heads, self.head_dim = heads, width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.project = nn.Linear(width, width)
        self.register_buffer("causal", torch.tril(torch.ones(context, context, dtype=torch.bool)))

    def forward(self, x):
        b, t, c = x.shape
        q, k, v = self.qkv(x).reshape(b,t,3,self.heads,self.head_dim).permute(2,0,3,1,4)
        weights = (q @ k.transpose(-2,-1)) / math.sqrt(self.head_dim)
        weights = torch.softmax(weights.masked_fill(~self.causal[:t,:t],float("-inf")),dim=-1)
        return self.project((weights @ v).transpose(1,2).contiguous().reshape(b,t,c))

class Block(nn.Module):
    def __init__(self,width=32,heads=4,context=12):
        super().__init__()
        self.ln1,self.ln2=nn.LayerNorm(width),nn.LayerNorm(width)
        self.attn=CausalAttention(width,heads,context)
        self.ff=nn.Sequential(nn.Linear(width,4*width),nn.GELU(),nn.Linear(4*width,width))
    def forward(self,x):
        x=x+self.attn(self.ln1(x))
        return x+self.ff(self.ln2(x))

class TinyGPT(nn.Module):
    def __init__(self,vocab_size,context=12,width=32,heads=4,layers=2):
        super().__init__()
        if vocab_size<2 or context<2 or layers<1: raise ValueError("invalid config")
        self.context,self.vocab_size=context,vocab_size
        self.tok,self.pos=nn.Embedding(vocab_size,width),nn.Embedding(context,width)
        self.blocks=nn.Sequential(*(Block(width,heads,context) for _ in range(layers)))
        self.norm,self.head=nn.LayerNorm(width),nn.Linear(width,vocab_size,bias=False)
    def forward(self,ids):
        if ids.ndim!=2 or not 1<=ids.shape[1]<=self.context:
            raise ValueError("expected [B,T], T in 1..context")
        pos=torch.arange(ids.shape[1],device=ids.device)
        return self.head(self.norm(self.blocks(self.tok(ids)+self.pos(pos)[None,:,:])))
    def next_token_loss(self,ids):
        if ids.ndim!=2 or not 2<=ids.shape[1]<=self.context+1:
            raise ValueError("expected [B,T+1] within context")
        logits=self(ids[:,:-1])
        return F.cross_entropy(logits.reshape(-1,self.vocab_size),ids[:,1:].reshape(-1))
    @torch.no_grad()
    def generate(self,ids,n=10):
        if n<0 or ids.ndim!=2 or not ids.shape[1]: raise ValueError("invalid generation")
        old=self.training
        self.eval()
        try:
            for _ in range(n):
                next_id=self(ids[:,-self.context:])[:,-1,:].argmax(dim=-1,keepdim=True)
                ids=torch.cat([ids,next_id],dim=1)
            return ids
        finally: self.train(old)

def toy_tokens():
    text=("hello tiny model! "*60)+("tiny models learn patterns. "*60)
    vocab={c:i for i,c in enumerate(sorted(set(text)))}
    return [vocab[c] for c in text],vocab

def batch(ids,context,size,rng):
    if len(ids)<=context or size<1: raise ValueError("bad batch configuration")
    positions=torch.randint(0,len(ids)-context,(size,),generator=rng).tolist()
    return torch.tensor([ids[p:p+context+1] for p in positions],dtype=torch.long)

def train_smoke(steps=25):
    if steps<1: raise ValueError("steps must be >= 1")
    torch.manual_seed(2026)
    ids,vocab=toy_tokens()
    model=TinyGPT(vocab_size=len(vocab))
    opt=torch.optim.AdamW(model.parameters(),lr=0.008)
    rng=torch.Generator().manual_seed(17)
    # Overfit sanity: reference is included in training, NOT a held-out set.
    reference=batch(ids,model.context,8,rng)
    model.eval()
    with torch.no_grad(): before=float(model.next_token_loss(reference))
    model.train()
    for step in range(steps):
        data=reference if step%2==0 else batch(ids,model.context,8,rng)
        opt.zero_grad(set_to_none=True)
        loss=model.next_token_loss(data)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
        opt.step()
    model.eval()
    with torch.no_grad(): after=float(model.next_token_loss(reference))
    return model,opt,before,after,vocab

def smoke():
    torch.set_num_threads(min(2,torch.get_num_threads()))
    model,opt,before,after,vocab=train_smoke()
    if not after<before: raise RuntimeError("loss did not decrease")
    seq=model.generate(torch.tensor([[vocab["h"]]],dtype=torch.long),n=14)
    decoded="".join({v:k for k,v in vocab.items()}[i] for i in seq[0].tolist())
    with tempfile.TemporaryDirectory() as tmp:
        file=Path(tmp)/"local.pt"
        torch.save({"model":model.state_dict(),"optimizer":opt.state_dict(),
                    "step":25,"torch_rng":torch.get_rng_state()},file)
        copy=TinyGPT(vocab_size=len(vocab)).eval()
        state=torch.load(file,map_location="cpu",weights_only=True)
        copy.load_state_dict(state["model"])
        other_opt=torch.optim.AdamW(copy.parameters(),lr=0.008)
        other_opt.load_state_dict(state["optimizer"])
        torch.testing.assert_close(model(seq[:,:model.context]),copy(seq[:,:model.context]))
        assert bool(other_opt.state_dict()["state"])
    print(f"SYNTHETIC_CHAR_GPT_CPU: training-batch loss {before:.4f} -> {after:.4f}")
    print(f"Argmax generated sequence: {decoded!r}")
    print("Temporary checkpoint model/optimizer reload: PASS")
    print("No BPE, no held-out generalization, no GPU or MiniMind/Qwen training.")

if __name__=="__main__":
    smoke()
