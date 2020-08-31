from flask import Flask
from rq import Queue
from worker import conn

app = Flask(__name__)

q = Queue(connection=conn)

from app import views


# Worker
from app.utils import count_words_at_url
result = q.enqueue(count_words_at_url, 'https://www.fastbreakdata.com')
