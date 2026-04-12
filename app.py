from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "12345"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        username TEXT UNIQUE,
        phone TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pg(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        rent INTEGER,
        image TEXT,
        owner_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wishlist(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        pg_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS booking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        phone TEXT,
        pg_id INTEGER,
        status TEXT,
        payment TEXT,
        amount INTEGER
    )
    """)

    conn.commit()
    conn.close()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("home.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and user['password'] == password:
            session['user'] = username
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect('/')

        return render_template("login.html", error="Invalid login")

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        data = (
            request.form['name'],
            request.form['email'],
            request.form['username'],
            request.form['phone'],
            request.form['password'],
            request.form['role']
        )

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (data[2],))
        if cur.fetchone():
            return "Username already exists ❌"

        cur.execute("""
        INSERT INTO users(name,email,username,phone,password,role)
        VALUES(?,?,?,?,?,?)
        """, data)

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

# ---------------- VIEW PG ----------------

@app.route('/viewpg')
def viewpg():
    conn = get_db()
    cur = conn.cursor()

    # 🔥 OWNER → only own PG
    if session.get('role') == 'owner':
        cur.execute("SELECT * FROM pg WHERE owner_id=?", (session['user_id'],))

    # 🔥 USER → EMPTY (no PG)
    else:
        cur.execute("SELECT * FROM pg WHERE 1=0")

    pgs = cur.fetchall()

    conn.close()

    return render_template("viewpg.html", pgs=pgs)

# ---------------- ADD PG ----------------
@app.route('/addpg', methods=['GET','POST'])
def addpg():

    if session.get('role') != "owner":
        return "Access Denied ❌"

    if request.method == "POST":
        name = request.form['name']
        location = request.form['location']
        rent = request.form['rent']
        image = request.files.get('image')

        # ✅ SAFE IMAGE HANDLE
        filename = "default.jpg"
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db()
        conn.execute(
            "INSERT INTO pg (name, location, rent, image, owner_id) VALUES (?,?,?,?,?)",
            (name, location, rent, filename, session['user_id'])
        )
        conn.commit()
        conn.close()

        flash("PG Added Successfully ✅")
        return redirect('/viewpg')

    return render_template("addpg.html")

# ---------------- DELETE PG ----------------
@app.route('/delete/<int:id>')
def delete_pg(id):

    if session.get('role') != 'owner':
        return "Unauthorized ❌"

    conn = get_db()
    conn.execute("DELETE FROM pg WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("PG Deleted Successfully 🗑️")
    return redirect('/viewpg')

# ---------------- EDIT PG ----------------
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    if session.get('role') != 'owner':
        return "Unauthorized ❌"

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("""
        UPDATE pg SET name=?, location=?, rent=? WHERE id=?
        """, (
            request.form['name'],
            request.form['location'],
            request.form['rent'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect('/viewpg')

    cur.execute("SELECT * FROM pg WHERE id=?", (id,))
    pg = cur.fetchone()
    conn.close()

    return render_template("editpg.html", pg=pg)

# ---------------- BOOK ----------------
@app.route('/book/<int:id>', methods=['GET','POST'])
def book(id):

    if 'user' not in session:
        return redirect('/login')

    if request.method == "POST":
        phone = request.form['phone']

        # 🔥 store in session
        session['booking_pg'] = id
        session['phone'] = phone

        # 🔥 PG rent fetch
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT rent FROM pg WHERE id=?", (id,))
        pg = cur.fetchone()
        conn.close()

        session['amount'] = pg['rent']   # 💰 amount save

        return redirect('/payment')

    return render_template("booking.html")

# ---------------- BOOKINGS ----------------
@app.route('/bookings')
def bookings():

    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT booking.*, pg.name, pg.location, pg.rent
    FROM booking
    JOIN pg ON booking.pg_id = pg.id
    WHERE booking.user_name=?
    """, (session['user'],))

    data = cur.fetchall()
    conn.close()

    return render_template("bookings.html", bookings=data)

@app.route('/payment', methods=['GET','POST'])
def payment():

    if 'booking_pg' not in session:
        return redirect('/viewpg')

    if request.method == "POST":

        conn = get_db()

        conn.execute("""
        INSERT INTO booking(user_name,phone,pg_id,status,payment,amount)
        VALUES(?,?,?,?,?,?)
        """, (
            session['user'],
            session['phone'],
            session['booking_pg'],
            "Booked",
            "Paid",
            session.get('amount',0)
        ))

        conn.commit()
        conn.close()

        # 🔥 clear session (important)
        session.pop('booking_pg', None)
        session.pop('phone', None)
        session.pop('amount', None)

        return render_template("success.html")   # animation page

    return render_template("payment.html", amount=session.get('amount'))

# ---------------- WISHLIST ----------------
@app.route('/wishlist/<int:pg_id>')
def wishlist(pg_id):

    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    # check already exists
    cur.execute("""
        SELECT * FROM wishlist 
        WHERE username=? AND pg_id=?
    """, (session['user'], pg_id))

    exists = cur.fetchone()

    if exists:
        cur.execute("""
            DELETE FROM wishlist 
            WHERE username=? AND pg_id=?
        """, (session['user'], pg_id))
    else:
        cur.execute("""
            INSERT INTO wishlist(username, pg_id)
            VALUES(?, ?)
        """, (session['user'], pg_id))

    conn.commit()
    conn.close()

    return redirect('/viewpg')

@app.route('/wishlist')
def wishlist_page():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT pg.* FROM pg
    INNER JOIN wishlist ON pg.id = wishlist.pg_id
    WHERE wishlist.username=?
    """, (session['user'],))

    pgs = cur.fetchall()
    conn.close()

    return render_template("wishlist.html", pgs=pgs)


@app.route('/search')
def search_page():
    return render_template("search.html")

@app.route('/recommend')
def recommend():
    return render_template("recommend_empty.html")

@app.route('/budget')
def budget():

    if 'user' not in session:
        return redirect('/login')

    max_budget = request.args.get('budget')

    conn = get_db()
    cur = conn.cursor()

    pgs = []

    # 🔥 only show when budget entered
    if max_budget:
        cur.execute("SELECT * FROM pg WHERE rent <= ?", (max_budget,))
        pgs = cur.fetchall()

    conn.close()

    return render_template("budget.html", pgs=pgs, max_budget=max_budget)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(booking)")
columns = cur.fetchall()

print("BOOKING TABLE COLUMNS 👇")
for col in columns:
    print(col)

conn.close()
app.run(host="0.0.0.0",port=10000)
