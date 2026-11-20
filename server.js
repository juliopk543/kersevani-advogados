// Servidor estático simples, sem dependências. Uso: npm start  (ou: node server.js)
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const ROOT = __dirname;
const PUBLIC_DIRS = ['css', 'js', 'images', 'fonts'];
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'application/vnd.ms-fontobject',
};

function allowed(rel) {
  if (rel === 'index.html') return true;
  const top = rel.split(path.sep)[0];
  return PUBLIC_DIRS.includes(top);
}

http
  .createServer((req, res) => {
    let urlPath;
    try { urlPath = decodeURIComponent(req.url.split('?')[0]); } catch { urlPath = '/'; }
    if (urlPath === '/') urlPath = '/index.html';
    const file = path.normalize(path.join(ROOT, urlPath));
    const rel = path.relative(ROOT, file);
    if (rel.startsWith('..') || path.isAbsolute(rel) || !allowed(rel)) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('404 - Não encontrado');
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        return res.end('404 - Não encontrado');
      }
      res.writeHead(200, {
        'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
        'Cache-Control': 'no-cache',
      });
      res.end(data);
    });
  })
  .listen(PORT, () => console.log(`Site rodando em http://localhost:${PORT}`));
