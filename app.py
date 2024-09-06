from flask import Flask,render_template,request
import sqlite3
import datetime

app=Flask(__name__)

@app.route('/',methods=["get","post"])
def index():
    return render_template('index.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    role = request.form.get("role")
    r = request.form.get("q")
    current_time = datetime.datetime.now()
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("insert into user values (?, ?, ?)", (role, r, current_time))
    conn.commit()
    c.close()
    conn.close()
    if role == "visitor":
        return render_template('Main.html', role=role, r=r)
    else:
        return render_template('Mainissuer.html', role=role, r=r)

@app.route('/backmain',methods=["get","post"])
def backmain():
    role = request.form.get("role")
    r = request.form.get("q")
    if role == "visitor":
        return render_template('Main.html', role=role, r=r)
    else:
        return render_template('Mainissuer.html', role=role, r=r)

@app.route('/mainadmin',methods=["get","post"])
def mainadmin():
    role = request.form.get("role")
    r = request.form.get("q")
    current_time = datetime.datetime.now()
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("insert into user values (?, ?, ?)", (role, r, current_time))
    conn.commit()
    c.close()
    conn.close()
    return render_template('Mainadmin.html', role=role, r=r)

@app.route('/backmainadmin',methods=["get","post"])
def backmainadmin():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Mainadmin.html', role=role, r=r)

@app.route('/issue',methods=["get","post"])
def issue():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Issue.html', role=role, r=r)

@app.route('/verify',methods=["get","post"])
def verify():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Verify.html', role=role, r=r)

@app.route('/detail',methods=["get","post"])
def detail():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Detail.html', role=role, r=r)

@app.route('/gallery',methods=["get","post"])
def gallery():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Gallery.html', role=role, r=r)

@app.route('/viewDB',methods=["get","post"])
def viewDB():
    role = request.form.get("role")
    r = request.form.get("q")
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    t = ""
    for row in c:
        t += str(row) + "\n"
    conn.commit()
    c.close()
    conn.close()
    return render_template('viewDB.html', t=t, role=role, r=r)

@app.route('/delDB',methods=["get","post"])
def delDB():
    role = request.form.get("role")
    r = request.form.get("q")
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return render_template('deleteDB.html', role=role, r=r)

if __name__=='__main__':
    app.run()

