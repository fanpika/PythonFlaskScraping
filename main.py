from flask import Flask, render_template, request, redirect, send_file
from scrapper.scrapper import scrape
from exporter import save_to_file

app = Flask("FlaskScrapper")

db = {}

# https://Nomad-Python-Flask-Scrapper.fanpika.repl.co
@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  # request.args : Dictionary
  word = request.args.get("word", "").lower()
  if word == "":
    return redirect("/")
  from_db = db.get(word)
  if from_db:
    jobs = from_db
  else:
    jobs = scrape(word)
    db[word] = jobs
  
  print(len(jobs))

  return render_template(
    "report.html", 
    searchingBy = word,
    resultsNumber = len(jobs),
    jobs=jobs
    )

@app.route("/export")
def export():
  try:
    word = request.args.get("word", "").lower()
    if word == "":
      raise Exception()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file(
      "jobs.csv", 
      mimetype='application/x-csv',
      attachment_filename='jobs.csv',
      as_attachment=True
      )
  except:
    return redirect("/")
  

# repl.it : host="0.0.0.0"
app.run(host="0.0.0.0")