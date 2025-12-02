from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

# --- ส่วนจัดการข้อมูล (เหมือนเดิม) ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"transactions": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"transactions": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- ส่วนหน้าจอและการทำงาน (Web Server) ---
@app.route("/")
def index():
    data = load_data()
    transactions = data["transactions"]
    
    # คำนวณยอดรวม
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    
    # ส่งข้อมูลไปแสดงที่หน้าจอ HTML
    return render_template("index.html", 
                           transactions=reversed(transactions), # โชว์รายการใหม่สุดก่อน
                           income=total_income, 
                           expense=total_expense, 
                           balance=balance)

@app.route("/add", methods=["POST"])
def add_transaction():
    t_type = request.form.get("type")
    amount = float(request.form.get("amount"))
    note = request.form.get("note")
    
    data = load_data()
    new_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": t_type,
        "amount": amount,
        "note": note
    }
    data["transactions"].append(new_data)
    save_data(data)
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    # host='0.0.0.0' เพื่อให้เข้าถึงได้ง่ายในมือถือ
    app.run(host='0.0.0.0', port=5000, debug=True)
