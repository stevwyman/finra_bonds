from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///history.db")

# create tables
#
# - create a table to store the stock details
db.execute("CREATE TABLE IF NOT EXISTS 'stock' ('symbol' TEXT PRIMARY KEY NOT NULL, 'name' TEXT NOT NULL, 'industry' TEXT, 'sector' TEXT, 'country' TEXT);")
# - create a table to store a watchlist
db.execute("CREATE TABLE IF NOT EXISTS 'watchlist' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'name' TEXT NOT NULL);")
# - create mapping between stock and watchlist
db.execute("CREATE TABLE IF NOT EXISTS 'stock2watchlist' ('watchlist_id' INTEGER NOT NULL references watchlist(id), 'stock_symbol' TEXT NOT NULL references stock(symbol), PRIMARY KEY ('watchlist_id', 'stock_symbol'));")
# - create a table to store the historic data of a stock
db.execute("CREATE TABLE IF NOT EXISTS 'history' ('symbol' TEXT NOT NULL, 'timestamp' DATETIME NOT NULL, 'open' INTEGER NOT NULL, 'high' INTEGER NOT NULL, 'low' INTEGER NOT NULL, 'close' INTEGER NOT NULL, 'volume' INTEGER, PRIMARY KEY ('symbol', 'timestamp'));")
