Mouzikty Music Player
Mouzikty is a simple music player application built using PyQt5 and MySQL for user authentication. It allows users to play music from their local folders, manage playlists, and offers features like shuffling and repeating songs. Users can also register and log in to the application to create and save playlists.

Features
User authentication with MySQL database
Play music from local folders
Create and manage playlists
Shuffle and repeat songs
Show recently played songs history
Prerequisites
Before running the application, make sure you have the following installed:

Python 3.x
PyQt5
PyQt5 Multimedia
PyQt5 QtMultimediaWidgets
PyQt5 QtMultimedia
PyQt5 QtSql
MySQL Connector
You should also have MySQL server installed and running with appropriate user and database setup.
Installation and Usage
Clone the repository to your local machine:
bash
Copy code
git clone <repository_url>
Install the required Python packages:
bash
Copy code
pip install PyQt5 PyQt5-Multimedia PyQt5-QtMultimediaWidgets PyQt5-QtMultimedia PyQt5-QtSql mysql-connector-python
Create a MySQL database named mouzikty and set up the users table with columns id, username, and password.

Update the MySQL database connection details in the LoginWindow class constructor:

python
Copy code
self.db_connection = mysql.connector.connect(
    host='localhost',
    user='your_mysql_username',
    password='your_mysql_password',
    database='mouzikty'
)
Run the application:
bash
Copy code
python mouzikty.py
The login window will appear. You can either log in with existing credentials or register a new account.

After logging in, the main music player window will open. Click the "Open Folder" button to select a folder containing your music files. You can then add songs to your playlist and control playback.

Screenshots
Login

Main

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to PyQt5 and MySQL for providing the tools necessary to build this application.
Icon sources: iconfinder.com
Background image source: freepik.com
Note: This README assumes that you have a basic understanding of Python, PyQt5, and MySQL. If you encounter any issues or have questions, please refer to the project's documentation or seek assistance from the community.
