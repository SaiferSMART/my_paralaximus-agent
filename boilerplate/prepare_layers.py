from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ATLAS = ASSETS / "atlas.png"

LAYERS = {
    "background": {"box": (0, 0, 0.5, 0.5), "needs_alpha": False},
    "far": {"box": (0.5, 0, 1, 0.5), "needs_alpha": True},
    "near": {"box": (0, 0.5, 0.5, 1), "needs_alpha": True},
    "mug": {"box": (0.5, 0.5, 1, 1), "needs_alpha": True},
}


def crop_box(width: int, height: int, relative_box: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    left, top, right, bottom = relative_box
    return (
        round(width * left),
        round(height * top),
        round(width * right),
        round(height * bottom),
    )


def alpha_ratio(image: Image.Image) -> float:
    if image.mode != "RGBA":
        return 0
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    transparent = sum(histogram[:245])
    return transparent / (image.width * image.height)


def border_pixels(image: Image.Image, inset: int = 10) -> list[tuple[int, int, int]]:
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels: list[tuple[int, int, int]] = []

    for x in range(width):
      for y in range(inset):
          pixels.append(rgb.getpixel((x, y)))
          pixels.append(rgb.getpixel((x, height - 1 - y)))

    for y in range(height):
      for x in range(inset):
          pixels.append(rgb.getpixel((x, y)))
          pixels.append(rgb.getpixel((width - 1 - x, y)))

    return pixels


def border_flatness(image: Image.Image) -> float:
    sample = Image.new("RGB", (len(border_pixels(image)), 1))
    sample.putdata(border_pixels(image))
    stat = ImageStat.Stat(sample)
    return sum(stat.stddev) / 3


def main() -> None:
    if not ATLAS.exists():
        raise FileNotFoundError(f"Atlas not found: {ATLAS}")

    ASSETS.mkdir(exist_ok=True)
    atlas = Image.open(ATLAS).convert("RGBA")
    width, height = atlas.size
    report = {
        "atlas": str(ATLAS),
        "atlas_size": [width, height],
        "layers": {},
        "note": "This script only crops the single atlas and checks alpha. It does not remove backgrounds locally.",
    }

    for name, config in LAYERS.items():
        layer = atlas.crop(crop_box(width, height, config["box"]))
        alpha = alpha_ratio(layer)
        flatness = border_flatness(layer)
        needs_mcp_remove_background = bool(config["needs_alpha"] and alpha < 0.05)

        output = ASSETS / f"{name}.png"
        layer.save(output)

        report["layers"][name] = {
            "file": str(output),
            "size": [layer.width, layer.height],
            "alpha": round(alpha, 4),
            "border_flatness": round(flatness, 2),
            "action": "cropped_only",
            "needs_mcp_remove_background": needs_mcp_remove_background,
        }

    (ASSETS / "layers-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
