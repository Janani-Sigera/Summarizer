from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from nltk.tokenize import RegexpTokenizer

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
# from django.core.serializers import json
from django.shortcuts import render
import json

# Create your views here.

text=''
def get_only_text(url):
    """
     return the title and the text of the article
     at the specified url
    """
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    print(text)
    print()
    return soup.title.text,text

def summary_ratio(averageTime,text):
    tokenizer = RegexpTokenizer("[\w']+")
    word = tokenizer.tokenize(text)
    count = len(word)
    rat = (float)((200*averageTime)/count)
    return rat

def summary_generator(url,averageTime):
    title, text = get_only_text(url)
    rat= (float)(summary_ratio(averageTime,text))
    summary= summarize(str(text), ratio=rat)
    # print('\nKeywords:')

    # higher ratio => more keywords
    # print(keywords(str(text), ratio=rat))
    return title,summary

def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')


@csrf_exempt
def gen_sum(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        payload = json.loads(data)
        url = payload['url']
        averageTime = payload['averageTime']
        try:
            # title, summary = summary_generator(url, averageTime)
            # # response = json.dumps([{'Title': title, 'Long Summary': summary}])
            # response = json.dumps([{'Title': title, 'Long Summary': summary}])

            title, summary = summary_generator(url, averageTime)
            response_data = {}
            response_data['title'] = title
            response_data['summary'] = summary
            response = json.dumps(response_data)
        except:
            response = json.dumps([{'Error': 'Internal Server Error'}])
    return HttpResponse(response, content_type='text/json')

def test(request):
    if request.method == 'GET':
        try:
            title, summary = summary_generator("http://www.adaderana.lk/news/50302/certain-reports-on-assassination-plot-are-false-mangala", 10)
            response_data = {}
            response_data['title'] = title
            response_data['summary'] = summary

            response = json.dumps(response_data)
        except:
            response = json.dumps([{ 'Error': 'No car with that name'}])
    return HttpResponse(response, content_type='application/json')
    # return HttpResponse(json.dumps(response_data), content_type="application/json")
