from model import SenseVoiceSmall
import torch
import habana_frameworks.torch as htorch
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import torch
import habana_frameworks.torch as htorch
from utils.gaudi_extension import Buckets
import time
import os

model_dir = "iic/SenseVoiceSmall"
m, kwargs = SenseVoiceSmall.from_pretrained(model=model_dir, device="hpu")
lazy_mode = os.getenv("PT_HPU_LAZY_MODE", "0") == "1"
skip_warmup = os.getenv("SKIP_HPU_WARMUP", "0") == "1"

if lazy_mode:
    m.encoder=htorch.hpu.wrap_in_hpu_graph(m.encoder)
    m.buckets = Buckets()
    if not skip_warmup:
        t1 = time.perf_counter()
        m.buckets.warmup_encoder(m.encoder)
        t2 = time.perf_counter()
        print(f"warmup time: {t2-t1}")
m.eval()

res = m.inference(
    data_in=f"{kwargs ['model_path']}/example/zh.mp3",
    language="zh", # "zh", "en", "yue", "ja", "ko", "nospeech"
    use_itn=True,
    ban_emo_unk=False,
    **kwargs,
)
res = m.inference(
    data_in=f"{kwargs ['model_path']}/example/zh.mp3",
    language="zh", # "zh", "en", "yue", "ja", "ko", "nospeech"
    use_itn=True,
    ban_emo_unk=False,
    data_lengths=torch.tensor([760]),
    **kwargs,
)

text = rich_transcription_postprocess(res [0][0]["text"])
print(text)
