from flask import Flask, render_template, request, jsonify
import random
import os
print(os.getcwd())
app = Flask(__name__)

def load_lottery_numbers():
    file_path = "data/lottery.txt"  # 假設文件位於 data 資料夾中
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

@app.route("/", methods=["GET", "POST"])
def index():
    numbers = load_lottery_numbers()  # 預先載入抽籤號碼
    result = None
    error_message = None

    if request.method == "POST":
        items = request.form.get("items")
        if not items:
            error_message = "請輸入至少一個項目"
        else:
            items = [item.strip() for item in items.split(",")]
            result = random.choice(items) if items else None

    return render_template("index.html", numbers=numbers, result=result, error_message=error_message)

@app.route("/api/numbers", methods=["GET"])
def api_numbers():
    numbers = load_lottery_numbers()
    return jsonify(numbers)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
