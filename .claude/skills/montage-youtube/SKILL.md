---
name: montage-youtube
description: Monte les vidéos longues YouTube déposées dans rushs/ - transcription locale, suppression des silences, ratés et répétitions, rendu FFmpeg, sous-titres et rapport. À utiliser pour "monte mes vidéos", le montage du dimanche, ou une vidéo précise à monter.
---

# Montage YouTube du dimanche

Tu es le monteur. Tout se passe en local : la vidéo ne quitte jamais l'ordinateur.
Python du projet : `.venv\Scripts\python.exe` (toujours lui, jamais un autre Python).

## Déroulé pour chaque vidéo de `rushs/` (hors `rushs/traites/`)

1. **Transcrire** : `.venv\Scripts\python.exe outils\transcrire.py "rushs\<fichier>"`
   (lance-le en arrière-plan si la vidéo dépasse 10 min ; c'est l'étape la plus longue).
2. **Lire** `travail\<nom>\blocs.txt` en entier. Chaque ligne = un bloc de parole entre deux pauses.
3. **Décider** les coupes selon le style ci-dessous, puis écrire `travail\<nom>\plan.json` :
   ```json
   {
     "supprimer": [3, 4, 17],
     "retirer": [[125.40, 126.10]],
     "raisons": {"3": "faux départ, repris au bloc 5", "4": "euh isolé"}
   }
   ```
   - `supprimer` : ids de blocs entiers à enlever.
   - `retirer` : plages en secondes (prises dans les horodatages des mots de `blocs.json`)
     pour enlever un morceau à l'intérieur d'un bloc qu'on garde.
   - Chaque suppression a une raison courte dans `raisons`.
4. **Monter** : `.venv\Scripts\python.exe outils\monter.py "rushs\<fichier>"`
5. **Rapport** : écrire `montages\<nom>_rapport.md` (voir plus bas).
6. **Ranger** : déplacer le rush dans `rushs\traites\` seulement si le montage a réussi.

Si une étape échoue, ne range pas le rush : note l'erreur dans le rapport et passe à la vidéo suivante.

## Style de montage (à ajuster au fil des semaines)

- **Ratés et faux départs** : quand une phrase est commencée puis reprise, garde uniquement
  la DERNIÈRE prise complète, supprime les précédentes.
- **Répétitions** : si la même idée est dite deux fois de suite, garde la version la plus claire.
- **Hésitations** : supprime les blocs qui ne contiennent que « euh », « bon », « alors »,
  « attends », « je recommence », « coupe ça », etc.
- **Consignes au monteur** : si je dis « coupe », « on la refait », « ça on enlève », supprime
  la phrase ratée ET la consigne.
- **Début** : la vidéo commence directement sur la première vraie phrase (pas de « c'est bon ça tourne ? »).
- **Fin** : coupe tout ce qui suit la dernière phrase de conclusion (« à la semaine prochaine », etc.).
- **Ne jamais** couper le milieu d'une phrase utile, ni une blague ou une respiration voulue :
  en cas de doute, GARDE et signale-le dans le rapport.
- Les silences sont déjà raccourcis automatiquement (`pause_coupure_s` et `marge_s` dans `config.json`).

## Prédications (enregistrements de culte en direct)

Les rushs sont le plus souvent des prédications filmées en direct, pas des prises refaites.
Le montage y est léger :
- Coupe le début s'il commence au milieu d'une phrase, et la fin si elle s'arrête net.
- Coupe les phrases clairement abandonnées, les bégaiements (« Tout Tout ») et les références
  répétées pendant que l'orateur cherche le passage (« Matthieu 11-29… Matthieu 11-29 »).
- GARDE les répétitions oratoires (insistance, reformulation volontaire), les citations bibliques
  lues, les « Amen », et la prière finale.
- Attention aux fautes de transcription sur les noms bibliques (Éphésiens, Colossiens, Romains…) :
  ce ne sont pas des erreurs de l'orateur, ne coupe rien pour ça. Corrige-les en revanche dans le
  titre, la description et les chapitres du rapport.

## Rapport `montages\<nom>_rapport.md`

- Durée avant / après, nombre de coupes.
- Liste des suppressions avec leur raison (les ids et horodatages d'origine).
- Les passages douteux que tu as gardés, à vérifier par moi.
- Proposition de **titre YouTube**, de **description** (3-4 lignes) et de **chapitres**
  (horodatages calculés sur la vidéo montée, en s'appuyant sur `<nom>_monte.srt`).
