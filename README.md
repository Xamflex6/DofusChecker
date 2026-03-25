# DofusChecker

Objectif actuel:
- Setup de Tesseract OCR
- Calibrage des coordonnees souris pour les colonnes NOM/PRIX
- Pretraitement d'un screenshot de prix en image binaire exploitable

## 1) Setup Tesseract (Windows)

Installer Tesseract:

```powershell
winget install --id UB-Mannheim.TesseractOCR -e
```

Puis verifier que le binaire existe, en general:

```text
C:/Program Files/Tesseract-OCR/tesseract.exe
```

Mettre ce chemin dans `config.json` si necessaire.

Installer les dependances Python:

```powershell
python -m pip install -r requirements.txt
```

Verifier la detection OCR:

```powershell
python main.py check-tesseract
```

## 2) Calibrage souris (temps reel)

Lancer le calibrage:

```powershell
python main.py calibrate --config config.json
```

Ce que fait la commande:
- Affiche en temps reel la position de la souris (X/Y)
- Demande de placer la souris sur la colonne NOM puis Entree
- Demande de placer la souris sur la colonne PRIX puis Entree
- Enregistre les coordonnees dans `config.json`

## 3) Pretraitement binaire d'un screenshot

Exemple:

```powershell
python main.py preprocess --input logs/prix_raw.png --output logs/prix_bw.png --scale 3
```

Pipeline applique:
- Passage en niveaux de gris
- Agrandissement (pour aider l'OCR)
- Reduction du bruit (bilateral filter)
- Binarisation Otsu (noir/blanc pur)
- Nettoyage morphologique leger

Image de sortie:
- Pixels uniquement a 0 ou 255
- Prete pour OCR de nombres de prix