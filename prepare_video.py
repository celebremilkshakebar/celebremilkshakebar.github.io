"""Transcode the supplied feedback video to a browser-compatible MP4."""
from pathlib import Path
import sys
import subprocess
import json
import struct
from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / '.media-tools'))
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
source = Path(r'C:\landing-celebre\media\Celebre - Video 02 - Feedbacks.mov')
output = ROOT / 'assets' / 'feedback.mp4'
subprocess.run([
    ffmpeg, '-hide_banner', '-y', '-i', str(source),
    '-map', '0:v:0', '-map', '0:a:0',
    '-vf', 'scale=720:-2', '-c:v', 'libx264', '-preset', 'medium',
    '-crf', '24', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
    '-c:a', 'copy', '-movflags', '+faststart', str(output)
], check=True)
for seconds, name in [(1.0, 'feedback-poster'), (4.0, 'feedback-frame-4'), (8.0, 'feedback-frame-8')]:
    png = ROOT / 'assets' / (name + '.png')
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
                    '-ss', str(seconds), '-i', str(output), '-frames:v', '1', str(png)], check=True)
    if name == 'feedback-poster':
        image = Image.open(png)
        image.save(ROOT / 'assets' / 'feedback-poster.webp', 'WEBP', quality=86, method=6)
        png.unlink()

reader = imageio_ffmpeg.read_frames(str(output))
metadata = next(reader)
reader.close()
print(json.dumps({'file': output.name, 'bytes': output.stat().st_size, 'metadata': metadata}, indent=2))

manifest_file = ROOT / 'assets' / 'manifest.json'
manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
manifest = [item for item in manifest if item['file'] not in ['feedback.mp4', 'feedback-poster.webp']]
manifest.append({'file': output.name, 'width': 720, 'height': 1280,
                 'bytes': output.stat().st_size, 'duration_seconds': metadata['duration'],
                 'video_codec': 'H264', 'audio_codec': 'AAC', 'faststart': True})
poster = ROOT / 'assets' / 'feedback-poster.webp'
manifest.append({'file': poster.name, 'width': 720, 'height': 1280, 'bytes': poster.stat().st_size})
manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

atoms = []
with output.open('rb') as video:
    position = 0
    while position < output.stat().st_size:
        video.seek(position)
        size, kind = struct.unpack('>I4s', video.read(8))
        atoms.append((kind.decode(), position, size))
        position += size
assert next(index for index, atom in enumerate(atoms) if atom[0] == 'moov') < next(index for index, atom in enumerate(atoms) if atom[0] == 'mdat')
print('Faststart validated:', atoms)
print('Assets bytes:', sum(path.stat().st_size for path in (ROOT / 'assets').iterdir() if path.is_file()))
# The temporary frames were inspected during preparation; only the poster is shipped.
(ROOT / 'assets' / 'feedback-frame-4.png').unlink()
(ROOT / 'assets' / 'feedback-frame-8.png').unlink()
