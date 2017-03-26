
'''
ProxyPool config
'''

import redis

# some config
PROXY_SIZE = 2000
check_IP_URL = 'http://wenshu.court.gov.cn/'
Check_Spacing_Time = 3600


# redis config
REDIS_DATABASE_NAME = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE_NAME)


# IP URL
XICIDAIL_WT_URL = 'http://www.xicidaili.com/wt/'
XICIDAIL_NN_URL = 'http://www.xicidaili.com/nn/'
XICIDAIL_WN_URL = 'http://www.xicidaili.com/wn/'
G66ip_URL = 'http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'
