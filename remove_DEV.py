from pathlib import Path
import shutil

directory = Path("files/directory-menu@torchipeppo")

# be very restrictive here to avoid accidents
po = list(directory.glob("po/*"))
for fname in po + [directory/"applet.js", directory/"popup_menu.py"]:
    with open(fname, "r") as f:
        content = f.read()
    content = content.replace("directory-menu-DEV", "directory-menu")
    content = content.replace("torchipeppo-DEV", "torchipeppo")
    with open(fname, "w") as f:
        f.write(content)

# this is a small known file, let's get aggressive
with open(directory/"metadata.json", "r") as f:
    content = f.read()
content = content.replace("-DEV", "")
content = content.replace(" DEV", "")
content = content.replace(" (DEVELOPMENT)", "")
with open(directory/"metadata.json", "w") as f:
    f.write(content)

# reset icon
shutil.copy("icon-standard.png", directory/"icon.png")
