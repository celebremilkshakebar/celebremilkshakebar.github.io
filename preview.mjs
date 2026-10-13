import http from 'node:http';
import { createReadStream, statSync } from 'node:fs';
import { dirname, resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.CELEBRE_PREVIEW_PORT || 4173);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp4': 'video/mp4' };

const server = http.createServer((request, response) => {
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }
  let file;
  try {
    const path = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    file = resolve(root, '.' + (path === '/' ? '/index.html' : path));
  } catch {
    response.writeHead(400).end('Requisição inválida.');
    return;
  }
  if (!file.startsWith(root + sep) || !['.html', '.css', '.js', '.webp', '.png', '.jpg', '.mp4'].includes(extname(file))) {
    response.writeHead(404).end('Arquivo não encontrado.');
    return;
  }
  let stat;
  try { stat = statSync(file); } catch { response.writeHead(404).end('Arquivo não encontrado.'); return; }
  if (!stat.isFile()) { response.writeHead(404).end('Arquivo não encontrado.'); return; }
  const headers = { 'Content-Type': types[extname(file)], 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff' };
  const range = request.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
  if (range) {
    const start = Number(range[1]);
    const end = range[2] ? Math.min(Number(range[2]), stat.size - 1) : stat.size - 1;
    if (start > end || start >= stat.size) { response.writeHead(416, { 'Content-Range': `bytes */${stat.size}` }).end(); return; }
    response.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${stat.size}`, 'Content-Length': end - start + 1 });
    if (request.method === 'HEAD') response.end(); else createReadStream(file, { start, end }).pipe(response);
  } else {
    response.writeHead(200, { ...headers, 'Content-Length': stat.size });
    if (request.method === 'HEAD') response.end(); else createReadStream(file).pipe(response);
  }
});
server.on('error', error => {
  console.error(error.code === 'EADDRINUSE' ? `A porta ${port} está em uso. Configure CELEBRE_PREVIEW_PORT com outra porta.` : error.message);
  process.exitCode = 1;
});
server.listen(port, '127.0.0.1', () => console.log(`Prévia da Celebre: http://127.0.0.1:${port}`));
