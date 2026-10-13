"""Compare lighter hero encodes before accepting them for the website."""
from pathlib import Path
import sys
import json
import subprocess
import shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
QA = ROOT / '.media-qa'
sys.path.insert(0, str(ROOT / '.media-tools'))
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SOURCE = Path(r'C:\Users\vinim\Downloads\Design sem nome.mp4')

if '--accept' not in sys.argv:
    for name, width in [('hero-loop', 720), ('hero-loop-mobile', 480)]:
        if '--mobile-only' in sys.argv and name == 'hero-loop':
            continue
        target = QA / f'{name}-candidate.mp4'
        subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(SOURCE),
                        '-map', '0:v:0', '-an', '-sn', '-dn', '-map_metadata', '-1',
                        '-vf', f'scale={width}:-2,fps=24', '-c:v', 'libx264', '-preset', 'slow',
                        '-crf', '29' if name.endswith('mobile') else '28', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '3.1',
                        '-g', '48', '-movflags', '+faststart', str(target)], check=True)
        current = ROOT / 'assets' / f'{name}.mp4'
        print(name, 'current_bytes', current.stat().st_size, 'candidate_bytes', target.stat().st_size,
              'reduction', 1-target.stat().st_size/current.stat().st_size, flush=True)
        for kind, video in [('current', current), ('candidate', target)]:
            for seconds in [7, 22, 42, 57]:
                subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
                                '-ss', str(seconds), '-i', str(video), '-frames:v', '1',
                                str(QA / f'{name}-{kind}-{seconds}.png')], check=True)
        sheet = Image.new('RGB', (1440, 1340), '#fcf8ef')
        draw = ImageDraw.Draw(sheet)
        for row, kind in enumerate(['current', 'candidate']):
            for column, seconds in enumerate([7, 22, 42, 57]):
                frame = Image.open(QA / f'{name}-{kind}-{seconds}.png')
                frame.thumbnail((360, 640), Image.Resampling.LANCZOS)
                sheet.paste(frame, (column * 360, row * 670 + 28))
                draw.text((column * 360 + 8, row * 670 + 7), f'{kind} / {seconds}s', fill='#472c27')
        sheet.save(QA / f'{name}-comparison.jpg', 'JPEG', quality=90)
else:
    manifest_path = ROOT / 'assets' / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for name in ['hero-loop', 'hero-loop-mobile']:
        candidate = QA / f'{name}-candidate.mp4'
        output = ROOT / 'assets' / f'{name}.mp4'
        assert candidate.stat().st_size <= output.stat().st_size * 0.75
        try:
            candidate.replace(output)
        except PermissionError:
            # A paused HTTP preview can retain a read handle that denies rename.
            # The preview is on the static cover before this fallback is used.
            shutil.copyfile(candidate, output)
        reader = imageio_ffmpeg.read_frames(str(output))
        metadata = next(reader)
        reader.close()
        for item in manifest:
            if item['file'] == output.name:
                item.update(bytes=output.stat().st_size, duration_seconds=metadata['duration'], fps=24)
                print(json.dumps(item), flush=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
