"""CPU-only TinyGPT tests, not a production model validation."""
import tempfile
import unittest
from pathlib import Path
import torch
from tiny_gpt import TinyGPT,toy_tokens,batch,train_smoke

class TinyGPTTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(min(2,torch.get_num_threads()))
    def test_logits_shape(self):
        m=TinyGPT(20,context=8,width=16,heads=4,layers=1)
        self.assertEqual(tuple(m(torch.randint(0,20,(2,8))).shape),(2,8,20))
    def test_future_does_not_leak_into_past(self):
        torch.manual_seed(1)
        m=TinyGPT(20,context=8,width=16,heads=4,layers=2).eval()
        a=torch.randint(0,20,(1,8))
        b=a.clone()
        b[0,5:]=(b[0,5:]+1)%20
        with torch.no_grad():
            torch.testing.assert_close(m(a)[:,:5],m(b)[:,:5],atol=1e-6,rtol=1e-6)
    def test_exactly_one_token_shift(self):
        m=TinyGPT(12,context=6,width=16,heads=4,layers=1)
        x=torch.tensor([[1,2,3,4,5,6,7]])
        logits=m(x[:,:-1])
        expected=torch.nn.functional.cross_entropy(logits.reshape(-1,12),x[:,1:].reshape(-1))
        torch.testing.assert_close(m.next_token_loss(x),expected)
    def test_backward_reaches_qkv(self):
        m=TinyGPT(12,context=6,width=16,heads=4,layers=1)
        m.next_token_loss(torch.randint(0,12,(2,7))).backward()
        self.assertGreater(float(m.blocks[0].attn.qkv.weight.grad.abs().sum()),0)
    def test_fixed_train_batch_loss_decreases(self):
        _,_,before,after,_=train_smoke(steps=15)
        self.assertLess(after,before)
    def test_checkpoint_and_optimizer_roundtrip(self):
        m=TinyGPT(12,context=6,width=16,heads=4,layers=1)
        opt=torch.optim.AdamW(m.parameters(),lr=1e-3)
        ids=torch.randint(0,12,(2,7))
        m.next_token_loss(ids).backward()
        opt.step()
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/"state.pt"
            torch.save({"model":m.state_dict(),"opt":opt.state_dict()},file)
            other=TinyGPT(12,context=6,width=16,heads=4,layers=1)
            other_opt=torch.optim.AdamW(other.parameters(),lr=1e-3)
            saved=torch.load(file,map_location="cpu",weights_only=True)
            other.load_state_dict(saved["model"])
            other_opt.load_state_dict(saved["opt"])
            with torch.no_grad():
                torch.testing.assert_close(m(ids[:,:-1]),other(ids[:,:-1]))
            self.assertTrue(other_opt.state_dict()["state"])
    def test_bad_dimensions_fail(self):
        with self.assertRaises(ValueError): TinyGPT(10,width=15,heads=4)
        m=TinyGPT(10,context=4)
        with self.assertRaises(ValueError): m(torch.randint(0,10,(1,5)))
        with self.assertRaises(ValueError): m.next_token_loss(torch.randint(0,10,(1,7)))
    def test_sampling_and_generation_shapes(self):
        ids,vocab=toy_tokens()
        rng=torch.Generator().manual_seed(3)
        x=batch(ids,8,2,rng)
        self.assertEqual(tuple(x.shape),(2,9))
        m=TinyGPT(len(vocab),context=8)
        self.assertEqual(tuple(m.generate(x[:,:1],n=10).shape),(2,11))

if __name__=="__main__":
    unittest.main()
