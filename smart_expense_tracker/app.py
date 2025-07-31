from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
DATA_FILE = "expenses.json"

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Medical", "Entertainment", "Other"]

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def analyze_expenses(expenses):
    analysis = {
        "total": sum(e["amount"] for e in expenses),
        "by_category": {cat: 0 for cat in CATEGORIES},
        "by_day": defaultdict(float),
        "by_week": defaultdict(float),
        "by_month": defaultdict(float),
        "by_year": defaultdict(float),
        "suggestions": []
    }

    for e in expenses:
        category = e["category"].title()
        if category not in CATEGORIES:
            category = "Other"

        analysis["by_category"][category] += e["amount"]

        date_obj = datetime.strptime(e["date"], "%Y-%m-%d %H:%M")
        analysis["by_day"][date_obj.strftime("%Y-%m-%d")] += e["amount"]
        analysis["by_week"][f"Week-{date_obj.isocalendar().week}"] += e["amount"]
        analysis["by_month"][date_obj.strftime("%Y-%m")] += e["amount"]
        analysis["by_year"][date_obj.strftime("%Y")] += e["amount"]

    for cat, amt in analysis["by_category"].items():
        if amt > 2000:
            analysis["suggestions"].append(f"⚠ High spending on {cat}! Consider setting a budget limit.")
        elif amt > 0:
            analysis["suggestions"].append(f"ℹ You spent ₹{amt} on {cat}. Keep tracking to avoid overspending.")
        else:
            analysis["suggestions"].append(f"✅ No expense on {cat}. Great job controlling unnecessary spending!")

    if analysis["total"] > 10000:
        analysis["suggestions"].append("⚠ Your total expenses are high. Consider tracking non-essential expenses.")
    elif 0 < analysis["total"] < 5000:
        analysis["suggestions"].append("✅ Good control over expenses this month! Keep it up.")
    elif analysis["total"] == 0:
        analysis["suggestions"].append("No expenses recorded yet. Start logging to track your finances better.")

    return analysis

def filter_expenses(expenses, filter_type, start_date=None, end_date=None):
    if filter_type == "7days":
        cutoff = datetime.now() - timedelta(days=7)
        return [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d %H:%M") >= cutoff]
    elif filter_type == "30days":
        cutoff = datetime.now() - timedelta(days=30)
        return [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d %H:%M") >= cutoff]
    elif filter_type == "year":
        this_year = datetime.now().year
        return [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d %H:%M").year == this_year]
    elif filter_type == "custom" and start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return [e for e in expenses if start <= datetime.strptime(e["date"], "%Y-%m-%d %H:%M") <= end]
    return expenses

@app.route("/", methods=["GET", "POST"])
def index():
    expenses = load_expenses()

    if request.method == "POST":
        if "amount" in request.form:  
            amount = float(request.form["amount"])
            category = request.form["category"]
            note = request.form["note"]
            date_input = request.form.get("date")

            if date_input:
                date_str = datetime.strptime(date_input, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M")
            else:
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

            expense = {
                "amount": amount,
                "category": category,
                "note": note,
                "date": date_str
            }

            expenses.append(expense)
            save_expenses(expenses)

    filter_type = request.args.get("filter", "all")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    filtered_expenses = filter_expenses(expenses, filter_type, start_date, end_date)
    analysis = analyze_expenses(filtered_expenses)

    return render_template("index.html", expenses=filtered_expenses, analysis=analysis, categories=CATEGORIES, filter_type=filter_type)

@app.route("/delete/<int:index>", methods=["POST"])
def delete_expense(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
