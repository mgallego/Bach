import urllib2, lxml.html
import settings
from urlparse import urlparse
from torrent_handler import TorrentHandler

class ElitetorrentSpider():

    def __init__(self, url):
        self.url = url
        parsed_uri = urlparse(url)
        self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        self.th = TorrentHandler()
        
    def load_torrents(self):
        for magnet in self.get_episodes_magnets():
	    try:
            	self.th.add_magnet(magnet.xpath('@href')[0]);
	    except:
		print "Error with magnet: " + magnet.xpath('@href')[0] 
        self.th.commit()

    def get_episodes_detail_url(self):
        req = urllib2.Request(self.url ,headers=settings.HEADERS)
        page = urllib2.urlopen(req)
        data = page.read()
        page.close()
        doc = lxml.html.document_fromstring(data)
        return doc.xpath("//*[@id='principal']/div[2]/ul/li/a/@href")

    def get_episodes_magnets(self):
        magnets = []
        for detail_url in self.get_episodes_detail_url():
            req = urllib2.Request(self.domain+detail_url ,headers=settings.HEADERS)
            page = urllib2.urlopen(req)
            data = page.read()
            page.close()
            doc = lxml.html.document_fromstring(data)
            magnets.append(doc.xpath("//a[contains(@href,'magnet')]")[0])
        return magnets
