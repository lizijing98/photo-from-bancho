"""将实拍照片与完整 COOKSTA 截图精确拼成 3:4 竖图。依赖 Pillow。"""

import argparse
from pathlib import Path

from PIL import Image, ImageOps


def position(value):
    """裁切对齐位置用 0～1 表示，防止静默接受无效取景参数。"""
    number = float(value)
    if not 0 <= number <= 1:
        raise argparse.ArgumentTypeError("position must be between 0 and 1")
    return number


def compose(photo_path, screenshot_path, output_path, width, centering):
    """照片填满上方余量；截图完整等比缩放，最多产生半像素的取整误差。"""
    if width < 3 or width % 3:
        raise ValueError("width must be a positive multiple of 3")
    output = Path(output_path)
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite: {output}")
    if output.suffix.lower() != ".png":
        raise ValueError("output must have a .png extension")
    height = width * 4 // 3
    with Image.open(photo_path) as source_photo, Image.open(screenshot_path) as source_screen:
        photo = ImageOps.exif_transpose(source_photo).convert("RGB")
        screen = ImageOps.exif_transpose(source_screen).convert("RGB")
        screen_height = max(1, round(width * screen.height / screen.width))
        photo_height = height - screen_height
        if photo_height <= 0:
            raise ValueError("Screenshot is too tall for the 3:4 collage")
        top = ImageOps.fit(photo, (width, photo_height), method=Image.Resampling.LANCZOS,
                           centering=centering)
        bottom = screen.resize((width, screen_height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (width, height))
        canvas.paste(top, (0, 0))
        canvas.paste(bottom, (0, photo_height))
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output, format="PNG")
    print(f"{output.resolve()} ({width}x{height}; photo={photo_height}, screenshot={screen_height})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photo", required=True, type=Path)
    parser.add_argument("--screenshot", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--width", type=int, default=1536)
    parser.add_argument("--photo-position-x", type=position, default=0.5)
    parser.add_argument("--photo-position-y", type=position, default=0.5)
    args = parser.parse_args()
    compose(args.photo, args.screenshot, args.output, args.width,
            (args.photo_position_x, args.photo_position_y))
