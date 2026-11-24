"""Monte le « blocking » du temple d'Ézéchiel dans Blender à partir de ezechiel/cotes.csv.

Dans Blender : onglet Scripting > Ouvrir ce fichier > Exécuter (le CSV est cherché à côté, dans ezechiel/).
En ligne de commande :
  blender --background --python construire_temple.py -- --csv ..\\cotes.csv --save temple_blocking.blend

Chaque ligne du CSV devient un objet (boîte ou cylindre) modélisé en coudées, rangé dans une
collection par catégorie, et rattaché à l'empty « Temple_Ezechiel » mis à l'échelle 0,525 :
la scène est donc en mètres réels. Couleurs : gris = cote du texte, bleu = déduit, ocre = hypothèse.
"""
import csv
import math
import sys
from pathlib import Path

import bmesh
import bpy

COUDEE_M = 0.525
RACINE = "Temple d'Ézéchiel"
COULEURS = {
    "texte": (0.78, 0.76, 0.72, 1.0),
    "deduit": (0.55, 0.68, 0.80, 1.0),
    "hypothese": (0.85, 0.65, 0.25, 1.0),
}


def arguments():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    opts = {"csv": None, "save": None}
    for i, a in enumerate(argv):
        if a in ("--csv", "--save") and i + 1 < len(argv):
            opts[a[2:]] = argv[i + 1]
    if opts["csv"] is None:
        base = Path(bpy.data.filepath).parent if bpy.data.filepath else None
        ici = Path(__file__).resolve().parent if "__file__" in globals() and Path(__file__).exists() else None
        for d in (ici, base):
            if d and (d.parent / "cotes.csv").exists():
                opts["csv"] = str(d.parent / "cotes.csv")
                break
            if d and (d / "cotes.csv").exists():
                opts["csv"] = str(d / "cotes.csv")
                break
    if not opts["csv"]:
        raise SystemExit("cotes.csv introuvable : passer --csv <chemin>.")
    return opts


def maillage_boite():
    me = bpy.data.meshes.get("ez_boite_unite")
    if me:
        return me
    me = bpy.data.meshes.new("ez_boite_unite")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me)
    bm.free()
    return me


def maillage_cylindre():
    me = bpy.data.meshes.get("ez_cylindre_unite")
    if me:
        return me
    me = bpy.data.meshes.new("ez_cylindre_unite")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=0.5, radius2=0.5, depth=1.0)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = len(p.vertices) == 4
    return me


def materiau(cert):
    nom = f"ez_{cert}"
    m = bpy.data.materials.get(nom)
    if m is None:
        m = bpy.data.materials.new(nom)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = COULEURS.get(cert, COULEURS["texte"])
            bsdf.inputs["Roughness"].default_value = 0.85
        m.diffuse_color = COULEURS.get(cert, COULEURS["texte"])
    return m


def collection(nom, parent):
    c = bpy.data.collections.get(nom)
    if c is None:
        c = bpy.data.collections.new(nom)
        parent.children.link(c)
    return c


def vider(racine):
    for c in list(racine.children_recursive):
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
    for o in list(racine.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def main():
    opts = arguments()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    racine = bpy.data.collections.get(RACINE)
    if racine is None:
        racine = bpy.data.collections.new(RACINE)
        scene.collection.children.link(racine)
    vider(racine)

    pivot = bpy.data.objects.new("Temple_Ezechiel", None)
    pivot.empty_display_type = "ARROWS"
    pivot.empty_display_size = 10
    pivot.scale = (COUDEE_M,) * 3
    pivot["note"] = "Objets en coudées ; l'échelle 0,525 de cet empty donne des mètres. Origine = centre de l'autel."
    racine.objects.link(pivot)

    boite, cyl = maillage_boite(), maillage_cylindre()
    n = 0
    with open(opts["csv"], newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            f = {k: float(r[k]) for k in ("centre_x", "centre_y", "centre_z", "long_x", "larg_y", "haut_z")}
            ob = bpy.data.objects.new(r["nom"], cyl if r["forme"] == "cylindre" else boite)
            ob.location = (f["centre_x"], f["centre_y"], f["centre_z"])
            ob.scale = (f["long_x"], f["larg_y"], f["haut_z"])
            ob.parent = pivot
            ob.color = COULEURS.get(r["certitude"], COULEURS["texte"])
            # maillage partagé : un emplacement de matériau lié à l'objet, pour colorer chaque objet à part
            if len(ob.data.materials) == 0:
                ob.data.materials.append(None)
            ob.material_slots[0].link = "OBJECT"
            ob.material_slots[0].material = materiau(r["certitude"])
            for k in ("versets", "certitude", "planche", "note"):
                if r.get(k):
                    ob[k] = r[k]
            collection(r["categorie"], racine).objects.link(ob)
            n += 1

    for zone in (bpy.context.screen.areas if bpy.context.screen else []):
        if zone.type == "VIEW_3D":
            for sp in zone.spaces:
                if sp.type == "VIEW_3D":
                    sp.shading.color_type = "OBJECT"
                    sp.clip_end = 5000

    print(f"{n} volumes créés depuis {opts['csv']}")
    if opts["save"]:
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(opts["save"]).resolve()))
        print(f"Enregistré : {opts['save']}")


main()
