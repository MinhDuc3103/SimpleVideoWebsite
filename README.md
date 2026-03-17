# Nhu Lun Cinema

A simple private video streaming website built with Flask. Stream your local movie and TV series collection through a clean, dark-themed web interface.

## Features

- Browse a collection of movies and TV series
- Separate browsing for Series (TV episodes) and Movies (feature films)
- Smooth video playback via Video.js with keyboard shortcuts
- Auto-resume: remembers where you left off per episode
- Auto-play next episode when current one ends
- Playback speed controls (0.5x - 2x)
- Mobile-friendly responsive layout
- HTTP range request support for seeking on all devices

## Project Structure

```
SimpleVideoWebsite/
├── app.py                  # Flask app and routes
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css       # All styles
│   ├── posters/            # Poster images (jpg/webp)
│   └── videos/             # Video files (not committed)
│       └── <slug>/
│           ├── series/     # TV episode files (MovieN.mp4)
│           └── movies/     # Feature film files (MovieN.mp4)
└── templates/
    ├── index.html          # Home / collection grid
    ├── choice.html         # Series vs Movies selection
    └── player.html         # Video player + episode list
```

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure your video library**

Edit `MOVIES_CONFIG` in `app.py` to point `base_path` to the folder containing your video files:

```python
MOVIES_CONFIG = {
    "my-show": {
        "title": "My Show",
        "desc": "A short description.",
        "poster": "/static/posters/my-show.jpg",
        "base_path": "/path/to/videos/my-show"
    }
}
```

Each `base_path` should contain a `series/` and/or `movies/` subfolder with video files named like `Movie1.mp4`, `Movie2.mp4`, etc.

**3. Run**

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## Video File Naming

Episode files should follow the pattern `Movie<N>.<ext>` (case-insensitive) so they are sorted correctly:

```
Movie1.mp4
Movie2.mp4
Movie10.mp4
```

Supported formats: `.mp4`, `.mkv`, `.webm`, `.avi`, `.mov`

## Keyboard Shortcuts (Player)

| Key | Action |
|-----|--------|
| Space | Play / Pause |
| Left Arrow | Seek back 10s |
| Right Arrow | Seek forward 10s |
| Up Arrow | Volume up |
| Down Arrow | Volume down |
