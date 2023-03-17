import urllib3
import pymongo
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from tabulate import tabulate
from bs4 import BeautifulSoup
from lxml import etree
from technical_analysis import EMA


FINRA_DATE_FORMAT = "%m/%d/%Y"
LOCAL_DATE_FORMAT = "%Y%m%d"

cookie = 'enter cookie here'

class OnlineReader:
    def __init__(self):
        # open a connection to a URL using urllib3
        self._http = urllib3.PoolManager()

    def return_data(self, data: str) -> dict:
        """
        takes a str and parses it to return an dictionary object for a given date

        """
    
        table = etree.HTML(str(data))

        # file date
        file_date = table.find(".//table").attrib["data-filedate"]
        # print(f"file_date: {file_date}")

        file_date_p = datetime.strptime(file_date, FINRA_DATE_FORMAT)
        file_date = int(datetime.strftime(file_date_p, "%Y%m%d"))

        # headers
        headers = [th.text for th in table.findall(".//tr/th")]
        # print(headers)

        columns = len(headers)

        data = list()

        row_description = table.findall(".//tbody/th")
        for description in row_description:
            row = list()
            row.append(description.text)
            data.append(row)

        entries = table.findall(".//tbody/td")

        entry = 0
        row = 0
        while entry < len(entries):
            for column in range(columns-1):
                # add the current entry to the list of entries for this row
                data[row].append(entries[entry].text)
                # next entry
                entry += 1
            # next row
            row += 1

        # print(tabulate(data,headers = headers,tablefmt='fancy_grid'))

        data_dict = {}
        for column in range(1,5):
            entry_dict = {}
            for row in range(6):
                entry_dict[data[row][0]] = int(data[row][column])
            data_dict[headers[column]] = entry_dict

        # print(data_dict)
        
        entries = len(data_dict)
        if entries == 0:
            print("... no data available")
        else:
            print(f"... received {entries} entries")
        
        return {"date": file_date, "bond_data": data_dict}

    def request_data(self, date: datetime) -> dict:
        """
        tries to grab data from the morningstar.com page and returns the pure data as str
        
        https://finra-markets.morningstar.com/transferPage.jsp?
            path=http://muni-internal.morningstar.com/public/MarketBreadth/C
            &date=03/08/2023
            &_=1678553779148
        
        """
        url = "https://finra-markets.morningstar.com/transferPage.jsp?path=http://muni-internal.morningstar.com/public/MarketBreadth/C"

        url += "&date=" + datetime.strftime(date, FINRA_DATE_FORMAT)

        date= datetime.utcnow() - datetime(1970, 1, 1)
        seconds =(date.total_seconds())
        milliseconds = round(seconds*1000)

        url += "&_=" + str(milliseconds)

        response = self._http.request("GET", url, headers={"Cookie": cookie})
        print(f"Response for {response.geturl()}: {response.status} ... ")
        # print(response.data)

        finra_html = response.data.decode("utf-8")
        parsed_html = BeautifulSoup(finra_html, features="lxml")
        # print(parsed_html)

        if parsed_html.body == None:
            raise RuntimeError("invalid response received - empty dataset")

        data_table = parsed_html.body.find("table")

        return self.return_data(data_table)


class LocaleDAO:

    def __init__(self):
        self._myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self._db = self._myclient.python_test
        self._collection = self._db.finra_bonds

    def write(self, bond_data: dict) -> None:
        file_date = bond_data["date"]
        data = bond_data["bond_data"]
        try:
            if (len(list(self._collection.find({"date": file_date}))) > 0):
                print(f"Entry exists already.")
            else:
                print(f"Adding new entry for {file_date}")
                self._collection.insert_one(bond_data)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Could not write data to locale storage: ", e)
        except KeyError:
            pass

    def read_all(self) -> list[dict]:
        """
        returns a list of all entries in the database sorted by date
        """
        try:
            cursor = self._collection.find().sort([('date', 1)])
            return list(cursor) 
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Could not read data from locale storage: ", e)
            return {}
        except KeyError as ke:
            return {}
        
    def read(self, limit: int) -> list[dict]:
        """
        returns a list of all entries in the database sorted by date
        """
        try:
            cursor = self._collection.find().sort([('date', -1)]).limit(limit) 
            return sorted(list(cursor), key=lambda d: d["date"]) 
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Could not read data from locale storage: ", e)
            return {}
        except KeyError as ke:
            return {}
    def read_by_dates(self, start_date: int, end_date: int) -> list[dict]:
        """
        returns a list of all entries in the database sorted by date
        """
        try:
            query = {"date": {"$gt": start_date, "$lt": end_date}}
            cursor = self._collection.find(query).sort([('date', -1)])
            return sorted(list(cursor), key=lambda d: d["date"]) 
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Could not read data from locale storage: ", e)
            return {}
        except KeyError as ke:
            return {}

    def read_by_date(self, date: int) -> dict:
        """
        using the given date string, find the matching Market Aggregate Information
        """
        try:
            return self._collection.find_one({"date": date})
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Could not read data from locale storage: ", e)
            return None
        except KeyError:
            return None
    
    def most_recent(self) -> datetime:
        recent_entry = self.read(1)
        if len(recent_entry) == 1:
            date_as_int = recent_entry[0]["date"]
            return datetime.strptime(str(date_as_int), LOCAL_DATE_FORMAT)
        else:
            raise ValueError("Currently no entries available")
        
        
    def close(self):
        self._myclient.close


def update() -> None:
    """
    checks the latest entry in the local data storage and then updates all missing data until today
    """
    local_dao = LocaleDAO()
    most_recent_date = local_dao.most_recent()
    today = datetime.now()
    update_range(datetime.strftime(most_recent_date, FINRA_DATE_FORMAT), datetime.strftime(today, FINRA_DATE_FORMAT))

def update_range(from_date: str, to_date: str) -> None:
    """
    updates the data storage with the entries specified by parameters
    parameters need to come in the following format: "mm/dd/yyyy" the finra data format
    """
    weekend = set([5, 6])
    start: datetime = datetime.strptime(from_date, FINRA_DATE_FORMAT)
    d: datetime = start
    end: datetime = datetime.strptime(to_date, FINRA_DATE_FORMAT)
    
    delta: timedelta = timedelta(days=1)
    
    local_dao: LocaleDAO = LocaleDAO()
    online_dao: OnlineReader = OnlineReader()

    print(f"collecting from {from_date} to {to_date}")

    while d <= end:
        if d.weekday() not in weekend:
            date_str = d.strftime(LOCAL_DATE_FORMAT)
            print(f"Checking {date_str}")

            # check if the entry is already existing
            data = local_dao.read_by_date(int(date_str))
            if data is None:
                try:
                    online_data = online_dao.request_data(d)
                    if d.strftime("%Y%m%d") == str(online_data["date"]):
                        local_dao.write(online_data)
                except RuntimeError as rt:
                    print(f"Could not get data for {d}: {rt}")
                time.sleep(4)    
        d += delta

def ad_chart(ad_history: list(), ad_ema=39) -> None:
    previous_ad = 100000

    ad_line = list()
    ad_dates = list()
    ad_trend = list()
    ad_ema = EMA(ad_ema)

    for entry in ad_history:
        """
        Current Day's Advancing Stock – Current Day's Declining Stocks + Previous Day's A/D Line Value
        """
        adv = entry["bond_data"]["High Yield"]["Advances"]
        dec = entry["bond_data"]["High Yield"]["Declines"]
        current_ad = adv - dec + previous_ad

        trend_value = ad_ema.add(current_ad)
        ad_trend.append(trend_value)

        ad_dates.append(datetime.strptime(str(entry["date"]), "%Y%m%d"))
        ad_line.append(current_ad)

        previous_ad = current_ad

    plt.title("Corp. High Yield Bonds A-D Line")
    plt.ylabel("Value")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
    plt.plot(ad_dates, ad_line, label="a-d line")
    plt.plot(ad_dates, ad_trend, label="5% trend")
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.show()

def ad_spy_chart(ad_history: list(), spy_history: list(), ad_ema=39, spy_ema=50) -> None:
    previous_ad = 100000

    ad_line = list()
    ad_dates = list()
    ad_trend = list()
    ad_ema = EMA(ad_ema)
    for entry in ad_history:
        """
        Current Day's Advancing Stock – Current Day's Declining Stocks + Previous Day's A/D Line Value
        """
        adv = entry["bond_data"]["High Yield"]["Advances"]
        dec = entry["bond_data"]["High Yield"]["Declines"]
        current_ad = adv - dec + previous_ad

        trend_value = ad_ema.add(current_ad)
        ad_trend.append(trend_value)

        ad_dates.append(datetime.strptime(str(entry["date"]), "%Y%m%d"))
        ad_line.append(current_ad)

        previous_ad = current_ad

    spy_dates = list()
    spy_closes = list()
    spy_trend = list()
    spy_ema = EMA(spy_ema)
    for entry in spy_history:
        close = entry["c"]
        timestamp = entry["t"]
        spy_dates.append(datetime.utcfromtimestamp(timestamp/1000))
        spy_closes.append(close)
        spy_trend.append(spy_ema.add(close))

    
    fig, ax_ad = plt.subplots()
    plt.title("SPY vs. Corp. High Yield Bonds A-D Line")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))

    ad_color = "tab:red"
    ax_ad.set_ylabel("ad-line", color=ad_color)
    ax_ad.plot(ad_dates, ad_line, color=ad_color, label="a-d line")
    #ax_ad.tick_params(axis='y', labelcolor=ax_color)
    #plt.plot(ad_dates, ad_trend, label="5% trend")
    
    ax_spy = ax_ad.twinx()  # instantiate a second axes that shares the same x-axis

    spy_color = "tab:blue"
    ax_spy.set_ylabel("SPY", color=spy_color)  # we already handled the x-label with ax1
    ax_spy.plot(spy_dates, spy_closes, color=spy_color, label="SPY")
    #ax_spy.tick_params(axis='y', labelcolor=spy_color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    
    plt.gcf().autofmt_xdate()
    #plt.legend()
    plt.show()