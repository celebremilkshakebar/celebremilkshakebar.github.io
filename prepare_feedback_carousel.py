"""Prepare additional feedback videos while preserving the first testimonial."""
from pathlib import Path
import sys
import subprocess
import json
import struct
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
ASSETS = ROOT / 'assets'
QA = ROOT / '.media-qa'
QA.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / '.media-tools'))
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SOURCES = {
    'feedback-2': Path(r'C:\Users\vinim\Downloads\Celebre - Video 02 - Feedbacks (1).mov'),
    'feedback-3': Path(r'C:\Users\vinim\Downloads\IMG_5193.MOV'),
}

def metadata(path):
    reader = imageio_ffmpeg.read_frames(str(path))
    result = next(reader)
    reader.close()
    return result

manifest_file = ASSETS / 'manifest.json'
manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
new_names = [name + suffix for name in SOURCES for suffix in ['.mp4', '-poster.webp']]
manifest = [item for item in manifest if item['file'] not in new_names]

for name, source in SOURCES.items():
    source_meta = metadata(source)
    print('SOURCE', str(source), source.stat().st_size, json.dumps(source_meta), flush=True)
    width = min(720, source_meta['size'][0])
    fps = min(30, source_meta['fps'])
    output = ASSETS / (name + '.mp4')
    subprocess.run([
        FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-map', '0:v:0', '-map', '0:a:0', '-map_metadata', '-1',
        '-vf', f'scale={width}:-2,fps={fps}',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '25',
        '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '3.1',
        '-c:a', 'copy', '-movflags', '+faststart', str(output)
    ], check=True)
    result = metadata(output)
    assert result['codec'] == 'h264'
    assert result['audio_codec'] == 'aac'
    assert abs(result['duration'] - source_meta['duration']) < 0.05
    assert result['fps'] <= 30
    atoms = []
    with output.open('rb') as video:
        position = 0
        while position < output.stat().st_size:
            video.seek(position)
            size, kind = struct.unpack('>I4s', video.read(8))
            atoms.append((kind.decode(), position, size))
            position += size
    assert next(index for index, atom in enumerate(atoms) if atom[0] == 'moov') < next(index for index, atom in enumerate(atoms) if atom[0] == 'mdat')
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
    audio_check = subprocess.run([FFMPEG, '-hide_banner', '-i', str(output), '-vn', '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, check=True)
    print('AUDIO', name, '\n'.join(line.strip() for line in audio_check.stderr.splitlines() if 'mean_volume' in line or 'max_volume' in line), flush=True)

    times = [round(source_meta['duration'] * fraction, 2) for fraction in [0.1, 0.35, 0.65, 0.9]]
    poster_time = times[0]
    for kind, video in [('source', source), ('output', output)]:
        for seconds in times:
            subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(seconds),
                            '-i', str(video), '-frames:v', '1', '-vf', 'scale=720:-2',
                            str(QA / f'{name}-{kind}-{seconds:.2f}.png')], check=True)
    poster_image = Image.open(QA / f'{name}-output-{poster_time:.2f}.png').convert('RGB')
    poster = ASSETS / f'{name}-poster.webp'
    poster_image.save(poster, 'WEBP', quality=86, method=6)
    manifest.append({'file': output.name, 'width': result['size'][0], 'height': result['size'][1],
                     'bytes': output.stat().st_size, 'duration_seconds': result['duration'],
                     'video_codec': 'H264', 'audio_codec': 'AAC', 'fps': result['fps'], 'faststart': True})
    manifest.append({'file': poster.name, 'width': poster_image.width, 'height': poster_image.height,
                     'bytes': poster.stat().st_size})
    print('OUTPUT', json.dumps(manifest[-2:]), flush=True)
    sheet = Image.new('RGB', (1440, 1340), '#fcf8ef')
    draw = ImageDraw.Draw(sheet)
    for row, kind in enumerate(['source', 'output']):
        for column, seconds in enumerate(times):
            frame = Image.open(QA / f'{name}-{kind}-{seconds:.2f}.png')
            frame.thumbnail((360, 640), Image.Resampling.LANCZOS)
            sheet.paste(frame, (column * 360, row * 670 + 28))
            draw.text((column * 360 + 8, row * 670 + 7), f'{kind} / {seconds:.2f}s', fill='#472c27')
    sheet.save(QA / f'{name}-contact-sheet.jpg', 'JPEG', quality=90)

manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
