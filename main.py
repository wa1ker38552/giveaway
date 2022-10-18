from flask import render_template
from datetime import datetime
from scraper import Scraper
from flask import redirect
from flask import request
from flask import Flask
import datetime as dt


app = Flask(__name__)
scraper = Scraper()

def sort(query):
  # sort query
  for i in range(len(query)):
    for j in range(len(query)-1):
      if query[j]['prediction'] < query[j+1]['prediction']:
        save = query[j]
        query[j] = query[j+1]
        query[j+1] = save
  return query

def generate_prediction(query):
  for i, post in enumerate(query):
    prediction = 0
    prediction += post['retweets']
    prediction += post['author']['followers']-(post['author']['following']/2)
    query[i]['prediction'] = round(prediction*0.1, 3)

    # convert time aswell
    time = datetime.strptime(post['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
    now = datetime.now()

    query[i]['created_ago'] = str(dt.timedelta(seconds=(now-time).total_seconds())).split(':')
  return query

def query(query):
  query = scraper.query(query)
  query = generate_prediction(query)
  return sort(query)

@app.route('/')
def home():
  if request.args.get('type') is None:
    data = query('giveaways')
  else:
    data = query(f'{request.args.get("type")} giveaways')
    
  return render_template('index.html', data=data)

@app.route('/api/search', methods=['POST'])
def search():
  return redirect(f'/?type={request.form["query"]}', code=302)


app.run(host='0.0.0.0', port=8080)
