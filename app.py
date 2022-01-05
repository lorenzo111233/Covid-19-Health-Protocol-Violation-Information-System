import sqlite3
import smtplib
from flask import Flask, render_template, request, url_for, g, flash, redirect, jsonify, make_response
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random
import string
import json
import os
import sys, requests, urllib
from datetime import datetime
import pdfkit
from twilio.rest import Client

account_sid = 'AC09e9c2b601c0ac8b97b62b19c5583f21'
auth_token = 'e1e7c0323aaaabf0ffb50485c00e5e9c'
client = Client(account_sid, auth_token)
def get_db_connection():
    conn = sqlite3.connect('database.db')   
    conn.row_factory = sqlite3.Row
    return conn
    conn.close()
    c = conn.cursor()
    
conn=sqlite3.connect("database.db")
conn.execute("create table if not exists image(pid integer primary key,img TEXT)")
conn.close()

  


app = Flask(__name__)

app.config['UPLOAD_FOLDER']="static\images"
app.config['SECRET_KEY'] = 'your secret key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lorenzomalla19@gmail.com'
app.config['MAIL_PASSWORD'] = 'silentkiller19'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
posta = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

global username



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    mail = db.Column(db.String(120))
    password = db.Column(db.String(80))
    position = db.Column(db.String(80))
    hashCode = db.Column(db.String(120))
    barangay = db.Column(db.String(80))

class violators(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    house_number = db.Column(db.String(30))
    street = db.Column(db.String(30))
    barangay = db.Column(db.String(30))
    contact = db.Column(db.Integer)
    violation = db.Column(db.String(30))
    penalty = db.Column(db.String(30))
    total_penalty = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(30))

class hi(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))


@app.route('/forgot',methods=["POST","GET"])
def forgot():
    if request.method=="POST":
        mail = request.form['mail']
        check = User.query.filter_by(mail=mail).first()

        if check:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'lorenzomalla19@gmail.com', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            posta.send(msg)
            flash('Code Sucessfully Send!')
            return render_template('forget.html')
    else:
        
        return render_template('forget.html')
@app.route('/municipal_chart')
def municipal_chart():
    conn = get_db_connection()
    municipal_db = conn.execute("SELECT COUNT(last_name) FROM violators").fetchall()
    aa = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Banca Banca'").fetchall()
    bb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Daniw'").fetchall()
    cc = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Masapang'").fetchall()
    dd = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Nanhaya'").fetchall()
    ee = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Pagalangan'").fetchall()
    ff = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Benito'").fetchall()
    gg = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Felix'").fetchall()
    hh = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Francisco'").fetchall()
    ii = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Roque'").fetchall()
    conn.close()
        
    income_vs_expense = db.session.query(db.func.count(violators.penalty=="Community Service"), violators.penalty=="300").group_by(violators.penalty).all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%d-%m-%y"))
        over_time_expenditure.append(amount)

    return render_template('municipal_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label),aa=aa,bb=bb,cc=cc,dd=dd,ee=ee,ff=ff,gg=gg,hh=hh,ii=ii,municipal_db=municipal_db
                        )    
@app.route('/daniw_chart')
def daniw_chart():
    conn = get_db_connection()
    municipal_db = conn.execute("SELECT COUNT(last_name) FROM violators").fetchall()
    aa = conn.execute("SELECT COUNT(last_name) FROM violators where violation='No Face Mask' and Barangay='Daniw'").fetchall()
    bb = conn.execute("SELECT COUNT(last_name) FROM violators where violation='No Face Shield' and Barangay='Daniw'").fetchall()
    cc = conn.execute("SELECT COUNT(last_name) FROM violators where violation='No Social Distancing' and Barangay='Daniw'").fetchall()
    dd = conn.execute("SELECT COUNT(last_name) FROM violators where violation='Curfew' and Barangay='Daniw'").fetchall()
    ee = conn.execute("SELECT COUNT(last_name) FROM violators where Barangay='Daniw'").fetchall()
    conn.close()
    income_vs_expense = db.session.query(db.func.count(violators.penalty=="Community Service"), violators.penalty=="300").group_by(violators.penalty).filter(violators.barangay=="Daniw").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Daniw").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).filter(violators.barangay=="Daniw").group_by(violators.date).order_by(violators.date).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('daniw_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label),aa=aa,bb=bb,cc=cc,dd=dd,ee=ee
                        )

@app.route('/bancabanca_chart')
def bancabanca_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Banca Banca").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Banca Banca").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="Banca Banca").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('bancabanca_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/masapang_chart')
def masapang_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Masapang").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Masapang").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="Masapang").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('masapang_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/nanhaya_chart')
def nanhaya_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Nanhaya").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Nanhaya").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="Nanhaya").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('nanhaya_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/pagalangan_chart')
def pagalangan_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Pagalangan").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Pagalangan").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="Pagalangan").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('pagalangan_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/sanbenito_chart')
def sanbenito_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Benito").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Benito").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="San Benito").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('sanbenito_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/sanfelix_chart')
def sanfelix_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Felix").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Felix").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="San Felix").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('sanfelix_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/sanfrancisco_chart')
def sanfrancisco_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Francisco").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Francisco").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="San Francisco").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('sanfrancisco_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route('/sanroque_chart')
def sanroque_chart():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Roque").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="San Roque").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="San Roque").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('sanroque_chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )

@app.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                flash('Password Sucessfully Changed!')
                return redirect(url_for('login'))
            else:
                return render_template('change_pass.html')
        else:   
            return render_template('change_pass.html')
    else:
        return redirect(url_for('forgot'))

@app.route('/', methods=('POST','GET'))
def login():
    
    conn = get_db_connection()
    
    barangayss = conn.execute('SELECT * FROM barangays').fetchall()
    
    if request.method == 'POST':
        
        cate1 = "Banca Banca"
        cate2 = "Daniw"
        cate3 = "Masapang"
        cate4 = "Nanhaya"
        cate5 = "Pagalangan"
        cate6 = "San Benito"
        cate7= "San Felix"
        cate8 = "San Francisco"
        cate9 = "San Roque"
        cate10 = "Municipal"
        cate11 = "Accounting"
        cate12 = "System Admin"
        uname = request.form.get('username')
        pword = request.form.get('password')
       
        
        action = 'Login'
        
        
        
        conn = get_db_connection()
        
        
        bancabanca = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate1)).fetchone()
        daniw = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate2)).fetchone()
        masapang = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate3)).fetchone()
        nanhaya = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate4)).fetchone()
        pagalangan = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate5)).fetchone()
        sanbenito = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate6)).fetchone()
        sanfelix = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate7)).fetchone()
        sanfrancisco = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate8)).fetchone()
        sanroque = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate9)).fetchone()
        municipals = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate10)).fetchone()
        accounting = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate11)).fetchone()
        admin = conn.execute('SELECT * FROM user WHERE username=? and password=? and barangay=?',(uname,pword,cate12)).fetchone()
        conn.commit()
        conn.close()
        
        

        

        if bancabanca and cate1:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate1))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('bancabanca_dashboard'))
        
        elif daniw and cate2:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate2))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('daniw_dashboard'))
        
        
        elif masapang and cate3:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate3))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('masapang_dashboard'))
        
        elif nanhaya and cate4:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate4))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('nanhaya_dashboard'))
        
        elif pagalangan and cate5:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate5))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))    
            conn.commit()
            conn.close()
            return redirect(url_for('pagalangan_dashboard'))
        
        elif sanbenito and cate6:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate6))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('sanbenito_dashboard'))
        
        elif sanfelix and dcate7:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate7))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('sanfelix_dashboard'))

        if sanfrancisco and cate8:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate8))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('sanfrancisco_dashboard'))
        
        elif sanroque and cate9:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate9))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('sanroque_dashboard'))

        elif municipals and cate10:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate10))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('municipal_dashboard'))

        elif accounting and cate11:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate11))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('accounting_dashboard'))

        elif admin and cate12:
            conn = get_db_connection()
            conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (uname, action, cate11))
            conn.execute('INSERT INTO hi (username, password) VALUES (?,?)', (uname, pword))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_dashboard'))
        
        
        
        else:
            flash("LogIn Failed!");
            return redirect(url_for('login'))
    hi.query.delete()       
    return render_template('login.html', barangayss=barangayss);

@app.route('/municipal')
def municipal():
    conn = get_db_connection()
    municipal = conn.execute("SELECT * FROM violators").fetchall()
    conn.close()
    return render_template('municipal_tab.html', municipal=municipal);

@app.route('/municipal_table')
def municipal_table():
    conn = get_db_connection()
    municipal = conn.execute("SELECT * FROM violators").fetchall()
    conn.close()
    return render_template('municipal_table.html', municipal=municipal);


@app.route('/bancabanca_reports')
def bancabanca_reports():
    return render_template('bancabanca_reports.html')

@app.route('/municipal_archive')
def municipal_archive():
    conn = get_db_connection()
    municipal_archive = conn.execute("SELECT * FROM archive").fetchall()
    conn.close()
    return render_template('municipal_archive.html', municipal_archive=municipal_archive)

@app.route('/admin_archive')
def admin_archive():
    conn = get_db_connection()
    admin_archive = conn.execute("SELECT * FROM archive").fetchall()
    conn.close()
    return render_template('admin_archive.html', admin_archive=admin_archive)

@app.route('/bancabanca_archive')
def bancabanca_archive():
    conn = get_db_connection()
    bancabanca = conn.execute("SELECT * FROM archive where barangay='Banca Banca'").fetchall()
    conn.close()
    return render_template('bancabanca_archive.html', bancabanca=bancabanca)
@app.route('/daniw_archive')
def daniw_archive():
    conn = get_db_connection()
    daniw = conn.execute("SELECT * FROM archive where barangay='Daniw'").fetchall()
    conn.close()
    return render_template('daniw_archive.html', daniw=daniw)
@app.route('/masapang_archive')
def masapang_archive():
    conn = get_db_connection()
    masapang = conn.execute("SELECT * FROM archive where barangay='Masapang'").fetchall()
    conn.close()
    return render_template('masapang_archive.html', masapang=masapang)
@app.route('/nanhaya_archive')
def nanhaya_archive():
    conn = get_db_connection()
    nanhaya = conn.execute("SELECT * FROM archive where barangay='Nanhaya'").fetchall()
    conn.close()
    return render_template('nanhaya_archive.html', nanhaya=nanhaya)
@app.route('/pagalangan_archive')
def pagalangan_archive():
    conn = get_db_connection()
    pagalangan = conn.execute("SELECT * FROM archive where barangay='Pagalangan'").fetchall()
    conn.close()
    return render_template('pagalangan_archive.html', pagalangan=pagalangan)
@app.route('/sanbenito_archive')
def sanbenito_archive():
    conn = get_db_connection()
    sanbenito = conn.execute("SELECT * FROM archive where barangay='San Benito'").fetchall()
    conn.close()
    return render_template('sanbenito_archive.html', sanbenito=sanbenito)
@app.route('/sanfelix_archive')
def sanfelix_archive():
    conn = get_db_connection()
    sanfelix = conn.execute("SELECT * FROM archive where barangay='San Felix'").fetchall()
    conn.close()
    return render_template('sanfelix_archive.html', sanfelix=sanfelix)
@app.route('/sanfrancisco_archive')
def sanfrancisco_archive():
    conn = get_db_connection()
    sanfrancisco = conn.execute("SELECT * FROM archive where barangay='San Francisco'").fetchall()
    conn.close()
    return render_template('sanfrancisco_archive.html', sanfrancisco=sanfrancisco)
@app.route('/sanroque_archive')
def sanroque_archive():
    conn = get_db_connection()
    sanroque = conn.execute("SELECT * FROM archive where barangay='San Roque'").fetchall()
    conn.close()
    return render_template('sanroque_archive.html', sanroque=sanroque)
      
@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    conn = get_db_connection()
    if request.method == 'POST':
        userid = request.form['id']
        last_name = request.form['last_name']
        print(userid,last_name)
        bancabanca = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchall()
    return jsonify({'htmlresponse': render_template('response.html',bancabanca=bancabanca)})

@app.route('/select', methods=['GET', 'POST'])
def select():   
    conn = get_db_connection()
    if request.method == 'POST': 
        employee_id = request.form['id']
        print(employee_id)      
        bancabanca = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'Id': rs['id'],
                    'emp_name': rs['name'],
                    'address': rs['address'],
                    'gender': rs['gender'],
                    'designation': rs['designation'],
                    'age': rs['age']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)

@app.route('/accounting')
def accounting():
        
        
        conn = get_db_connection()
        accounting = conn.execute("SELECT * FROM violators where penalty!='Community Service' and total_penalty!='0'").fetchall()
        accvl = conn.execute("SELECT * FROM violators").fetchall()
        payy = conn.execute("SELECT * FROM pay").fetchall()
        total = conn.execute("SELECT sum(penalty) FROM pay").fetchall()
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        ham = total
        if payy is None:
            total = 0
        else:
            total = conn.execute("SELECT sum(penalty) FROM pay").fetchall()
        conn.close()        

        

        return render_template('accounting.html',accounting=accounting,payy=payy,total=total,accvl=accvl,violations=violations,stat=stat);
datetime = datetime.today()
@app.route('/<id>/receipt' ,methods=["POST","GET"])
def receipt(id):
    conn = get_db_connection()
    receipt = conn.execute('SELECT * FROM violators WHERE id = ?',(id,)).fetchone()
    return render_template('receipt.html',receipt=receipt)
    
@app.route('/<id>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<violation>/<total_penalty>/<penalty>/receipt1',methods=["POST","GET"])
def receipt1(id,last_name,first_name,middle_name,house_number,street,barangay,violation,total_penalty,penalty):
        rendered = render_template('receipt1.html', id=id, last_name=last_name, first_name=first_name, 
                middle_name=middle_name, house_number=house_number, street=street, barangay=barangay, violation=violation, total_penalty=total_penalty, 
                penalty=penalty)
        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response    
            
@app.route('/municipal_service')
def municipal_service():
        
        
        conn = get_db_connection()
        municipal_service = conn.execute("SELECT * FROM violators where penalty='Community Service'").fetchall()
        conn.close()

        return render_template('municipal_service.html',municipal_service=municipal_service);

@app.route('/admin_account')
def admin_account():
        
        
        conn = get_db_connection()
        admin_account = conn.execute("SELECT * FROM user").fetchall()
        conn.close()

        return render_template('admin_account.html',admin_account=admin_account);

@app.route('/bancabanca_service')
def bancabanca_service():
        
        
        conn = get_db_connection()
        bancabanca_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='Banca Banca' ").fetchall()
        conn.close()

        return render_template('bancabanca_service.html',bancabanca_service=bancabanca_service);
@app.route('/daniw_service')
def daniw_service():
        
        
        conn = get_db_connection()
        daniw_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='Daniw' ").fetchall()
        conn.close()

        return render_template('daniw_service.html', daniw_service=daniw_service);
@app.route('/masapang_service')
def masapang_service():
        
        
        conn = get_db_connection()
        masapang_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='Masapang' ").fetchall()
        conn.close()

        return render_template('masapang_service.html',masapang_service=masapang_service);
@app.route('/nanhaya_service')
def nanhaya_service():
        
        
        conn = get_db_connection()
        nanhaya_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='Nanhaya' ").fetchall()
        conn.close()

        return render_template('nanhaya_service.html',nanhaya_service=nanhaya_service);
@app.route('/pagalangan_service')
def pagalangan_service():
        
        
        conn = get_db_connection()
        pagalangan_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='Pagalangan' ").fetchall()
        conn.close()

        return render_template('pagalangan_service.html',pagalangan_service=pagalangan_service);
@app.route('/sanbenito_service')
def sanbenito_service():
        
        
        conn = get_db_connection()
        sanbenito_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='San Benito' ").fetchall()
        conn.close()

        return render_template('sanbenito_service.html',sanbenito_service=sanbenito_service);
@app.route('/sanfelix_service')
def sanfelix_service():
        
        
        conn = get_db_connection()
        sanfelix_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='San Felix' ").fetchall()
        conn.close()

        return render_template('sanfelix_service.html',sanfelix_service=sanfelix_service);
@app.route('/sanfrancisco_service')
def sanfrancisco_service():
        
        
        conn = get_db_connection()
        sanfrancisco_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='San Francisco' ").fetchall()
        conn.close()

        return render_template('sanfrancisco_service.html',sanfrancisco_service=sanfrancisco_service);
@app.route('/sanroque_service')
def sanroque_service():
        
        
        conn = get_db_connection()
        sanroque_service = conn.execute("SELECT * FROM violators where penalty='Community Service' and barangay='San Roque' ").fetchall()
        conn.close()

        return render_template('sanroque_service.html',sanroque_service=sanroque_service);
    
@app.route('/bancabanca')
def bancabanca():
        
        
        conn = get_db_connection()
        bancabanca = conn.execute("SELECT * FROM violators where barangay='Banca Banca'").fetchall()
        conn.close()

        return render_template('bancabanca_tab.html',bancabanca=bancabanca);

@app.route('/more_settings')
def more_settings():
        
        
        conn = get_db_connection()
        more_settings = conn.execute("SELECT * FROM violations").fetchall()
        more_settings2 = conn.execute("SELECT * FROM stat").fetchall()
        conn.close()

        return render_template('more_settings.html',more_settings=more_settings,more_settings2=more_settings2);


@app.route('/daniw')
def daniw():
        
        
        conn = get_db_connection()
        daniw = conn.execute("SELECT * FROM violators where barangay='Daniw'").fetchall()
        conn.close()

        return render_template('daniw_tab.html',daniw=daniw);

@app.route('/masapang')
def masapang():
        
        
        conn = get_db_connection()
        masapang = conn.execute("SELECT * FROM violators where barangay='Masapang'").fetchall()
        conn.close()

        return render_template('masapang_tab.html',masapang=masapang);

@app.route('/nanhaya')
def nanhaya():
        
        
        conn = get_db_connection()
        nanhaya = conn.execute("SELECT * FROM violators where barangay='Nanhaya'").fetchall()
        conn.close()

        return render_template('nanhaya_tab.html',nanhaya=nanhaya);

@app.route('/pagalangan')
def pagalangan():
        
        
        conn = get_db_connection()
        pagalangan = conn.execute("SELECT * FROM violators where barangay='Pagalangan'").fetchall()
        conn.close()

        return render_template('pagalangan_tab.html',pagalangan=pagalangan);

@app.route('/sanbenito')
def sanbenito():
        
        
        conn = get_db_connection()
        sanbenito = conn.execute("SELECT * FROM violators where barangay='San Benito'").fetchall()
        conn.close()

        return render_template('sanbenito_tab.html',sanbenito=sanbenito);

@app.route('/sanfelix')
def sanfelix():
        
        
        conn = get_db_connection()
        sanfelix = conn.execute("SELECT * FROM violators where barangay='San Felix'").fetchall()
        conn.close()

        return render_template('sanfelix_tab.html',sanfelix=sanfelix);

@app.route('/sanfrancisco')
def sanfrancisco():
        
        
        conn = get_db_connection()
        sanfrancisco = conn.execute("SELECT * FROM violators where barangay='San Francisco' ORDER BY(last_name)").fetchall()
        conn.close()

        return render_template('sanfrancisco_tab.html',sanfrancisco=sanfrancisco);

@app.route('/sanroque')
def sanroque():
        
        
        conn = get_db_connection()
        sanroque = conn.execute("SELECT * FROM violators where barangay='San Roque'").fetchall()
        conn.close()

        return render_template('sanroque_tab.html',sanroque=sanroque);

@app.route('/admin_dashboard', methods=('POST','GET'))
def admin_dashboard():
        
       
        conn = get_db_connection()
        ta = conn.execute("SELECT COUNT(*) FROM user where barangay!='Municipal' and barangay!='Accounting' and barangay!='System Admin'").fetchall()
        superuser = conn.execute("SELECT COUNT(username) FROM user where barangay='Municipal'").fetchall()
        accounting = conn.execute("SELECT COUNT(username) FROM user where barangay='Accounting'").fetchall()
        systemadmin = conn.execute("SELECT COUNT(username) FROM user where barangay='System Admin'").fetchall()
        ad = conn.execute("SELECT COUNT(*) as 'barangay' FROM user where barangay='Banca Banca' and barangay='San Fracisco'").fetchall()
        conn.close()
        return render_template('admin_dashboard.html',ta=ta,ad=ad,superuser=superuser,systemadmin=systemadmin,accounting=accounting);

@app.route('/accounting_dashboard', methods=('POST','GET'))
def accounting_dashboard():
    conn = get_db_connection()
    aa = conn.execute("SELECT COUNT(last_name) FROM violators").fetchall()
    conn.close()


    
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Daniw").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Daniw").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="Daniw").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('accounting_dashboard.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label),
                           aa=aa
                        )

@app.route('/accounting_transaction', methods=('POST','GET'))
def accounting_transaction():
        conn = get_db_connection()
        aa = conn.execute("SELECT * FROM violators").fetchall()
        conn.close()
        return render_template('accounting_transaction.html',aa=aa);

@app.route('/accounting_logs', methods=('POST','GET'))
def accounting_logs():
        conn = get_db_connection()
        bblogs = conn.execute("SELECT * FROM logs where address='Accounting'").fetchall()
        conn.close()
        return render_template('accounting_logs.html');

@app.route('/accounting_reports', methods=('POST','GET'))
def accounting_reports():
    income_vs_expense = db.session.query(db.func.sum(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Daniw").all()

    category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.violation).filter(violators.barangay=="Daniw").all()

    dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).filter(violators.barangay=="Daniw").all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('accounting_reports.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )
    
            

@app.route('/bancabanca_dashboard', methods=('POST','GET'))
def bancabanca_dashboard():
        
       
        conn = get_db_connection()
        aa = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Banca Banca'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()
        return render_template('bancabanca_dashboard.html',aa=aa,hi=hi);

@app.route('/municipal_dashboard', methods=('POST','GET')) 
def municipal_dashboard():
        conn = get_db_connection()
        municipal_db = conn.execute("SELECT COUNT(last_name) FROM violators").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        aa = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Banca Banca'").fetchall()
        bb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Daniw'").fetchall()
        cc = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Masapang'").fetchall()
        dd = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Nanhaya'").fetchall()
        ee = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Pagalangan'").fetchall()
        ff = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Benito'").fetchall()
        gg = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Felix'").fetchall()
        hh = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Francisco'").fetchall()
        ii = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Roque'").fetchall()
        conn.close()

        income_vs_expense = db.session.query(db.func.count(violators.penalty=="Community Service"), violators.penalty=="300").group_by(violators.penalty).all()

        category_comparison = db.session.query(db.func.count(violators.penalty), violators.violation).group_by(violators.barangay).all()

        dates = db.session.query(db.func.count(violators.penalty), violators.date).group_by(violators.date).all()

        income_category = []
        for amounts, _ in category_comparison:
            income_category.append(amounts)

        income_expense = []
        for total_amount, _ in income_vs_expense:
            income_expense.append(total_amount)

        over_time_expenditure = []
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_expenditure.append(amount)
    
        return render_template('municipal_dashboard.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label),
                            municipal_db=municipal_db,aa=aa,bb=bb,cc=cc,dd=dd,ee=ee,ff=ff,gg=gg,hh=hh,ii=ii,hi=hi);

@app.route('/daniw_dashboard')
def daniw_dashboard():
    
        conn = get_db_connection()
        ddb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Daniw'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('daniw_dashboard.html',ddb=ddb,hi=hi);

@app.route('/masapang_dashboard')
def masapang_dashboard():
        
        
        conn = get_db_connection()
        mdb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Masapang'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('masapang_dashboard.html',mdb=mdb,hi=hi);

@app.route('/nanhaya_dashboard')
def nanhaya_dashboard():
        
        
        conn = get_db_connection()
        ndb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Nanhaya'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('nanhaya_dashboard.html',ndb=ndb,hi=hi);

@app.route('/pagalangan_dashboard')
def pagalangan_dashboard():
        
        
        conn = get_db_connection()
        pdb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='Pagalangan'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('pagalangan_dashboard.html',pdb=pdb,hi=hi);

@app.route('/sanbenito_dashboard')
def sanbenito_dashboard():
        
        
        conn = get_db_connection()
        sbdb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Benito'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('sanbenito_dashboard.html',sbdb=sbdb,hi=hi);
    
@app.route('/sanfelix_dashboard')
def sanfelix_dashboard():
        
        
        conn = get_db_connection()
        fdb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Felix'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('sanfelix_dashboard.html',fdb=fdb,hi=hi);

@app.route('/sanfrancisco_dashboard')
def sanfrancisco_dashboard():
        
        
        conn = get_db_connection()
        sfdb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Francisco'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('sanfrancisco_dashboard.html',sfdb=sfdb,hi=hi);

@app.route('/sanroque_dashboard')
def sanroque_dashboard():
        
        
        conn = get_db_connection()
        srdb = conn.execute("SELECT COUNT(last_name) FROM violators where barangay='San Roque'").fetchall()
        hi = conn.execute("SELECT * FROM hi").fetchall()
        conn.close()

        return render_template('sanroque_dashboard.html',srdb=srdb,hi=hi);

@app.route('/bancabanca_logs')
def bancabanca_logs():
        
        
        conn = get_db_connection()
        bblogs = conn.execute("SELECT * FROM logs where address='Banca Banca'").fetchall()
        conn.close()

        return render_template('bancabanca_logs.html',bblogs=bblogs);

@app.route('/municipal_logs')
def municipal_logs():
        
        
        conn = get_db_connection()
        mmlogs = conn.execute("SELECT * FROM logs").fetchall()
        conn.close()

        return render_template('municipal_logs.html',mmlogs=mmlogs);

@app.route('/admin_logs')
def admin_logs():
        
        
        conn = get_db_connection()
        mmlogs = conn.execute("SELECT * FROM logs").fetchall()
        conn.close()

        return render_template('admin_logs.html',mmlogs=mmlogs);

@app.route('/daniw_logs')
def daniw_logs():
        
        
        conn = get_db_connection()
        dlogs = conn.execute("SELECT * FROM logs where address='Daniw'").fetchall()
        conn.close()

        return render_template('daniw_logs.html',dlogs=dlogs);

@app.route('/masapang_logs')
def masapang_logs():
        
        
        conn = get_db_connection()
        mlogs = conn.execute("SELECT * FROM logs where address='Masapang'").fetchall()
        conn.close()

        return render_template('masapang_logs.html',mlogs=mlogs);

@app.route('/nanhaya_logs')
def nanhaya_logs():
        
        
        conn = get_db_connection()
        nlogs = conn.execute("SELECT * FROM logs where address='Nanhaya'").fetchall()
        conn.close()

        return render_template('nanhaya_logs.html',nlogs=nlogs);

@app.route('/pagalangan_logs')
def pagalangan_logs():
        
        
        conn = get_db_connection()
        plogs = conn.execute("SELECT * FROM logs where address='Pagalangan'").fetchall()
        conn.close()

        return render_template('pagalangan_logs.html',plogs=plogs);

@app.route('/sanbenito_logs')
def sanbenito_logs():
        
        
        conn = get_db_connection()
        sblogs = conn.execute("SELECT * FROM logs where address='San Benito'").fetchall()
        conn.close()

        return render_template('sanbenito_logs.html',sblogs=sblogs);


@app.route('/sanfelix_logs')
def sanfelix_logs():
        
        
        conn = get_db_connection()
        flogs = conn.execute("SELECT * FROM logs where address='San Felix'").fetchall()
        conn.close()

        return render_template('sanfelix_logs.html',flogs=flogs);

@app.route('/sanfrancisco_logs')
def sanfrancisco_logs():
        
        
        conn = get_db_connection()
        sflogs = conn.execute("SELECT * FROM logs where address='San Francisco'").fetchall()
        conn.close()

        return render_template('sanfrancisco_logs.html',sflogs=sflogs);

@app.route('/sanroque_logs')
def sanroque_logs():
        
        
        conn = get_db_connection()
        srlogs = conn.execute("SELECT * FROM logs where address='San Roque'").fetchall()
        conn.close()

        return render_template('sanroque_logs.html',srlogs=srlogs);


        
    
    
@app.route('/<table>/add', methods=('GET','POST'))
def add(table):
        
        
    conn = get_db_connection()
    if(table=="sfvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'San Francisco'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('sanfrancisco'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name=? and first_name=? and middle_name=?',( total_penalty_up, last_name,first_name,middle_name))
                conn.commit()
                conn.close()
                return redirect(url_for('sanfrancisco'))
            
        return render_template('add_sanfrancisco.html', violations=violations, stat=stat);
    elif(table=="bbvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'Banca Banca'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                
                conn.commit()
                conn.close()
                
                return redirect(url_for('bancabanca'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('bancabanca'))
            
        return render_template('add_bancabanca.html', violations=violations, stat=stat);

    elif(table=="dvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'Daniw'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                flash('"{}" was successfully edited!'.format(last_name))
                return redirect(url_for('daniw'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('daniw'))
            
        return render_template('add_daniw.html', violations=violations, stat=stat);

    elif(table=="mvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'Masapang'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('masapang'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('masapang'))
            
        return render_template('add_masapang.html', violations=violations, stat=stat);

    elif(table=="nvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'Nanhaya'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('nanhaya'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('nanhaya'))
            
        return render_template('add_nanhaya.html', violations=violations, stat=stat);

    elif(table=="pvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'Pagalangan'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('pagalangan'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('pagalangan'))
            
        return render_template('add_pagalangan.html', violations=violations, stat=stat);

    elif(table=="sbvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'San Benito'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('sanbenito'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('sanbenito'))
            
        return render_template('add_sanbenito.html', violations=violations, stat=stat);

    elif(table=="fvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'San Felix'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('sanfelix'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('sanfelix'))
            
        return render_template('add_sanfelix.html', violations=violations, stat=stat);

    elif(table=="srvl"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = 'San Roque'
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('sanroque'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('sanroque'))
            
        return render_template('add_sanroque.html', violations=violations, stat=stat);

    elif(table=="municipal"):
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        barangayss = conn.execute('SELECT * FROM barangays').fetchall()
        
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            house_number = request.form['house_number']
            street = request.form['street']
            barangay = request.form['barangay']
            contact = request.form['contact']
            violation = request.form['violation']
            penalty = request.form['penalty']
            status = 'Pending'
            action = 'Add Violators'
            total_penalty = 1
            bayan = conn.execute('SELECT * FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ? ',(last_name,first_name,middle_name,penalty,)).fetchone()
            
            if bayan is None:
                
                conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status))
                conn.execute('INSERT INTO municipal_logs (username, action, address) VALUES (?,?,?)', (last_name, action, barangay))
                conn.commit()
                conn.close()
                return redirect(url_for('municipal'))
            else:
                pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                up = conn.execute('SELECT penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
                total_penalty_up = pen['total_penalty'] + total_penalty
                conn.execute('UPDATE violators SET total_penalty=? WHERE last_name = ?',( total_penalty_up, last_name))
                conn.commit()
                conn.close()
                return redirect(url_for('municipal'))
            
        return render_template('add_municipal.html', violations=violations, stat=stat, barangayss=barangayss);

    elif(table=="mmacc"):
        if request.method == 'POST':
            username = request.form['username']
            mail = request.form['mail']
            password = request.form.get('password')
            barangay = request.form['barangay']
            position = request.form['position']
            action = "Add Account"
            address = "System Admin"
            bayan = conn.execute('SELECT * FROM user WHERE username = ?',(username,)).fetchone()
            
            if bayan is None:
                conn.execute('INSERT INTO user (username, password, mail, position, barangay ) VALUES (?,?,?,?,?)', (username, password, mail, position, barangay))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (username, action, address))
                conn.commit()
                conn.close()
                return redirect(url_for('admin_account'))
            else:
                flash("Account Aldready Exist!")
                return redirect(url_for('add', table="mmacc"))
            
        return render_template('add_admin_account.html')

    elif(table=="viol"):
        if request.method == 'POST':
            v = request.form['violation']
            vio = conn.execute('SELECT * FROM violations WHERE violation = ?',(v,)).fetchone()
            if vio is None:
                conn.execute('INSERT INTO violations (violation) VALUES (?)', (v,))
                conn.commit()
                conn.close()
                return redirect(url_for('more_settings'))  
            
    return render_template('add_more.html');

@app.route('/add_penalty', methods=('GET','POST'))
def add_penalty():
    conn = get_db_connection()
    if request.method == 'POST':
            p = request.form['penalty']
            conn.execute('INSERT INTO stat (penalty) VALUES (?)', (p,))
            conn.commit()
            conn.close()  
            return redirect(url_for('more_settings'))
    return render_template('add_more2.html');

@app.route('/<table>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<total_penalty>/<date>/<status>/delete_perma', methods=('GET','POST'))
def delete_perma(table,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty, total_penalty, date, status):
    conn = get_db_connection()
    if table == "municipal":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and house_number=? and street=? and barangay=? and contact=? and violation=? and penalty=? and total_penalty=? and date=? and status=?', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('municipal_archive'));
    if table == "admin":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and house_number=? and street=? and barangay=? and contact=? and violation=? and penalty=? and total_penalty=? and date=? and status=?', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('admin_archive'));
    elif table == "bbvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and house_number=? and street=? and barangay=? and contact=? and violation=? and penalty=? and total_penalty=? and date=? and status=?', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('bancabanca_archive'));
    elif table == "dvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('daniw_archive'));
    elif table == "mvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('masapang_archive'));
    elif table == "nvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('nanhaya_archive'));
    elif table == "pvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('pagalangan_archive'));
    elif table == "sbvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanbenito_archive'));
    elif table == "fvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanfelix_archive'));
    elif table == "sfvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanfrancisco'));
    elif table == "srvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanroque_archive'));
    
@app.route('/<table>/<id>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<total_penalty>/<date>/<status>/delete', methods=('GET','POST'))
def delete(table,id,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty, total_penalty, date, status):
    conn = get_db_connection()
    if table == "municipal":
        conn.execute('DELETE FROM violators WHERE id=? and last_name = ? and first_name=? and middle_name=? and house_number=? and street=? and barangay=? and contact=? and violation=? and penalty=? and total_penalty=? and date=? and status=?', (id,last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('municipal'));
    elif table == "bbvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and house_number=? and street=? and barangay=? and contact=? and violation=? and penalty=? and total_penalty=? and date=? and status=?', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('bancabanca'));
    elif table == "dvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('daniw'));
    elif table == "mvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('masapang'));
    elif table == "nvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('nanhaya'));
    elif table == "pvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('pagalangan'));
    elif table == "sbvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('sanbenito'));
    elif table == "fvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('sanfelix'));
    elif table == "sfvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('sanfrancisco'));
    elif table == "srvl":
        conn.execute('DELETE FROM violators WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO archive (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(last_name))
        return redirect(url_for('sanroque'));



@app.route('/<table>/<id>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<date>/<status>/add_topay', methods=('GET','POST'))
def add_topay(table,id,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty, date, status):
    conn = get_db_connection()
    pen = conn.execute('SELECT total_penalty FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
    quantity = request.form.get('quantity', True)
    accvl = conn.execute("SELECT * FROM violators").fetchall()
    penalty_up = pen['total_penalty'] - quantity
    hello = pen['total_penalty'] > quantity
    if table == "admin" and hello:
        conn.execute('UPDATE violators set total_penalty=? WHERE last_name = ?', (penalty_up, last_name,))
        conn.commit()
        conn.execute('INSERT INTO pay (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, quantity, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully add to pay section!'.format(last_name))
        return redirect(url_for('accounting'));
    elif pen['total_penalty'] == quantity:
        conn.execute('DELETE FROM violators WHERE id = ?', (id,))
        conn.commit()
        conn.execute('INSERT INTO pay (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, quantity, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully add to pay section!'.format(last_name))
        return redirect(url_for('accounting'));
    else:
        flash('Insufficient')
        return redirect(url_for('accounting'));
    return render_template('add_to_pay.html',accvl=accvl);
@app.route('/<table>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<total_penalty>/<date>/<status>/add_back', methods=('GET','POST'))
def add_back(table,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty, total_penalty, date, status):
    conn = get_db_connection()
    if table == "admin":
        conn.execute('DELETE FROM pay WHERE last_name = ?', (last_name,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully remove to pay section!'.format(last_name))
        return redirect(url_for('accounting'));

@app.route('/<table>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<total_penalty>/<date>/<status>/restore', methods=('GET','POST'))
def restore(table,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty, total_penalty, date, status):
    conn = get_db_connection()
    if table == "municipal":
        conn.execute('DELETE FROM archive WHERE last_name = ?', (last_name,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('municipal_archive'));
    if table == "admin":
        conn.execute('DELETE FROM archive WHERE last_name = ?', (last_name,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('admin_archive'));
    elif table == "bbvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and house_number=? and street=? and barangay=? and contact=? and violation=? and penalty=? and total_penalty=? and date=? and status=?', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('bancabanca_archive'));
    elif table == "dvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('daniw_archive'));
    elif table == "mvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('masapang_archive'));
    elif table == "nvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('nanhaya_archive'));
    elif table == "pvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('pagalangan_archive'));
    elif table == "sbvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanbenito_archive'));
    elif table == "fvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanfelix_archive'));
    elif table == "sfvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanfrancisco'));
    elif table == "srvl":
        conn.execute('DELETE FROM archive WHERE last_name = ? and first_name=? and middle_name=? and penalty=?', (last_name,first_name,middle_name,penalty,))
        conn.commit()
        conn.execute('INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, date, status))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(last_name))
        return redirect(url_for('sanroque_archive'));
    
@app.route('/<table>/<violation>/delete_more', methods=('GET','POST'))
def delete_more(table,violation):
    conn = get_db_connection()
    if table == "vio":
        conn.execute('DELETE FROM violations WHERE violation = ?', (violation,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(violation))
        return redirect(url_for('more_settings'));

@app.route('/<table>/<penalty>/delete_more2', methods=('GET','POST'))
def delete_more2(table,penalty):
    conn = get_db_connection()
    if table == "sta":
        conn.execute('DELETE FROM stat WHERE penalty = ?', (penalty,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully restored!'.format(penalty))
        return redirect(url_for('more_settings'));
    

    
@app.route('/<table>/<username>/delete_account', methods=('GET','POST'))
def delete_account(table,username):
    conn = get_db_connection()
    if table == "mmacc":
        conn.execute('DELETE FROM user WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(username))
        return redirect(url_for('admin_account'));
    
@app.route('/<table>/<id>/edit', methods=('GET','POST'))
def edit(table,id):
    conn = get_db_connection()
    if table == "sfvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        sfvl = conn.execute('SELECT * FROM violators WHERE id = ?',(id,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE id != ? AND id = ?',(id,id)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="sfvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET last_name=?, first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE id = ?',(last_name, first_name, middle_name, house_number, street, contact, violation, penalty, id))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('sanfrancisco'));
        return render_template('edit_sanfrancisco.html',sfvl=sfvl, violations=violations,stat=stat)
    
    elif table == "bbvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        bbvl = conn.execute('SELECT * FROM violators WHERE id = ?',(id,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE id != ? AND id = ?',(id,id)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="bbvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('bancabanca'));
        return render_template('edit_bancabanca.html',bbvl=bbvl, violations=violations,stat=stat)

    
    elif table == "dvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        dvl = conn.execute('SELECT * FROM violators WHERE id = ?',(id,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE id != ? AND id = ?',(id,id)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="dvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET last_name=?, first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE id = ?',(last_name, first_name, middle_name, house_number, street, contact, violation, penalty, id))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('daniw'));
        return render_template('edit_daniw.html',dvl=dvl, violations=violations,stat=stat)

    elif table == "mvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        mvl = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE last_name != ? AND last_name = ?',(last_name,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="mvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('masapang'));
        return render_template('edit_masapang.html',mvl=mvl, violations=violations,stat=stat)

    elif table == "nvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        nvl = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE last_name != ? AND last_name = ?',(last_name,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="nvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('nanhaya'));
        return render_template('edit_nanhaya.html',nvl=nvl, violations=violations,stat=stat)

    elif table == "pvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        pvl = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE last_name != ? AND last_name = ?',(last_name,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="pvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('pagalangan'));
        return render_template('edit_pagalangan.html',pvl=pvl, violations=violations,stat=stat)

    elif table == "sbvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        sbvl = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE last_name != ? AND last_name = ?',(last_name,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="sbvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('sanbenito'));
        return render_template('edit_sanbenito.html',sbvl=sbvl, violations=violations,stat=stat)

    elif table == "fvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        fvl = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE last_name != ? AND last_name = ?',(last_name,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="fvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('sanbenito'));
        return render_template('edit_sanbenito.html',fvl=fvl, violations=violations,stat=stat)

    elif table == "srvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        srvl = conn.execute('SELECT * FROM violators WHERE last_name = ?',(last_name,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE last_name != ? AND last_name = ?',(last_name,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="srvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('sanroque'));
        return render_template('edit_sanroque.html',srvl=srvl, violations=violations,stat=stat)

    elif table == "mmvl":
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        mmvl = conn.execute('SELECT * FROM violators WHERE id = ?',(id,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE id != ? AND id = ?',(id,id)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="mmvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                barangay = request.form['barangay']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, barangay=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, barangay, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('municipal'));
        return render_template('edit_municipal.html',mmvl=mmvl, violations=violations,stat=stat)
    
    elif table == "accvl":
        accounting = conn.execute("SELECT * FROM violators where penalty!='Community Service' and total_penalty!='0'").fetchall()
        accvl = conn.execute('SELECT * FROM violators WHERE id = ?',(id,)).fetchone()
        payy = conn.execute("SELECT * FROM pay").fetchall()
        total = conn.execute("SELECT sum(penalty) FROM pay").fetchall()
        violations = conn.execute('SELECT * FROM violations').fetchall()
        stat = conn.execute('SELECT * FROM stat').fetchall()
        if request.method == "POST":
            updated_name = request.form['last_name']
            existing_employee = conn.execute('SELECT * FROM violators WHERE id != ? AND id = ?',(id,updated_name)).fetchone()
            if existing_employee:
                flash('Violators {} Already exist!'.format(updated_name))
                return redirect(url_for('edit',table="accvl",last_name=last_name))
            else:
                last_name = request.form['last_name']
                first_name = request.form['first_name']
                middle_name = request.form['middle_name']
                house_number = request.form['house_number']
                street = request.form['street']
                barangay = request.form['barangay']
                contact = request.form['contact']
                violation = request.form['violation']
                penalty = request.form['penalty']
                
            conn.execute('UPDATE violators SET first_name=?, middle_name=?, house_number=?, street=?, barangay=?, contact=?, violation=?,  penalty=? WHERE last_name = ?',( first_name, middle_name, house_number, street, barangay, contact, violation, penalty, last_name))
            conn.commit()
            conn.close()
            
            flash('"{}" was successfully edited!'.format(last_name))
            return redirect(url_for('accounting'));
        return render_template('response.html',accounting=accounting,payy=payy,total=total,accvl=accvl,violations=violations,stat=stat)

@app.route('/<table>/<username>/edit_account', methods=('GET','POST'))
def edit_account(table,username):
    conn = get_db_connection()
    if table == "mmacc":
        mmacc = conn.execute('SELECT * FROM user WHERE username = ?',(username,)).fetchone()
        if request.method == "POST":
            updated_name = request.form['username']
            existing_account = conn.execute('SELECT * FROM user WHERE username != ? AND username = ?',(username,updated_name)).fetchone()
            if existing_account:
                flash('Account {} Already exist!'.format(updated_name))
                return redirect(url_for('edit_account',table="mmacc",username=username));
            else:
                
                flash('Account {} Successfully Edited!'.format(updated_name))
                username = updated_name
                
                username = request.form['username']    
                password = request.form['password']
                mail = request.form['mail']
                position = request.form['position']
                barangay = request.form['barangay']
                action = 'Edit Account'
                address = 'Municipal'
                mail = request.form['mail']
                conn.execute('UPDATE user SET username=?, password=?, mail=?, position=?, barangay=? WHERE username=?',(updated_name, password, mail, position, barangay, username))
                conn.execute('INSERT INTO logs (username, action, address) VALUES (?,?,?)', (username, action, address))
                conn.commit()
                conn.close()
                return redirect(url_for('admin_account'));
        return render_template('edit_admin_account.html', mmacc=mmacc);
    
@app.route('/<table>/<date>/<address>/delete_logs', methods=('GET','POST'))
def delete_logs(table,date,address):
    
    conn = get_db_connection()
    if table == "bblogs":
        conn.execute('DELETE FROM logs WHERE date = ? and address=?', (date,address,))
        conn.commit()
        conn.close()
        flash('Successfully Removed!'.format())
        return redirect(url_for('bancabanca_logs'));

@app.route("/bancabanca_guidelines", methods=['GET','POST'])
def bancabanca_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("bancabanca_guidelines.html",data=data)

@app.route("/daniw_guidelines", methods=['GET','POST'])
def daniw_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("daniw_guidelines.html",data=data)

@app.route("/masapang_guidelines", methods=['GET','POST'])
def masapang_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("masapang_guidelines.html",data=data)

@app.route("/nanhaya_guidelines", methods=['GET','POST'])
def nanhaya_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("nanhaya_guidelines.html",data=data)

@app.route("/pagalangan_guidelines", methods=['GET','POST'])
def pagalangan_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("pagalangan_guidelines.html",data=data)

@app.route("/sanbenito_guidelines", methods=['GET','POST'])
def sanbenito_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("sanbenito_guidelines.html",data=data)

@app.route("/sanfelix_guidelines", methods=['GET','POST'])
def sanfelix_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("sanfelix_guidelines.html",data=data)

@app.route("/sanfrancisco_guidelines", methods=['GET','POST'])
def sanfrancisco_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("sanfrancisco_guidelines.html",data=data)

@app.route("/sanroque_guidelines", methods=['GET','POST'])
def sanroque_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    return render_template("sanroque_guidelines.html",data=data)

@app.route("/municipal_guidelines",methods=['GET','POST'])
def municipal_guidelines():

    con = sqlite3.connect("myimage.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from image")
    data = cur.fetchall()
    con.close()

    if request.method=='POST':
        upload_image=request.files['upload_image']

        if upload_image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            con=sqlite3.connect("myimage.db")
            cur=con.cursor()
            cur.execute("insert into image(img)values(?)",(upload_image.filename,))
            con.commit()
            flash("File Upload Successfully","success")

            con = sqlite3.connect("myimage.db")
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("select * from image")
            data=cur.fetchall()
            con.close()
            return render_template("municipal_guidelines.html",data=data)
    return render_template("municipal_guidelines.html",data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=sqlite3.connect("myimage.db")
        cur=con.cursor()
        cur.execute("delete from image where pid=?",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("municipal_guidelines"))
        con.close()

@app.route('/<table>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<total_penalty>/<date>/<status>/cancel', methods=('GET','POST'))
def cancel(table,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty,total_penalty, date, status):
    conn = get_db_connection()
    stat = conn.execute('SELECT status FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
    if table == "bbup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('bancabanca_service'));
    else:
        status = "Pending"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('bancabanca_service'));
        
    return redirect(url_for('bancabanca_service'));

@app.route('/<table>/<id>/<last_name>/<first_name>/<middle_name>/<house_number>/<street>/<barangay>/<contact>/<violation>/<penalty>/<total_penalty>/<date>/<status>/update', methods=('GET','POST'))
def update(table,id,last_name,first_name,middle_name,house_number, street, barangay, contact, violation, penalty,total_penalty, date, status):
    conn = get_db_connection()
    stat = conn.execute('SELECT status FROM violators WHERE last_name = ? and first_name = ? and middle_name = ? and penalty = ?',(last_name,first_name,middle_name,penalty,)).fetchone()
    if table == "dup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('daniw_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE id = ?', (status, id,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('daniw_service'));
        
    return redirect(url_for('daniw_service'));


    if table == "bbup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('daniw_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('bancabanca_service'));
        
    return redirect(url_for('daniw_service'));

   

    if table == "mup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('masapang_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('masapang_service'));
        
    return redirect(url_for('masapang_service'));

    if table == "nup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('nanhaya_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('nanhaya_service'));
        
    return redirect(url_for('nanhaya_service'));

    if table == "pup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('pagalangan_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('pagalangan_service'));
        
    return redirect(url_for('pagalangan_service'));

    if table == "sbup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('sanbemito_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('sanbemito_service'));
        
    return redirect(url_for('sanbemito_service'));

    if table == "fup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('sanfelix_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('sanfelix_service'));
        
    return redirect(url_for('sanfelix_service'));

    if table == "sfup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('sanfrancisco_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('sanfrancisco_service'));
        
    return redirect(url_for('sanfrancisco_service'));

    if table == "srup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('sanroques_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('sanroques_service'));
        
    return redirect(url_for('sanroques_service'));

    if table == "mmup" and stat == "Done":
        
        flash('"{}" Already done!'.format(last_name))
        return redirect(url_for('municipal_service'));
    else:
        status = "Done"
        
        conn.execute('update violators set status=? WHERE last_name = ?', (status, last_name,))
        conn.commit()
        conn.close()
        flash('"{}" was done!'.format(last_name))
        return redirect(url_for('municipal_service'));
        
    return redirect(url_for('municipal_service'));

@app.route('/<table>/<contact>/<last_name>/sendsms', methods=('GET','POST'))
def sendsms(table,contact,last_name):
    if table == "sms":
        client.messages.create(
    
        to="+63"+contact,
        from_="+15074804294",
        body="Hi," +last_name+"! We would like to remind you that you have violations and penalties to pay. Kindly settle this in accounting of Municipality of Victoria, Laguna"
        )
        flash('Successfully notified "{}"!'.format(last_name))
    return redirect(url_for('accounting'));

app.run(debug = True)
db.create_all()
