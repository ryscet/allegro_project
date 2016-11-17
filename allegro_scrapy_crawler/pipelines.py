import sqlite3 as lite
 
con = None  # db connection
 
class StoreInSqlitePipeline(object):
 
    def __init__(self):
        self.setupDBCon()
        self.createAllegroSalesTable()
 
 
    def process_item(self, item, spider):
        # item['name'] is a list, which cannot be added as is to sql. Hack to deliver it item by item
        # TODO how to avoid iteration
        try:
            for title, price, saleDate, in zip(item['offer_title'], item['price'], item['date_of_sale']):
                self.storeInDb(title, price, saleDate, item['url'][0]) # item['url'] is always a list of len 1, i.e. url is not copied for each item

        except KeyError:
            print('No items found at: %s' % item['url'][0])
            pass

        return item
 
 
    def storeInDb(self, title, price, saleDate, url):
        """Add a scraped item to sqlite db."""
        self.cur.execute("INSERT INTO Macs(offer_title, price, date_of_sale, url) VALUES(?,?,?,?)",(title, price, saleDate, url))
        self.con.commit()
 
 
    def setupDBCon(self):
        """# The database will be created if it doesn't exist, if it does it will connect."""
        self.con = lite.connect('./allegro_flask_app/AllegroSales.db') 
        self.cur = self.con.cursor()
 
    def createAllegroSalesTable(self):
        """Overwrites a table each time a crawl is initiated"""
        self.cur.execute("DROP TABLE IF EXISTS Macs")

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Macs(Id INTEGER PRIMARY KEY, offer_title TEXT, price TEXT, date_of_sale TEXT, url TEXT)''')
 
 
    def closeDB(self):
        self.con.close()

    def __del__(self):
        self.closeDB()