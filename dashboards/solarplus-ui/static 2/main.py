#main.py
from flask import Flask
import boto3
import boto.ses
from flask import url_for, jsonify, render_template

app = Flask(__name__)

AWS_ACCESS_KEY = 'AKIAJUKTYK6QQG75FWDQ'  
AWS_SECRET_KEY = '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'

class Email(object):  
        def __init__(self, to, subject):
            self.to = to
            self.subject = subject
            self._html = None
            self._text = None
            self._format = 'html'

        def html(self, html):
            self._html = html

        def text(self, text):
            self._text = text

        def send(self, from_addr=None):
            body = self._html

            if isinstance(self.to, basestring):
                self.to = [self.to]
            if not from_addr:
                from_addr = 'webwizards193@gmail.com'
            if not self._html and not self._text:
                raise Exception('You must provide a text or html body.')
            if not self._html:
                self._format = 'text'
                body = self._text

            connection = boto.ses.connect_to_region(
                'us-west-2',
                aws_access_key_id=AWS_ACCESS_KEY, 
                aws_secret_access_key=AWS_SECRET_KEY
            )

            return connection.send_email(
                from_addr,
                self.subject,
                None,
                self.to,
                format=self._format,
                text_body=self._text,
                html_body=self._html
            )

# Create an SNS client
client = boto3.client(
"sns",
aws_access_key_id="AKIAJUKTYK6QQG75FWDQ",
aws_secret_access_key="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",
region_name="us-west-2"
)

@app.route('/')
def index():
    return render_template('contact2.html')


@app.route('/aws', methods=['POST'])
def aws():
    # Send your sms message.
    client.publish(
    PhoneNumber="+15309794654",
    Message="Your Issue Ticket has been received! Thank you! :)"
    )

    email = Email(to='webwizards193@gmail.com', subject='New Issue Ticket Posted!')  
    email.text('This is a text body. Foo bar.')  
    email.html('<html><body>This is an email highlighting the bugs/issues found in our application. <strong>Will be fixed immediately.</strong></body></html>')  # Optional  
    email.send()  

    return jsonify({"message": "done"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)


