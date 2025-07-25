from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv 
import os

UPLOAD_FOLDER = 'static/images/work'
ALLOWED_EXTENSIONS = {'png', 'jpeg'}

app = Flask(__name__)
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Strict')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_next_id(file):
    id = 1
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        reader = list(csv.reader(csv_file))
        if len(reader) > 1:
            last_row = reader[-1]
        if last_row:
            id += int(last_row[0])
    return id
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Strict')

def get_next_id(file):
    id = 1
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        reader = list(csv.reader(csv_file))
        if len(reader) > 1:
            last_row = reader[-1]
        if last_row:
            id += int(last_row[0])
    return id

@app.route("/")
def show_index():
    return render_template("index.html")

@app.get('/add_work')
def index():
    return  render_template('add_work.html')

@app.get('/add_subscription')
def add_subscription():
    return render_template('add_subscription.html')

@app.post('/add_subscription')
def subscription_form():
    return redirect(url_for('works'))

@app.post('/add_work')
def add_work():
    id = get_next_id('works.csv')
    
    work_name=request.form.get('work_name')

    original_work_date=request.form.get('work_date')
    work_date= datetime.strptime(original_work_date, "%Y-%m-%d")

    work_date = work_date.strftime("%m/%d/%Y")

    work_description=request.form.get('work_description')
    work_requirements=request.form.get('work_requirements')
    work_address=request.form.get('work_adress')

    image = request.files.get('image')
    image_path = None

    if image and allowed_file(image.filename):
        extension = image.filename.rsplit('.', 1)[1].lower()
        filename = f"{id}.{extension}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        
        image_path = f"images/work/{filename}"


    new_work=[
        id,
        work_name,
        work_description,
        work_requirements,
        work_date,
        work_address,
        image_path
    ]

    with open("works.csv", mode="a", encoding="utf-8", newline="") as csv_file:
        writer=csv.writer(csv_file)
        writer.writerow(new_work)

    return redirect(url_for('works'))

def delete_work():
    pass

@app.route("/sign_up")
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html', failed=False)
    else:
        with open("users.csv", mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["username"] == request.form["username"]:
                    return render_template('sign_up.html', failed=True)
        
        id = get_next_id('users.csv')
        username = request.form["username"]
        password = request.form["password"]

        with open("users.csv", mode="a", encoding="utf-8") as csv_file:
            csv_writer = csv.DictWriter(csv_file)
            csv_writer.writerow({'id': id, 'username': username, 'password': password})
                
        return redirect(url_for("index")).set_cookie("login", f"{username}|{password}", max_age=60*60*24)

@app.route("/sign_in")
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html', failed=False)
    else:
        with open("users.csv", mode="r", encoding="utf-8") as csv_file:
            username = request.form["username"]
            password = request.form["password"]

            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["username"] == username and row["password"] == password:
                    return redirect(url_for("index")).set_cookie("login", f"{username}|{password}", max_age=60*60*24)
                
        return render_template('sign_in.html', failed=True)

@app.route("/work")
def works():
    work_places = []
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            work_places.append(row)

    return render_template("works.html", work_places=work_places)

@app.route("/work/<int:id>")
def work(id):
    work_place = {}
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row["id"]) == id:
                work_place = row
                break


    return render_template("work.html", work_place=work_place)

@app.route("/map")
def map():
    work_places = []
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            work_places.append(row)

    return render_template("map.html", work_places=work_places)

if __name__ == "__main__":
    app.run(debug=True)