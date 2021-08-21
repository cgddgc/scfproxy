#!python3
#-*-coding:utf-8-*-

from mitmproxy import ctx
import json, time, random
import requests, base64



class scf:
    def __init__(self):
        self.token = '/it00ls'                    #/token可以不改
        self.urls = {                                                                        
        #'local':'http://127.0.0.1:59998/',
        'gz':'https://service-xxxx-xxxxxxx.gz.apigw.tencentcs.com/release',         #访问路径,可在多个地区新建函数然后随机选择
        }

    def request(self, flow):
        request = flow.request
        header = {}
        for k,v in request.headers.items():
            header[k] = v
        header['Accept-Encoding'] = 'deflate'
        header['accept-encoding'] = 'deflate'
        reqdata = {
        'headers':base64.b64encode(json.dumps(header).encode()).decode(),
        'data':base64.b64encode(request.content).decode(),
        'method':request.method,
        'url':request.url
        }

        data = base64.b64encode(json.dumps(reqdata).encode()).decode()


        request.headers['Content-Type'] = 'application/json'
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
        request.headers['Accept-Encoding'] = 'deflate'
        request.headers['accept-encoding'] = 'deflate'
        request.method = 'POST'
        request.content = json.dumps({'data':data}).encode()
        urlss =  [u + self.token for u in self.urls.values()]
        
        request.url = random.choice(urlss)
        #request.url = self.urls['gz'] + self.token
        



    def response(self, flow):
        flow.response.headers["Content-Encoding"] = 'identity'


    


addons = [
    scf(),
]

