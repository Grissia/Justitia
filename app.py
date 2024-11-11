from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 模擬一個簡單的記分板 (可以用資料庫替代)
scoreboard = []

LOG_FILE = "scoreboard.log"

def log_action(action, name=None, score=None):
    """將操作記錄儲存到日誌檔案中"""
    with open(LOG_FILE, "a") as f:
        if action == 'add':
            f.write(f"{datetime.now()}: Added {name} with score {score}\n")
        elif action == 'update':
            f.write(f"{datetime.now()}: Updated {name} with additional score {score}\n")
        elif action == 'delete':
            f.write(f"{datetime.now()}: Deleted {name} from scoreboard\n")

def add_or_update_score(name, score):
    # 檢查是否已經存在該名稱
    for player in scoreboard:
        if player["name"].lower() == name.lower():  # 不分大小寫比對名稱
            player["score"] += score
            log_action('update', name, score)
            break
    else:
        # 如果名稱不存在，新增新的玩家
        scoreboard.append({"name": name, "score": score})
        log_action('add', name, score)

    # 每次更新後依分數從高到低排序
    scoreboard.sort(key=lambda x: x["score"], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', scoreboard=scoreboard)

@app.route('/add', methods=['POST'])
def add_score():
    name = request.form['name']
    score = request.form['score']
    if name and score.isdigit():
        add_or_update_score(name, int(score))
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_score(index):
    if 0 <= index < len(scoreboard):
        player = scoreboard.pop(index)
        log_action('delete', player['name'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)