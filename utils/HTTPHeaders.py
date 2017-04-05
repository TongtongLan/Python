


class HTTPHeader():
    XICIDAIL_header = {'Accept-Language': 'en-US,en;q=0.5',
              'Accept-Encoding': 'gzip, deflate',
              'Host': 'www.xicidaili.com',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:49.0) Gecko/20100101 Firefox/49.0',
              'Connection': 'keep-alive'
                       }

    G66IP_header = {'Accept-Language': 'en-US,en;q=0.5',
              'Accept-Encoding': 'gzip, deflate',
              'Host': 'www.66ip.cn',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:49.0) Gecko/20100101 Firefox/49.0',
              'Connection': 'keep-alive',
              'Cookie': '__cfduid=d8d4843450ba5624c40690847e0de60081489924186; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1490431126,1490433302,1490434620,1490450614; UM_distinctid=15b049453779-02b6c0430958f98-3e6e0c41-100200-15b049453781a4; CNZZDATA1253901093=1894918268-1490428844-null%7C1490572841; cf_clearance=3b68eb3fa56a8cdbd3e16fdde150230c0a1e6a5b-1491390479-604800'
                    }



    def GetxicidailHttpHeader(self):
        return self.XICIDAIL_header

    def Get66ipHeader(self):
        return  self.G66IP_header