import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from huggingface_hub import snapshot_download

# 你的模型保存目录
CACHE_PATH = r"G:\MinerU_Models"

# ----------------下载2个小仓库（全部文件很小，无多余资源）
small_repos = [
    "unstructuredio/yolo_x_layout",
    "opendatalab/MinerU-Clipper"
]
for repo in small_repos:
    print(f"下载 {repo}")
    snapshot_download(
        repo_id=repo,
        cache_dir=CACHE_PATH,
        resume_download=True,
        local_dir_use_symlinks=False
    )

# ----------------下载主模型，过滤掉全部外文OCR
print("开始下载 PDF‑Extract‑Kit‑1.0【中文精简版】")
snapshot_download(
    repo_id="opendatalab/PDF-Extract-Kit-1.0",
    cache_dir=CACHE_PATH,
    resume_download=True,
    local_dir_use_symlinks=False,
    # 黑名单：所有非中文OCR文件，禁止下载
    ignore_patterns=[
        "models/OCR/PaddleOCR/arabic*",
        "models/OCR/PaddleOCR/cyrillic*",
        "models/OCR/PaddleOCR/devanagari*",
        "models/OCR/PaddleOCR/el_*",
        "models/OCR/PaddleOCR/japan*",
        "models/OCR/PaddleOCR/korean*",
        "models/OCR/PaddleOCR/thai*",
        "models/OCR/PaddleOCR/vietnamese*",
        "models/OCR/PaddleOCR/latin*",
        "models/OCR/PaddleOCR/fr_*",
        "models/OCR/PaddleOCR/german*",
        "models/OCR/PaddleOCR/*_PP-OCRv5_rec_infer.pth",
        "models/OCR/PaddleOCR/*_PP-OCRv4_rec_server_infer.pth"
    ]
)

print("✅最小中文离线包下载完成")
