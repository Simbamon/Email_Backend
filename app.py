from flask import Flask, json
from flask_mail import Mail, Message
import requests
import json

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "sbhan9511@gmail.com"
app.config['MAIL_PASSWORD'] = ""
app.config['MAIL_DEFAULT_SENDER'] = ('customname', 'sbhan9511@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/sendemail')
def index():
    
    # data = request.get_json()
    # email = data['email']
    # picture = data['picture']

    msg = Message('Hello there')
    msg.add_recipient('sbhan9511@gmail.com')
    msg.body = 'This is the body with'
    
    with app.open_resource('picture.jpg') as picture:
        msg.attach('custom.jpg', 'image/jpeg', picture.read())

    mail.send(msg)
    return "Success" 

@app.route('/gettoken')
def token():
    url = "https://kauth.kakao.com/oauth/token"

    token_data = {
        "grant_type" : "authorization_code",
        "client_id" : "",
        "redirect_uri" : "http://127.0.0.1:5000/sendkakao",
        "code" : ""
        
    }
    response = requests.post(url, data=token_data)

    tokens = response.json()

    print(tokens)

    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)

    return "successfully generated token"

@app.route('/sendkakao')
def send_k():

    with open("kakao_token.json", "r") as fp:
        access_token = json.load(fp)

    print(access_token['access_token'])
    headers = {'Authorization': 'Bearer ' + access_token['access_token']}
    data = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "Hello, world!",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
        })
    }

    response = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send", headers=headers, data=data)
    
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('Success')
    else:
        print('Error: ' + str(response.json()))

    return "sucessfully sent message"

if __name__ == '__main__':
    app.run()