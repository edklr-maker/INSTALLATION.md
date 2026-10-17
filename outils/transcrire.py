"""Niveau 1 : transcrit une vidéo (en local, avec Whisper) et la découpe en blocs de parole.

Usage : python outils/transcrire.py rushs/ma_video.mp4

Produit dans travail/<nom>/ :
  blocs.json  - les blocs de parole avec leurs mots horodatés
  blocs.txt   - la version lisible, un bloc par ligne, pour décider quoi couper
  plan.json   - le plan de montage à remplir (blocs à supprimer)
"""
import os
import subprocess
import sys
import time

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

import numpy as np
from faster_whisper import WhisperModel

from commun import config, dossier_travail, ecrire_json, horodatage, outil


def audio_16k(video):
    """Extrait l'audio en mono 16 kHz avec FFmpeg (plus fiable que le décodeur intégré)."""
    brut = subprocess.run(
        [outil("ffmpeg"), "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
         "-f", "s16le", "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(brut, np.int16).astype(np.float32) / 32768.0


def transcrire(video):
    cfg = config()
    debut = time.time()
    modele = WhisperModel(cfg["modele_whisper"], device="cpu", compute_type="int8")
    segments, info = modele.transcribe(
        audio_16k(video),
        language=cfg["langue"],
        word_timestamps=True,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    mots = []
    for seg in segments:
        for m in seg.words or []:
            mots.append({"debut": round(m.start, 3), "fin": round(m.end, 3), "mot": m.word})
    duree = info.duration

    # Un nouveau bloc commence à chaque pause plus longue que pause_coupure_s
    blocs = []
    for m in mots:
        if blocs and m["debut"] - blocs[-1]["fin"] < cfg["pause_coupure_s"]:
            b = blocs[-1]
            b["fin"] = m["fin"]
            b["mots"].append(m)
        else:
            blocs.append({"id": len(blocs) + 1, "debut": m["debut"], "fin": m["fin"], "mots": [m]})
    for b in blocs:
        b["texte"] = "".join(m["mot"] for m in b["mots"]).strip()

    travail = dossier_travail(video)
    ecrire_json(travail / "blocs.json", {"video": str(video), "duree": duree, "blocs": blocs})

    lignes = [f"# {video}  |  durée {horodatage(duree, '.')}  |  {len(blocs)} blocs", ""]
    for b in blocs:
        lignes.append(
            f"[{b['id']}] {horodatage(b['debut'], '.')} -> {horodatage(b['fin'], '.')} "
            f"({b['fin'] - b['debut']:.1f}s)  {b['texte']}"
        )
    (travail / "blocs.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")

    plan = travail / "plan.json"
    if not plan.exists():
        ecrire_json(plan, {"supprimer": [], "raisons": {}})

    parle = sum(b["fin"] - b["debut"] for b in blocs)
    print(f"OK {video} : {len(blocs)} blocs, {parle:.0f}s de parole sur {duree:.0f}s "
          f"(transcrit en {time.time() - debut:.0f}s)")
    print(f"-> {travail / 'blocs.txt'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    transcrire(sys.argv[1])
