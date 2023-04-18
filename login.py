from flask import Flask,redirect, url_for,jsonify
from flask_restful import Resource, Api
#from resources import BoardResource
from flask_httpauth import HTTPBasicAuth
from configparser import ConfigParser
app = Flask(__name__)
#api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()
#USER_DATA = {
#	"user": "pwd"
#}
def get_USER_DATA():
    try:
        parser = ConfigParser()
        config_file_path = 'c:/path/db_config.ini'  # full absolute path here!
        parser.read(config_file_path)
        userdata = {}
        if parser.has_section("as"):
            items = parser.items("as")
            for item in items:
                userdata[item[0]] = item[1]
        else:
            print("Error in read ConfigParser")
        #print(userdata)
        return userdata   
    except Exception as e:
        raise Exception(e)

#route to verify the password
@auth.verify_password
def verify(username, password):
    cred=get_USER_DATA()
    if (not(username) or not(password)) or (username==None or password == None):
        return False
    elif username in cred['username'] and password in (cred['password']):
        return True
    else:
        return False

    
'''	if not(username) and not(password):
		return False
	cred=get_USER_DATA()
	return cred['password'] == password'''
     


@app.route('/private')
@auth.login_required
def private_page():
    return redirect(url_for('foo'))
    #return "Only for authorized people!"

'''@app.route('/private')
#class PrivateResource(Resource):
@auth.login_required
def get():
		#return redirect('foo')
        return redirect(url_for('foo'))
	    #return {"Success" : "OK"}'''

@app.route('/foo', methods=['GET','POST'])
def foo():
	stderr = "hey its inside foo"
	return stderr

#api.add_resource(PrivateResource, '/private')
if __name__ == '__main__':
	app.run(debug=True,port =2000)
