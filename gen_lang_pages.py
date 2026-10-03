#!/usr/bin/env python3
"""Sinh link riêng theo ngôn ngữ cho trang web giới thiệu (03/10/2026).

    index.html      → tiếng Việt (mặc định, không có tiền tố)
    en/index.html   → tiếng Anh   (…/en/)
    vi/index.html   → tiếng Việt  (…/vi/)

Chỉ sửa ``index.html``; chạy lại script này sau mỗi lần sửa để hai bản
``en/`` và ``vi/`` khớp:

    python3 brand/web/gen_lang_pages.py

Bản sinh ra giống hệt ``index.html``, chỉ đổi đường dẫn ảnh / favicon lùi một
cấp (``../``) và thẻ ``<html lang>``. Ngôn ngữ hiện ra do script trong trang
đọc từ đường dẫn (``/en`` → tiếng Anh).
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'index.html'

# Tài nguyên tương đối trong index.html — ở thư mục con phải lùi một cấp.
RELATIVE = [
    ('href="favicon/', 'href="../favicon/'),
    ('src="logo_in_app_login_shop.png"', 'src="../logo_in_app_login_shop.png"'),
]


def build(lang: str) -> None:
    html = SOURCE.read_text(encoding='utf-8')
    for old, new in RELATIVE:
        if old not in html:
            raise SystemExit(f'Không thấy {old!r} trong index.html — sửa RELATIVE trong script.')
        html = html.replace(old, new)
    html = html.replace('<html lang="vi">', f'<html lang="{lang}">', 1)
    html = html.replace(
        '<head>',
        '<head>\n    <!-- SINH TỰ ĐỘNG từ ../index.html bằng gen_lang_pages.py — đừng sửa tay. -->',
        1,
    )
    out = HERE / lang / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'đã ghi {out.relative_to(HERE)}')


if __name__ == '__main__':
    for lang in ('en', 'vi'):
        build(lang)
