from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',  # MySQL 用户名
    'password': '123456',  # MySQL 密码
    'database': 'flask_login_db'
}

# 创建数据库连接
def get_db_connection():

    conn = MySQLdb.connect(**db_config)
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 验证用户名和密码
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[2] == password:  # user[2] 是密码列
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            error = "Invalid username or password."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    return render_template('welcome.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        # 将新用户添加到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            return redirect(url_for('login'))
        except MySQLdb.IntegrityError:
            error = "Username already exists."
            return render_template('register.html', error=error)
        finally:
            conn.close()

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
