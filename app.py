from flask import Flask, render_template, request, redirect, url_for, session
from firebase_admin import credentials, initialize_app, firestore
from firebase_config import load_firebase_config

# Initialize Firebase
firebase_config = load_firebase_config()
cred = credentials.Certificate("config/service_account.json")
initialize_app(cred, {"projectId": firebase_config["project_id"]})
db = firestore.client()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route("/")
def index():
    if 'username' in session:
        # If user is logged in, show app content
        return render_template("index.html", username=session['username'])
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Add user data to Firebase
        db.collection("users").document(username).set({"password": password})

        # Set session to log in the user immediately
        session['username'] = username
        
        return redirect(url_for('workout'))  # Redirect to the workout data entry page after signup

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username and password:
            session["username"] = username
            return redirect(url_for("workout"))
        else:
            print("Invalid username or password")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/workout", methods=["GET", "POST"])
def workout():
    if 'username' not in session:
        return redirect("/login")  # Redirect to login page if user is not logged in
    
    if request.method == "POST":
        workout_type = request.form["workout_type"]
        duration = request.form["duration"]
        calories_burned = request.form["calories_burned"]

        db.collection("users").document(session['username']).collection("workouts").add({
            "workout_type": workout_type,
            "duration": duration,
            "calories_burned": calories_burned,
        })

        return redirect(url_for("workout"))  # Stay on the workout page after submitting data

    return render_template("workout_form.html")  # Render the workout form page

@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect("/login")  # Redirect to login page after logout

if __name__ == "__main__":
    app.run(debug=True)
