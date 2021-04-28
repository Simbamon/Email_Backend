from flask import Flask, request
from flask_mail import Mail, Message

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

if __name__ == '__main__':
    app.run()