# Installer l'agent de montage sur un autre ordinateur (Windows)

## 1. Copier le dossier

**Depuis GitHub** : sur https://github.com/edklr-maker/INSTALLATION.md, bouton vert **Code →
Download ZIP**, puis décompresse et renomme le dossier en `vidéosdudimanche` (dans `Vidéos`).

**Ou à la main** : copie tout le dossier `vidéosdudimanche` sur l'autre PC (clé USB, disque externe…), de préférence
dans `Vidéos`. **Inutile de copier** `.venv` (il est recréé) ni `travail` (fichiers temporaires).
`rushs` et `montages` sont facultatifs.
Évite les emplacements très profonds (au-delà de ~200 caractères de chemin, Windows refuse de lancer Python).

## 2. Installer les outils

Double-clique sur **`installer.bat`**. Il installe FFmpeg, Python 3.12, les bibliothèques et le
modèle Whisper (compter 5 à 10 min, connexion Internet nécessaire la première fois).
Si Windows affiche « Windows a protégé votre ordinateur » : *Informations complémentaires → Exécuter quand même*.

## 3. Créer la tâche du dimanche

Sur l'autre PC, ouvre l'application Claude, choisis ce dossier comme dossier de travail et écris :

> Lis INSTALLATION.md et crée la tâche du dimanche pour cet ordinateur.

Claude (toi, si tu lis ceci) : crée la tâche planifiée `montage-du-dimanche`, titre
« Montage vidéo du dimanche », planification `0 14 * * 0` (dimanche 14 h), avec le prompt
ci-dessous en remplaçant `{DOSSIER}` par le chemin absolu de ce dossier sur cet ordinateur.
Vérifie d'abord que `{DOSSIER}\.venv\Scripts\python.exe` existe ; sinon, lance `installer.bat`.

```
Tu es mon monteur vidéo. Travaille dans le dossier {DOSSIER} (utilise toujours ce chemin absolu).

1. Lis {DOSSIER}\CLAUDE.md puis la skill {DOSSIER}\.claude\skills\montage-youtube\SKILL.md et suis-la exactement.
2. Liste les vidéos (.mp4, .mov, .mkv, .m4v, .avi, .webm) directement dans {DOSSIER}\rushs (pas dans rushs\traites). S'il n'y en a aucune, termine en disant simplement « Aucun rush à monter cette semaine ».
3. Pour chaque vidéo : transcrire, lire blocs.txt, écrire plan.json selon le style de la skill, monter, écrire le rapport, puis déplacer le rush dans rushs\traites si tout a réussi. Utilise uniquement {DOSSIER}\.venv\Scripts\python.exe. Les transcriptions de vidéos longues prennent du temps : lance-les en arrière-plan et attends qu'elles finissent.
4. Ne publie rien, n'envoie rien, ne supprime aucun rush : tout reste en local.
5. Termine par un résumé court en français : pour chaque vidéo, durée avant/après, nombre de coupes, chemin du montage et du rapport, et les passages douteux à vérifier.
```

## 4. Un seul ordinateur à la fois

Chaque PC a sa propre tâche du dimanche. **Mets en pause la tâche sur l'ordinateur qui ne monte
pas** (barre latérale de Claude → *Scheduled* → *Montage vidéo du dimanche*), sinon les deux
monteraient les mêmes rushs si le dossier est synchronisé (OneDrive, etc.).

Les réglages (`config.json`) et le style de montage (`.claude\skills\montage-youtube\SKILL.md`)
voyagent avec le dossier : si tu les modifies sur un PC, recopie-les sur l'autre.

## Matériel

- Windows 10 ou 11, 8 Go de RAM minimum, environ 3 Go libres pour les outils.
- Pas besoin de carte graphique : tout tourne sur le processeur. Un processeur plus récent
  accélère surtout le rendu (prévoir ~40 min pour une prédication de 35 min sur ce PC-ci).
