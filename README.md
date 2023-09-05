
# Mouzikty 

Mouzikty is a 100% Tunisian versatile and user-friendly music player application built using Python and the PyQt5 framework. It empowers music enthusiasts to enjoy their favorite tunes, organize playlists, and manage their digital music libraries seamlessly. With its intuitive interface and a host of features, Mouzikty provides a rich music listening experience.


## Key Features
### 1. User Authentication and Registration

Mouzikty includes a secure login system, allowing registered users to access their personalized music libraries.
New users can easily register by creating an account with a unique username and password.

### 2. Playlist Management

Users can create, load, and save playlists to curate their music collections.
Playlists offer a convenient way to organize songs for different moods, occasions, or genres.

### 3. Playback Control

Mouzikty offers standard music playback controls, including play, pause, next track, and previous track.
Users can adjust the volume using an intuitive slider to suit their preferences.

### 4. Shuffle and Repeat Modes

Users can toggle the shuffle mode to randomize the playback order, adding an element of surprise to their music experience.
The repeat mode allows for continuous playback of a single track or the entire playlist.

### 5. Recently Played Songs

Mouzikty keeps track of the recently played songs, making it easy for users to revisit their favorite tracks.
The history feature displays the most recently played songs in a user-friendly menu.

### 6. Keyboard Shortcuts

For efficiency, Mouzikty includes keyboard shortcuts for common actions like play/pause and navigating tracks.
## Requirements
Before using Mouzikty, ensure you have the following dependencies installed on your system:

Python 3

PyQt5

PyQt5 Multimedia

MySQL Connector (for database operations)

Additional libraries may be required for image handling, depending on your setup.


## How To Run

Follow these steps to run Mouzikty on your machine:

Clone this repository to your local computer.

Open a terminal or command prompt and navigate to the project directory.

Install the required dependencies using pip:

```bash
pip install PyQt5 PyQt5Multimedia mysql-connector-python
```
Set up your MySQL database. You can use a tool like `phpMyAdmin` or any `MySQL` management tool to create a database named mouzikty and a table named users with columns `username` and `password`. Update the database connection details in the code as necessary.

Run the main application:

```bash
python main_with_login.py
```

The login window will appear. You can use the provided login credentials or register a new account.

After logging in, the main music player window will open. You can start adding music to your playlist and enjoy your favorite songs!

### Ps: Dont forget to change the host , user , password and database variables in the code 


## Authors

- Mouzikty was created by [@OmarBelll](https://github.com/OmarBelll) and is open-source. Contributions and improvements are welcome from the community.


## Feedback

If you have any feedback, please reach out to us at omarbellolxd@gmail.com

