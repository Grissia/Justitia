from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

participants = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global participants
    if request.method == 'POST':
        numbers = request.form.get('numbers')
        try:
            participants = list(map(int, numbers.split(',')))
            if len(participants) < 2:
                return "<h3>參與者人數不足，至少需要 2 人參加！</h3>"
            return redirect(url_for('result'))  # 轉向 /result
        except ValueError:
            return "<h3>輸入格式有誤！請輸入以逗號分隔的座號，例如：1,2,3,4</h3>"
    return render_template('index.html', numbers=load_prefix_numbers())

@app.route('/result', methods=['GET'])
def result():
    global participants
    if len(participants) < 2:
        return "<h3>參與者人數不足，至少需要 2 人參加！</h3>"
    
    gift_exchange_result = assign_gifts(participants)  # 在這裡進行隨機化
    first_participant = gift_exchange_result[participants[0]]
    return render_template('result.html', result=gift_exchange_result, first_participant=first_participant)

def load_prefix_numbers():
    file_path = "static/numbers.txt"  # 假設文件位於 data 資料夾中
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            numbers = [line.strip() for line in file if line.strip()]  # 去除空行
        return numbers
    except FileNotFoundError:
        print(f"Error: 文件未找到 - {file_path}")
        return []
    except Exception as e:
        print(f"Error: 讀取文件時出錯 - {e}")
        return []

def assign_gifts(participants):
    receivers = participants.copy()
    random.shuffle(receivers)
    print(participants)
    print(receivers)
    # 確保每個人都不和自己交換禮物
    while any(sender == receiver for sender, receiver in zip(participants, receivers)):
        random.shuffle(receivers)
        
    return {sender: receiver for sender, receiver in zip(participants, receivers)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
