from flask import Flask, render_template, request, redirect
# import the class from friend.py
from user import Email

app = Flask(__name__)
app.secret_key = 'many random bytes'

@app.route('/create_email', methods=["POST"])
def create_email():
    if not Email.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    data = {
        "email" : request.form["email"]
    }
    Email.save(data)
    return redirect('/emails')

@app.route("/emails")
def showemails():
    emails = Email.get_all()
    print(emails)
    return render_template("newuser.html", emails=emails)


@app.route("/")
def index():
    return render_template("index.html")
            





            
if __name__ == "__main__":
    app.run(debug=True)
