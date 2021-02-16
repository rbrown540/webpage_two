# 
# 
from flask import Flask, render_template, request, redirect
import datetime
import pandas as pd
import csv
import re
login_count = 0

app = Flask(__name__)


@app.route('/')
def home():
    """  """
    return render_template('LogInForm.html')


@app.route('/get_login_data', methods=['POST', 'GET'])
def get_login_data():
    """  """
    user_name = request.form['userName']
    pass_word = request.form['passWord']
    
    if 'poop' == validate_login(user_name, pass_word):
        return change_form()
    else:
        return redirect('/')


def validate_login(username, password):
    """ Used to validate user name and user password against a file """
    global login_count
    uname_pwd_df = pd.read_csv('username_password.csv')
    upassword_prev = pd.read_csv('username_password_previous.csv')
    # uname_pwd_df.columns = ['USERNAME', 'PASSWORD']
    # print(uname_pwd_df)
    if username in uname_pwd_df.values and password in uname_pwd_df.values:
        if password in upassword_prev.values:
            login_count += 1
            print('login count: ', login_count)
            if login_count == 15:
                exit()
            return redirect('/')
        else:
            login_count = 0
            return 'poop'
    else:
        login_count += 1
        print('login count: ', login_count)
        if login_count == 15:
            exit()
        return redirect('/')


@app.route('/change_form')
def change_form():
    """  """
    return render_template('ChangePassWord.html')


@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    """  """
    user_name = request.form['userName']
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    new_password_again = request.form['new_password_again']
    nogo_prev_pwd = pd.read_csv('username_password_previous.csv')
    nogo_pwd = pd.read_csv('Untitled.txt')
    uname_pwd_df = pd.read_csv('username_password.csv')

    if new_password == new_password_again:
        if new_password in nogo_pwd.values:
            print('that is a common passowrd')
            redirect('/change_form')
        elif new_password in nogo_prev_pwd.values:        
            print("that's a previous password yo")
            redirect('/change_form')
        else:
            with open('username_password.csv', 'a') as fix_it:
                writer = csv.writer(fix_it)
                writer.writerow([user_name, new_password])
            print(uname_pwd_df)
            previous_passwords(current_password)
            return render_template('StarWars.html')

    
def previous_passwords(current_pwd):
    with open('username_password_previous.csv', 'a') as prev_csv:
        writer = csv.writer(prev_csv)
        writer.writerow([current_pwd])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080)


