# -*- coding: UTF-8 -*-
import requests
import re
import json
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

def github_json(user,repo,branch):
    if user =='':
        result = json.loads("['error':'用户为空']")
    else:
        try:
            if repo =='':
                repo = 'friends'
            if branch =='':
                branch = 'master'
            requests_path = 'https://github.com/' + user + '/' +repo + '/blob/'+branch+'/friendlist.json'
            r = requests.get(requests_path)
            r.encoding = 'utf-8'
            gitpage = r.text
            soup = BeautifulSoup(gitpage, 'html.parser')
            main_content = soup.find('td',id = 'LC1').text
            result = json.loads(main_content)
        except:
            result = json.loads("['error':'参数填入有误']")
    return result

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        path = path.replace("'", '"')
        repo_reg = re.compile(r'repo="(.*?)"')
        user_reg = re.compile(r'user="(.*?)"')
        branch_reg = re.compile(r'branch="(.*?)"')
        user = user_reg.findall(path)[0]
        repo = repo_reg.findall(path)[0]
        branch = branch_reg.findall(path)[0]
        data = github_json(user,repo，branch)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
