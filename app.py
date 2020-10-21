from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flaskinfos'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM infos')
    data = cur.fetchall()
    cur.close()
    return render_template('main.html', infos=data)

@app.route('/add/')
def add():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM infos')
    data = cur.fetchall()
    cur.close()
    return render_template('add-infos.html')

@app.route('/add_infos', methods=['POST'])
def add_infos():
    if request.method == 'POST':
        id_number = request.form['id_number']
        fullname = request.form['fullname']
        course = request.form['course']
        year_level = request.form['year_level']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM infos WHERE id_number = %s', (id_number,))
        checker = cur.fetchone()
        if checker:
            flash('THIS INFO ALREADY EXISTS')
            return redirect(url_for('Index'))
        else:
            cur.execute("INSERT INTO infos (id_number, fullname, course, year_level, email) VALUES (%s,%s,%s,%s,%s)", (id_number, fullname, course, year_level, email))
            mysql.connection.commit()
            flash('infos Added successfully')
            return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_infos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM infos WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-infos.html', infos = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_infos(id):
    if request.method == 'POST':
        id_number = request.form['id_number']
        fullname = request.form['fullname']
        course = request.form['course']
        year_level = request.form['year_level']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE infos
            SET id_number = %s,
                fullname = %s,
                course = %s,
                year_level = %s,
                email = %s        
            WHERE id = %s
        """, (id_number, fullname, course, year_level, email, id))
        flash('Infos Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_infos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM infos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Infos Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == '__main__':
    app.run(host="localhost", port=3306, debug=True)
