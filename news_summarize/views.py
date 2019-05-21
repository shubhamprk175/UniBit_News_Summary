from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def search_stock(request):

    import requests
    import json
    API_KEY = "6cTbE6TyUbH-_H4d_VsNCUsUhn97leWM"

    ticker = request.POST['search_stock_query']
    ticker = ticker.upper()
    print(ticker)
    url = f'https://api.unibit.ai/api/news/classification/{ticker}?'
    print("URL", url)
    params = {"range":"1w", "AccessKey":"demo", "datatype":"json"}

    res = requests.get(url, params)

    if(res.status_code != 200):
        raise ConnectionError(res.json())

    context = {"Stock_News":res.json()["Stock News"]}

    return render(request, "news_search.html", context)

def summarize(request):
    import nltk
    import urllib.request
    import re
    import bs4

    news_url = request.POST['news_url']
    print(news_url)

    data = urllib.request.urlopen(news_url)

    parsed_article = bs4.BeautifulSoup(data.read(), "lxml")

    paras = parsed_article.find_all('p')
    title = parsed_article.find('title').text
    print(title)

    full_text = ""

    for para in paras:
        full_text += para.text

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', full_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    formatted_article_text = formatted_article_text.lower()
    sentence_list = nltk.sent_tokenize(full_text)

    stopwords = nltk.corpus.stopwords.words('english')
    word_freq = {}

    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            freq = word_freq.get(word, 0)
            word_freq[word] = freq+1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = (word_freq[word]/max_freq)

    sent_score = {}

    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq.keys() and len(sent.split(' ')) < 30:
                score = sent_score.get(sent, 0)
                sent_score[sent] = score + word_freq[word]

    import heapq
    summary_sentences = heapq.nlargest(7, sent_score, key=sent_score.get)

    summary = ' '.join(summary_sentences)

    context = {'summary' : [summary]}

    return render(request, "summary.html", context)



def news_home(request):
    return render(request, "news_home.html")
