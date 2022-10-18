import requests
import os

class Scraper:
  def __init__(self, auth_key='AUTH'):
    self.client = requests.Session()
    self.client.headers = {'Authorization': f'Bearer {os.environ[auth_key]}'}

  def query(self, query):
    data = []
    request = self.client.get(f'https://api.twitter.com/2/tweets/search/recent?query={query} -is:retweet&max_results=50&expansions=author_id&tweet.fields=created_at,public_metrics&user.fields=name,public_metrics')
    request = request.json()

    try:
      request['data']
    except KeyError: return []
    
    for i, post in enumerate(request['data']):
      if 'giveaway' in post['text']:
        if len(post['text'].split()) > 12:
          text = ' '.join(post['text'].split()[:12])+'...'
        else:
          text = post['text']

        try:
          author = {
            'followers': request['includes']['users'][i]['public_metrics']['followers_count'],
            'following': request['includes']['users'][i]['public_metrics']['following_count'],
            'tweets': request['includes']['users'][i]['public_metrics']['tweet_count']
          }
        except IndexError:
          author = {'followers': 0, 'following': 0, 'tweets': 0}

        try: display = request['includes']['users'][i]['name']
        except IndexError: display = None

        try: username = request['includes']['users'][i]['username']
        except IndexError: username = None
          
        data.append({
          'id': post['id'],
          'created': post['created_at'],
          'text': text,
          'retweets': post['public_metrics']['retweet_count'],
          'reply_count': post['public_metrics']['reply_count'],
          'likes': post['public_metrics']['like_count'],
          'display': display,
          'username': username,
          'author': author
        })
    return data
    
