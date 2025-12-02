from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

# --- ส่วนจัดการข้อมูล ---
def load_data():
    default_data = {
        "transactions": [],
        "settings": {"hourly_wage": 0} # ค่าเริ่มต้น
    }
    
    if not os.path.exists(DATA_FILE):
        return default_data
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # ป้องกัน error กรณีไฟล์เก่าไม่มี settings
            if "settings" not in data:
                data["settings"] = {"hourly_wage": 0}
            return data
    except:
        return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Routes ---
@app.route("/")
def index():
    data = load_data()
    transactions = data["transactions"]
    settings = data.get("settings", {"hourly_wage": 0})
    
    # คำนวณยอดรวม
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    
    # กราฟ
    expense_by_cat = {}
    for t in transactions:
        if t["type"] == "expense":
            cat = t.get("category", "อื่นๆ")
            expense_by_cat[cat] = expense_by_cat.get(cat, 0) + t["amount"]
    
    chart_labels = list(expense_by_cat.keys())
    chart_data = list(expense_by_cat.values())

    return render_template("index.html", 
                           transactions=reversed(transactions), 
                           income=total_income, 
                           expense=total_expense, 
                           balance=balance,
                           settings=settings,
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
        "id": str(uuid.uuid4()),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": t_type,
        "category": category,
        "amount": amount,
        "note": note
    }
    data["transactions"].append(new_data)
    save_data(data)
    return redirect(url_for("index"))

@app.route("/update_settings", methods=["POST"])
def update_settings():
    wage = float(request.form.get("hourly_wage", 0))
    data = load_data()
    data["settings"]["hourly_wage"] = wage
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete/<string:t_id>")
def delete_transaction(t_id):
    data = load_data()
    data["transactions"] = [t for t in data["transactions"] if t.get("id") != t_id]
    save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
