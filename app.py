from flask import Flask,render_template,request
import sqlite3
import datetime
import requests

app=Flask(__name__)

@app.route('/',methods=["get","post"])
def index():
    return render_template('index.html')

@app.route('/role',methods=["get","post"])
def role():
    r = request.form.get("q")
    return render_template('Role.html', r=r)

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

@app.route('/store-credential', methods=["POST"])
def store_credential():
    data = request.get_json()
    credentialHash = data.get('credentialHash')
    fileLink = data.get('fileLink')

    if not credentialHash or not fileLink:
        return {"message": "Missing data"}, 400

    # 下载 PDF 文件并获取其二进制内容
    try:
        response = requests.get(fileLink)
        response.raise_for_status()  # 检查请求是否成功
        pdf_data = response.content  # PDF 的二进制内容
        
        # 将 credentialHash 和 pdf_data 存入数据库
        conn = sqlite3.connect('user.db')
        with conn:
            conn.execute('insert into credentialHash2pdf (hash, pdf_data) VALUES (?, ?)', 
                         (credentialHash, pdf_data))
        conn.close()
        print("success")
        return {"message": "Credential stored successfully"}, 200

    except requests.RequestException as e:
        return {"message": f"Error downloading file: {str(e)}"}, 500

@app.route('/verify',methods=["get","post"])
def verify():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Verify.html', role=role, r=r)

@app.route('/detail',methods=["get","post"])
def detail():
    role = request.form.get("role")
    r = request.form.get("q")

    credential_hash = request.args.get('credentialHash')
    holder_address = request.args.get('holderAddress')

    return render_template('Detail.html', role=role, r=r, credentialHash=credential_hash, holderAddress=holder_address)

@app.route('/gallery',methods=["get","post"])
def gallery():
    role = request.form.get("role")
    r = request.form.get("q")
    return render_template('Gallery.html', role=role, r=r)

@app.route('/get-pdf/<credential_hash>', methods=["GET"])
def get_pdf(credential_hash):
    # 从数据库获取 PDF 数据
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("select pdf_data from credentialHash2pdf where hash = ?", (credential_hash,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"message": "PDF not found for this credential hash"}, 404

    pdf_data = row[0]
    
    # Return the PDF data as a binary stream
    response = app.response_class(pdf_data, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename={credential_hash}.pdf'
    return response

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

