from flask import Flask, request, render_template,flash
import MySQLdb

app = Flask(__name__)
app.secret_key = 'vologuessectretstring'

@app.route('/')
def success():
   return render_template("index.html")

@app.route('/login',methods = ['POST','GET'])
def login():
    user = request.args.get('nm')
    passw=request.args.get('pass')
    con = MySQLdb.connect("localhost", "root", "toor", "stud")
    cur = con.cursor()
    que = '''select * from students where Name ="%s"''' % (user)
    if(user=='admin' and passw=='admin'):
        cur.execute("select * from students")
        rows=cur.fetchall()
        return render_template("admin.html", i=rows)
        con.close()

    else:
        cur.execute(que)
        result=cur.fetchall()
        if result==():
            flash('INVALID LOGIN!')
            return render_template("index.html")
        if result[0][5]==passw:
            return render_template('student.html',row=result[0])
            con.close()
        else:
            flash('INVALID LOGIN!')
            return render_template("index.html")

@app.route('/update',methods = ['POST','GET'])
def update():
    if request.method == 'POST':

        name = request.form['name']
        sub1 = request.form['sub1']
        sub2 = request.form['sub2']
        sub3 = request.form['sub3']
        sub4 = request.form['sub4']
        con = MySQLdb.connect("localhost", "root", "toor", "stud")
        cur=con.cursor()
        que="UPDATE students SET  sub1= '%d', sub2= '%d',sub3= '%d', sub4= '%d' WHERE Name = '%s'" %(int(sub1), int(sub2), int(sub3), int(sub4), name)
        try:
            cur.execute(que)
            con.commit()
            flash('Update Successful')
        except:
            flash('Error')
    cur.execute("select * from students")
    rows = cur.fetchall();
    con.close()
    return render_template("admin.html", i=rows,na=name)

@app.route('/register', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            pas = request.form['pass']
            v=0
            con = MySQLdb.connect("localhost", "root", "toor", "stud")
            cur = con.cursor()
            cur.execute("INSERT INTO students (sub1,sub2,sub3,sub4,Name,pass)VALUES('%d', '%d', '%d', '%d', '%s', '%s')" % (v,v,v,v,nm,pas) )
            con.commit()
        except:
            con.rollback()
            flash('Rgistration Unsuccesfull')
            return render_template("index.html")


        finally:
            flash('Registration Successful')
            return render_template("index.html")

if __name__ == '__main__':
   app.run(debug = True)