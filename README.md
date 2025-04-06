# Devine le Nombre - Jeu Élégant en PySide6

Un jeu interactif et élégant où vous devez deviner un nombre entre 1 et 100 choisi par l'ordinateur, avec une interface graphique moderne et des effets sonores.

## Fonctionnalités

- Interface graphique élégante avec la police Gabriola
- Effets sonores pour le démarrage, les victoires et la musique de fond
- Animations et effets visuels
- Feedback visuel pour les réponses correctes et incorrectes
- Mode de jeu intuitif avec progression claire

## Installation

Pour installer les dépendances nécessaires :

```
pip install -r requirements.txt
```

Ou avec Python 3.12+ :

```
py -m pip install -r requirements.txt
```

## Comment jouer

1. Exécutez le fichier `guess_number_game.py`
2. Cliquez sur le bouton "Commencer le jeu"
3. Entrez votre proposition dans le champ de texte
4. Cliquez sur "Valider" ou appuyez sur Entrée
5. Suivez les indications (trop haut/trop bas) jusqu'à trouver le nombre
6. Une fois le nombre trouvé, vous pouvez démarrer une nouvelle partie

## Structure du projet

- `guess_number_game.py` : Le fichier principal du jeu
- `images/` : Dossier contenant les images du jeu
  - `bg.jpg` : Image de fond
  - `true.png` : Image pour les réponses correctes
  - `false.png` : Image pour les réponses incorrectes
  - `icon.png` : Icône du jeu
- `sounds/` : Dossier contenant les effets sonores du jeu
  - `start_game.mp3` : Son joué au démarrage d'une partie
  - `brass-fanfare-with-timpani-and-winchimes-reverberated-146260.mp3` : Son de victoire
  - `lady-of-the-80x27s-128379.mp3` : Musique de fond

## Caractéristiques techniques

- Développé avec Python et PySide6 (Qt)
- Palette de couleurs cohérente
- Interfaces personnalisées (StylishFrame, AnimatedButton, AnimatedLineEdit)
- Gestion avancée des états de jeu
- Effets visuels avec QPainter

## Crédits

Développé comme exemple de jeu simple avec une interface graphique professionnelle.
