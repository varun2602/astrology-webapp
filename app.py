from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_file, make_response
import flask_mail
# from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from test import run, coord
from json2html import *
import json
# import pdfkit
import smtplib
from flask_mail import Mail, Message
import os
import re
import random
import sqlite3

# from helpers import render_pdf

# from helpers import run

# Initiate flask
app = Flask(__name__)


# Flask mail configuration
# Configure email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'vedicastro2617@gmail.com',
    "MAIL_PASSWORD": 'mjthvxxxmrbstlca'
}
app.config.update(mail_settings)
mail = Mail(app)

otp = random.randint(0000, 9999)
# List to help with password recovery
forgot = []



# Configuring session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initiate the database
def get_db():
    conn = sqlite3.connect("astro2.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")

# Register route
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        u_name=request.form.get("name")
        password=request.form.get("password")
        cpassword=request.form.get("cpassword")

        # checking if user has entered the username
        if not u_name:
            return render_template("apology.html", message="Please enter the username")
        # checking if password is entered
        if not password:
            return render_template("apology.html", message="Password required")
        # chechking for confirm password
        if not cpassword:
            return render_template("apology.html", message = "Please confirm the password")
        # checking if passwords match
        if password != cpassword:
            return render_template("apology.html", message="Passwords do not match")

        hash1 = generate_password_hash(password)
        
        # CHECKING IF USER IS REGISTERED
        # reg1 = db.execute("select id from users where name=?", u_name)
        conn = sqlite3.connect("astro2.db")
        cur = conn.cursor()
        cur.execute("select name from users where name = ?",(u_name,))

        reg1 = cur.fetchone()
        
       

        # ###########
        # Checking if user is registered
        if reg1 != None:
            return render_template("apology.html", message = "User already registered")
        
        

        # # db.execute("insert into users(name, hash) values(?,?)", u_name, hash1)
        # Inserting the data into the database:
        conn2 = sqlite3.connect("astro2.db")
        cur = conn2.cursor()
        conn2.cursor().execute("insert into users(name, hash) values(?, ?)", (u_name, hash1))
        conn2.commit()

        


        # Send email
        message = "You have been registered successfully!"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        # app password = vluxushzxskkwmgz
        server.login("vedicastro2617@gmail.com", "mjthvxxxmrbstlca")
        server.sendmail("vedicastro2617@gmail.com", u_name,message)

        conn.close()
        return render_template("success.html", message = "YOU ARE REGISTERED!")

# Login route
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        if not session.get("name"):
            return render_template("login.html")
        else:
            return redirect("/")
    if request.method == "POST":
        session.clear()

        name = request.form.get("name")
        password = request.form.get("password")

        if not name:
            return render_template("apology.html", message = "Name required")
        if not password:
            return render_template("apology.html", message = "Password required")
        # reg1 = db.execute("select * from users where name = ?", name)
        
        
        # Checking if user exists
        conn = sqlite3.connect("astro2.db")
        cur = conn.cursor()
        cur.execute("select name from users where name = ?",(name,))
        reg1 = cur.fetchone()
        if reg1 == None:
            return render_template("apology.html", message = "User does not exists")
        
        # Checking for password
        cur.execute("select hash from users where name = ?", (name,))
        reg2 = cur.fetchone()
        print(reg2[0])
        check = check_password_hash(reg2[0], password)
        print(check)
        
        if check == False:
            return render_template("apology.html", message = "Incorrect password")

        session["name"] = name
        conn.close()
        return redirect("/")
# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Route for birth details
@app.route("/api", methods = ["GET", "POST"])
def api():
    if not session.get("name"):
        return redirect("/login")
    if request.method == "GET":
        return render_template("details.html", v = "birth-details")
    if request.method == "POST":
# arranging parameters required by the run function to call the api
        path = "/birth-details"
        date = request.form.get("date")
        time = request.form.get("time")
        city = request.form.get("place")
        ayanamsha = request.form.get("ayanamsha")




# Storing the api data returned in json format in a variable
        apiresponse = coord(city, date, time, path, ayanamsha)
# Converting json to html and passing to the html template
        s = json2html.convert(json = apiresponse)
        return render_template("birthdetails.html", message = s)

@app.route("/advanced", methods = ["GET", "POST"])
def advanced():
    if not session.get("name"):
        return redirect("/login")
    if request.method == "GET":
        return render_template("details.html", v = "advanced")

    if request.method == "POST":
#Arranging the parameters
        path = "/kundli/advanced"
        date = request.form.get("date")
        city = request.form.get("place")
        time = request.form.get("time")
        ayanamsha = request.form.get("ayanamsha")
# Storing the API response in a variable
        m = coord(city, date, time, path, ayanamsha)
# Converting the json response to html format using json to html
        s = json2html.convert(json = m)
        return render_template("birthdetails.html", message = s)

# Route to create a downloadable pdf
@app.route("/download")
def download():
    r = render_template("birthdetails.html")
    responsestring = pdfkit.from_string(r, False)
    response = make_response(responsestring)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename = output.pdf'
    return response

# Nakshatra details
@app.route("/nakshatra", methods = ['GET', 'POST'])
def nakshatra():
    if not session.get("name"):
        return redirect("/login")
    if request.method == "GET":
        return render_template("details.html")
    if request.method == "POST":
#Arranging the parameters
        path = "/birth-details"
        date = request.form.get("date")
        city = request.form.get("place")
        time = request.form.get("time")
        ayanamsha = request.form.get("ayanamsha")
# Storing the API response in a variable
        m = coord(city, date, time, path, ayanamsha)
        print(m)
        print("****")
# Extracting nakshatra name from the json api data
        json_res = json.dumps(m)
        res = json.loads(json_res)
        data = res['data']
        nak_details = data['nakshatra']
        nak_name = nak_details['name']
        print(f"Nakshatra name:{{nak_name}}")
        template = f"{nak_name}.html"
        return render_template(template)

@app.route("/verify_email", methods = ["GET", "POST"])
def verify():
    if request.method == "GET":
        return render_template("verify.html")
    if request.method == "POST":
        email = request.form.get("email")


        # Check whether the user is registered
        # reg1 = db.execute("select * from users where name = ?", email)
        conn3 = sqlite3.connect("astro2.db")
        cur = conn3.cursor()
        cur.execute("select name from users where name = ?", (email,))
        reg1 = cur.fetchone()
        print(reg1)
        if reg1 == None:
            return render_template("apology.html", message = "User doesn't exist")

        msg = mail.send_message("OTP", sender = "cosmosv26@gmail.com", recipients = [email], body =f" Your OTP is {str(otp)}. Never share your OTP with anyone.")

        # forgot_name.append(email)
        forgot.append(email)
        conn3.close()
        return redirect("/otp_verify")

@app.route("/otp_verify", methods = ["GET", "POST"])
def otp_verify():
    if request.method == "GET":
        return render_template("otp.html")
    if request.method == "POST":
        otp_number = request.form.get("otp")

        if not otp_number:
            return render_template("apology.html", message = "OTP required")

        if str(otp) != otp_number:
            return render_template("apology.html", message = "Incorrect OTP")

        return redirect("final_verify")

@app.route("/final_verify", methods = ["GET", "POST"])
def final_verify():
    if request.method == "GET":
        return render_template("change.html")
    if request.method == "POST":
        password = request.form.get("password")


        if not password:
            return render_template("apology.html", message = "Password required")
        if not request.form.get("cpassword"):
            return render_template("apology.html", message = "Confirm the password")

        hash1 = generate_password_hash(password)

        # db.execute("update users set hash = ? where name = ?", hash1, forgot[0])
        conn = sqlite3.connect("astro2.db")
        cur = conn.cursor()
        cur.execute("update users set hash = ? where name = ?", (hash1, forgot[0]))
        print("success!")


        forgot.pop(0)
        print(forgot)
        return redirect("/login")








 







































# TODO: Run through the route of birth details, fetch the birthdetails, return the nakshatra name and render the template
# @app.route("/test")
# def test():
#     return render_template("Revati.html")






