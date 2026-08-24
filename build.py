#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path
import zipfile

ROOT_DIR = Path(__file__).parent.resolve()

# Resolve ./tmp/p8 as an absolute path inside the project
P8_HOME = (ROOT_DIR / "tmp" / "p8").resolve()
BUILD_DIR = ROOT_DIR / "build"
EXPORT_DIR = ROOT_DIR / "picogreed.bin"
P8_FILE = (ROOT_DIR / "picogreed.p8").as_posix()

# Prepare directories
P8_HOME.mkdir(parents=True, exist_ok=True)
shutil.rmtree(BUILD_DIR, ignore_errors=True)
BUILD_DIR.mkdir(exist_ok=True)

# Base PICO-8 execution command with isolated home directory
PICO8_BASE_CMD = ["pico8", "-home", P8_HOME.as_posix(), P8_FILE]

# Run Pico-8 exports
subprocess.run(
    [*PICO8_BASE_CMD, "-export", "picogreed.bin -i 64 -c 16"],
    check=True,
)

subprocess.run(
    [*PICO8_BASE_CMD, "-export", "picogreed.p8.png"],
    check=True,
)

subprocess.run(
    [*PICO8_BASE_CMD, "-export", "picogreed.html"],
    check=True,
)

Path("./picogreed.html").write_text(
    Path("./picogreed.html")
    .read_text(encoding="utf-8")
    .replace("PICO-8 Cartridge", "PicoGreed"),
    encoding="utf-8",
)

with zipfile.ZipFile("picogreed_web.zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write("./picogreed.html", arcname="index.html")
    zf.write("./picogreed.js", arcname="picogreed.js")

shutil.move("picogreed_web.zip", BUILD_DIR / "picogreed_web.zip")

Path("./picogreed.html").unlink(missing_ok=True)
Path("./picogreed.js").unlink(missing_ok=True)

# Move ZIP files to build/
for zip_file in EXPORT_DIR.glob("*.zip"):
    shutil.move(str(zip_file), BUILD_DIR / zip_file.name)

# Move exported PNG
shutil.move("picogreed.p8.png", BUILD_DIR / "picogreed.p8.png")

# Remove export directory
if EXPORT_DIR.exists():
    shutil.rmtree(EXPORT_DIR)
