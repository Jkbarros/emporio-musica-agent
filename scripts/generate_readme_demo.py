#!/usr/bin/env python3
"""Gera docs/demo.gif para o README (mock da UI Streamlit + ferramentas)."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    raise SystemExit("Instale Pillow: pip install pillow") from e

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "demo.gif"

W, H = 720, 420
SIDEBAR_W = 200
BG = (250, 250, 252)
SIDEBAR = (240, 242, 246)
TEXT = (38, 39, 48)
MUTED = (120, 124, 140)
USER_BUBBLE = (240, 242, 246)
BOT_BUBBLE = (230, 245, 255)
ACCENT = (255, 75, 75)
TOOL_BG = (255, 248, 220)
TOOL_BORDER = (230, 200, 120)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    path = candidates[0 if not bold else 0]
    for p in candidates:
        if Path(p).exists():
            path = p
            break
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def _draw_frame(
    user: str | None,
    bot: str | None,
    tools: str | None,
    caption: str,
) -> Image.Image:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    title_f = _font(18, bold=True)
    body_f = _font(14)
    cap_f = _font(12)
    small_f = _font(11)

    d.rectangle((0, 0, SIDEBAR_W, H), fill=SIDEBAR)
    d.line((SIDEBAR_W, 0, SIDEBAR_W, H), fill=(210, 214, 220))
    d.text((16, 20), "Empório da Música", fill=TEXT, font=title_f)
    d.text((16, 48), "Atendente: Lúcia", fill=MUTED, font=small_f)
    d.rounded_rectangle((16, 78, SIDEBAR_W - 16, 108), radius=6, fill=(255, 255, 255), outline=(210, 214, 220))
    d.text((28, 88), "+ Nova conversa", fill=TEXT, font=small_f)
    d.text((16, 130), "Idioma: Português", fill=MUTED, font=small_f)

    main_x = SIDEBAR_W + 24
    d.text((main_x, 16), "🎸 Empório da Música", fill=TEXT, font=title_f)
    d.text((main_x, 44), "Converse com a Lúcia, nossa assistente virtual.", fill=MUTED, font=small_f)

    y = 78
    bubble_w = W - SIDEBAR_W - 48

    if user:
        lines = _wrap(d, user, body_f, bubble_w - 24)
        bh = 16 + len(lines) * 18
        d.rounded_rectangle((main_x + 80, y, main_x + bubble_w, y + bh), radius=10, fill=USER_BUBBLE)
        ty = y + 8
        for line in lines:
            d.text((main_x + 92, ty), line, fill=TEXT, font=body_f)
            ty += 18
        y += bh + 12

    if bot:
        lines = _wrap(d, bot, body_f, bubble_w - 24)
        bh = 16 + len(lines) * 18
        d.rounded_rectangle((main_x, y, main_x + bubble_w - 60, y + bh), radius=10, fill=BOT_BUBBLE)
        ty = y + 8
        for line in lines:
            d.text((main_x + 12, ty), line, fill=TEXT, font=body_f)
            ty += 18
        y += bh + 10

    if tools:
        lines = _wrap(d, f"🔧 {tools}", small_f, bubble_w - 32)
        th = 12 + len(lines) * 16
        d.rounded_rectangle((main_x, y, main_x + bubble_w - 40, y + th), radius=8, fill=TOOL_BG, outline=TOOL_BORDER)
        ty = y + 6
        for line in lines:
            d.text((main_x + 10, ty), line, fill=(90, 70, 20), font=small_f)
            ty += 16

    d.rectangle((0, H - 28, W, H), fill=(32, 36, 48))
    d.text((16, H - 22), caption, fill=(220, 224, 232), font=cap_f)
    return im


def main() -> None:
    frames = [
        _draw_frame(
            "Tem violão até R$ 1.000?",
            None,
            None,
            "Catálogo — pergunta do cliente",
        ),
        _draw_frame(
            "Tem violão até R$ 1.000?",
            "Encontrei 3 violões nessa faixa. O Yamaha F310 está em promoção.",
            "buscar_produtos(termo=violão, preco_max=1000)",
            "Resposta com busca no catálogo",
        ),
        _draw_frame(
            "Posso devolver se me arrepender?",
            "Sim, conforme o manual: até 7 dias em perfeito estado.",
            "consultar_politicas(pergunta=devolução)",
            "Políticas via RAG no PDF",
        ),
        _draw_frame(
            "Status do pedido #1042",
            "Para sua segurança, confirme o e-mail cadastrado no pedido.",
            "listar_pedidos_do_cliente",
            "Pedidos com validação de identidade",
        ),
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=2200,
        loop=0,
        optimize=True,
    )
    print(f"Gerado: {OUT} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
