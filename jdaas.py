import csv
import random
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)
app.debug = True

def readCSVtoList(csvname, arrayname):
    with open(csvname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            arrayname.append(row)

@app.route('/')
def welcome():
    return render_template('jdaas_index.html')
# """
#    Welcome to Jeff Dean as a Service- A RESTful solution for having Jeff Dean solve all of your problems. Now, us mere mortals outside of the GooglePlex can experience the awesomeness of Jeff at scale.
#    
#    In version 1, we have 3 API calls available: 
#    -/jokes     returns a Jeff Dean joke
#    -/advice    get some advice from Jeff
#    -/numbers   returns numbers Jeff thinks you should know
#    setup https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7
#    ssl https://certbot.eff.org/instructions?ws=nginx&os=ubuntuother
#    try_files $uri $uri/ was problem in  sudo nano /etc/nginx/sites-available/default
#    restart after changes sudo systemctl restart helloworld
#    """

@app.route('/slack', methods=['POST'])
def SlackResponse():
    jd_action = request.form.get('text')

    resp_type = 'in_channel'

    if jd_action == 'numbers':
        resp = numbersEveryEngineerShouldKnow()
    elif jd_action == 'advice':
        resp = JeffAdvice()
    elif jd_action == 'joke':
        resp = JdJokes()
    else: 
        resp = 'Sorry you must enter joke, advice or numbers. (only you can see this message)'
        resp_type = 'ephemeral'

    return jsonify(response_type= resp_type, text= resp)


@app.route('/jokes', methods=['GET'])
def JdJokes():

    joke_array = []
    readCSVtoList('/Users/alexlegault/Documents/GitHub/jdaas/jeffdeanjokes.csv', joke_array)

    return random.choice(joke_array)[0]



@app.route('/advice', methods=['GET'])
def JeffAdvice():

    advice_array = []
    readCSVtoList('/home/ubuntu/jdaas/jeffdeanadvice.csv', advice_array)

    return random.choice(advice_array)[0]



@app.route('/numbers', methods=['GET'])
def numbersEveryEngineerShouldKnow():

    numbers_array = []
    readCSVtoList('/home/ubuntu/jdaas/importantnumbers.csv', numbers_array)

    return random.choice(numbers_array)[0]

@app.errorhandler(500)
def internalServerError(e):
    return "Sorry, server error (500). Our server is probably busy running one of Jeff Dean's MapReduce jobs. please try again later"

if __name__ == '__main__':
    app.run()
  
