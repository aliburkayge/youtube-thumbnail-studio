"""Build the illustrative README animation; no API calls or user images."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
OUT = HERE / "demo.gif"
W, H = 960, 540
FONT = Path("C:/Windows/Fonts/segoeui.ttf")
BOLD = Path("C:/Windows/Fonts/segoeuib.ttf")


def font(size, bold=False):
    path = BOLD if bold else FONT
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def gradient(c1, c2, width, height):
    image = Image.new("RGB", (width, height))
    d = ImageDraw.Draw(image)
    for x in range(width):
        t = x / max(width - 1, 1)
        color = tuple(round(a * (1 - t) + b * t) for a, b in zip(c1, c2))
        d.line((x, 0, x, height), fill=color)
    return image


def draw_card(base, box, number, phase):
    x, y, w, h = box
    palette = [
        ((91, 37, 188), (232, 68, 140), "WOW!", "01 / HOOK"),
        ((11, 132, 156), (45, 215, 171), "LEVEL UP", "02 / VALUE"),
        ((213, 63, 67), (250, 172, 62), "BEFORE →", "03 / STORY"),
        ((39, 81, 201), (122, 140, 243), "NEXT BIG", "04 / IMPACT"),
    ]
    c1, c2, headline, tag = palette[number]
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x, y, x + w, y + h), radius=16, fill="#1d2542", outline="#435170", width=2)
    if phase < 1:
        d.text((x + 18, y + 16), f"0{number + 1}", font=font(20, True), fill="#77839b")
        d.line((x + 18, y + h - 25, x + w - 18, y + h - 25), fill="#36415e", width=4)
        return
    card = gradient(c1, c2, w - 4, h - 4)
    base.paste(card, (x + 2, y + 2))
    d = ImageDraw.Draw(base)
    d.ellipse((x + w - 115, y + 25, x + w - 5, y + 135), fill=tuple(min(255, v + 23) for v in c2))
    d.text((x + 20, y + 15), tag, font=font(18, True), fill="white")
    d.text((x + 20, y + h - 64), headline, font=font(34 if len(headline) < 10 else 29, True), fill="white")
    d.rounded_rectangle((x + 18, y + h - 22, x + w - 18, y + h - 17), radius=2, fill="#ffffff")


def frame(index):
    image = gradient((11, 17, 39), (19, 30, 59), W, H)
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((24, 22, W - 24, H - 20), radius=28, outline="#344366", width=2)
    d.rounded_rectangle((47, 44, 220, 76), radius=15, fill="#253450")
    d.text((61, 51), "NANO BANANA PRO", font=font(15, True), fill="#82ece5")
    d.text((48, 101), "ONE IDEA. FOUR DIRECTIONS.", font=font(38, True), fill="white")
    d.text((49, 154), "A clearer choice for your next YouTube cover", font=font(20), fill="#aabbd6")

    boxes = [(48, 220, 205, 196), (270, 220, 205, 196), (492, 220, 205, 196), (714, 220, 205, 196)]
    for j, box in enumerate(boxes):
        draw_card(image, box, j, int(index >= 3 + j * 3))

    d = ImageDraw.Draw(image)
    if index < 3:
        status = "01  /  VIDEO BRIEF"
    elif index < 15:
        status = "02  /  FOUR UNIQUE CONCEPTS"
    else:
        status = "03  /  PICK YOUR DIRECTION"
    d.rounded_rectangle((48, 447, 911, 490), radius=14, fill="#1b2845")
    d.text((67, 457), status, font=font(18, True), fill="#b5eee8")
    d.text((724, 457), "gemini-3-pro-image", font=font(14), fill="#a6b6d3")
    if index >= 15:
        active = (index - 15) // 2 % 4
        x, y, w, h = boxes[active]
        d.rounded_rectangle((x - 4, y - 4, x + w + 4, y + h + 4), radius=19, outline="white", width=5)
    return image


frames = [frame(i).quantize(colors=96, method=Image.Quantize.MEDIANCUT) for i in range(23)]
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=[260] * 22 + [1000], loop=0, optimize=True, disposal=2)
print(f"Saved {OUT} ({OUT.stat().st_size:,} bytes)")
