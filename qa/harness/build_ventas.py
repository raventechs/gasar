#!/usr/bin/env python3
"""Arma el sitio comercial independiente (ventas.raventechsapp.com): vendedores, landing de prueba, folletos y guías estáticas."""
import shutil, pathlib, re, subprocess, json, sys

SRC = pathlib.Path('/home/claude/raventechs.github.io')
OUT = pathlib.Path('/home/claude/ventas')
OLD, NEW = 'https://raventechs.github.io', 'https://ventas.raventechsapp.com'
if OUT.exists():
    for p in OUT.iterdir():
        if p.name != '.git': shutil.rmtree(p) if p.is_dir() else p.unlink()
OUT.mkdir(exist_ok=True)

for d in ['vendedores', 'folletos']:
    shutil.copytree(SRC / d, OUT / d)
# folleto de GasAR (estático) y guías estáticas de GasAR y manejAr
shutil.copy('/home/claude/gasar/gasar-folleto.html', OUT / 'folletos' / 'folleto-gasar.html')
for app, src in [('gasar', '/home/claude/gasar/ayuda'), ('manejar', '/home/claude/manejar/ayuda')]:
    shutil.copytree(src, OUT / 'ayuda' / app)
(OUT / 'CNAME').write_text('ventas.raventechsapp.com')
(OUT / 'index.html').write_text('''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RavenTechs</title><meta http-equiv="refresh" content="0; url=/folletos/"></head>
<body style="font-family:system-ui;background:#0a0c12;color:#eef0f6;text-align:center;padding:40px">
<p>RavenTechs · <a style="color:#f0b84a" href="/folletos/">Ver los folletos</a></p></body></html>
''', encoding='utf-8')

# ── Catálogo: dominio nuevo para lo comercial; GasAR y manejAr conservan sus apps donde están ──
v = (OUT / 'vendedores' / 'index.html').read_text(encoding='utf-8')
v = v.replace(OLD + '/folletos/', NEW + '/folletos/')
v = v.replace(OLD + '/probar/', NEW + '/probar/')
v = v.replace(OLD + '/vendedores/', NEW + '/vendedores/')
def set_field(v, appid, field, val):
    i = v.index(f"{{ id:'{appid}'"); j = v.index(f"{field}:", i)
    k = j + len(field) + 1
    # el valor termina en la próxima coma o llave de cierre del objeto
    m = re.compile(r"(?:'[^']*'|D\([^)]*\)(?:\s*\+\s*'[^']*')?|null)").match(v, k)
    assert m, (appid, field, v[k:k+60])
    return v[:k] + f"'{val}'" + v[m.end():]
v = set_field(v, 'gasar', 'ficha', NEW + '/folletos/folleto-gasar.html')
v = set_field(v, 'gasar', 'ayuda', NEW + '/ayuda/gasar/')
v = set_field(v, 'manejar', 'ayuda', NEW + '/ayuda/manejar/')
assert OLD + '/gasar/gasar-admin.html' in v and OLD + '/ManejAr/manejar.html' in v   # las apps siguen donde están
v = v.replace('  - v1.8 (02/11/2026)', '  - v1.9 (03/11/2026): sitio comercial en su propio dominio (ventas.raventechsapp.com) por la alerta de Navegación segura sobre raventechs.github.io; folleto e instructivo de GasAR y manejAr servidos desde el dominio nuevo.\n  - v1.8 (02/11/2026)', 1)
v = v.replace('VERSIÓN: v1.8', 'VERSIÓN: v1.9', 1)
(OUT / 'vendedores' / 'index.html').write_text(v, encoding='utf-8')
sw = (OUT / 'vendedores' / 'sw.js').read_text(encoding='utf-8').replace("vendedores-v1.8", "vendedores-v1.9")
(OUT / 'vendedores' / 'sw.js').write_text(sw, encoding='utf-8')

# folletos: el pie nombra el dominio
for f in (OUT / 'folletos').glob('*.html'):
    t = f.read_text(encoding='utf-8')
    t2 = t.replace('raventechs.github.io', 'ventas.raventechsapp.com')
    if t2 != t: f.write_text(t2, encoding='utf-8')

# catálogo → JSON para regenerar la landing con los datos nuevos
js = subprocess.run(['node', '-e', r'''
const fs=require('fs');const s=fs.readFileSync('/home/claude/ventas/vendedores/index.html','utf8');
const m=s.match(/const D = [^\n]*\n(const APPS = \[[\s\S]*?\n\];)/);
const D=(d)=>'https://'+d+'.raventechsapp.com/';
eval(m[1].replace('const APPS','global.APPS'));
fs.writeFileSync('/tmp/apps.json',JSON.stringify(APPS));'''], capture_output=True, text=True)
assert js.returncode == 0, js.stderr
print('ok catálogo')
