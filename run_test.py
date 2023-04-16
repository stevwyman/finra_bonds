from local_data import History_DAO
from technical_analysis import EMA
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates



local_dao = History_DAO()
#local_dao.update("SPY")

history = local_dao.read("SPY", 500)

price_line = list()
price_dates = list()
price_trend = list()
price_ema = EMA(50)

for data in history:

    print(data)
    
    price_dates.append(datetime.fromtimestamp(data["date"] / 1000))

    close = data["price"]
    price_line.append(close)
    ema = price_ema.add(close)
    price_trend.append(ema)

plt.title(f"SPY {close} EMA(50): {ema:.2f}")
plt.ylabel("Value")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
plt.plot(price_dates, price_line, label="close")
plt.plot(price_dates, price_trend, label="ema(50)")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()