#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path
import zipfile

# Root directory of the repository
ROOT_DIR = Path(__file__).parent.resolve()

# Set up isolated home directory and carts path for PICO-8
P8_HOME = (ROOT_DIR / "tmp" / "p8").resolve()
CARTS_DIR = P8_HOME / "carts"
BUILD_DIR = ROOT_DIR / "build"
EXPORT_DIR = ROOT_DIR / "picogreed.bin"

# Prepare directories
shutil.rmtree(P8_HOME, ignore_errors=True)
CARTS_DIR.mkdir(parents=True, exist_ok=True)
shutil.rmtree(BUILD_DIR, ignore_errors=True)
BUILD_DIR.mkdir(exist_ok=True)

# Symlink the cartridge into PICO-8's carts directory
cart_link = CARTS_DIR / "picogreed.p8"
cart_link.symlink_to(ROOT_DIR / "picogreed.p8")

# Base command passes the isolated home and relative cart name
PICO8_BASE_CMD = ["pico8", "-home", P8_HOME.as_posix(), "picogreed.p8"]

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

# Process HTML output
html_file = ROOT_DIR / "picogreed.html"
html_file.write_text(
    html_file.read_text(encoding="utf-8").replace("PICO-8 Cartridge", "PicoGreed"),
    encoding="utf-8",
)

# Bundle Web build
web_zip = ROOT_DIR / "picogreed_web.zip"
with zipfile.ZipFile(web_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write(ROOT_DIR / "picogreed.html", arcname="index.html")
    zf.write(ROOT_DIR / "picogreed.js", arcname="picogreed.js")

shutil.move(web_zip, BUILD_DIR / "picogreed_web.zip")

(ROOT_DIR / "picogreed.html").unlink(missing_ok=True)
(ROOT_DIR / "picogreed.js").unlink(missing_ok=True)

# Move ZIP files to build/
for zip_file in EXPORT_DIR.glob("*.zip"):
    shutil.move(str(zip_file), BUILD_DIR / zip_file.name)

# Move exported PNG
shutil.move(ROOT_DIR / "picogreed.p8.png", BUILD_DIR / "picogreed.p8.png")

# Clean up temporary directories
shutil.rmtree(P8_HOME, ignore_errors=True)
if EXPORT_DIR.exists():
    shutil.rmtree(EXPORT_DIR)