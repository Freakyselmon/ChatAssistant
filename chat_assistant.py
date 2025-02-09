from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Function to execute queries
def query_database(query, params=()):
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Natural Language Query Processing
def process_query(user_query):
    user_query = user_query.lower()

    # Query 1: Show all employees in a department
    match = re.search(r"show me all employees in the (.+) department", user_query)
    if match:
        department = match.group(1).capitalize()
        result = query_database("SELECT Name FROM Employees WHERE Department = ?", (department,))
        return [row[0] for row in result] if result else ["No employees found in this department."]

    # Query 2: Find the manager of a department
    match = re.search(r"who is the manager of the (.+) department", user_query)
    if match:
        department = match.group(1).capitalize()
        result = query_database("SELECT Manager FROM Departments WHERE Name = ?", (department,))
        return result[0][0] if result else "No manager found for this department."

    # Query 3: List employees hired after a specific date
    match = re.search(r"list all employees hired after (\d{4}-\d{2}-\d{2})", user_query)
    if match:
        date = match.group(1)
        result = query_database("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
        return [row[0] for row in result] if result else ["No employees hired after this date."]

    # Query 4: Get total salary expense for a department
    match = re.search(r"what is the total salary expense for the (.+) department", user_query)
    if match:
        department = match.group(1).capitalize()
        result = query_database("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
        return f"Total salary expense: {result[0][0]}" if result[0][0] else "No data available."

    return "Sorry, I didn't understand that query."

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "No query provided"}), 400
    
    response = process_query(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
