# from crypt import methods
from flask import*
from flask import Flask, render_template, url_for, request, session, redirect
import pymongo
import webbrowser

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["employee"]
my_collection = db["login"]

edit_user = 'na'

@app.route("/", methods =["GET", "POST"])
def index():
    # if 'username' in session:
    #     return 'You are logged in as ' + session['username']

    return render_template('sign_in.html')



@app.route('/login', methods=['POST'])
def login():
    users = my_collection
    login_user = users.find_one({'name' : request.form['username']})
    
    
    # for item in my_collection.find():
    #     li.append(item)
        
    
    if login_user:
        if request.form['pass']=="Sujit@1234" and request.form['username']=="Sujit_44":
            
            return render_template('HR.html')
            
            
        elif login_user['password']==request.form['pass']:
            session['username'] = request.form['username']
            users = my_collection
            collect = users.find_one({'name':request.form['username']})
            return render_template('employee.html', group=collect)

    return 'Invalid username/password combination'



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = my_collection
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            user_detail = {'name' : request.form['username'], 'password' : request.form['pass'], 'email': request.form['mail'], 'mobile': request.form['mob']}
            users.insert_one(user_detail)
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route("/Edit_Detail",methods=['POST'])
def edit():
    edit_user = request.form['search']
    un = my_collection.find_one({'name' : edit_user})
    return render_template('edit.html', val=un)
    
@app.route("/change_details",methods=['POST'])
def change():
    if request.method == 'POST': 
        change_s = request.form['schange']
        userval = request.form['user']
        my_collection.update_one({'name':userval},{"$set":{'salary':change_s}})
        found = my_collection.find_one({'name' : userval})
        return render_template('final.html', rec=found)


@app.route("/logout",methods=['GET'])
def logout():
    session["name"] = None
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(debug=True)