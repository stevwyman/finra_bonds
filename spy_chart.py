from online_data import PolygonIO
from datetime import datetime
from technical_analysis import EMA
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

online_dao = PolygonIO()
answer = online_dao.lookupHistory("SPY", "2021-01-01", "2023-03-14")
results = answer["results"]

dates = list()
closes = list()
ema_50 = list()
ema = EMA(50)
for result in results:
    close = result["c"]
    timestamp = result["t"]
    dates.append(datetime.utcfromtimestamp(timestamp/1000))
    closes.append(close)
    ema_50.append(ema.add(close))
    
plt.title("SPY daily")
plt.ylabel("SPY")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
plt.plot(dates, closes, label="close")
plt.plot(dates, ema_50, label="EMA(50)")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()

