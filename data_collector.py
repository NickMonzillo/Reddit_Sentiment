import praw
from datetime import datetime
from json import dumps
'''
class Comment(object):
    #Represents a comment on Reddit.
    def __init__(self,body,score,created,id_num):
        Initializes a Comment object.
        self.body = body
        self.score = score
        self.created = fromtimestamp(created)
        self.id_num = id_num
        
    def form_json(self):
        #Returns a dictionary of comment information.
        json_dict = {'body':self.body,
                     'score':self.score,
                     'created':self.created,
                     'id':self.id_num}
        return json_dict
'''

class Collector(object):
    '''Collects comments from Reddit using PRAW.'''
    def __init__(self):
        '''Initializes the Collector object.'''
        self.session = praw.Reddit('windows:comment_sentiment_analyzer:v0.1')
        self.to_push = []
        self.placeholder = None
            
    def grab_data(self,subreddit='all',limit=100):
        '''Grabs an iterable of comments.'''
        return self.session.get_comments(subreddit,limit=limit,place_holder=self.placeholder)

    #def convert_comment(self,comment):
    #   '''Converts a Reddit Comment object to a native Comment object.'''
    #  return Comment(comment.body,comment.score,comment.created_utc,comment.id)

    def form_json(self,comment):
        '''Returns a dictionary of comment information.'''
        json_dict = {'body':comment.body,
                     'score':comment.score,
                     'date':datetime.fromtimestamp(comment.created_utc).strftime('%x'),
                     'time':datetime.fromtimestamp(comment.created_utc).strftime('%X'),
                     'id':comment.id}
        return dumps(json_dict)
    
    def parse_data(self,comment_iter):
        '''Parses an iterable of comments and appends the Comment objects to self.to_push'''
        last = None
        for comment in comment_iter:
            self.to_push.append(self.form_json(comment))
            last = comment
        self.placeholder = last.id

    #def find_placeholder(self,num_placeholders=3):
     #   return self.to_push[-1]['id']

class Pusher(Collector):
    '''Pushes data from Collector class into a database.'''
    def __init__(self):
        '''Initializes the Pusher object.'''
        while 1:
            #Initialize an infinite loop to keep running forever
            self.collect_data(self.placeholder)
            self.push_db()
    
    def collect_data(self,placeholder_id):
        '''Collects and parses comment data.'''
        data = self.grab_data()
        self.parse_data(data)
        
    def push_db(self):
        #insert code here to push to db
        #Insert self.to_push
        self.to_push = []
        return None
        
c = Collector()
data = c.grab_data(limit=3)
c.parse_data(data)
print c.to_push
print c.placeholder





