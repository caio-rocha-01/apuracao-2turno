"""Gera a página a partir dos arquivos desta pasta.

Uso: python3 dados/build.py  (na raiz do repositório). Escreve index.html na raiz e dados/public.html.
"""
""" (versão pública do painel) a partir de exterior.json, tse.json e primeiro_turno.json.

Uso: python3 build_public.py   (gera public.html e site.html; site.html vira o index.html do site)
"""
import json, datetime, pathlib

here = pathlib.Path(__file__).parent
exterior = json.loads((here / "exterior.json").read_text())
tse = [r for r in json.loads((here / "tse.json").read_text()) if r.get("hora")]
primeiro = json.loads((here / "primeiro_turno.json").read_text())
aptos = json.loads((here / "aptos.json").read_text())["aptos"]
gerado = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")
dados = json.dumps({"exterior": exterior, "tse": tse, "primeiro": primeiro, "aptos": aptos, "media_abst_r1": 0.6269, "gerado": gerado}, ensure_ascii=False).replace("</", "<\\/")

html = (here / "public_template.html").read_text().replace("/*__DADOS__*/{}", dados)
(here / "public.html").write_text(html)  # versão sem cabeçalho HTML

# Versão completa para o GitHub Pages (documento HTML com cabeçalho e ajustes para celular).
site = (
    '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<meta name="description" content="Boletins de urna do exterior, comparação com o 1º turno e totalização do TSE no 2º turno da eleição presidencial de 2026.">'
    '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
    '*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%;text-size-adjust:100%}'
    'body{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
    '</head><body>' + html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '') + '</body></html>'
)
(here.parent / "index.html").write_text(site)
print("public.html gerado", gerado, len(exterior), "países,", len(tse), "registros do TSE")
