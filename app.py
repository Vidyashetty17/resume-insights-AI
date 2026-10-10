from flask import *
from models import db,User
import os
from config import Config
from services.ai_service import analyze_resume
from services.pdf_service import extract_text
from services.file_service import save_file
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)
db.init_app(app)

@app.route("/",methods = ["GET"])
def home():
    return render_template("index.html")

@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        if "@" not in request.form.get("email") and len(request.form.get("email")):
            flash("invalid email")
            return render_template("register.html")
        if request.form.get("password") != request.form.get("confirm_password"):
            flash("password didnt match with the confirm password try again")
            return render_template("register.html")
        
        user = User.query.filter_by(email = request.form.get("email")).first()
        if user:
           return jsonify({"message":"Email already exits...!!"})
        password = generate_password_hash(request.form.get("password"))
        user = User(
            name = request.form.get("name"),
            email = request.form.get("email"),
            password_hash = password
        )
        db.session.add(user)
        db.session.commit()
        flash("register succesfully......")
        return render_template("index.html")
    
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user and check_password_hash(user.password_hash, request.form.get("password")):
            flash("login successfulll....")
            session["user"] = user.name
            return redirect(url_for("dashboard"))
        flash("invalid credentials")
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    if "user" in session:
        return render_template("dashboard.html")
    flash ("Access denied.....")
    return redirect(url_for("home"))

@app.route("/analyse",methods=["POST"])
def analyse():
    resume = request.files["resume"]
    filepath = save_file(resume)

    text = extract_text(filepath)

    result = analyze_resume(text)

    return render_template("result.html",result = result)


