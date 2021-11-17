from flask import Flask, render_template, request, redirect, session, flash
from user import User

app = Flask(__name__)
app.secret_key = 'many random bytes'

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_user(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "pw" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")



@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.pw, request.form['pw']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    data = {
        "user_id": session['user_id']
    }
    users = User.get_byid(data)
    return render_template('dashboard.html', users=users)

@app.route("/users")
def showusers():
    users = User.get_all()
    print(users)
    return render_template("newuser.html", users=users)

@app.route("/logout", methods=['POST'])
def clearsession():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")
            





            
if __name__ == "__main__":
    app.run(debug=True)
