"""Intentionally vulnerable demo app for the SQL Injection Test Cases resource.

DO NOT deploy this anywhere. The /vulnerable/* endpoints build SQL by string
concatenation on purpose, so the pytest suite can demonstrate what real SQLi
looks like against a live target. The /secure/* endpoints implement the same
features with parameterized queries.

The tests use Flask's test_client, so no running server or network is needed.
"""

import sqlite3

from flask import Flask, jsonify, request

SEED = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    email TEXT
);
INSERT INTO users (id, username, password, email) VALUES
    (1, 'admin', 's3cr3t-admin-hash', 'admin@lab.local'),
    (2, 'qa.tester', 'hunter2', 'qa@lab.local');

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
);
INSERT INTO products (id, name, category, price) VALUES
    (1, 'Keyboard', 'Electronics', 49.99),
    (2, 'Mouse', 'Electronics', 19.99),
    (3, 'Mug', 'Home', 9.99);
"""

app = Flask(__name__)
db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(SEED)


# --- Intentionally vulnerable endpoints (string concatenation) ---------------


@app.post("/vulnerable/login")
def vulnerable_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    query = (
        "SELECT id, username FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )
    row = db.execute(query).fetchone()
    if row:
        return jsonify({"status": "ok", "user": row[1]}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.get("/vulnerable/products")
def vulnerable_products():
    category = request.args.get("category", "")
    query = (
        "SELECT name, price, category FROM products "
        f"WHERE category = '{category}'"
    )
    rows = db.execute(query).fetchall()
    return jsonify({"products": [list(r) for r in rows]}), 200


@app.get("/vulnerable/product")
def vulnerable_product():
    pid = request.args.get("id", "")
    query = f"SELECT id, name, price FROM products WHERE id = {pid}"
    rows = db.execute(query).fetchall()
    return jsonify({"products": [list(r) for r in rows]}), 200


# --- Secure endpoints (parameterized queries) --------------------------------


@app.post("/secure/login")
def secure_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    row = db.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    if row:
        return jsonify({"status": "ok", "user": row[1]}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.get("/secure/products")
def secure_products():
    category = request.args.get("category", "")
    rows = db.execute(
        "SELECT name, price, category FROM products WHERE category = ?",
        (category,),
    ).fetchall()
    return jsonify({"products": [list(r) for r in rows]}), 200


@app.get("/secure/product")
def secure_product():
    pid = request.args.get("id", "")
    rows = db.execute(
        "SELECT id, name, price FROM products WHERE id = ?",
        (pid,),
    ).fetchall()
    return jsonify({"products": [list(r) for r in rows]}), 200
