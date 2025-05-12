# 🎥 Youtube_Backup

**Youtube_Backup** est un script Python permettant de sauvegarder les vidéos d’une chaîne YouTube grâce à l’API officielle de Google.  
Idéal pour archiver automatiquement tes contenus ou faire une copie locale avant suppression/privatisation.

---

## 🚀 Fonctionnalités

- Récupération des vidéos d'une chaîne à partir de son ID
- Téléchargement via l’API officielle (pas de scraping sauvage)
- Possibilité de reprendre depuis une vidéo spécifique
- Utilisation simple en ligne de commande

---

## 🛠️ Installation

1. Clone le repo :
```bash
git clone https://github.com/Ybucaille/Youtube_Backup.git
cd Youtube_Backup
```

2. Installe les dépendances :
```bash
pip install -r requirements.txt
```

3. Configure ton accès API :
- Crée une clé API ici → [Google Cloud Console](https://console.cloud.google.com/)
- Crée un fichier `api_key.json` avec ce format :
```json
{
  "api_key": "TON_API_KEY"
}
```

---

## 💡 Utilisation

Lancement du script :
```bash
python main.py --start <VIDEO_ID>
```

Options disponibles :
```bash
--start     ID de la vidéo à partir de laquelle commencer
--help      Affiche l’aide
```

---

## 🧪 Exemple

```bash
python main.py --start dQw4w9WgXcQ
```

---

## 📦 Fichiers importants

- `main.py` → Script principal
- `api_key.json` → Clé API privée (à ne jamais publier)
- `requirements.txt` → Dépendances Python nécessaires

---

## 📜 Licence

[MIT License](LICENSE)

---

> Développé par [Yann Bucaille](https://github.com/Ybucaille) — pour garder une trace de ce qui compte.
