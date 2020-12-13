from flask import Flask, request, render_template
import pandas as pd #importation of pandas for cleaning the dataset
import os 
import csv
import numpy as np
import pandas as pd
import random
import time
from tweet import Tweet   

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary

REQUESTS = Counter('flask_redis_app_access_total','How many times the application has been accessed')
EXECPTIONS = Counter('flask_redis_app_exeptions_total','How many times the application issued an execption')

INPROGRESS = Gauge('flask_redis_app_inprogress','How many request the app are currently in progress')
LAST= Gauge('flask_redis_app_access_gauge','When was the application last accessed')

LATENCY = Summary('flask_redis_app_lattency_seconds','time needed for a request')
app = Flask(__name__)

df = pd.read_csv("./Data/tweets.csv")#path of the file 
df =df.drop(["link","Unnamed: 0","id"],axis=1)#we remove the column with no interest
df.apply(lambda x: x.astype(str).str.lower())#just lower all the carachter that's better for the model
df.head(10)#display the 10 first row this line can be delete that's was just to check...

vectorizer = TfidfVectorizer()# Get tf-idf matrix using fit_transform function

X = vectorizer.fit_transform(df['text']) # Store tf-idf representations of all docs

@app.route('/', methods=['GET', 'POST'])
def index():
    REQUEST.inc()
    with EXECPTIONS.count_exceptions:
        if random.random() < 0.2:
            raise Exception
    LAST.set(time.time())
    INPROGRESS.inc()
    start = time.time()
    time.sleep(2)

    if request.method == 'POST':
        query = request.form['query']
        query_vec = vectorizer.transform([query]) #(n_docs,x),(n_docs,n_Feats)
        results = cosine_similarity(X,query_vec).reshape((-1,)) #Cosine Sim with each doc
        tweets = []
        for i in results.argsort()[-20:][::-1]:
            tweets.append( Tweet(df.iloc[i,0], df.iloc[i,2],df.iloc[i,3]))

        return render_template('Home.html', query=query, tweets=tweets)
    INPROGRESS.dec()
    LATENCY.observe(time.time() - start)
    return render_template('Home.html')
    

if __name__ == '__main__':
    start_http_server(8010)
    app.run(host='0.0.0.0')
