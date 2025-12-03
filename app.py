from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

# --- Data Management ---
def load_data():
    default_data = {
        "transactions": [],
        "settings": {"hourly_wage": 0.0},
        "savings_goals": [],
        "salary_preset": {} 
    }
    if not os.path.exists(DATA_FILE): return default_data
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in default_data:
                if key not in data: data[key] = default_data[key]
            return data
    except: return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Routes ---
@app.route("/")
def index():
    data = load_data()
    transactions = data["transactions"]
    settings = data.get("settings", {"hourly_wage": 0.0})
    savings = data.get("savings_goals", [])
    salary_preset = data.get("salary_preset", {})
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    
    category_summary = {}
    for t in transactions:
        cat = t["category"]
        if cat not in category_summary:
            category_summary[cat] = {"amount": 0, "type": t["type"]}
        category_summary[cat]["amount"] += t["amount"]

    return render_template("index.html", 
                           transactions=reversed(transactions), 
                           income=total_income, expense=total_expense, balance=balance,
                           settings=settings, savings=savings, salary_preset=salary_preset,
                           category_summary=category_summary)

@app.route("/add", methods=["POST"])
def add_transaction():
    data = load_data()
    try: amount = float(request.form.get("amount"))
    except: amount = 0.0
    
    new_data = {
        "id": str(uuid.uuid4()),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": request.form.get("type"),
        "category": request.form.get("category"),
        "amount": amount,
        "note": request.form.get("note")
    }
    data["transactions"].append(new_data)
    save_data(data)
    return redirect(url_for("index"))

@app.route("/edit_transaction", methods=["POST"])
def edit_transaction():
    t_id = request.form.get("id")
    data = load_data()
    
    for t in data["transactions"]:
        if t["id"] == t_id:
            try: t["amount"] = float(request.form.get("amount"))
            except: pass
            t["type"] = request.form.get("type")
            t["category"] = request.form.get("category")
            t["note"] = request.form.get("note")
            break
            
    save_data(data)
    return redirect(url_for("index"))

@app.route("/reset_month", methods=["POST"])
def reset_month():
    data = load_data()
    data["transactions"] = []
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete/<string:t_id>")
def delete_transaction(t_id):
    data = load_data()
    data["transactions"] = [t for t in data["transactions"] if t.get("id") != t_id]
    save_data(data)
    return redirect(url_for("index"))

@app.route("/save_salary_preset", methods=["POST"])
def save_salary_preset():
    preset = request.json
    data = load_data()
    data["salary_preset"] = preset
    save_data(data)
    return jsonify({"status": "success"})

@app.route("/add_saving_goal", methods=["POST"])
def add_saving_goal():
    data = load_data()
    new_goal = {
        "id": str(uuid.uuid4()),
        "name": request.form.get("name"),
        "target": float(request.form.get("target")),
        "current": 0.0
    }
    data["savings_goals"].append(new_goal)
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete_saving/<string:goal_id>")
def delete_saving(goal_id):
    data = load_data()
    data["savings_goals"] = [g for g in data["savings_goals"] if g.get("id") != goal_id]
    save_data(data)
    return redirect(url_for("index"))

@app.route("/update_saving", methods=["POST"])
def update_saving():
    goal_id = request.form.get("goal_id")
    action = request.form.get("action") 
    try: amount = float(request.form.get("amount"))
    except: amount = 0.0
    if amount <= 0: return redirect(url_for("index"))

    data = load_data()
    for goal in data["savings_goals"]:
        if goal["id"] == goal_id:
            if action == "deposit":
                goal["current"] += amount
                data["transactions"].append({
                    "id": str(uuid.uuid4()),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": "expense",
                    "category": "เงินออม",
                    "amount": amount,
                    "note": f"ออมเงินเพื่อ: {goal['name']}"
                })
            elif action == "withdraw":
                real_withdraw = min(amount, goal["current"])
                if real_withdraw > 0:
                    goal["current"] -= real_withdraw
                    data["transactions"].append({
                        "id": str(uuid.uuid4()),
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "income",
                        "category": "เงินออม",
                        "amount": real_withdraw,
                        "note": f"แคะกระปุก: {goal['name']}"
                    })
            break
    save_data(data)
    return redirect(url_for("index"))

@app.route("/update_settings", methods=["POST"])
def update_settings():
    try: wage = float(request.form.get("hourly_wage", 0.0))
    except: wage = 0.0
    data = load_data()
    data["settings"]["hourly_wage"] = wage
    save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
