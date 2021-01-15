#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020

@author: aness
"""

################################## Déclaration des classes ##################################

import datetime as dt

import pickle # librairie permettant 

# on cree la classe corpus
class Corpus():
    
    # initialisation
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
        self.txt = []
        
    # méthode permettant d'ajouter un doc
    def add_doc(self, doc):
        
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
        self.txt.append(doc.get_text())
           
    #méthode permettant d'ajouter un auteur
    def add_aut(self, aut_name,doc):
        
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        
        self.naut += 1
    
    # methode permettant de recuperer l'id d'un auteur
    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi

    # methode permettant de recuper le doc en precisant l'id
    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection
    
    # methode permettant de recuperer le contenu du corpus
    def get_txt(self):
        return self.txt

    # methode permettant de renvoyer d'ou vient le corpus ainsi que le nombre de documents et le nombre d'auteurs
    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    # methode permettant de trier les titres
    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]
    # methode permettant de trier les dates
    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    # methode permettant de sauvegarder un corpus
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
    # methode permettant de rendre en minuscule le contenu d'un corpus           
    def nettoyer_texte(self):
      self.txt = self.text.lower()
      self.txt.replace("\n"," ")
      #print(self.text)
    

    def stat(self):
        vocabulaire = [] # on cree une liste vide qui va contenir le vocabulaire du corpus
        import nltk
        from nltk.corpus import stopwords # cette librairie va nous permettre de gérer les stopwords
        for i in range(len(self.txt)):
            self.txt[i] = self.txt[i].lower()
            x = self.txt[i]
            import string
            punct = string.punctuation
            for c in punct:
                x = x.replace(c, "") # on supprime les ponctuations
            x= x.replace("user", " ") # on supprime reddit et user
            x= x.replace("reddit", " ")
            x = x.split(" ") # on split
            for i in x:
                if i not in stopwords.words('english') and i != '' and i not in string.ascii_lowercase and i != "i'm" and i != "don't" and i.isnumeric() != True:   
                    vocabulaire.append(i)
        
        vocabulaire = set(vocabulaire)
        import pandas as pd
        test = pd.DataFrame.from_dict(vocabulaire) # on transforme le vocabulaire en dataframe
        for y in range(len(self.txt)):
            for i in range(len(test)):
                if self.txt[y].count(test.loc[i,0]) != 0:
                    test.loc[i,1]=self.txt[y].count(test.loc[i,0]) # on rajoute le nombre d'occurence d'un mot dans une autre colonne 
        return test # on retourne le data frame
    
    # méthode permettant de calculer le poids d'un mots dans un corpus    
    def tfidf(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_vectorizer.fit(self.txt)
        import numpy as np
        np.set_printoptions(precision=2)
        X_TFxIDF = tfidf_vectorizer.transform(self.txt)
        return X_TFxIDF.toarray()
        
        
        
# on cree la classe auteur
class Author():
    def __init__(self,name):
        self.name = name
        self.production = {}
        self.ndoc = 0
     # methode permettant d'ajouter un auteur   
    def add(self, doc):     
        self.production[self.ndoc] = doc
        self.ndoc += 1
    # methode permettant d'affier l'auteur et son nombre de documents
    def __str__(self):
        return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)
    def __repr__(self):
        return self.name
    



# on cree la classe document
class Document():
    
    # on initialise
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
    
    
    #methode permettant de recuperer les auteurs d'un document
    def get_author(self):
        return self.author
    # methode permettant de recuperer le titre du document
    def get_title(self):
        return self.title
    # methode permettant de recuperer la date
    def get_date(self):
        return self.date
    # methode permettant de recuperer la source
    def get_source(self):
        return self.source
    # methode permettant de recuperer le contenu du docuemnt    
    def get_text(self):
        return self.text

    def __str__(self):
        return "Document " + self.getType() + " : " + self.title
    
    def __repr__(self):
        return self.title
    #methode permettant de resumer un texte     
    def resume(self): 
        from gensim.summarization.summarizer import summarize
        print(summarize(self.text))
        
    def getType(self):
        pass
    
   

    
# classe fille permettant de modéliser un Document Reddit
class RedditDocument(Document):
    
    def __init__(self, date, title,
                 author, text, url, num_comments):        
        Document.__init__(self, date, title, author, text, url)
        # ou : super(...)
        self.num_comments = num_comments
        self.source = "Reddit"
    #methode permettant de retourner le nombre de commentaire d'un documetn    
    def get_num_comments(self):
        return self.num_comments
    # methode permettant de renvoyer le type
    def getType(self):
        return "reddit"
    
    def __str__(self):
        return Document.__str__(self) + " [" + str(self.num_comments) + " commentaires]"
    
# classe fille permettant de modéliser un Document Arxiv
class ArxivDocument(Document):
    
    def __init__(self, date, title, author, text, url, coauteurs):
        Document.__init__(self, date, title, author, text, url)
        self.coauteurs = coauteurs
    
    def get_num_coauteurs(self):
        if self.coauteurs is None:
            return(0)
        return(len(self.coauteurs) - 1)

    def get_coauteurs(self):
        if self.coauteurs is None:
            return([])
        return(self.coauteurs)
        
    def getType(self):
        return "arxiv"

    def __str__(self):
        s = Document.__str__(self)
        if self.get_num_coauteurs() > 0:
            return s + " [" + str(self.get_num_coauteurs()) + " co-auteurs]"
        return s


import praw

import urllib.request
import xmltodict   



################################## Création du Corpus ##################################

corpus = Corpus("chess")
#on choisit le theme ainsi que le nombre de resultats
url = 'http://export.arxiv.org/api/query?search_query=all:chess&start=0&max_results=50'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']
coauthor = []
for i in docs:
    datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
    try:
        author = [aut['name'] for aut in i['author']][0]
    except:
        author = i['author']['name']
    #gestion de co auteurs    
    if len(i['author']) != 0:
        for y in range(1,len(i['author'])):
             try:
                 coauthor.append([aut['name'] for aut in i['author']][y])
             except: pass
    txt = i['title']+ ". " + i['summary']
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    # ajout du document
    doc = ArxivDocument(datet,
                   i['title'],
                   author,
                   txt,
                   i['id'],
                   coauthor)
    corpus.add_doc(doc)

# on recupere le nombre d'occurence du corpus
voc_arxiv = corpus.stat()    
#on recupere le poids des mots dans le corpus
tdidf_arxiv = corpus.tfidf()


corpus2 = Corpus("chess")
reddit = praw.Reddit(client_id='4h9QntGTMSiK-w', client_secret='BsZTgGuRBvkOvAI4HT2iBXaa-ipD6A', user_agent='bst')
hot_posts = reddit.subreddit('chess').hot(limit=50)
for post in hot_posts:
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = RedditDocument(datet,
                   post.title,
                   post.author_fullname,
                   txt,
                   post.url,
                   post.num_comments)
    corpus2.add_doc(doc)


voc_reddit = corpus2.stat()    
tdidf_reddit = corpus2.tfidf()




# =============================================================================
# print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))
# print(corpus)
# print()
# 
# print("Corpus trié par titre (4 premiers)")
# res = corpus.sort_title(4)
# print(res)
#     
# print()
# 
# print("Corpus trié par date (4 premiers)")
# res = corpus.sort_date(4)
# print(res)
# 
# print()
# 
# print("Enregistrement du corpus sur le disque...")
# corpus.save("Corona.crp")
# 
# =============================================================================



#affichage des différents graphes notamment le nuage de mots ainsi que l'histogramme des mots les plus fréquents


#####################################################################################
# =============================================================================
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
# 
# voc = voc_arxiv.sort_values(by=[1], ascending=False)
# voc2 = voc_reddit.sort_values(by=[1], ascending=False)
# 
# # =============================================================================
# # voc.hist() # histogramme montrant le nombre de fois qu'un mot est utilisé 
# # =============================================================================
# 
# import seaborn as sns
# 
# hist_arxiv = voc.head(6)
# sns.barplot(hist_arxiv[0], hist_arxiv[1])
# 
# # =============================================================================
# # hist_reddit = voc2.head(6)
# # sns.barplot(hist_reddit[0], hist_reddit[1])
# # =============================================================================
# 
# from wordcloud import WordCloud
# text = ""
# for i in range(len(voc)):
#     text = text + " " + voc.iloc[i,0]
# wordcloud = WordCloud().generate(text)
# fig = plt.figure()
# plt.imshow(wordcloud)
# plt.axis('off')
# plt.show()
# 
# =============================================================================
# =============================================================================
# text2 = ""
# for i in range(len(voc2)):
#     text2 = text2 + " " + voc2.iloc[i,0]
# wordcloud = WordCloud().generate(text2)
# fig = plt.figure()
# plt.imshow(wordcloud)
# plt.axis('off')
# plt.show()
# =============================================================================

###############"

