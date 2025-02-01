from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mock Data
farmers = []
buyers = []
users = [{"username": "admin", "password": "admin", "role": "admin"}]  # Admin for login

vegetables = [
    "Tomatoes", "Potatoes", "Carrots", "Lettuce", "Spinach", "Broccoli", "Cabbage", "Cucumber", 
    "Onions", "Garlic", "Beans", "Peas", "Zucchini", "Bell Pepper", "Cauliflower", "Pumpkin", 
    "Radish", "Sweet Corn", "Eggplant", "Chili"
]

# Login Route
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check for valid login
        user = next((user for user in users if user["username"] == username and user["password"] == password), None)
        if user:
            session['user'] = user["username"]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials!")
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template("index.html", vegetables=farmers)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        users.append({"username": username, "password": password, "role": role})
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/farmer_dashboard', methods=["GET", "POST"])
def farmer_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        crop = request.form.get("crop")
        price = request.form.get("price")
        contact = request.form.get("contact")
        feedback = request.form.get("feedback")
        video_link = request.form.get("video_link")
        image_url = "static/Farmer.jpg"  # Add farmer's image URL

        farmers.append({
            "crop": crop, "price": price, "contact": contact, "feedback": feedback,
            "video_link": video_link, "image_url": image_url
        })
        return redirect(url_for('farmer_dashboard'))

    return render_template("farmer_dashboard.html", farmers=farmers)

@app.route('/buyer_dashboard')
def buyer_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("buyer_dashboard.html", farmers=farmers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

