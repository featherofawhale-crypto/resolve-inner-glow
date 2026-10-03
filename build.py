"""Build the standalone Inner Glow Fusion template with Python's standard library."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "内发光.drfx"
FILES = ("内发光.setting", "内发光.png")
PREFIX = "Edit/Effects/WREN/"
ZIP_DATE = (2026, 10, 3, 21, 54, 32)


def build() -> str:
    source = (ROOT / FILES[0]).read_text(encoding="utf-8")
    for forbidden in ("Loader {", "RunScript", "os.execute", "io.popen", "/Users/", "https://"):
        if forbidden in source:
            raise ValueError(f"Unexpected dependency in template: {forbidden}")
    with zipfile.ZipFile(PACKAGE, "w") as archive:
        for name in FILES:
            info = zipfile.ZipInfo(PREFIX + name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, (ROOT / name).read_bytes())
    digest = hashlib.sha256(PACKAGE.read_bytes()).hexdigest()
    (ROOT / "SHA256SUMS.txt").write_text(f"{digest}  {PACKAGE.name}\n", encoding="utf-8")
    return digest


if __name__ == "__main__":
    print(f"{PACKAGE.name}  SHA256 {build()}")
