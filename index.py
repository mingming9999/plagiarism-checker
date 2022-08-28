from flask import Flask
import requests
from flask import request
from googlesearch import search
#from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from numpy import vectorize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
app = Flask(__name__)

@app.route('/')
def index():
  query = request.args.get('data', default = '*', type = str)
  print(query)
  flies = [doc for doc in os.listdir() if doc.endswith('.txt')]
  for l in range(1,len(flies)):
      os.remove(flies[l])
  #query = "dog"
  hanap(query)
  out_data =[]
  for data in check_plagiarism():
    if "0.txt" in data:
      out_data.append(data)    
  return out_data


def hanap(query):
  
  # to search 
  for j in search(query, tld="co.in", num=5, stop=5, pause=0.5):
    try:
       response = requests.get(j)
       print (response.status_code)
       html = (response.content)
       soup = BeautifulSoup(html, features="html.parser")
       name = j.replace(":","@")
       name = name.replace("/","AAAA")
       # kill all script and style elements
       for script in soup(["script", "style"]):
          script.extract()    # rip it out

       # get text
       text = ""
       for data in soup.find_all("p"): 
          text+=data.get_text()
       lines = (line.strip() for line in text.splitlines())
       # break multi-headlines into a line each
       chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
       # drop blank lines
       text = ' '.join(chunk for chunk in chunks if chunk)
       
      
       f1 = open("0.txt", "w")
       f1.write(query)
       f1.close() 
       f = open(name+".txt", "w")
       f.write(text)
       f.close()  
       
    except:
       print("404") 
   



 
def check_plagiarism():
    sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    sample_contents = [open(File).read() for File in sample_files]
 
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
 
    vectors = vectorize(sample_contents)
    s_vectors = list(zip(sample_files, vectors))
    results = set()
    #global s_vectors
    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((sample_a, text_vector_a))
        del new_vectors[current_index]
        for sample_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            sample_pair = sorted((sample_a, sample_b))
            score = sample_pair[0], sample_pair[1], sim_score
            results.add(score)
    return results

  
app.run(host='0.0.0.0', port=80)
 
