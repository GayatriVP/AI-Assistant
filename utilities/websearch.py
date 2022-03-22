from urllib.parse import urlparse
import webbrowser
import re
from utilities.speech_functions import * 
import urllib
import requests
from utilities.confirm import *
from requests_html import HTMLSession


def parse_results(response):    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)
    # print(results)

    output = []
    
    for result in results:
        # print('in for')

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href']             
        }
        try: 
            result.find(css_identifier_text, first=True).text
            item['text']=result.find(css_identifier_text, first=True).text
        except:
            item['text']=''
        
        output.append(item)
        
    return output

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    
    return response

def google_search(query):
    response = get_results(query)
    return parse_results(response)

def search_for(query):
    results = google_search(query)
    result = ''
    j=''
    # print(results)
    for a in results:
        desc= a['text']
        if not(desc==''):
            if len(desc) > 100:
                text = desc.partition('.')[0] + '.'
                t = urlparse(a['link']).netloc
                titl=t.split('.')[-2:][0]
                result = "According to "+titl+" : "+text
                j=a['link']
                break;

    print(result)
    speak(result)
    speak('Do you want to open the site?')
    print('Do you want to open the site?')
    # ch = input('Do you want to open the site?(y/n)')
    while True:
        if confirm():
            webbrowser.open_new_tab(j)
            return
        else:
            return


def youtube(param):
    chelen = param.split()
    if len(chelen)>1:
        param=param.replace(' ','+')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + param)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    final = "https://www.youtube.com/watch?v=" + video_ids[0]
    speak('Do you want to view on youtube?')
    print('Do you want to view on youtube?')
    # ch = input('Do you want to open the site?(y/n)')
    while True:
        if confirm():
            webbrowser.open_new_tab(final)
            return
        else:
            return
