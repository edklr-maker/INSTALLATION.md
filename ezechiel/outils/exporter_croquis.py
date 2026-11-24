"""Exporte les planches du storyboard d'Ézéchiel en SVG (A3) et PNG 4K.

Usage : .venv\\Scripts\\python.exe ezechiel\\outils\\exporter_croquis.py
Le dessin des planches vit dans storyboard-ezechiel.html (entre /*<planches>*/ et
/*</planches>*/) ; cartouche.js le met en page. Le rendu passe par Edge ou Chrome
en mode headless, aucun paquet Python n'est nécessaire.
"""
import html
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.parse
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
SORTIE = RACINE / "croquis"
NAVIGATEURS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]
PNG_L, PNG_H = 3840, 2715  # 4K, rapport A3


def navigateur() -> str:
    for p in NAVIGATEURS:
        if Path(p).exists():
            return p
    sys.exit("Ni Edge ni Chrome trouvé : impossible de rendre les planches.")


def slug(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def lancer(nav: str, profil: Path, *args: str) -> str:
    cmd = [nav, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=1", f"--user-data-dir={profil}", *args]
    r = subprocess.run(cmd, capture_output=True, timeout=180)
    return r.stdout.decode("utf-8", errors="replace")


def main() -> None:
    nav = navigateur()
    src = (RACINE / "storyboard-ezechiel.html").read_text(encoding="utf-8")
    m = re.search(r"/\*<planches>\*/(.*?)/\*</planches>\*/", src, re.S)
    if not m:
        sys.exit("Marqueurs /*<planches>*/ introuvables dans le storyboard.")
    cartouche = (ICI / "cartouche.js").read_text(encoding="utf-8")
    tmp = Path(tempfile.mkdtemp(prefix="ezechiel_"))
    try:
        page = tmp / "export.html"
        page.write_text('<!doctype html><meta charset="utf-8"><body><div id="out"></div><script>'
                        + m.group(1) + "\n" + cartouche + "</script></body>", encoding="utf-8")
        dom = lancer(nav, tmp / "profil", "--virtual-time-budget=5000", "--dump-dom", page.as_uri())
        items = re.findall(r'<div data-n="([^"]+)" data-t="([^"]*)" data-svg="([^"]+)"', dom)
        if not items:
            sys.exit("Aucune planche produite (le rendu headless a échoué).")
        SORTIE.mkdir(exist_ok=True)
        for n, titre, data in items:
            svg = urllib.parse.unquote(html.unescape(data))
            nom = f"planche-{n}-{slug(html.unescape(titre))}"
            (SORTIE / f"{nom}.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg, encoding="utf-8")
            png_src = tmp / f"{nom}.svg"
            png_src.write_text(svg.replace('width="420mm" height="297mm"', f'width="{PNG_L}" height="{PNG_H}"', 1),
                               encoding="utf-8")
            lancer(nav, tmp / "profil", f"--screenshot={SORTIE / (nom + '.png')}",
                   f"--window-size={PNG_L},{PNG_H}", png_src.as_uri())
            print(f"planche {n} -> {nom}.svg / .png")
        print(f"{len(items)} planches exportées dans {SORTIE}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
