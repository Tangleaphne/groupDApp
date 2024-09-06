from flask import Flask,render_template,request
import sqlite3
import datetime

app=Flask(__name__)

@app.route('/',methods=["get","post"])
def index():
    return render_template('index.html')

@app.route('/backmain',methods=["get","post"])
def backmain():
    return render_template('index.html')

@app.route('/issue',methods=["get","post"])
def issue():
    return render_template('Issue.html')

@app.route('/verify',methods=["get","post"])
def verify():
    return render_template('Verify.html')

@app.route('/detail',methods=["get","post"])
def detail():
    return render_template('Detail.html')

@app.route('/gallery',methods=["get","post"])
def gallery():
    return render_template('Gallery.html')

if __name__=='__main__':
    app.run()

