"""只将新动态贴回原始截图指定区域，以 PNG 保留区域外的像素。"""

import argparse
from pathlib import Path

from PIL import Image, ImageOps


def check_box(box, size, label):
    """坐标采用左闭右开的边界，且必须落在图片内。"""
    left, top, right, bottom = box
    width, height = size
    if not (0 <= left < right <= width and 0 <= top < bottom <= height):
        raise ValueError(f"{label} {box} is outside the image or empty ({width}x{height})")


def replace_feed(base_path, patch_path, output, feed_box, source_box, keep_boxes):
    if output.suffix.lower() != ".png":
        raise ValueError("output must have a .png extension")

    with Image.open(base_path) as source_base, Image.open(patch_path) as source_patch:
        base = ImageOps.exif_transpose(source_base)
        patch = ImageOps.exif_transpose(source_patch)
        check_box(feed_box, base.size, "feed box")
        for box in keep_boxes:
            check_box(box, base.size, "keep box")
        if source_box is not None:
            check_box(source_box, patch.size, "source box")
            patch = patch.crop(source_box)

        # 只缩放新内容，保留底图尺寸、透明度和色彩配置。
        mode = "RGBA" if "A" in base.getbands() or "transparency" in base.info else "RGB"
        base = base.convert(mode)
        result = base.copy()
        left, top, right, bottom = feed_box
        result.paste(patch.convert(mode).resize((right - left, bottom - top),
                                                Image.Resampling.LANCZOS), (left, top))
        for box in keep_boxes:
            result.paste(base.crop(box), box[:2])

        result.info.clear()
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as file:
            result.save(file, format="PNG", icc_profile=base.info.get("icc_profile"))
    print(f"{output.resolve()} ({result.width}x{result.height})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--patch", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--feed-box", required=True, type=int, nargs=4,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--source-box", type=int, nargs=4,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--keep-box", action="append", default=[], type=int, nargs=4,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    args = parser.parse_args()
    replace_feed(args.base, args.patch, args.output, args.feed_box, args.source_box, args.keep_box)
