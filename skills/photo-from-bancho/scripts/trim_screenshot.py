"""在白色手机内容面板下边缘裁齐截图；坐标由查看当前图片后确定。"""

import argparse
from pathlib import Path

from PIL import Image


def trim(source, output, bottom):
    """保留 [0, bottom) 行，不缩放、不重绘，也不覆盖原图。"""
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite: {output}")
    if output.suffix.lower() != ".png":
        raise ValueError("output must have a .png extension")
    with Image.open(source) as image:
        if not 0 < bottom <= image.height:
            raise ValueError("bottom must be within the image height")
        cropped = image.crop((0, 0, image.width, bottom))
        output.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(output, format="PNG")
        print(f"{output.resolve()} ({cropped.width}x{cropped.height})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bottom", required=True, type=int)
    args = parser.parse_args()
    trim(args.input, args.output, args.bottom)
