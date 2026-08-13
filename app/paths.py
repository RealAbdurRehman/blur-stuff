from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

FACE_MODEL = MODELS_DIR / "faces.pt"
PLATE_MODEL = MODELS_DIR / "plates.pt"
NANOTRACK_HEAD = MODELS_DIR / "nanotrack_head_sim.onnx"
NANOTRACK_BACKBONE = MODELS_DIR / "nanotrack_backbone_sim.onnx"
