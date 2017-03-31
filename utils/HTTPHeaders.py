


class HTTPHeader():
    XICIDAIL_header = {'Accept-Language': 'en-US,en;q=0.5',
              'Accept-Encoding': 'gzip, deflate',
              'Host': 'www.xicidaili.com',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:49.0) Gecko/20100101 Firefox/49.0',
              'Connection': 'keep-alive',
              'Cookie': 'UM_distinctid=15ae61c28c418b-0e660bf061392b-3e6e0c41-100200-15ae61c28c5ef; CNZZDATA1256960793=2146794335-1489916912-%7C1490356165; _free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTdjNTgyZDkxY2QzZmIzNGZhODk4NGNiYzg3YWNkMTYyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVFRV2xTc2tzblY2WEZMWTlxNEFEVk5Id1JmWmZYcWtFcC9CWGdJV1pvMFk9BjsARg%3D%3D--c97a4c638f5c6b459a16cf08ba1d93d2c36c269d'}

    G66IP_header = {'Accept-Language': 'en-US,en;q=0.5',
              'Accept-Encoding': 'gzip, deflate',
              'Host': 'www.66ip.cn',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:49.0) Gecko/20100101 Firefox/49.0',
              'Connection': 'keep-alive',
              'Cookie': '__cfduid=d8d4843450ba5624c40690847e0de60081489924186; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1490431126,1490433302,1490434620,1490450614; UM_distinctid=15b049453779-02b6c0430958f98-3e6e0c41-100200-15b049453781a4; CNZZDATA1253901093=1894918268-1490428844-null%7C1490572841; cf_clearance=db4162687a85713cc54a3365fa245d2a4fbc7b14-1490576168-604800'
                    }



    def GetxicidailHttpHeader(self):
        return self.XICIDAIL_header

    def Get66ipHeader(self):
        return  self.G66IP_header