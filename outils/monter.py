"""Niveau 1 : applique le plan de montage et rend la vidéo finale avec FFmpeg.

Usage : python outils/monter.py rushs/ma_video.mp4

Lit travail/<nom>/blocs.json et travail/<nom>/plan.json :
  "supprimer" : ids de blocs à enlever entièrement (ratés, répétitions, hors-sujet)
  "retirer"   : plages [debut, fin] en secondes à enlever à l'intérieur d'un bloc gardé
Les pauses entre blocs gardés sont toujours raccourcies à la marge configurée.

Produit dans montages/ : <nom>_monte.mp4 et <nom>_monte.srt (sous-titres recalés).
"""
import json
import subprocess
import sys
from pathlib import Path

from commun import RACINE, config, dossier_travail, horodatage, lire_json, outil


def plages_gardees(blocs, plan, duree, marge):
    supprimer = set(plan.get("supprimer", []))
    plages = []
    for b in blocs:
        if b["id"] in supprimer:
            continue
        debut, fin = max(b["debut"] - marge, 0), min(b["fin"] + marge, duree)
        if plages and debut <= plages[-1][1]:
            plages[-1][1] = max(plages[-1][1], fin)
        else:
            plages.append([debut, fin])

    for r_debut, r_fin in sorted(plan.get("retirer", [])):
        nouvelles = []
        for debut, fin in plages:
            if r_fin <= debut or r_debut >= fin:
                nouvelles.append([debut, fin])
                continue
            if r_debut > debut:
                nouvelles.append([debut, r_debut])
            if r_fin < fin:
                nouvelles.append([r_fin, fin])
        plages = nouvelles
    return [p for p in plages if p[1] - p[0] > 0.1]


def images_par_seconde(video):
    sortie = subprocess.run(
        [outil("ffprobe"), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=avg_frame_rate", "-of", "json", str(video)],
        capture_output=True, text=True, check=True,
    ).stdout
    num, den = json.loads(sortie)["streams"][0]["avg_frame_rate"].split("/")
    return round(int(num) / int(den), 3) if int(den) else 30


def texte(mots):
    return "".join(m["mot"] for m in mots).strip()


def sous_titres(blocs, plages, chemin):
    mots = [m for b in blocs for m in b["mots"]]
    lignes, decalage = [], 0.0
    for debut, fin in plages:
        courants = [m for m in mots if m["debut"] >= debut - 0.01 and m["fin"] <= fin + 0.01]
        groupe = []
        for m in courants + [None]:
            trop_long = groupe and (m is None or len(texte(groupe + [m])) > 42
                                    or m["fin"] - groupe[0]["debut"] > 3.5)
            if trop_long:
                lignes.append((groupe[0]["debut"] - debut + decalage, groupe[-1]["fin"] - debut + decalage,
                               texte(groupe)))
                groupe = []
            if m is not None:
                groupe.append(m)
        decalage += fin - debut
    with open(chemin, "w", encoding="utf-8") as f:
        for i, (d, fn, phrase) in enumerate(lignes, 1):
            f.write(f"{i}\n{horodatage(d)} --> {horodatage(fn)}\n{phrase}\n\n")


def monter(video):
    cfg = config()
    video = Path(video)
    travail = dossier_travail(video)
    donnees = lire_json(travail / "blocs.json")
    plan = lire_json(travail / "plan.json")
    plages = plages_gardees(donnees["blocs"], plan, donnees["duree"], cfg["marge_s"])
    if not plages:
        raise SystemExit("Le plan ne garde rien : vérifie plan.json")

    ffmpeg, ips, fondu = outil("ffmpeg"), images_par_seconde(video), cfg["fondu_audio_s"]
    morceaux = travail / "morceaux"
    morceaux.mkdir(exist_ok=True)
    for f in morceaux.glob("*.mp4"):
        f.unlink()

    liste = []
    for i, (debut, fin) in enumerate(plages, 1):
        duree = fin - debut
        sortie = morceaux / f"{i:04d}.mp4"
        subprocess.run(
            [ffmpeg, "-v", "error", "-y", "-ss", f"{debut:.3f}", "-i", str(video), "-t", f"{duree:.3f}",
             "-af", f"afade=t=in:d={fondu},afade=t=out:st={max(duree - fondu, 0):.3f}:d={fondu}",
             "-r", str(ips), "-c:v", "libx264", "-crf", str(cfg["qualite_crf"]), "-preset", cfg["preset"],
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(sortie)],
            check=True,
        )
        liste.append(f"file '{sortie.as_posix()}'")
        print(f"\r  morceau {i}/{len(plages)}", end="", flush=True)
    print()

    (travail / "liste.txt").write_text("\n".join(liste) + "\n", encoding="utf-8")
    dossier_sortie = RACINE / "montages"
    dossier_sortie.mkdir(exist_ok=True)
    finale = dossier_sortie / f"{video.stem}_monte.mp4"
    subprocess.run(
        [ffmpeg, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(travail / "liste.txt"),
         "-c", "copy", "-movflags", "+faststart", str(finale)],
        check=True,
    )
    sous_titres(donnees["blocs"], plages, finale.with_suffix(".srt"))

    gardee = sum(f - d for d, f in plages)
    print(f"OK {finale} : {gardee:.0f}s gardées sur {donnees['duree']:.0f}s "
          f"({100 * (1 - gardee / donnees['duree']):.0f}% coupés, {len(plages)} plans)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    monter(sys.argv[1])
