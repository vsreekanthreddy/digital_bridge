from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Mock user data (for simplicity, you can replace it with a real database in production)
users = []
logged_in_user = None

# Mock data for farmers and buyers
farmers = [
    {"name": "John Doe", "crop": "Tomatoes", "price": "$50 per kg", "contact": "123-456-7890", "image": "farmer_placeholder.jpg"},
    {"name": "Jane Smith", "crop": "Potatoes", "price": "$30 per kg", "contact": "987-654-3210", "image": "farmer_placeholder.jpg"}
]
buyers = []

@app.route('/')
def index():
    return render_template("index.html", farmers=farmers, buyers=buyers)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        users.append({"username": username, "password": password, "role": role})
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    global logged_in_user
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Simple login logic (replace with proper validation)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username
            session['role'] = user['role']
            logged_in_user = user
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, try again."
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/farmer_dashboard', methods=["GET", "POST"])
def farmer_dashboard():
    if 'role' not in session or session['role'] != 'Farmer':
        return redirect(url_for('login'))
    if request.method == "POST":
        name = request.form.get("name")
        crop = request.form.get("crop")
        price = request.form.get("price")
        contact = request.form.get("contact")
        farmers.append({"name": name, "crop": crop, "price": price, "contact": contact, "image": "farmer_placeholder.jpg"})
        return redirect(url_for('farmer_dashboard'))
    return render_template("farmer_dashboard.html", farmers=farmers)

@app.route('/buyer_dashboard', methods=["GET", "POST"])
def buyer_dashboard():
    if 'role' not in session or session['role'] != 'Buyer':
        return redirect(url_for('login'))
    return render_template("buyer_dashboard.html", farmers=farmers, buyers=buyers)

if __name__ == '__main__':
    app.run(debug=True)
