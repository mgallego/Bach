import sqlite3, transmissionrpc, settings, os

class TorrentHandler():

    def __init__(self):
	dir_path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(dir_path + '/bach.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS Torrents(link TEXT)")
        self.cur = self.conn.cursor()  
        self.tc = transmissionrpc.Client(settings.TRASMISSION['url'], user=settings.TRASMISSION['user'], password=settings.TRASMISSION['password'], port=settings.TRASMISSION['port'])
        
    def is_in_database(self, magnet):
        self.cur.execute("SELECT COUNT(*) FROM Torrents WHERE link = '"+magnet+"'")
        return self.cur.fetchone()[0] != 0

    def add_magnet(self, magnet):
        if (not self.is_in_database(magnet)):
            self.tc.add_torrent(magnet)
            self.cur.execute("INSERT INTO Torrents VALUES ('"+magnet+"')")
            
    def commit(self):
        self.conn.commit()
        self.conn.close()
