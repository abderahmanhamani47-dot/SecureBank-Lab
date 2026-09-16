from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "securebank-secret-key"

DATABASE = "securebank.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_number TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Compte admin de laboratoire
    admin = conn.execute(
        "SELECT id FROM users WHERE username = 'admin'"
    ).fetchone()

    if not admin:
        cursor = conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )
        admin_id = cursor.lastrowid

        conn.execute(
            "INSERT INTO accounts (user_id, account_number, balance) VALUES (?, ?, ?)",
            (admin_id, "SB-ADMIN-001", 15000)
        )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>SecureBank Lab</title>
    </head>
    <body>
        <h1>SecureBank Lab</h1>
        <h2>Web Application Pentest Laboratory</h2>

        <p>Educational vulnerable banking application.</p>

        <a href="/register">Register</a><br>
        <a href="/login">Login</a>
    </body>
    </html>
    """


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        try:
            cursor = conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            user_id = cursor.lastrowid

            conn.execute(
                "INSERT INTO accounts (user_id, account_number, balance) VALUES (?, ?, ?)",
                (user_id, f"SB-{user_id:04d}", 1000)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

        conn.close()

        return redirect("/login")

    return """
    <html>
    <head>
        <title>Register - SecureBank</title>
    </head>
    <body>

        <h1>Create account</h1>

        <form method="POST">

            <label>Username:</label><br>
            <input type="text" name="username">

            <br><br>

            <label>Password:</label><br>
            <input type="password" name="password">

            <br><br>

            <button type="submit">Create account</button>

        </form>

        <br>
        <a href="/">Home</a>

    </body>
    </html>
    """


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect("/dashboard")

        return "Invalid username or password"

    return """
    <html>
    <head>
        <title>Login - SecureBank</title>
    </head>
    <body>

        <h1>SecureBank Login</h1>

        <form method="POST">

            <label>Username:</label><br>
            <input type="text" name="username">

            <br><br>

            <label>Password:</label><br>
            <input type="password" name="password">

            <br><br>

            <button type="submit">Login</button>

        </form>

        <br>
        <a href="/">Home</a>

    </body>
    </html>
    """


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    account = conn.execute(
        "SELECT * FROM accounts WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return f"""
    <html>
    <head>
        <title>Dashboard - SecureBank</title>
    </head>

    <body>

        <h1>SecureBank Dashboard</h1>

        <h2>Welcome {user["username"]}</h2>

        <p><strong>Role:</strong> {user["role"]}</p>

        <hr>

        <h3>Bank Account</h3>

        <p>Account number: {account["account_number"]}</p>

        <p>Balance: €{account["balance"]:.2f}</p>

        <hr>

        <a href="/users">Users</a><br>
        <a href="/account?id={account["id"]}">Account details</a><br>
        <a href="/logout">Logout</a>

    </body>
    </html>
    """


@app.route("/users")
def users():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    users = conn.execute(
        "SELECT id, username, role FROM users"
    ).fetchall()

    conn.close()

    rows = ""

    for user in users:
        rows += f"""
        <tr>
            <td>{user["id"]}</td>
            <td>{user["username"]}</td>
            <td>{user["role"]}</td>
            <td>
                <a href="/user?id={user["id"]}">View</a>
            </td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Users - SecureBank</title>
    </head>

    <body>

        <h1>User Management</h1>

        <table border="1" cellpadding="10">

            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Role</th>
                <th>Action</th>
            </tr>

            {rows}

        </table>

        <br>
        <a href="/dashboard">Dashboard</a>

    </body>
    </html>
    """


@app.route("/user")
def user():

    if "user_id" not in session:
        return redirect("/login")

    user_id = request.args.get("id")

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if not user:
        return "User not found"

    return f"""
    <html>
    <head>
        <title>User Profile - SecureBank</title>
    </head>

    <body>

        <h1>User Profile</h1>

        <p><strong>ID:</strong> {user["id"]}</p>

        <p><strong>Username:</strong> {user["username"]}</p>

        <p><strong>Password:</strong> {user["password"]}</p>

        <p><strong>Role:</strong> {user["role"]}</p>

        <br>

        <a href="/users">Back to users</a>

    </body>
    </html>
    """


@app.route("/account")
def account():

    if "user_id" not in session:
        return redirect("/login")

    account_id = request.args.get("id")

    conn = get_db()

    account = conn.execute(
        "SELECT * FROM accounts WHERE id = ?",
        (account_id,)
    ).fetchone()

    conn.close()

    if not account:
        return "Account not found"

    return f"""
    <html>
    <head>
        <title>Account Details - SecureBank</title>
    </head>

    <body>

        <h1>Account Details</h1>

        <p><strong>Account ID:</strong> {account["id"]}</p>

        <p><strong>Account number:</strong> {account["account_number"]}</p>

        <p><strong>Balance:</strong> €{account["balance"]:.2f}</p>

        <br>

        <a href="/dashboard">Dashboard</a>

    </body>
    </html>
    """


@app.route("/api/users")
def api_users():

    conn = get_db()

    users = conn.execute(
        "SELECT id, username, role FROM users"
    ).fetchall()

    conn.close()

    return {
        "users": [
            {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
            for user in users
        ]
    }


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
