import urllib
'''
download mp3 files
'''

class Download_Mp3():

    def download_Mp3(self, SongDownloadUrl, SaveSongFileRout):

        urllib.urlretrieve(SongDownloadUrl, SaveSongFileRout)
