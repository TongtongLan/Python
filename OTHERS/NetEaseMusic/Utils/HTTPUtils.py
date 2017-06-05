import requests
from bs4 import BeautifulSoup

from OTHERS.NetEaseMusic.Utils import config


class HttpUtils:
    def get_Request(self, url):
        response = requests.get(url)
        return response.text

    def post_Request(self, url, headers, data):
        return requests.post(config.SEARCH_URL, headers=config.headers, data=data)

    def update_PostData(self, string, type):
        config.data['type'] = type
        config.data['s'] = string
        return config.data

class HtmlParserUtils:
    def init_Html(self, res):
        return BeautifulSoup(res, 'html.parser')

    def get_TagList(self, content, tag, attrs={}):
        return content.findAll(tag, attrs)

class JsonParserUtils:

    def get_ResponseCodeAndResult(self, response):
        code = self.get_JsonValue(response.json(), 'code')
        result = self.get_JsonValue(response.json(), 'result')
        return code, result

    def get_JsonValue(self, json, key):
        return json[key]

    def get_JsonValues(self, jsondata, startname='', value={}, *args):
        values = value
        if isinstance(args[0], tuple):
            args = args[0]
        for key in args:
            try:
                values[startname + '_' + key] = self.get_JsonValue(jsondata, key)
            except:
                if isinstance(key, list):
                    data = self.get_JsonValue(jsondata, key[0])
                    if isinstance(data, list):
                        for data in self.get_JsonValue(jsondata, key[0]):
                            self.get_JsonValues(data, key[0], values, tuple(key[1]))
                    elif isinstance(data, dict):
                        self.get_JsonValues(self.get_JsonValue(jsondata, key[0]), key[0], values, tuple(key[1]))

        return values


