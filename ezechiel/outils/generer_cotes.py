"""Génère ezechiel/cotes.csv : tous les volumes du temple d'Ézéchiel en boîtes cotées.

Usage : .venv\\Scripts\\python.exe ezechiel\\outils\\generer_cotes.py

Repère (choix validés le 24/11/2026) :
- unité : coudée longue = 0,525 m ; enceinte de 500 coudées ;
- origine au centre de l'autel (= centre de l'enceinte), X vers l'est, Y vers le nord, Z vers le haut ;
- Z = 0 au sol extérieur au pied des 7 marches.
Les plans des croquis utilisent px (vers l'est, 0 au mur ouest) et py (vers le sud, 0 au mur nord) ;
X = px - 250, Y = 250 - py.
certitude : texte (cote écrite), deduit (calculé à partir du texte), hypothese (choix de reconstitution).
"""
import csv
from pathlib import Path

COUDEE_M = 0.525
SORTIE = Path(__file__).resolve().parents[1] / "cotes.csv"

# Niveaux (en coudées)
Z_EXT = 0.0          # sol extérieur
Z_OUT = 3.5          # parvis extérieur : 7 marches de 1/2 coudée (hypothèse)
Z_IN = 7.5           # parvis intérieur : 8 marches de plus (hypothèse)
Z_TEMPLE = Z_IN + 6  # plate-forme du temple : 1 roseau (41:8)
H_PORTE = 20.0       # hauteur des bâtiments de porte (hypothèse)
H_CHAMBRE = 10.0     # chambres du parvis (hypothèse)
ETAGE = 5.0          # hauteur d'étage (1 R 6:10, hypothèse)
H_NEF = 30.0         # hauteur intérieure du temple (hypothèse)

LIGNES = []


def boite(nom, cat, planche, versets, cert, px0, px1, py0, py1, z0, z1, forme="boite", note=""):
    x0, x1 = sorted((px0 - 250, px1 - 250))
    y0, y1 = sorted((250 - py0, 250 - py1))
    LIGNES.append(dict(nom=nom, categorie=cat, planche=planche, versets=versets, certitude=cert, forme=forme,
                       x_min=x0, x_max=x1, y_min=y0, y_max=y1, z_min=z0, z_max=z1, note=note))


# ---------- Enceinte et terrains ----------
def enceinte():
    v = "40:5 ; 42:15-20"
    for a, b in ((0, 237.5), (262.5, 500)):
        boite("Mur d'enceinte nord", "enceinte", "01", v, "texte", a, b, 0, 6, Z_EXT, 6)
        boite("Mur d'enceinte sud", "enceinte", "01", v, "texte", a, b, 494, 500, Z_EXT, 6)
        boite("Mur d'enceinte est", "enceinte", "01", v, "texte", 494, 500, a, b, Z_EXT, 6)
    boite("Mur d'enceinte ouest", "enceinte", "01", v, "texte", 0, 6, 0, 500, Z_EXT, 6)
    boite("Terre-plein du parvis extérieur", "terrain", "01", "40:17", "hypothese", 6, 494, 6, 494, Z_EXT, Z_OUT,
          note="niveau déduit des 7 marches de 1/2 coudée")
    boite("Terrasse du parvis intérieur et du temple", "terrain", "06", "40:31", "hypothese", 100, 300, 200, 300,
          Z_OUT, Z_IN, note="niveau déduit des 8 marches de 1/2 coudée")
    dal = "40:17-18"
    boite("Dallage nord", "terrain", "04", dal, "deduit", 6, 494, 6, 50, Z_OUT, Z_OUT + 0.2)
    boite("Dallage sud", "terrain", "04", dal, "deduit", 6, 494, 450, 494, Z_OUT, Z_OUT + 0.2)
    boite("Dallage ouest", "terrain", "04", dal, "deduit", 6, 50, 50, 450, Z_OUT, Z_OUT + 0.2)
    boite("Dallage est", "terrain", "04", dal, "deduit", 450, 494, 50, 450, Z_OUT, Z_OUT + 0.2)


# ---------- Portes ----------
def porte(nom, vers_plan, z_sol, z_bas, nb_marches, interieure):
    """u = profondeur 0..50 depuis la face extérieure (ou côté parvis extérieur), v = largeur 0..25."""
    pl = "05" if interieure else "02"
    vs = "40:28-37" if interieure else "40:6-16"

    def ajoute(n, u0, u1, v0, v1, z0, z1, cert, note=""):
        if interieure:  # vestibule côté parvis extérieur : miroir en u
            u0, u1 = 50 - u1, 50 - u0
        (a, b), (c, d) = vers_plan(u0, v0), vers_plan(u1, v1)
        boite(f"{nom} - {n}", "portes", pl, vs, cert, min(a, c), max(a, c), min(b, d), max(b, d), z0, z1, note=note)

    h = z_sol + H_PORTE
    for i, (u, w) in enumerate([(0, 6), (12, 5), (23, 5), (34, 6), (48, 2)], 1):
        ajoute(f"pilier {i} gauche", u, u + w, 0, 6, z_sol, h, "texte", "hauteur supposée")
        ajoute(f"pilier {i} droit", u, u + w, 19, 25, z_sol, h, "texte", "hauteur supposée")
    ajoute("jambage entrée gauche", 0, 6, 6, 7.5, z_sol, h, "deduit", "ouverture de 10 (40:11)")
    ajoute("jambage entrée droit", 0, 6, 17.5, 19, z_sol, h, "deduit", "ouverture de 10 (40:11)")
    for i, u in enumerate((6, 17, 28), 1):
        ajoute(f"barrière loge {i} gauche", u, u + 6, 6, 7, z_sol, z_sol + 1, "deduit", "1 coudée (40:12), hauteur supposée")
        ajoute(f"barrière loge {i} droite", u, u + 6, 18, 19, z_sol, z_sol + 1, "deduit", "1 coudée (40:12), hauteur supposée")
    ajoute("mur latéral gauche", 0, 50, -1.5, 0, z_sol, h, "hypothese", "25 lu de fond de loge à fond de loge")
    ajoute("mur latéral droit", 0, 50, 25, 26.5, z_sol, h, "hypothese", "25 lu de fond de loge à fond de loge")
    if interieure:
        ajoute("sol de la porte", 0, 50, -1.5, 26.5, z_bas, z_sol, "hypothese")
    # Marches devant la face u = 0 (après miroir pour les portes intérieures : côté vestibule) ;
    # la marche 1 est la plus éloignée et la plus basse.
    for i in range(nb_marches):
        u0 = -(nb_marches - i) * 1.5
        (p, q), (r, s) = vers_plan(u0, 0), vers_plan(u0 + 1.5, 25)
        boite(f"{nom} - marche {i + 1}", "portes", pl, "40:22, 26" if not interieure else "40:31, 34, 37",
              "texte", min(p, r), max(p, r), min(q, s), max(q, s), z_bas, z_bas + 0.5 * (i + 1),
              note="nombre de marches du texte, hauteur et giron supposés")


def portes():
    porte("Porte extérieure est", lambda u, v: (500 - u, 237.5 + v), Z_OUT, Z_EXT, 7, False)
    porte("Porte extérieure nord", lambda u, v: (237.5 + v, u), Z_OUT, Z_EXT, 7, False)
    porte("Porte extérieure sud", lambda u, v: (237.5 + v, 500 - u), Z_OUT, Z_EXT, 7, False)
    porte("Porte intérieure est", lambda u, v: (350 - u, 237.5 + v), Z_IN, Z_OUT, 8, True)
    porte("Porte intérieure nord", lambda u, v: (237.5 + v, 150 + u), Z_IN, Z_OUT, 8, True)
    porte("Porte intérieure sud", lambda u, v: (237.5 + v, 350 - u), Z_IN, Z_OUT, 8, True)


# ---------- Parvis ----------
def parvis():
    xs = [56, 90, 124, 158, 192, 274, 308, 342, 376, 410]
    for i, x in enumerate(xs, 1):
        boite(f"Chambre du parvis N{i}", "parvis", "04", "40:17", "hypothese", x, x + 26, 8, 22, Z_OUT, Z_OUT + H_CHAMBRE,
              note="nombre (30) du texte ; taille et place supposées")
        boite(f"Chambre du parvis S{i}", "parvis", "04", "40:17", "hypothese", x, x + 26, 478, 492, Z_OUT, Z_OUT + H_CHAMBRE,
              note="nombre (30) du texte ; taille et place supposées")
        boite(f"Chambre du parvis E{i}", "parvis", "04", "40:17", "hypothese", 478, 492, x, x + 26, Z_OUT, Z_OUT + H_CHAMBRE,
              note="nombre (30) du texte ; taille et place supposées")
    for nom, (x, y) in {"NO": (6, 6), "NE": (454, 6), "SO": (6, 464), "SE": (454, 464)}.items():
        v, z1 = "46:21-24", Z_OUT + 4
        n = "hauteur et épaisseur du muret supposées"
        boite(f"Cuisine {nom} - muret nord", "parvis", "04", v, "texte", x, x + 40, y, y + 1, Z_OUT, z1, note=n)
        boite(f"Cuisine {nom} - muret sud", "parvis", "04", v, "texte", x, x + 40, y + 29, y + 30, Z_OUT, z1, note=n)
        boite(f"Cuisine {nom} - muret ouest", "parvis", "04", v, "texte", x, x + 1, y + 1, y + 29, Z_OUT, z1, note=n)
        boite(f"Cuisine {nom} - muret est", "parvis", "04", v, "texte", x + 39, x + 40, y + 1, y + 29, Z_OUT, z1, note=n)
    boite("Chambre des prêtres de la Maison (vers le sud)", "parvis", "06", "40:44-45", "hypothese",
          266, 288, 203, 211, Z_IN, Z_IN + H_CHAMBRE)
    boite("Chambre des prêtres de l'autel (vers le nord)", "parvis", "06", "40:44, 46", "hypothese",
          266, 288, 289, 297, Z_IN, Z_IN + H_CHAMBRE)


# ---------- Autel ----------
def autel():
    v = "43:13-17"
    for nom, c, z0, z1 in (("base 18 x 18", 18, 0, 1), ("palier 16 x 16", 16, 1, 3),
                           ("palier 14 x 14", 14, 3, 7), ("foyer 12 x 12", 12, 7, 11)):
        h = c / 2
        boite(f"Autel - {nom}", "autel", "12", v, "texte", 250 - h, 250 + h, 250 - h, 250 + h, Z_IN + z0, Z_IN + z1)
    for i, (x, y) in enumerate(((244, 244), (255, 244), (244, 255), (255, 255)), 1):
        boite(f"Autel - corne {i}", "autel", "12", "43:15", "hypothese", x, x + 1, y, y + 1, Z_IN + 11, Z_IN + 12,
              note="cornes du texte, taille supposée")


# ---------- Temple ----------
def temple():
    def t(nom, tx0, tx1, ty0, ty1, z0, z1, cert, v, pl="07", forme="boite", note=""):
        boite(f"Temple - {nom}", "temple", pl, v, cert, 100 + tx0, 100 + tx1, 225 + ty0, 225 + ty1,
              Z_TEMPLE + z0, Z_TEMPLE + z1, forme=forme, note=note)

    boite("Temple - plate-forme", "temple", "08", "41:8, 41:11", "texte", 95, 183, 220, 280, Z_IN, Z_TEMPLE,
          note="1 roseau de haut, déborde de l'espace libre de 5")
    boite("Temple - plate-forme du vestibule", "temple", "08", "41:8", "deduit", 183, 200, 234, 266, Z_IN, Z_TEMPLE)
    for i in range(10):
        boite(f"Temple - marche {i + 1}", "temple", "07", "40:49 (LXX)", "hypothese",
              205 - 0.5 * (i + 1), 205 - 0.5 * i, 243, 257, Z_IN, Z_IN + 0.6 * (i + 1),
              note="10 marches (LXX) pour 6 coudées : hauteur 0,6")
    hc = 3 * ETAGE
    t("mur extérieur des chambres nord", 0, 83, 0, 5, 0, hc, "texte", "41:9", note="hauteur supposée")
    t("mur extérieur des chambres sud", 0, 83, 45, 50, 0, hc, "texte", "41:9", note="hauteur supposée")
    t("mur extérieur des chambres ouest", 0, 5, 5, 45, 0, hc, "texte", "41:9", note="hauteur supposée")
    for k, (z0, z1) in enumerate(((0, ETAGE), (ETAGE, 2 * ETAGE), (2 * ETAGE, H_NEF))):
        n = "retraits de 1 coudée par étage (41:6-7, 1 R 6:6)"
        t(f"mur nord niveau {k + 1}", 9, 83, 9 + k, 15, z0, z1, "deduit", "41:5-7", pl="08", note=n)
        t(f"mur sud niveau {k + 1}", 9, 83, 35, 41 - k, z0, z1, "deduit", "41:5-7", pl="08", note=n)
        t(f"mur ouest niveau {k + 1}", 9 + k, 15, 9 + k, 41 - k, z0, z1, "deduit", "41:5-7", pl="08", note=n)
    for k, z in enumerate((ETAGE, 2 * ETAGE, 3 * ETAGE), 2):
        nom = "toit des chambres" if k == 4 else f"plancher étage {k}"
        ext = 0 if k == 4 else 5
        t(f"{nom} nord", ext, 83, ext, 9 + min(k - 1, 2), z, z + 0.5, "hypothese", "41:6", pl="08")
        t(f"{nom} sud", ext, 83, 41 - min(k - 1, 2), 50 - ext, z, z + 0.5, "hypothese", "41:6", pl="08")
        t(f"{nom} ouest", ext, 9 + min(k - 1, 2), ext, 50 - ext, z, z + 0.5, "hypothese", "41:6", pl="08")
    t("pilier de la nef nord", 77, 83, 15, 20, 0, H_NEF, "texte", "41:1-2")
    t("pilier de la nef sud", 77, 83, 30, 35, 0, H_NEF, "texte", "41:1-2")
    t("cloison du Saint des saints nord", 35, 37, 15, 22, 0, H_NEF, "texte", "41:3")
    t("cloison du Saint des saints sud", 35, 37, 28, 35, 0, H_NEF, "texte", "41:3")
    t("mur du vestibule nord", 83, 100, 9, 15, 0, H_NEF, "deduit", "40:48-49")
    t("mur du vestibule sud", 83, 100, 35, 41, 0, H_NEF, "deduit", "40:48-49")
    t("pilier du vestibule nord", 95, 100, 15, 18, 0, H_NEF, "texte", "40:48 (LXX)")
    t("pilier du vestibule sud", 95, 100, 32, 35, 0, H_NEF, "texte", "40:48 (LXX)")
    t("colonne nord", 100.8, 103.2, 14.8, 17.2, 0, 20, "hypothese", "40:49", forme="cylindre",
      note="colonnes du texte, diamètre et hauteur supposés")
    t("colonne sud", 100.8, 103.2, 32.8, 35.2, 0, 20, "hypothese", "40:49", forme="cylindre",
      note="colonnes du texte, diamètre et hauteur supposés")
    t("toit", 9, 100, 9, 41, H_NEF, H_NEF + 1, "hypothese", "-", pl="08", note="toit plat supposé")


# ---------- Bâtiment occidental ----------
def batiment():
    v, n, h = "41:12", "hauteur supposée", Z_OUT + 20
    boite("Bâtiment ouest - mur nord", "batiment", "10", v, "texte", 0, 80, 200, 205, Z_OUT, h, note=n)
    boite("Bâtiment ouest - mur sud", "batiment", "10", v, "texte", 0, 80, 295, 300, Z_OUT, h, note=n)
    boite("Bâtiment ouest - mur ouest", "batiment", "10", v, "texte", 0, 5, 205, 295, Z_OUT, h, note=n)
    boite("Bâtiment ouest - mur est", "batiment", "10", v, "texte", 75, 80, 205, 295, Z_OUT, h, note=n)


# ---------- Chambres des prêtres ----------
def chambres_pretres():
    for cote, f in (("nord", lambda ly: 150 + ly), ("sud", lambda ly: 350 - ly)):
        def c(nom, lx0, lx1, ly0, ly1, z0, z1, cert, v="42:1-12", note=""):
            a, b = sorted((f(ly0), f(ly1)))
            boite(f"Chambres des prêtres {cote} - {nom}", "pretres", "11", v, cert, 100 + lx0, 100 + lx1, a, b,
                  Z_OUT + z0, Z_OUT + z1, note=note)
        for k, r in enumerate((0, 3, 6)):
            z0, z1 = k * ETAGE, (k + 1) * ETAGE
            c(f"aile parvis extérieur, étage {k + 1}", 0, 50, 0, 20 - r, z0, z1, "deduit",
              note="aile de 50 (42:8), recul des galeries supposé")
            c(f"aile côté temple, étage {k + 1}", 0, 100, 30 + r, 50, z0, z1, "deduit",
              note="aile de 100 (42:8), recul des galeries supposé")
        c("mur de 50", 50, 100, 0, 1.2, 0, ETAGE, "texte", "42:7", "épaisseur et hauteur supposées")
        c("lieu de cuisson", -13, -3, 30, 50, 0, ETAGE, "hypothese", "46:19-20")


def main():
    enceinte(); portes(); parvis(); autel(); temple(); batiment(); chambres_pretres()
    champs = ["id", "nom", "categorie", "planche", "versets", "certitude", "forme",
              "x_min", "x_max", "y_min", "y_max", "z_min", "z_max",
              "centre_x", "centre_y", "centre_z", "long_x", "larg_y", "haut_z",
              "long_x_m", "larg_y_m", "haut_z_m", "note"]
    with SORTIE.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=champs, delimiter=";")
        w.writeheader()
        for i, l in enumerate(LIGNES, 1):
            lx, ly, lz = l["x_max"] - l["x_min"], l["y_max"] - l["y_min"], l["z_max"] - l["z_min"]
            r = dict(l, id=i,
                     centre_x=(l["x_min"] + l["x_max"]) / 2, centre_y=(l["y_min"] + l["y_max"]) / 2,
                     centre_z=(l["z_min"] + l["z_max"]) / 2, long_x=lx, larg_y=ly, haut_z=lz,
                     long_x_m=lx * COUDEE_M, larg_y_m=ly * COUDEE_M, haut_z_m=lz * COUDEE_M)
            w.writerow({k: (f"{v:.3f}".rstrip("0").rstrip(".") if isinstance(v, float) else v) for k, v in r.items()})
    print(f"{len(LIGNES)} volumes écrits dans {SORTIE}")


if __name__ == "__main__":
    main()
