"""Arma publicar/index.html (la app para GitHub Pages) a partir de App.html: misma página, pero habla con el servidor por internet."""
import re, pathlib
B = pathlib.Path(__file__).resolve().parent.parent
URL = 'https://script.google.com/macros/s/AKfycbyGBh8RPG6dGpo0-QEQ5II-lgxNXAtaBDjah9L8J64OSlze_Akn2TA_E-nvu8ewfmvsag/exec'
h = (B / 'App.html').read_text(encoding='utf-8')
viejo_r = "const REVISAR = '<?= revisar ?>';"
nuevo_r = r"const REVISAR = (new URLSearchParams(location.search).get('revisar') || '').replace(/[^\w-]/g, '').slice(0, 20);"
viejo_l = "  return new Promise((ok, mal) => google.script.run.withSuccessHandler(ok).withFailureHandler(e => mal(e && e.message ? e.message : String(e)))[fn](...args));"
nuevo_l = ("  return fetch('" + URL + "', {method: 'POST', headers: {'Content-Type': 'text/plain;charset=utf-8'}, body: JSON.stringify({fn: fn, args: args})})\n"
           "    .then(r => r.json(), () => { throw 'Sin conexión a internet. Intenta de nuevo.'; })\n"
           "    .then(j => { if (!j.ok) throw j.error; return j.r; });")
for a, b in [(viejo_r, nuevo_r), (viejo_l, nuevo_l)]:
    assert h.count(a) == 1, a[:40]; h = h.replace(a, b)
assert '<?' not in h and 'google.script' not in h
if '<title>' in h: h = re.sub(r'<title>.*?</title>', '<title>TML · Registro</title>', h, count=1)
else: h = h.replace('<head>', '<head>\n<title>TML · Registro</title>', 1)
if 'name="viewport"' not in h: h = h.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">', 1)
if 'charset' not in h[:500]: h = h.replace('<head>', '<head>\n<meta charset="utf-8">', 1)
(B / 'publicar' / 'index.html').write_text(h, encoding='utf-8')
print('ok', len(h))
