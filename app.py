from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, User, Design
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from ai_engine import generate_design

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route("/")
def home():
    return render_template("home.html")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):

            session["user_id"] = user.user_id
            session["username"] = user.username

            flash("Login successful!", "success")
            return redirect(url_for("create_design"))

        flash("Invalid email or password", "error")

    return render_template("login.html")



@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully", "info")

    return redirect(url_for("home"))



@app.route("/create-design")
def create_design():

    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))

    return render_template("create_design.html")



@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        flash("Login required", "error")
        return redirect(url_for("login"))

    if "image" not in request.files:
        flash("No file uploaded", "error")
        return redirect(url_for("create_design"))

    file = request.files["image"]

    if file.filename == "":
        flash("No selected file", "error")
        return redirect(url_for("create_design"))

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        unique_name = str(uuid.uuid4()) + "_" + filename

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)

        file.save(filepath)

        ai_result = generate_design(filepath, "modern")

        new_design = Design(
            user_id=session["user_id"],
            image_path=unique_name,
            style_theme="modern",
            ai_output=str(ai_result)
        )

        db.session.add(new_design)
        db.session.commit()

        flash("Image uploaded successfully!", "success")

        return redirect(url_for("gallery"))

    flash("Invalid file type", "error")
    return redirect(url_for("create_design"))


@app.route("/gallery")
def gallery():

    designs = Design.query.order_by(Design.created_at.desc()).all()

    return render_template("gallery.html", designs=designs)



if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)