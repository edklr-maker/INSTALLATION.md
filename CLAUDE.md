# Montage vidéo du dimanche

Agent de montage pour vidéos longues YouTube. La procédure complète et le style sont dans la skill
`.claude/skills/montage-youtube/SKILL.md` : la suivre pour tout montage.

- `rushs/` : vidéos brutes à monter ; `rushs/traites/` : rushs déjà montés
- `montages/` : vidéos finales, sous-titres .srt et rapports
- `travail/` : fichiers intermédiaires (transcriptions, plans, morceaux) - peut être vidé
- `outils/` : scripts Python ; Python du projet : `.venv\Scripts\python.exe`
- `config.json` : réglages (modèle Whisper, seuil de pause, marges, qualité)
- `installer.bat` / `INSTALLATION.md` : installation sur un autre ordinateur et création de la tâche du dimanche
