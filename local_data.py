from online_data import PolygonIO
from datetime import datetime, timedelta
from cs50 import SQL

class History_DAO():

    def __init__(self):
        self.__db = SQL("sqlite:///history.db")

    def update(self, symbol: str):

        now = datetime.now()
        fromDate = (now - timedelta(days = 2 * 365)).strftime('%Y-%m-%d')
        endDate = now.strftime('%Y-%m-%d')

        online_dao = PolygonIO()

        
        aggregates = online_dao.lookupHistory(symbol, fromDate, endDate)

        #print(aggregates)
        
        symbol = aggregates['ticker']
        history = aggregates['results']
        self.__db.execute("DELETE FROM history WHERE symbol=?;", symbol)

        for bar in history:
            self.__db.execute("INSERT INTO history (symbol, timestamp, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        symbol, bar['t'], bar['h'], bar['l'], bar['o'], bar['c'], bar['v'],)
            
    def read(self, symbol: str, entries: int):
        
        return self.__db.execute("SELECT * FROM (SELECT timestamp AS date, close AS price FROM history WHERE symbol=? ORDER BY timestamp DESC LIMIT ?) ORDER BY date ASC;", symbol, entries)
