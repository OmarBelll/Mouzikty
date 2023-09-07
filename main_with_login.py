import sys
import os
import random
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QSlider, QMenu, QAction, QSizePolicy, QDialog, QLineEdit, QMessageBox,
    QProgressBar, QCheckBox, QFormLayout, QShortcut
)
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont
import mysql.connector
import glob

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel(self)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setPixmap(QPixmap("logo.png"))
        layout.addWidget(logo_label)

        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        current_font = self.username_input.font()
        current_font.setPointSize(int(current_font.pointSize() * 1.3))
        self.username_input.setFont(current_font)
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        current_font = self.password_input.font()
        current_font.setPointSize(int(current_font.pointSize() * 0.9))
        self.password_input.setFont(current_font)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        show_password_layout = QHBoxLayout()
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet(
            """
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                image: url(eye_open.png);
            }
            QCheckBox::indicator:unchecked {
                image: url(eye_closed.png);
            }
            QCheckBox::indicator:unchecked:hover {
                background-color: #f0f0f0;
            }
            """
        )
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        show_password_layout.addWidget(self.show_password_checkbox)
        layout.addLayout(show_password_layout)

        button_layout = QHBoxLayout()

        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )
        self.login_button.clicked.connect(self.check_login)
        button_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            """
        )
        self.register_button.clicked.connect(self.show_registration_dialog)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.db_connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database=''
        )
        self.cursor = self.db_connection.cursor()

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def show_registration_dialog(self):
        registration_dialog = RegistrationDialog(self.cursor, self)
        registration_dialog.exec_()

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        self.cursor.execute(query, values)
        user_data = self.cursor.fetchone()
        if user_data:
            self.accept()
        else:
            QMessageBox.warning(self, "Login Error", "Invalid username or password.")

class RegistrationDialog(QDialog):
    def __init__(self, cursor, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setFixedSize(400, 350)
        self.cursor = cursor  # Store the cursor for database operations

        layout = QVBoxLayout()

        title_label = QLabel("Create an Account")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title_label)

        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        form_layout.addRow("Password:", self.password_input)

        self.password_strength_label = QLabel("Password Strength:")
        self.password_strength = QProgressBar()
        self.password_strength.setRange(0, 100)
        self.password_strength.setValue(0)
        form_layout.addRow(self.password_strength_label, self.password_strength)

        layout.addLayout(form_layout)

        # Add a label for validation messages
        self.validation_label = QLabel("", self)
        self.validation_label.setStyleSheet("font-size: 14px; color: red; margin-top: 10px;")
        layout.addWidget(self.validation_label)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Add a register button
        self.register_button = QPushButton("Register", self)
        self.register_button.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            """
        )
        self.register_button.clicked.connect(self.register_user)
        button_layout.addWidget(self.register_button)

        # Add a cancel button
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            """
        )
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.password_input.textChanged.connect(self.update_password_strength)

    def validate_username(self, username):
        # Check if the username is not empty
        if not username:
            return "Username cannot be empty."

        # Check if the username already exists in the database
        query = "SELECT username FROM users WHERE username = %s"
        values = (username,)
        self.cursor.execute(query, values)
        existing_username = self.cursor.fetchone()

        if existing_username:
            return "Username already exists. Please choose a different one."

        # Username is valid
        return None

    def update_password_strength(self):
        password = self.password_input.text()
        strength = self.calculate_password_strength(password)
        self.display_password_strength(strength)

    def calculate_password_strength(self, password):
        # Calculate password strength based on various criteria (e.g., length, complexity)
        length = len(password)
        uppercase = any(c.isupper() for c in password)
        lowercase = any(c.islower() for c in password)
        digits = any(c.isdigit() for c in password)
        symbols = any(not c.isalnum() for c in password)

        strength = 0
        if length >= 8:
            strength += 20
        if uppercase:
            strength += 20
        if digits:
            strength += 20
        if symbols:
            strength += 20
        if lowercase:
            strength += 20

        return strength

    def display_password_strength(self, strength):
        self.password_strength.setValue(strength)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Validate the username
        validation_message = self.validate_username(username)

        if validation_message:
            self.validation_label.setText(validation_message)
            return

        # Proceed with user registration
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password)
        self.cursor.execute(query, values)
        # Commit the changes to the database
        self.cursor.connection.commit()
        QMessageBox.information(self, "Registration", "Registration successful!")
        self.accept()


class MouziktyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouzikty")
        self.player = QMediaPlayer()
        self.playlist = []
        self.current_song_index = -1
        self.current_position = 0
        self.is_playing = False
        self.is_shuffling = False
        self.is_repeating = False
        self.play_history = []

        self.init_ui()
        self.init_player()
        self.create_actions()
        self.create_menus()
        self.create_shortcuts()

        # Apply a global style for the entire application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

    def previous_song(self):
        if not self.playlist:
            return
        if self.is_shuffling:
            self.current_song_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
        self.play_current_song()
    def create_shortcuts(self):
        # Create keyboard shortcuts for common actions
        play_pause_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        play_pause_shortcut.activated.connect(self.play_pause_music)

        next_track_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        next_track_shortcut.activated.connect(self.next_song)

        prev_track_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        prev_track_shortcut.activated.connect(self.previous_song)
    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        self.playlist_label = QLabel("Playlist:")
        self.playlist_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.playlist_label)
        self.playlist_widget = QListWidget()
        self.playlist_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout.addWidget(self.playlist_widget)
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Folder")
        self.open_button.setStyleSheet("QPushButton { background-color: #3498db; color: white; }")
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
        self.play_button.clicked.connect(self.play_pause_music)
        button_layout.addWidget(self.play_button)
        self.shuffle_button = QPushButton("Shuffle")
        self.shuffle_button.setStyleSheet("QPushButton { background-color: #e67e22; color: white; }")
        self.shuffle_button.clicked.connect(self.toggle_shuffle)
        button_layout.addWidget(self.shuffle_button)
        self.repeat_button = QPushButton("Repeat")
        self.repeat_button.setStyleSheet("QPushButton { background-color: #9b59b6; color: white; }")
        self.repeat_button.clicked.connect(self.toggle_repeat)
        button_layout.addWidget(self.repeat_button)
        layout.addLayout(button_layout)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)
        self.volume_label = QLabel("Volume: 50%")
        layout.addWidget(self.volume_label)
        self.song_info_label = QLabel("")
        layout.addWidget(self.song_info_label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def init_player(self):
        self.player.setVolume(50)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

    def set_volume(self, volume):
        self.player.setVolume(volume)
        self.volume_label.setText(f"Volume: {volume}%")

    def create_actions(self):
        self.remove_action = QAction("Remove from Playlist", self)
        self.remove_action.triggered.connect(self.remove_from_playlist)
        self.save_playlist_action = QAction("Save Playlist", self)
        self.save_playlist_action.triggered.connect(self.save_playlist)
        self.load_playlist_action = QAction("Load Playlist", self)
        self.load_playlist_action.triggered.connect(self.load_playlist)

    def create_menus(self):
        menubar = self.menuBar()
        playlist_menu = menubar.addMenu("Playlist")
        playlist_menu.addAction(self.save_playlist_action)
        playlist_menu.addAction(self.load_playlist_action)
        history_menu = menubar.addMenu("History")
        self.show_history_action = QAction("Show History", self)
        self.show_history_action.triggered.connect(self.show_play_history_menu)
        history_menu.addAction(self.show_history_action)

    def open_file(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "", QFileDialog.ShowDirsOnly)
        if folder_path:
            mp3_files = glob.glob(os.path.join(folder_path, "*.mp3"))
            self.playlist.extend(mp3_files)
            self.playlist_widget.addItems([os.path.basename(file) for file in mp3_files])

    def play_pause_music(self):
        if not self.playlist:
            return
        if self.is_playing:
            self.pause_music()
        else:
            self.play_music()

    def play_music(self):
        if self.current_song_index == -1:
            self.current_song_index = 0
        if not self.is_playing:
            self.play_button.setText("Pause")
            self.is_playing = True
            if self.current_position == 0:
                self.play_current_song()
            else:
                self.play_current_song(self.current_position)

    def pause_music(self):
        if self.is_playing:
            self.play_button.setText("Play")
            self.is_playing = False
            self.current_position = self.player.position()
            self.player.pause()

    def update_song_info(self):
        song_name = os.path.splitext(os.path.basename(self.playlist[self.current_song_index]))[0]
        self.song_info_label.setText(f"Now Playing: {song_name}")

    def media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            if self.is_repeating:
                self.play_current_song()
            else:
                self.next_song()

    def position_changed(self, position):
        pass

    def duration_changed(self, duration):
        self.update_song_info()

    def play_current_song(self, position=0):
        self.player.setPosition(position)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[self.current_song_index])))
        self.player.play()
        self.update_song_info()
        self.update_play_history()  # Update play history when playing a new song

    def next_song(self):
        if self.is_shuffling:
            self.current_song_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        self.play_current_song()

    def toggle_shuffle(self):
        self.is_shuffling = not self.is_shuffling
        self.shuffle_button.setStyleSheet(
            "QPushButton { background-color: #e67e22; color: white; }" if self.is_shuffling else ""
        )

    def toggle_repeat(self):
        self.is_repeating = not self.is_repeating
        self.repeat_button.setStyleSheet(
            "QPushButton { background-color: #9b59b6; color: white; }" if self.is_repeating else ""
        )

    def show_context_menu(self, position):
        selected_item = self.playlist_widget.itemAt(position)
        if selected_item:
            menu = QMenu(self)
            menu.addAction(self.remove_action)
            menu.exec_(self.playlist_widget.viewport().mapToGlobal(position))

    def remove_from_playlist(self):
        selected_item = self.playlist_widget.currentItem()
        if selected_item:
            index = self.playlist_widget.row(selected_item)
            self.playlist.pop(index)
            self.playlist_widget.takeItem(index)

    def save_playlist(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Playlist", "", "Playlist Files (*.m3u)")
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(self.playlist))

    def load_playlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Playlist", "", "Playlist Files (*.m3u)")
        if file_path:
            with open(file_path, "r") as f:
                self.playlist = f.read().splitlines()
                self.playlist_widget.clear()
                self.playlist_widget.addItems([os.path.splitext(os.path.basename(song_path))[0] for song_path in self.playlist])

    def update_play_history(self):
        if self.current_song_index != -1:
            song_path = self.playlist[self.current_song_index]
            if song_path in self.play_history:
                self.play_history.remove(song_path)
            self.play_history.insert(0, song_path)
            if len(self.play_history) > 10:
                self.play_history.pop()

    def show_play_history_menu(self):
        history_submenu = QMenu(self)
        history_submenu.setTitle("Recently Played Songs")
        for index, song_path in enumerate(self.play_history):
            song_name = os.path.splitext(os.path.basename(song_path))[0]
            action = QAction(f"{index + 1}. {song_name}", self)
            history_submenu.addAction(action)

        # Use QCursor to specify the position
        cursor = self.mapToGlobal(QPoint(0, 0))  # Replace with the desired position
        history_submenu.exec_(cursor)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        main_window = MouziktyApp()
        main_window.show()

    sys.exit(app.exec_())
