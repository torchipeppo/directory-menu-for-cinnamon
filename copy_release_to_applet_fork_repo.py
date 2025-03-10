"""
Copy all files to release into my fork of cinnamon-spices-applets.

An upgrade over the ole remove-DEV.py in that I don't have to change the dev repo
and undo the changes immediately after.

(not copying readme and icon b/c they're a little different b/w versions)
"""

from pathlib import Path
import shutil
import json
import re

# get UUIDs
with open("files/directory-menu@torchipeppo/metadata.json", "r") as f:
    develop_uuid = json.load(f)["uuid"]
with open("files/directory-menu@torchipeppo/metadata-RELEASE.json", "r") as f:
    release_uuid = json.load(f)["uuid"]



VERSION_DIR_PATTERN = re.compile(r"[0123456789.]+")

def copy_replacing_uuid(src, dst):
    with open(src, "r") as f:
        content = f.read()
    content = content.replace(develop_uuid, release_uuid)
    with open(dst, "w") as f:
        f.write(content)

def copy_code_dir(src : Path, dst : Path):
    dst.mkdir(exist_ok=True)
    for p in src.iterdir():
        if (
            not p.is_dir()
            and (
                p.suffix == ".js"
                or p.suffix == ".py"
                or (p.suffix == ".json" and "metadata" not in p.stem)
            )
        ):
            if p.is_symlink():
                dst_file = dst / p.name
                if dst_file.exists():
                    dst_file.unlink()
                shutil.copy(p, dst_file, follow_symlinks=False)
            else:
                copy_replacing_uuid(p, dst/p.name)

        elif (p.is_dir() and re.match(VERSION_DIR_PATTERN, p.name)):
            copy_code_dir(src / p.name, dst / p.name)



# step 1: files here

src_dir = Path(__file__).resolve().parent
dst_dir = src_dir.parent / "cinnamon repo forks/cinnamon-spices-applets" / release_uuid
dst_dir.mkdir(exist_ok=True)

for fname in ["info.json", "screenshot.png", "LICENSE", "test_popup_menu.py"]:
    shutil.copy(src_dir/fname, dst_dir)



# step 2: code

src_dir = src_dir / "files" / "directory-menu@torchipeppo"
dst_dir = dst_dir / "files" / release_uuid
dst_dir.mkdir(exist_ok=True, parents=True)

shutil.copy(src_dir/"metadata-RELEASE.json", dst_dir/"metadata.json")
copy_code_dir(src_dir, dst_dir)



# step 3: translations

src_dir = src_dir / "po"
dst_dir = dst_dir / "po"
dst_dir.mkdir(exist_ok=True)

copy_replacing_uuid(src_dir/f"{develop_uuid}.pot", dst_dir/f"{release_uuid}.pot")
for p in src_dir.iterdir():
    if p.suffix == ".po":
        copy_replacing_uuid(p, dst_dir/p.name)
