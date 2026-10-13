"""Create website media copies without changing original assets."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json
import sys
import argparse

ROOT = Path(__file__).parent
SOURCE = Path(r'C:\landing-celebre\media')
OUTPUT = ROOT / 'assets'
OUTPUT.mkdir(exist_ok=True)
FILES = {
    'hero': 'A&F-2232.jpg',
    'carrinho': 'WhatsApp Image 2026-09-22 at 11.59.45.jpeg',
    'balcao': '561e1542-041f-46c9-9765-7cdeb3972659.jpg',
    'preparo': '0602 (1)(13).png',
    'morango': '0602 (1)(6).png',
    'oreo': 'IMG_0977.PNG',
    'favoritos': r'C:\Users\vinim\Downloads\IMG_2684.HEIC',
    'detalhes': r'C:\Users\vinim\Downloads\IMG_2880.png',
    'equipe': 'IMG_0963.PNG',
    'casamento': 'A&F-2238.jpg',
}
report = []
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only', choices=FILES, help='Prepare one image family and preserve every other asset.')
options = parser.parse_args()

def open_reference(filename):
    reference = Path(filename)
    if not reference.is_absolute():
        reference = SOURCE / reference
    if reference.suffix.lower() in ['.heic', '.heif']:
        # HEIC support is provided by pillow-heif, when installed globally or locally.
        sys.path.insert(0, str(ROOT / '.image-tools'))
        try:
            import pillow_heif
        except ModuleNotFoundError as error:
            raise RuntimeError('HEIC input requires pillow-heif in this Python environment.') from error
        pillow_heif.register_heif_opener()
    return ImageOps.exif_transpose(Image.open(reference))

def record(path, image):
    report.append({'file': path.name, 'width': image.width, 'height': image.height, 'bytes': path.stat().st_size})

for name, filename in FILES.items():
    if options.only and name != options.only:
        continue
    original = open_reference(filename)
    color_profile = original.info.get('icc_profile', b'')
    if original.mode == 'RGBA':
        opaque = Image.new('RGB', original.size, '#fcf8ef')
        opaque.paste(original, mask=original.getchannel('A'))
        original = opaque
    else:
        original = original.convert('RGB')
    for nominal_width in [480, 800, 1200]:
        width = min(nominal_width, original.width)
        height = round(width * original.height / original.width)
        resized = original.resize((width, height), Image.Resampling.LANCZOS)
        path = OUTPUT / f'{name}-{nominal_width}.webp'
        resized.save(path, 'WEBP', quality=83, method=6, icc_profile=color_profile)
        record(path, resized)

if options.only:
    manifest_path = OUTPUT / 'manifest.json'
    existing = json.loads(manifest_path.read_text(encoding='utf-8'))
    updated_names = {item['file'] for item in report}
    existing = [item for item in existing if item['file'] not in updated_names]
    manifest_path.write_text(json.dumps(existing + report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0)

original_logo = Image.open(SOURCE / 'logo-fundo-transparente.png').convert('RGBA')
cropped_logo = original_logo.crop(original_logo.getchannel('A').getbbox())
cropped_logo.thumbnail((600, 600), Image.Resampling.LANCZOS)
logo_path = OUTPUT / 'logo.webp'
cropped_logo.save(logo_path, 'WEBP', lossless=True, method=6)
record(logo_path, cropped_logo)

# Preserve the brand's existing milkshake symbol for the small browser icon.
symbol_area = original_logo.crop((0, 0, original_logo.width, 1540))
symbol = symbol_area.crop(symbol_area.getchannel('A').getbbox())
symbol.thumbnail((52, 52), Image.Resampling.LANCZOS)
favicon = Image.new('RGBA', (64, 64), '#fcf8ef')
favicon.alpha_composite(symbol, ((64-symbol.width)//2, (64-symbol.height)//2))
favicon_path = OUTPUT / 'favicon.png'
favicon.save(favicon_path)
record(favicon_path, favicon)

share = Image.new('RGB', (1200, 630), '#fcf8ef')
hero = ImageOps.exif_transpose(Image.open(SOURCE / FILES['hero'])).convert('RGB')
hero = ImageOps.fit(hero, (520, 630), method=Image.Resampling.LANCZOS, centering=(0.45, 0.66))
share.paste(hero, (680, 0))
draw = ImageDraw.Draw(share)
font_dir = Path(r'C:\Windows\Fonts')
title = ImageFont.truetype(str(font_dir / 'georgia.ttf'), 72)
subtitle = ImageFont.truetype(str(font_dir / 'arial.ttf'), 30)
small = ImageFont.truetype(str(font_dir / 'arial.ttf'), 22)
pill = ImageFont.truetype(str(font_dir / 'arialbd.ttf'), 18)
share_symbol = symbol_area.crop(symbol_area.getchannel('A').getbbox())
share_symbol.thumbnail((56, 108), Image.Resampling.LANCZOS)
share.paste(share_symbol, (64, 54), share_symbol)
draw.text((144, 88), 'A 1ª ilha de milkshakes', font=small, fill='#6f4035')
draw.text((144, 120), 'para eventos do RS', font=small, fill='#6f4035')
draw.text((60, 214), 'Celebre', font=title, fill='#472c27')
draw.text((64, 310), 'Milkshake Bar', font=subtitle, fill='#9e4e36')
draw.line((64, 378, 586, 378), fill='#dccabd', width=2)
draw.text((64, 412), 'Milkshakes à vontade.', font=subtitle, fill='#472c27')
draw.text((64, 460), 'Celebrações inesquecíveis.', font=subtitle, fill='#472c27')
draw.rounded_rectangle((64, 536, 584, 581), radius=22, fill='#eadacb')
draw.text((90, 548), 'NOVO HAMBURGO, REGIÃO E PROXIMIDADES', font=pill, fill='#6f4035')
share_path = OUTPUT / 'compartilhamento.jpg'
share.save(share_path, 'JPEG', quality=88, optimize=True)
record(share_path, share)

(OUTPUT / 'manifest.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(report, indent=2, ensure_ascii=False))
