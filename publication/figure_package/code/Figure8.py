# ============================================================
# Figure 8: Public ARCCRAFT Demonstrator Access
# Supports: Data, code, and reproducibility statement
# Data: Validated public deployment of the integrated demonstrator
# Output: figures/Figure8.png (300 dpi, publication-ready)
# ============================================================

from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H


DEMO_URL = "https://arccraft-research-companion.vercel.app/en/"
OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "Figure8.png"
NAVY_DARK = "#0A1940"


def main() -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=28,
        border=4,
    )
    qr.add_data(DEMO_URL)
    qr.make(fit=True)
    image = qr.make_image(fill_color=NAVY_DARK, back_color="white").convert("RGB")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", dpi=(300, 300))


if __name__ == "__main__":
    main()
