# Temple d'Ézéchiel (Ez 40-48) — croquis et blocking Blender

Choix validés le 24/11/2026 : coudée longue = 52,5 cm (roseau = 3,15 m), enceinte de 500 coudées,
vestibule de 12 coudées, porte lue 6 + 13 + 6, hauteurs supposées (étages de 5, marches de ½),
portion sacrée 25 000 × 25 000 coudées (Lévites / prêtres / ville), annexe de la brique de siège gardée.

| Fichier | Contenu |
|---|---|
| `storyboard-ezechiel.html` | Storyboard des 18 planches ; contient le dessin de toutes les planches |
| `croquis/planche-XX-*.svg` | Planches A3 paysage avec cartouche, échelle et légende (vectoriel, éditable) |
| `croquis/planche-XX-*.png` | Les mêmes en 3840 × 2715 px |
| `cotes.csv` | 301 volumes : position, dimensions en coudées et en mètres, versets, certitude |
| `blender/construire_temple.py` | Construit le blocking dans Blender à partir de `cotes.csv` |
| `blender/temple_ezechiel_blocking.blend` | Résultat déjà construit (Blender 4.1) |
| `outils/` | Scripts de génération |

## Repère du modèle

Origine au centre de l'autel (= centre de l'enceinte), X vers l'est, Y vers le nord, Z vers le haut,
Z = 0 au sol extérieur. Les objets sont en coudées, rattachés à l'empty `Temple_Ezechiel` mis à
l'échelle 0,525 : la scène est en mètres. Couleur d'objet : gris = cote du texte, bleu = déduit,
ocre = hypothèse (chaque objet porte aussi `versets`, `certitude` et `note` en propriétés).

Niveaux : parvis extérieur +3,5 ; parvis intérieur +7,5 ; plate-forme du temple +13,5 (coudées).

## Régénérer

```powershell
.venv\Scripts\python.exe ezechiel\outils\exporter_croquis.py
```

```powershell
.venv\Scripts\python.exe ezechiel\outils\generer_cotes.py
```

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe" --background --python ezechiel\blender\construire_temple.py -- --csv ezechiel\cotes.csv --save ezechiel\blender\temple_ezechiel_blocking.blend
```

Pour changer une hypothèse (hauteur des portes, de la nef, des étages…), modifier les constantes en
tête de `outils/generer_cotes.py`, puis relancer les deux dernières commandes.
