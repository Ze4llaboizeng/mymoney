from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

# --- ส่วนจัดการข้อมูล ---
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

# --- ส่วนหน้าจอและการทำงาน ---
@app.route("/")
def index():
    data = load_data()
    transactions = data["transactions"]
    
    # คำนวณยอดรวม
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    
    # เตรียมข้อมูลสำหรับกราฟ (Group รายจ่ายตามหมวดหมู่)
    expense_by_cat = {}
    for t in transactions:
        if t["type"] == "expense":
            cat = t.get("category", "อื่นๆ")
            expense_by_cat[cat] = expense_by_cat.get(cat, 0) + t["amount"]
    
    # ส่งข้อมูลกราฟเป็น List เพื่อให้ JavaScript ใช้ง่ายๆ
    chart_labels = list(expense_by_cat.keys())
    chart_data = list(expense_by_cat.values())

    return render_template("index.html", 
                           transactions=reversed(transactions), 
                           income=total_income, 
                           expense=total_expense, 
                           balance=balance,
                           chart_labels=json.dumps(chart_labels, ensure_ascii=False),
                           chart_data=json.dumps(chart_data))

@app.route("/add", methods=["POST"])
def add_transaction():
    t_type = request.form.get("type")
    category = request.form.get("category")
    amount = float(request.form.get("amount"))
    note = request.form.get("note")
    
    data = load_data()
    new_data = {
        "id": str(uuid.uuid4()), # สร้าง ID ไม่ซ้ำ
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": t_type,
        "category": category,
        "amount": amount,
        "note": note
    }
    data["transactions"].append(new_data)
    save_data(data)
    
    return redirect(url_for("index"))

@app.route("/delete/<string:t_id>")
def delete_transaction(t_id):
    data = load_data()
    # กรองเอาเฉพาะรายการที่ ID ไม่ตรงกับที่ส่งมา (คือการลบนั่นเอง)
    data["transactions"] = [t for t in data["transactions"] if t.get("id") != t_id]
    save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
