#!/usr/bin/env python3
"""Draw the app icon — a chalk stick figure flexing — and write the PNG sizes
iOS and Android need.

Run from the repo root:  python3 tools/make_icons.py

Everything is drawn at 8x and downsampled with LANCZOS, which is what gives
the strokes clean antialiased edges. PIL has no round line caps, so each
segment gets a circle stamped at both ends.
"""

from PIL import Image, ImageDraw, ImageFilter

INK = (20, 20, 31)
CHALK = (230, 233, 242)
LILAC = (155, 140, 232)

SS = 8            # supersample factor
BASE = 512        # design space
FIG_SCALE = 1.15  # grow the figure about its centre to tighten the margins
FIG_CY = 247      # vertical centre of the figure in design space


OFFSET_Y = 9      # nudge down so the optical centre sits in the middle


def scaled(pt, zoom):
    """Scale a design-space point about the figure centre, then to canvas px."""
    x, y = pt
    x = 256 + (x - 256) * FIG_SCALE * zoom
    y = FIG_CY + (y - FIG_CY) * FIG_SCALE * zoom + OFFSET_Y * zoom
    return x * SS, y * SS


def stroke(draw, pts, width, fill, zoom):
    """Polyline with round caps and joins."""
    px = [scaled(p, zoom) for p in pts]
    w = width * FIG_SCALE * zoom * SS
    draw.line(px, fill=fill, width=int(round(w)))
    for x, y in px:  # round the caps and joins by hand
        r = w / 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def ring(draw, centre, radius, width, fill, zoom):
    cx, cy = scaled(centre, zoom)
    r = radius * FIG_SCALE * zoom * SS
    w = width * FIG_SCALE * zoom * SS
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=int(round(w)))


def dot(draw, centre, radius, fill, zoom):
    cx, cy = scaled(centre, zoom)
    r = radius * FIG_SCALE * zoom * SS
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def render(zoom=1.0):
    """Draw the icon at BASE*SS and return it."""
    side = BASE * SS
    img = Image.new("RGB", (side, side), INK)

    # Soft lilac glow from above, echoing the gradient on the page itself.
    glow = Image.new("RGB", (side, side), INK)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([side * 0.05, -side * 0.42, side * 0.95, side * 0.60],
               fill=(44, 40, 72))
    glow = glow.filter(ImageFilter.GaussianBlur(side * 0.10))
    img = Image.blend(img, glow, 0.85)

    d = ImageDraw.Draw(img)
    W = 22  # stroke weight in design space

    # Head — a thin ring, or the hole closes up at 32px and it reads as a blob
    ring(d, (256, 136), 44, 17, CHALK, zoom)
    # Neck and torso
    stroke(d, [(256, 182), (256, 306)], W, CHALK, zoom)
    # Arms. Upper arms run straight out at shoulder height and the forearms
    # come back up — the flat elbow is what makes this read as a flex rather
    # than as someone just holding their hands in the air.
    stroke(d, [(256, 212), (152, 212), (184, 146)], W, CHALK, zoom)
    stroke(d, [(256, 212), (360, 212), (328, 146)], W, CHALK, zoom)
    # Fists
    dot(d, (184, 146), 15, LILAC, zoom)
    dot(d, (328, 146), 15, LILAC, zoom)
    # Legs, planted wide
    stroke(d, [(256, 306), (212, 392), (192, 400)], W, CHALK, zoom)
    stroke(d, [(256, 306), (300, 392), (320, 400)], W, CHALK, zoom)

    return img


def save(img, size, path):
    img.resize((size, size), Image.LANCZOS).save(path, optimize=True)
    print(f"  {path}  {size}x{size}")


if __name__ == "__main__":
    full = render()
    save(full, 180, "icons/apple-touch-icon.png")
    save(full, 192, "icons/icon-192.png")
    save(full, 512, "icons/icon-512.png")
    save(full, 32, "icons/favicon-32.png")

    # Android may crop a maskable icon to a circle, so this one is drawn
    # smaller to keep the whole figure inside the safe zone.
    save(render(zoom=0.62), 512, "icons/icon-512-maskable.png")
