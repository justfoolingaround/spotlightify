# Spotlightify+

Spotlightify is a GUI based application designed to allow users to quickly interact with the Spotify Desktop application across Windows, Linux and macOS, originally found [here.](https://github.com/spotlightify/spotlightify)

This is a fork that makes this project **work on a free Spotify account** by using [spotivents](https://github.com/justfoolingaround/spotivents).

![Spotlightify](preview.gif)

## Prerequisites

-   Spotify's `sp_dc` cookie
-   Python 3.7 or later

## Installing Dependencies

### OS Specific Setup

To setup a virtual environment, perform the following commands.

#### Windows

```
cd path\to\spotlightify-root
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
To run the application as an independent process (i.e. it will not end when the command line is exited), use: `pythonw app.py`

#### MacOS

```
cd path/to/spotlightify-root
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Linux

```
cd path/to/spotlightify-root
python3 -m venv venv
. venv/bin/activate
sudo apt-get install python3-pyqt5
pip3 install -r requirements.txt

python3 app.py
```


### Installing Fonts

The fonts found in `assets/fonts` must be installed for this to display correctly.

## Usage

The GUI is activated by using the shortcut `ctrl + space`. Here is the current list of available functions:

### List of Commands

```
| Name     | Description                                        | Prefix            | Parameter     |
|----------|----------------------------------------------------|-------------------|---------------|
| Play     | Find and play a song                               | play              | song name     |
| Queue    | Find and queues a song                             | queue             | song name     |
| Playlist | Find and play a saved/followed playlist            | playlist          | playlist name |
| Album    | Find and play a saved album                        | album             | album name    |
| Artist   | Find and play songs from a saved/followed artist   | artist            | artist name   |
| Liked    | Plays saved/liked music                            | liked             | None          |
| Volume   | Changes music volume                               | volume            | 1 - 10        |
| Go to    | Seeks a position in a song                         | goto              | e.g. 1:24     |
| Resume   | Resumes music playback                             | resume            | None          |
| Skip     | Skips the current song                             | next              | None          |
| Previous | Plays pervious song                                | previous          | None          |
| Pause    | Pauses music playback                              | pause             | None          |
| Shuffle  | Toggles shuffle playback                           | shuffle           | None          |
| Device   | Select device for music playback                   | device            | None          |
| Repeat   | Toggles repeating modes                            | repeat            | None          |
| Current  | Provides currently playing song info               | currently playing | None          |
| Share    | Copies the current song's URL to clipboard         | share             | None          |
| Exit     | Exits the application                              | exit              | None          |
```

### List of Song Options

```
| Name                      | Description                                        |
|---------------------------|----------------------------------------------------|
| Add Song to Queue         | Adds the selected song to the queue                |
| Add Song to Playlist      | Adds the selected song to the selected playlist    |
| Play Song Radio           | Plays a Spotify radio related to the selected song |
| Save/Like Song            | Saves the selected song to user Spotify library    |
| Share Song                | Copies the selected song's URL to the clipboard    |
```
Song options are shown by holding down either `shift` key and `left clicking`/pressing the `enter` key on the song.  


## Additional Information

### Built With

-   <a href="https://spotipy.readthedocs.io/en/2.12.0/" target="_blank">Spotipy</a> - A Spotify API wrapper for Python
-   <a href="https://www.riverbankcomputing.com/software/pyqt/" target="_blank">PyQt5</a> - A cross platform GUI framework for Python

### Reddit Posts

- https://www.reddit.com/r/Python/comments/go6no5/spotlightify_a_overlay_controller_for_spotify/
- https://www.reddit.com/r/Python/comments/gtnyll/spotlightify_the_spotify_overlay_controller/

### Contributing

Join us on <a href="https://discord.gg/nrDke3q" target="_blank">discord</a> to discuss how to contribute to the project.
