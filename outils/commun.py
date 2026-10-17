"""Fonctions partagées par les outils de montage."""
import glob
import json
import os
import shutil
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
EXTENSIONS_VIDEO = {".mp4", ".mov", ".mkv", ".m4v", ".avi", ".webm"}


def config():
    with open(RACINE / "config.json", encoding="utf-8") as f:
        return json.load(f)


def outil(nom):
    """Trouve ffmpeg/ffprobe même si le PATH n'est pas encore rechargé après l'installation winget."""
    chemin = shutil.which(nom)
    if chemin:
        return chemin
    motif = os.path.expandvars(rf"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\{nom}.exe")
    trouves = glob.glob(motif)
    if trouves:
        return trouves[0]
    raise SystemExit(f"{nom} introuvable : installe-le avec  winget install Gyan.FFmpeg")


def dossier_travail(video):
    d = RACINE / "travail" / Path(video).stem
    d.mkdir(parents=True, exist_ok=True)
    return d


def ecrire_json(chemin, donnees):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)


def lire_json(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def horodatage(s, sep=","):
    h, reste = divmod(max(s, 0), 3600)
    m, reste = divmod(reste, 60)
    sec = int(reste)
    ms = int(round((reste - sec) * 1000))
    if ms == 1000:
        sec, ms = sec + 1, 0
    return f"{int(h):02d}:{int(m):02d}:{sec:02d}{sep}{ms:03d}"
