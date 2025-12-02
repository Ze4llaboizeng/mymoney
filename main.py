import json
import os
from datetime import datetime

# ชื่อไฟล์สำหรับเก็บข้อมูล
DATA_FILE = "account_data.json"

def load_data():
    """โหลดข้อมูลจากไฟล์ JSON"""
    if not os.path.exists(DATA_FILE):
        return {"transactions": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"transactions": []}

def save_data(data):
    """บันทึกข้อมูลลงไฟล์ JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_transaction(type_name, amount, note):
    """เพิ่มรายการ (รายรับ หรือ รายจ่าย)"""
    data = load_data()
    transaction = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": type_name, # "income" หรือ "expense"
        "amount": float(amount),
        "note": note
    }
    data["transactions"].append(transaction)
    save_data(data)
    print(f"\n✅ บันทึก {type_name} จำนวน {amount} เรียบร้อยแล้ว!")

def show_summary():
    """แสดงสรุปยอดเงิน"""
    data = load_data()
    total_income = sum(t["amount"] for t in data["transactions"] if t["type"] == "income")
    total_expense = sum(t["amount"] for t in data["transactions"] if t["type"] == "expense")
    balance = total_income - total_expense

    print("\n" + "="*30)
    print("      📊 สรุปบัญชีของคุณ")
    print("="*30)
    print(f"💰 รายรับรวม  : {total_income:,.2f} บาท")
    print(f"💸 รายจ่ายรวม : {total_expense:,.2f} บาท")
    print("-" * 30)
    print(f"💵 คงเหลือ    : {balance:,.2f} บาท")
    print("="*30)
    
    # แสดง 5 รายการล่าสุด
    print("\n📜 5 รายการล่าสุด:")
    for t in reversed(data["transactions"][-5:]):
        type_th = "รายรับ" if t["type"] == "income" else "รายจ่าย"
        print(f"[{t['date']}] {type_th}: {t['amount']} ({t['note']})")
    print("\n")

def main():
    while True:
        print("\n=== แอพบัญชีรายรับ-รายจ่าย (Termux Edition) ===")
        print("1. ➕ เพิ่มรายรับ")
        print("2. ➖ เพิ่มรายจ่าย")
        print("3. 📊 ดูสรุปยอดเงิน")
        print("4. ❌ ออกจากโปรแกรม")
        
        choice = input("เลือกเมนู (1-4): ")
        
        if choice == "1":
            try:
                amt = float(input("ระบุจำนวนเงิน: "))
                note = input("บันทึกช่วยจำ: ")
                add_transaction("income", amt, note)
            except ValueError:
                print("⚠️ กรุณาใส่ตัวเลขเท่านั้น")
        
        elif choice == "2":
            try:
                amt = float(input("ระบุจำนวนเงิน: "))
                note = input("บันทึกช่วยจำ: ")
                add_transaction("expense", amt, note)
            except ValueError:
                print("⚠️ กรุณาใส่ตัวเลขเท่านั้น")
                
        elif choice == "3":
            show_summary()
            
        elif choice == "4":
            print("👋 บ๊ายบาย!")
            break
        else:
            print("❌ เลือกไม่ถูกต้อง ลองใหม่นะครับ")

if __name__ == "__main__":
    main()
