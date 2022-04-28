from flask import Flask,session,render_template,redirect,request
import sqlite3
import os
import threading
import time
file_path = "./static/images/"
app = Flask(__name__)

# upload
@app.route('/upload',methods=["GET","POST"])
def upload():
	if(request.method=="POST"):
		conn = sqlite3.connect('data.db')
		con= conn.cursor()
		name = request.form['name']
		email = request.form['email']
		file = request.files['file']
		contact = request.form['contact']
		color = request.form['color']
		work = request.form['work']
		address = request.form['address']
		age = request.form['age']
		# gender = request.form['gender']
		gender = "male"
		conn.execute("CREATE TABLE if not exists data(sno INTEGER not null unique,name TEXT not null,email text unique,contact text unique,age INTEGER , work TEXT ,color text,gender text not null,address TEXT ,file BLOB not null unique ,filename not null,PRIMARY KEY(sno AUTOINCREMENT) )")
		res = conn.execute(f"SELECT * FROM data where email='{email}' or contact='{contact}' ")
		if(res.fetchall()):
			con.close()
			return render_template('upload.html',error='data exists.',error_class='error') 
		else:
			insert_table = "INSERT INTO data(name,email,contact,age,work,color,gender,address,file,filename) VALUES (?,?,?,?,?,?,?,?,?,?)"
			if(name==''):
				con.close()
				return render_template('upload.html',error='please enter name ?',error_class='error')
			if(gender==""):
				con.close()
				return render_template('upload.html',error='please select gender ?',error_class='error')
			if(file==''):
				con.close()
				return render_template('upload.html',error='please choose file ?',error_class='error')
			file.save(f"{file_path}{file.filename}")
			files = open(f"{file_path}{file.filename}",'rb')
			file_data = files.read()
			insert_data =(name,email,contact,age,work,color,gender,address,file_data,file.filename)
			conn.execute(insert_table,insert_data)
			con.close()
			conn.commit()
			os.system("cd static/images && rm * ")
			return render_template('upload.html',success='successfully upload .',success_class='success')

	return render_template('upload.html')

# home
@app.route("/")
def home():
	conn = sqlite3.connect('data.db')
	con = conn.cursor()
	t1 = threading.Thread(target=remove_image,args=(1,))
	t1.start()
	img = conn.execute("SELECT * FROM data")
	for x in img:
		file = open(f"{file_path}{x[10]}","wb")
		file.write(x[9])
	data = conn.execute("SELECT * FROM data")
	con.close()
	return render_template('index.html',data=data)


def remove_image(value):
	time.sleep(10)
	os.system("cd static/images/ && rm *")
app.run(debug=True)