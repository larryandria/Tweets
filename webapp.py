from flask import Flask, request, render_template
import pandas as pd #importation of pandas for cleaning the dataset
import os 
import csv
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

df = pd.read_csv("/home/neiltoffa/Documents/project_data_engineering/tweets.csv")#path of the file 
df =df.drop(["link","Unnamed: 0","id"],axis=1)#we remove the column with no interest
df.apply(lambda x: x.astype(str).str.lower())#just lower all the carachter that's better for the model
df.head(10)#display the 10 first row this line can be delete that's was just to check...

vectorizer = TfidfVectorizer()# Get tf-idf matrix using fit_transform function

X = vectorizer.fit_transform(df['text']) # Store tf-idf representations of all docs

print(X.shape) # (dimension of the dataset) you can delete this one too

#query = input()#"I'm the best in the world"query correspond to the query 





@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        query_vec = vectorizer.transform([query]) #(n_docs,x),(n_docs,n_Feats)
        results = cosine_similarity(X,query_vec).reshape((-1,)) #Cosine Sim with each doc
        tweets = []
        for i in results.argsort()[-20:][::-1]:
            tweets.append(df.iloc[i,0]+"---"+df.iloc[i,2]+"---"+df.iloc[i,3])

        return render_template('Home.html', query=query, tweets=tweets)
    return render_template('Home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
