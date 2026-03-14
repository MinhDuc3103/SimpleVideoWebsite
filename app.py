from flask import Flask, render_template, abort, request, send_file
import os
import re

app = Flask(__name__)

MOVIES_CONFIG = {
    "doraemon_longtieng": {
        "title": "Doraemon Lồng Tiếng",
        "desc": "The adventures of a robotic cat from the 22nd century.",
        "poster": "/static/posters/bg.jpg",
        "base_path": "/home/koro/video_website/static/videos/doraemon_longtieng"
    },
    "doraemon_vietsub": {
        "title": "Doraemon Vietsub",
        "desc": "The adventures of a robotic cat from the 22nd century.",
        "poster": "/static/posters/bg.jpg",
        "base_path": "/home/koro/video_website/static/videos/doraemon_vietsub"
    },
    "phineas-and-ferb": {
        "title": "Phineas and Ferb",
        "desc": "Two stepbrothers find inventive ways to spend summer vacation.",
        "poster": "/static/posters/P&F.jpg",
        "base_path": "/home/koro/video_website/static/videos/phineseandferb"
    },
    "barbie": {
        "title": "Barbie",
        "desc": "Step into the colorful world of Barbie.",
        "poster": "/static/posters/barbie.jpg",
        "base_path": "/home/koro/video_website/static/videos/barbie"
    }
}

VIDEO_EXTS = ('.mp4', '.mkv', '.webm', '.avi', '.mov')

def extract_episode_number(filename):
    match = re.search(r'Movie(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else 9999

def scan_folder_for_videos(path):
    if not os.path.exists(path):
        return []
    files = [f for f in os.listdir(path) if f.lower().endswith(VIDEO_EXTS)]
    files.sort(key=lambda x: extract_episode_number(x))
    return [{"index": i, "num": extract_episode_number(f), "filename": f} for i, f in enumerate(files)]

@app.route('/')
def index():
    return render_template('index.html', configs=MOVIES_CONFIG)

@app.route('/choice/<slug>')
def choice(slug):
    config = MOVIES_CONFIG.get(slug)
    if not config: abort(404)
    return render_template('choice.html', slug=slug, config=config)

@app.route('/player/<slug>/<content_type>', defaults={'ep_index': 0})
@app.route('/player/<slug>/<content_type>/<int:ep_index>')
def player(slug, content_type, ep_index):
    config = MOVIES_CONFIG.get(slug)
    if not config or content_type not in ['series', 'movies']: abort(404)
    
    full_path = os.path.join(config['base_path'], content_type)
    episodes = scan_folder_for_videos(full_path)
    
    if not episodes:
        return render_template(
            'player.html',
            config=config,
            slug=slug,
            content_type=content_type,
            episodes=[],
            current_ep=None,
            ep_index=0,
            message="Hết dung lượng gòi nên chưa có thêm phim. Yêu bà thúi."
        )
    
    current_ep = episodes[min(ep_index, len(episodes) - 1)]
    return render_template('player.html', config=config, slug=slug, 
                           content_type=content_type, episodes=episodes, 
                           current_ep=current_ep, ep_index=ep_index)

# --- FIXED STREAMING ROUTE ---
@app.route('/video_stream/<slug>/<content_type>/<filename>')
def video_stream(slug, content_type, filename):
    config = MOVIES_CONFIG.get(slug)
    if not config: abort(404)

    file_path = os.path.join(config['base_path'], content_type, filename)

    if not os.path.exists(file_path):
        abort(404)

    # conditional=True is the key. It automatically handles 
    # 'Range' requests for both PC and Mobile.
    return send_file(file_path, mimetype='video/mp4', conditional=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)