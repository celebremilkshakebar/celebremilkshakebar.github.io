"""Build lightweight, silent hero videos from the supplied complete clip."""
from pathlib import Path
import sys
import subprocess
import struct
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
ASSETS = ROOT / 'assets'
QA = ROOT / '.media-qa'
QA.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / '.media-tools'))
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SOURCE = Path(r'C:\Users\vinim\Downloads\Design sem nome (2).mp4')
FRAME_TAG = 'v2'

def metadata(path):
    reader = imageio_ffmpeg.read_frames(str(path))
    result = next(reader)
    reader.close()
    return result

source_meta = metadata(SOURCE)
print('SOURCE', str(SOURCE), SOURCE.stat().st_size, json.dumps(source_meta), flush=True)
sample_times = [round(source_meta['duration'] * fraction, 2) for fraction in [0.10, 0.35, 0.65, 0.92]]

for seconds in sample_times:
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
                    '-ss', str(seconds), '-i', str(SOURCE), '-vf', 'scale=360:-2',
                    '-frames:v', '1', str(QA / f'source-{FRAME_TAG}-{seconds:.2f}.png')], check=True)

manifest_file = ASSETS / 'manifest.json'
manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
names = ['hero-loop.mp4', 'hero-loop-mobile.mp4']
manifest = [item for item in manifest if item['file'] not in names]

for name, width, quality in [('hero-loop.mp4', 720, 28), ('hero-loop-mobile.mp4', 480, 29)]:
    output = ASSETS / name
    subprocess.run([
        FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(SOURCE),
        '-map', '0:v:0', '-an', '-sn', '-dn', '-map_metadata', '-1',
        '-vf', f'scale={width}:-2,fps=24',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', str(quality),
        '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '3.1',
        '-g', '48', '-movflags', '+faststart', str(output)
    ], check=True)
    result = metadata(output)
    atoms = []
    with output.open('rb') as video:
        position = 0
        while position < output.stat().st_size:
            video.seek(position)
            size, kind = struct.unpack('>I4s', video.read(8))
            atoms.append((kind.decode(), position, size))
            position += size
    assert next(index for index, atom in enumerate(atoms) if atom[0] == 'moov') < next(index for index, atom in enumerate(atoms) if atom[0] == 'mdat')
    assert result['codec'] == 'h264'
    assert result.get('audio_codec') is None
    assert abs(result['duration'] - source_meta['duration']) < 0.05
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
    manifest.append({'file': name, 'width': result['size'][0], 'height': result['size'][1],
                     'bytes': output.stat().st_size, 'duration_seconds': result['duration'],
                     'video_codec': 'H264', 'audio_codec': None, 'fps': 24, 'faststart': True})
    print('OUTPUT', json.dumps(manifest[-1]), flush=True)
    for seconds in sample_times:
        subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
                        '-ss', str(seconds), '-i', str(output), '-vf', 'scale=360:-2',
                        '-frames:v', '1', str(QA / f'{output.stem}-{FRAME_TAG}-{seconds:.2f}.png')], check=True)

manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

sheet = Image.new('RGB', (1440, 1920), '#fcf8ef')
draw = ImageDraw.Draw(sheet)
for row, basename in enumerate(['source', 'hero-loop', 'hero-loop-mobile']):
    for column, seconds in enumerate(sample_times):
        frame = Image.open(QA / f'{basename}-{FRAME_TAG}-{seconds:.2f}.png')
        frame.thumbnail((360, 604), Image.Resampling.LANCZOS)
        sheet.paste(frame, (column * 360, row * 640 + 28))
        draw.text((column * 360 + 8, row * 640 + 7), f'{basename} / {seconds}s', fill='#472c27')
sheet.save(QA / f'hero-contact-sheet-{FRAME_TAG}.jpg', 'JPEG', quality=88)
print('CONTACT SHEET', str(QA / f'hero-contact-sheet-{FRAME_TAG}.jpg'), flush=True)
