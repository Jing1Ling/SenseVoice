import torch
import  habana_frameworks.torch as htorch
import torch.nn.functional as F
from tqdm import tqdm

class Buckets:

    def __init__(self, feature_dim=560):
        self.feature_dim = feature_dim
        self.device = "hpu"
        self.buckets = [32, 64, 96, 128, 192, 256, 512, 768, 1024, 1536]
        print(f"Created buckets:{self.buckets}")
    
    def warmup_encoder(self, encoder, repeat=3):
        print(f"Warmup encoder graph for {len(self.buckets)} buckets...")
        for frames in tqdm(self.buckets):
            x = torch.randn(1, frames, self.feature_dim, device=self.device)
            x_len = torch.tensor([frames], dtype=torch.int32, device=self.device)
            for i in range(repeat):
                with torch.no_grad():
                    _ = encoder(x, x_len)
        print("Encoder graph warmup complete.")
    
    def pad_to_buckets(self, speech):
        assert len(speech.shape) == 3  # (bs, frame, feat)
        frame = speech.shape[1]
        if frame in self.buckets or frame > self.buckets[-1]:
            return speech
        for bucket in self.buckets:
            if frame < bucket:
                speech = F.pad(speech, (0, 0, 0, max(0, bucket - frame)))
                return speech