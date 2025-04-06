import sys
import random
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QMessageBox, QFrame, QGraphicsOpacityEffect, QSplitter)
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QBrush, QLinearGradient, QPainter
from PySide6.QtCore import Qt, QUrl, QSize, QPropertyAnimation, QEasingCurve, QTimer, Property, QRect
from PySide6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput

# Cohesive color scheme
COLORS = {
    'primary': '#6a4c93',      # Purple - primary color
    'secondary': '#1982c4',    # Blue - secondary color
    'accent': '#8ac926',       # Green - accent color
    'warning': '#ffca3a',      # Yellow - warning color
    'danger': '#ff595e',       # Red - danger color
    'light': '#f8f9fa',        # Light color for text
    'dark': '#343a40',         # Dark color for text
    'bg_gradient_start': '#6a4c93',  # Start of background gradient
    'bg_gradient_end': '#1982c4'     # End of background gradient
}

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['light']};
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                font-family: Gabriola;
                font-size: 18px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['dark']};
            }}
        """)
        
        # Setup animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.8)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)

class AnimatedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {COLORS['primary']};
                border-radius: 15px;
                padding: 8px 15px;
                background-color: rgba(255, 255, 255, 0.8);
                selection-background-color: {COLORS['primary']};
                font-family: Gabriola;
                font-size: 18px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['secondary']};
                background-color: white;
            }}
        """)

class StylishFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            StylishFrame {{
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)

class GuessNumberGame(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Game variables
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = True
        
        # Setup UI
        self.setWindowTitle("Devine le Nombre")
        self.setFixedSize(1200, 600)
        self.setWindowIcon(QIcon("images/icon.png"))
        
        # Set background
        self.set_background()
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)
        
        # Title in a stylish frame
        self.title_frame = StylishFrame()
        self.title_layout = QVBoxLayout(self.title_frame)
        self.title_layout.setContentsMargins(20, 20, 20, 20)
        
        self.title_label = QLabel("Devine le Nombre !")
        title_font = QFont("Gabriola", 52, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {COLORS['secondary']}; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.title_label)
        
        # Instructions and attempts in the same row
        self.info_frame = QFrame()
        self.info_layout = QHBoxLayout(self.info_frame)
        
        self.instructions = QLabel("L'ordinateur a choisi un nombre entre 1 et 100.")
        self.instructions.setFont(QFont("Gabriola", 26))
        self.instructions.setStyleSheet(f"color: {COLORS['light']};")
        self.info_layout.addWidget(self.instructions)
        
        self.attempts_label = QLabel("Nombre d'essais : 0")
        self.attempts_label.setFont(QFont("Gabriola", 24))
        self.attempts_label.setStyleSheet(f"color: {COLORS['light']}; background-color: rgba(106, 76, 147, 0.3); border-radius: 15px; padding: 5px 15px;")
        self.info_layout.addWidget(self.attempts_label)
        
        self.title_layout.addWidget(self.info_frame)
        
        # Start game button (initially visible)
        self.start_game_button = AnimatedButton("Commencer le jeu")
        self.start_game_button.setFont(QFont("Gabriola", 28))
        self.start_game_button.clicked.connect(self.start_game)
        self.title_layout.addWidget(self.start_game_button)
        
        self.main_layout.addWidget(self.title_frame)
        
        # Game content area with splitter
        self.content_frame = StylishFrame()
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # Input area - initially hidden
        self.input_frame = StylishFrame()
        self.input_frame.setVisible(False)  # Initially hidden until game starts
        self.input_layout = QHBoxLayout(self.input_frame)
        self.input_layout.setContentsMargins(25, 20, 25, 20)
        self.input_layout.setAlignment(Qt.AlignCenter)  # Center the input elements
        
        self.input_label = QLabel("Votre proposition :")
        self.input_label.setFont(QFont("Gabriola", 28))
        self.input_label.setStyleSheet(f"color: {COLORS['light']}; background-color: transparent;")
        self.input_layout.addWidget(self.input_label)
        
        self.input_field = AnimatedLineEdit()
        self.input_field.setFont(QFont("Gabriola", 28))
        self.input_field.setFixedWidth(180)
        self.input_field.returnPressed.connect(self.check_guess)
        self.input_layout.addWidget(self.input_field)
        
        self.guess_button = AnimatedButton("Valider")
        self.guess_button.setFont(QFont("Gabriola", 28))
        self.guess_button.clicked.connect(self.check_guess)
        self.input_layout.addWidget(self.guess_button)
        
        self.content_layout.addWidget(self.input_frame)
        
        # Feedback area with image - initially hidden
        self.feedback_frame = StylishFrame()
        self.feedback_frame.setVisible(False)  # Initially hidden
        self.feedback_frame.setStyleSheet(f"""
            StylishFrame {{
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        self.feedback_layout = QHBoxLayout(self.feedback_frame)
        self.feedback_layout.setContentsMargins(25, 20, 25, 20)
        
        self.feedback_image = QLabel()
        self.feedback_image.setFixedSize(120, 120)
        self.feedback_image.setScaledContents(True)
        self.feedback_layout.addWidget(self.feedback_image)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Gabriola", 32, QFont.Bold))
        self.feedback_label.setStyleSheet(f"color: {COLORS['light']}; background-color: transparent;")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setMinimumHeight(120)
        self.feedback_layout.addWidget(self.feedback_label)
        
        self.content_layout.addWidget(self.feedback_frame)
        
        # New game button
        self.new_game_button = AnimatedButton("Nouvelle Partie")
        self.new_game_button.setFont(QFont("Gabriola", 28))
        self.new_game_button.clicked.connect(self.start_new_game)
        self.new_game_button.setVisible(False)
        self.content_layout.addWidget(self.new_game_button)
        
        self.main_layout.addWidget(self.content_frame)
        
        # Load sounds
        self.setup_sounds()
        
        # Start background music
        self.play_background_music()
        
        # Start game animation
        QTimer.singleShot(500, self.animate_startup)
    
    def set_background(self):
        # Set background image
        palette = self.palette()
        bg_image = QPixmap("images/bg.jpg")
        if not bg_image.isNull():
            palette.setBrush(QPalette.Window, QBrush(bg_image.scaled(
                self.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation)))
        else:
            # Fallback to gradient if image not found
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(COLORS['bg_gradient_start']))
            gradient.setColorAt(1, QColor(COLORS['bg_gradient_end']))
            palette.setBrush(QPalette.Window, QBrush(gradient))
        
        self.setPalette(palette)
    
    def setup_sounds(self):
        try:
            # Sound effects - using QMediaPlayer for all sounds for better compatibility
            self.correct_sound = QMediaPlayer()
            self.correct_sound_output = QAudioOutput()
            self.correct_sound.setAudioOutput(self.correct_sound_output)
            self.correct_sound_output.setVolume(0.7)
            self.correct_sound.setSource(QUrl.fromLocalFile(os.path.abspath("sounds/start_game.mp3")))
            
            # Win sound
            self.win_sound = QMediaPlayer()
            self.win_sound_output = QAudioOutput()
            self.win_sound.setAudioOutput(self.win_sound_output)
            self.win_sound_output.setVolume(0.7)
            self.win_sound.setSource(QUrl.fromLocalFile(os.path.abspath("sounds/brass-fanfare-with-timpani-and-winchimes-reverberated-146260.mp3")))
            
            # Background music player
            self.music_player = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.music_player.setAudioOutput(self.audio_output)
            self.audio_output.setVolume(0.3)  # Set volume to 30%
            self.music_player.setSource(QUrl.fromLocalFile(os.path.abspath("sounds/lady-of-the-80x27s-128379.mp3")))
            self.music_player.setLoops(QMediaPlayer.Infinite)
        except Exception as e:
            print(f"Erreur lors du chargement des sons: {e}")
    
    def play_background_music(self):
        try:
            self.music_player.play()
        except Exception as e:
            print(f"Erreur lors de la lecture de la musique: {e}")
    
    def animate_startup(self):
        try:
            self.correct_sound.play()
        except Exception as e:
            print(f"Erreur lors de la lecture du son de démarrage: {e}")
    
    def start_game(self):
        self.game_over = False
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.attempts_label.setText("Nombre d'essais : 0")
        self.input_frame.setVisible(True)
        self.start_game_button.setVisible(False)
        self.input_field.setFocus()
        try:
            self.correct_sound.stop()
            self.correct_sound.play()
        except Exception as e:
            print(f"Erreur lors de la lecture du son de démarrage: {e}")
    
    def check_guess(self):
        if self.game_over:
            return
            
        # Get input
        guess_text = self.input_field.text().strip()
        self.input_field.clear()
        
        # Validate input
        if not guess_text.isdigit():
            QMessageBox.warning(self, "Entrée invalide", "Veuillez entrer un nombre valide.")
            return
            
        guess = int(guess_text)
        if guess < 1 or guess > 100:
            QMessageBox.warning(self, "Entrée invalide", "Veuillez entrer un nombre entre 1 et 100.")
            return
        
        # Show feedback frame if it was hidden
        if not self.feedback_frame.isVisible():
            self.feedback_frame.setVisible(True)
            
        # Increment attempts
        self.attempts += 1
        self.attempts_label.setText(f"Nombre d'essais : {self.attempts}")
        
        # Check guess
        if guess < self.secret_number:
            self.feedback_label.setText("Trop bas !")
            self.feedback_label.setStyleSheet(f"color: {COLORS['secondary']}; font-weight: bold; background-color: transparent;")
            self.feedback_image.setPixmap(QPixmap("images/false.png"))
        elif guess > self.secret_number:
            self.feedback_label.setText("Trop haut !")
            self.feedback_label.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold; background-color: transparent;")
            self.feedback_image.setPixmap(QPixmap("images/false.png"))
        else:
            self.feedback_label.setText(f"Bravo ! Vous avez trouvé le nombre en {self.attempts} essais.")
            self.feedback_label.setStyleSheet(f"color: {COLORS['accent']}; font-weight: bold; background-color: transparent;")
            self.feedback_image.setPixmap(QPixmap("images/true.png"))
            self.game_over = True
            
            # Hide input frame and show new game button
            self.input_frame.setVisible(False)
            self.new_game_button.setVisible(True)
            
            try:
                self.win_sound.stop()
                self.win_sound.play()
            except Exception as e:
                print(f"Erreur lors de la lecture du son de victoire: {e}")
    
    def start_new_game(self):
        # Reset game variables and start a new game directly
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False  # Set to false to start game immediately
        
        # Reset UI
        self.attempts_label.setText("Nombre d'essais : 0")
        self.feedback_label.setText("")
        self.feedback_label.setStyleSheet(f"color: {COLORS['light']}; background-color: transparent;")
        self.feedback_frame.setVisible(False)
        self.new_game_button.setVisible(False)
        self.start_game_button.setVisible(False)  # Keep hidden
        self.input_frame.setVisible(True)  # Show input frame directly
        self.input_field.setFocus()
        
        try:
            self.correct_sound.stop()
            self.correct_sound.play()
        except Exception as e:
            print(f"Erreur lors de la lecture du son de démarrage: {e}")

    def resizeEvent(self, event):
        # Update background when window is resized
        self.set_background()
        super().resizeEvent(event)
        
    def paintEvent(self, event):
        # Add some custom painting for a more polished look
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        # Draw subtle decorative elements
        painter.setBrush(QColor(255, 255, 255, 15))
        painter.drawEllipse(QRect(50, 50, 100, 100))
        painter.drawEllipse(QRect(self.width() - 150, self.height() - 150, 100, 100))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the game window
    game = GuessNumberGame()
    game.show()
    
    sys.exit(app.exec())