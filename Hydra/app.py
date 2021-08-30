from flask import Flask, redirect, url_for, render_template, flash, request, session
from api_integration import api_call
from cluster import DominantColors
from cluster import change_image
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData
from datetime import datetime, timedelta
from dateutil import parser
import os
import glob
import time


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hydrapicterra'
app.config['UPLOADED_IMAGES_DEST'] = 'static/images'

db_url = 'sqlite:///sqlite/hydra.db'
db = db = create_engine(db_url)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

uploads_left = 10

@app.route("/")
def home():
    session['loggedin'] = False
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/demos.html")
def demos():
    if not session['loggedin']:
       return redirect(url_for('login'))
    return render_template("demos.html")

@app.route("/sanramon.html")
def sanramon():
    if not session['loggedin']:
       return redirect(url_for('login'))
    return render_template("sanramon.html")

@app.route("/pleasanton.html")
def pleasanton():
    if not session['loggedin']:
       return redirect(url_for('login'))
    return render_template("pleasanton.html")

@app.route("/hayward.html")
def hayward():
    if not session['loggedin']:
       return redirect(url_for('login'))
    return render_template("hayward.html")

@app.route("/login.html", methods=['GET', 'POST'])
def login():
    if session["loggedin"]:
        return redirect(url_for('demos'))
    msg = ''

    today_date = datetime.now()
    print(f'todays date: {today_date}')

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
#        print(username,password)
        with db.connect() as conn:
             select_statement = "SELECT user_id, username, activation_date, trial_length FROM users WHERE username = :username AND user_password = :password"
             results = conn.execute(select_statement, (username, password))
             for account in results:
                print('DB Results:',account)
                if account:
                    print('trial_length: ', account['trial_length'])
                    print('timedelta: ', timedelta(days=account['trial_length']))
                    end_date = parser.parse(account['activation_date']) + timedelta(days=account['trial_length'])
                    print('parse: ', parser.parse(account['activation_date']))
                    print('end date:', end_date)

                    if end_date >= today_date:
                        # Create session data
                        session['loggedin'] = True
                        session['id'] = account['user_id']
                        session['username'] = account['username']
                        # Redirect to home page
                        return redirect(url_for('demos'))
                    else:
                        return render_template('login.html')
                else:
                    # Account doesnt exist or username/password incorrect
                    msg = 'Incorrect username/password!'
                    
    return render_template('login.html', msg='')

@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   # print(session['loggedin'])
#    session.pop('loggedin', None)
   session['loggedin'] = False
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


class MyForm(FlaskForm):
    image = FileField('image')
    

@app.route('/upload.html', methods=['GET', 'POST'])
def upload_file():

    if not session['loggedin']:
       return redirect(url_for('login'))

    print(session["loggedin"])

    username = session['username']

    form = MyForm()

    if form.validate_on_submit():

        with db.connect() as conn:
            
            check_eligibility = "SELECT upload_count, upload_limit FROM users WHERE username = :username"
            elig_val = conn.execute(check_eligibility, username)

            for elig in elig_val:
                if elig['upload_limit']-elig['upload_count']>0:
                    
                    filename = images.save(form.image.data)
                    new_filename = f'static/images/{username}_original.png'
                    print(new_filename)

                    os.rename(f'static/images/{filename}', new_filename)

                    print(os.getcwd())

                    # time.sleep(300)
                    # api_call(username, new_filename)
                    with db.connect() as conn:

                        update_statement = "UPDATE users SET upload_count = upload_count+1 WHERE username = :username"
                        conn.execute(update_statement, username)

                        select_statement = "SELECT upload_count FROM users WHERE username = :username"
                        upload = conn.execute(select_statement, username)

                        find_triallength = "SELECT upload_limit FROM users WHERE username = :username"
                        triallength = conn.execute(find_triallength, username)
                        uplimit=10

                        for length in triallength:
                            if length:
                                uplimit=int(length[0])
                            else:
                                msg = "No limit!"

                        for value in upload:
                            if value:
                                print(int(value[0]))
                                upload_count = int(value[0])
                            else:
                                msg = 'No values!'

                    uploads_left = uplimit-upload_count

                    justgrass_filename = f'static/images/{username}_justgrass.png'

                    print(justgrass_filename)

                    change_image(username, new_filename, justgrass_filename, 6)

                    changed_filename = f'static/images/{username}_changed.png'
                    print(changed_filename)

                    return render_template("upload.html", orig_image = new_filename, new_image = changed_filename, form = form, uploads_left = uploads_left)
                    
                else:
                    return render_template("upload.html", form=form, uploads_left = 0)

    else:

        with db.connect() as conn:
            select_statement = "SELECT upload_count FROM users WHERE username = :username"
            print(select_statement)
            upload = conn.execute(select_statement, username)
            print(upload)

            find_triallength = "SELECT upload_limit FROM users WHERE username = :username"
            triallength = conn.execute(find_triallength, username)
            uplimit=10

            for length in triallength:
                if length:
                    uplimit=int(length[0])
                else:
                    msg = "No limit!"

            for value in upload:
                if value:
                    print(int(value[0]))
                    upload_count = int(value[0])
                else:
                    msg = 'No values!'

            uploads_left = uplimit-upload_count

        return render_template("upload.html", form=form, uploads_left = uploads_left)

        


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port='80')

