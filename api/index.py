# -*- coding: UTF-8 -*-
import requests
import json
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

def github_json(user,repo,branch):
    requests_path = 'https://github.com/' + user + '/' +repo + '/blob/'+branch+'/friendlist.json'
    r = requests.get(requests_path)
    r.encoding = 'utf-8'
    gitpage = r.text
    soup = BeautifulSoup(gitpage, 'html.parser')
    main_content = soup.find('td',id = 'LC1').text
    result = json.loads(main_content)
    return result

def url_split(url):
    info_list = []
    url_text_list = url.split('/')
    if len(url_text_list) == 7:
        info_list.append(url_text_list[4])
        info_list.append(url_text_list[5])
        info_list.append(url_text_list[6])
    if len(url_text_list) == 6:
        info_list.append(url_text_list[4])
        info_list.append(url_text_list[5])
        info_list.append('master')
    if len(url_text_list) == 5:
        info_list.append(url_text_list[4])
        info_list.append('friends')
        info_list.append('master')
    return info_list

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        info_list = url_split(url)
        try:
            user = info_list[0]
            repo = info_list[1]
            branch = info_list[2]
            data = github_json(user,repo,branch)
        except:
            data =['message':'error']
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
