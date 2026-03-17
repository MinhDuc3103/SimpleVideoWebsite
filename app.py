from flask import Flask, render_template, abort, send_file
import os
import re

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def vpath(*parts):
    return os.path.join(BASE_DIR, 'static', 'videos', *parts)

MOVIES_CONFIG = {
    "doraemon_longtieng": {
        "title": "Doraemon Lồng Tiếng",
        "desc": "The adventures of a robotic cat from the 22nd century.",
        "poster": "/static/posters/bg.jpg",
        "base_path": vpath("doraemon_longtieng")
    },
    "doraemon_vietsub": {
        "title": "Doraemon Vietsub",
        "desc": "The adventures of a robotic cat from the 22nd century.",
        "poster": "/static/posters/bg.jpg",
        "base_path": vpath("doraemon_vietsub")
    },
    "phineas-and-ferb": {
        "title": "Phineas and Ferb",
        "desc": "Two stepbrothers find inventive ways to spend summer vacation.",
        "poster": "/static/posters/P&F.jpg",
        "base_path": vpath("phineseandferb")
    },
    "barbie": {
        "title": "Barbie",
        "desc": "Step into the colorful world of Barbie.",
        "poster": "/static/posters/barbie.jpg",
        "base_path": vpath("barbie")
    }
}

VIDEO_EXTS = ('.mp4', '.mkv', '.webm', '.avi', '.mov')

def extract_episode_number(filename):
    match = re.search(r'Movie(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else None

def scan_folder_for_videos(path):
    if not os.path.exists(path):
        return []
    files = [f for f in os.listdir(path) if f.lower().endswith(VIDEO_EXTS)]
    files.sort(key=lambda x: extract_episode_number(x) or 9999)
    result = []
    for i, f in enumerate(files):
        num = extract_episode_number(f)
        ep_num = str(num) if num is not None else str(i + 1)
        display_name = re.sub(r'[._]+', ' ', os.path.splitext(f)[0]).strip()
        result.append({"index": i, "num": ep_num, "name": display_name, "filename": f})
    return result

@app.route('/')
def index():
    return render_template('index.html', configs=MOVIES_CONFIG)

@app.route('/choice/<slug>')
def choice(slug):
    config = MOVIES_CONFIG.get(slug)
    if not config: abort(404)
    return render_template('choice.html', slug=slug, config=config)

@app.route('/episodes/<slug>/<content_type>')
def episodes_page(slug, content_type):
    config = MOVIES_CONFIG.get(slug)
    if not config or content_type not in ['series', 'movies']: abort(404)
    full_path = os.path.join(config['base_path'], content_type)
    eps = scan_folder_for_videos(full_path)
    message = "Hết dung lượng gòi nên chưa có thêm phim. Yêu bà thúi." if not eps else None
    return render_template('episodes.html', config=config, slug=slug,
                           content_type=content_type, episodes=eps, message=message)

@app.route('/player/<slug>/<content_type>', defaults={'ep_index': 0})
@app.route('/player/<slug>/<content_type>/<int:ep_index>')
def player(slug, content_type, ep_index):
    config = MOVIES_CONFIG.get(slug)
    if not config or content_type not in ['series', 'movies']: abort(404)
    full_path = os.path.join(config['base_path'], content_type)
    episodes = scan_folder_for_videos(full_path)
    if not episodes: abort(404)
    current_ep = episodes[min(ep_index, len(episodes) - 1)]
    return render_template('player.html', config=config, slug=slug,
                           content_type=content_type, episodes=episodes,
                           current_ep=current_ep, ep_index=ep_index)

@app.route('/video_stream/<slug>/<content_type>/<filename>')
def video_stream(slug, content_type, filename):
    config = MOVIES_CONFIG.get(slug)
    if not config: abort(404)
    file_path = os.path.join(config['base_path'], content_type, filename)
    if not os.path.exists(file_path): abort(404)
    return send_file(file_path, mimetype='video/mp4', conditional=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
