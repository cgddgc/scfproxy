#!python3
#-*-coding:utf-8-*-

from mitmproxy import ctx
import json, random, base64, pickle


#执行命令: mitmdump -s scfv2.py --ssl-insecure --listen-port 8082



class scf:
    def __init__(self):
        self.apigateways = {                                         #api网关地址
        #'local':'http://127.0.0.1:59998/',
        'gz':'https://servi025341.gz.apigw.tencentcs.com/release',
        #'sh':'https://serv25341.sh.apigw.tencentcs.com/release',
        #'sg':'https://ser41.sg.apigw.tencentcs.com/release',
        #'bj':'https://servi41.bj.apigw.tencentcs.com/release',
        #'cd':'https://serv341.cd.apigw.tencentcs.com/release',
        #'gg':'https://servi1.usw.apigw.tencentcs.com/release',      #硅谷
        #'sr':'https://serv5341.kr.apigw.tencentcs.com/release',
        #'fl':'https://serv025341.de.apigw.tencentcs.com/release',
        'hk':'https://servic41.hk.apigw.tencentcs.com/release'
        }
        
        urls =  [u for u in self.apigateways.values()]
        
        self.url = random.choice(urls)              #随机选择上面的API网关
        #self.url = self.apigateways['hk']           #只用其中一个API网关（通常只用广州、香港等，延迟低不容易出错）


    def request(self, flow):
        request = flow.request

        header = {}
        for k,v in request.headers.items():
            header[k] = v

        header['accept-encoding'] = 'gzip'
        header['Connection'] = 'close'

        reqdata = {
        'headers':base64.b64encode(json.dumps(header).encode()).decode(),
        'data':base64.b64encode(request.raw_content).decode(),
        'method':request.method,
        'url':request.url
        }

        data = base64.b64encode(json.dumps(reqdata).encode()).decode()

        myheaders = {
        'Content-Type':'application/json',
        'User-Agent':'scfproxy-client',
        }

        myheaders['Host'] = self.url.split('/')[2]
        
        flow.request = flow.request.make(url = self.url, method = 'POST', headers = myheaders, content = json.dumps({'data': data}))



    def response(self, flow):
        try:
            data = pickle.loads(base64.b64decode(flow.response.text))
            flow.response = flow.response.make(content = data.content, headers = dict(data.headers), status_code = data.status_code)
        except Exception as e:
            flow.response = flow.response.make(content = flow.response.text)
            print(e)
            print(flow.response.text)


addons = [
    scf(),
]

