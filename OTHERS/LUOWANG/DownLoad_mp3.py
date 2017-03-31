import urllib
'''
download mp3 files
'''

class download_mp3():

    def download(self, url, song_filename):

        urllib.urlretrieve(url, song_filename)
