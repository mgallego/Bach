import urllib2, lxml.html
import settings
from torrent_handler import TorrentHandler

class EztvSpider():

    def __init__(self, url):
        self.url = url
        self.th = TorrentHandler()
        
    def load_torrents(self):
        for magnet in self.get_episodes_magnets():
            self.th.add_magnet(magnet.xpath('@href')[0]);
        self.th.commit()

    def get_episodes_magnets(self):
        req = urllib2.Request(self.url ,headers=settings.HEADERS)
        page = urllib2.urlopen(req)
        data = page.read()
        page.close()
        doc = lxml.html.document_fromstring(data)
        return doc.xpath("//a[contains(@href,'magnet')]")
