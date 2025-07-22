from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv 

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.get('/add_work')
def index():
    return  render_template('add work.html')

@app.post('/add_work')
def add_work():
    id=1
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        reader=list(csv.reader(csv_file))
        if len(reader) > 1:
            last_row = reader[-1]
        if last_row:
            id += int(last_row[0])
    
    work_name=request.form.get('work_name')

    original_work_date=request.form.get('work_date')
    work_date= datetime.strptime(original_work_date, "%Y-%m-%d")

    work_date = work_date.strftime("%m/%d/%Y")

    work_decription=request.form.get('work_description')
    work_adress=request.form.get('work_adress')


    new_work=[
        id,
        work_date,
        work_decription,
        work_adress
        ]

    with open("works.csv", mode="a", encoding="utf-8", newline="") as csv_file:
        writer=csv.writer(csv_file)
        writer.writerow(new_work)

    return redirect(url_for('index'))

@app.route("/work/<int:id>")
def work(id):
    work_place = {}
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row["id"]) == id:
                work_place = row
    print(work_place)

    return render_template("work.html", work_place=work_place)

@app.route("/map")
def map():
    work_places = []
    with open("works.csv", mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            work_places.append(row)
    print(work_places)

    return render_template("map.html", work_places=work_places)

if __name__ == "__main__":
    app.run(debug=True)