import urllib3
import os
import json
import configparser

class PolygonIO():

    def __init__(self):
        # open a connection to a URL using urllib3
        self._http = urllib3.PoolManager()
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.__api_key__ = config.get("API-KEY","polygon")

    def lookupSymbol(self, symbol):
        """Look up ticker data from online API."""

        # contact API
        url = f"https://api.polygon.io/v3/reference/tickers/{symbol}?apiKey={self.__api_key__}"
        response = self._http.request(url)
        response.raise_for_status()
        return response.json()
        

    def lookupHistory(self, symbol, startDate, endDate):
        """Look up history for symbol from online API."""

        # Contact API
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{startDate}/{endDate}?adjusted=true&sort=asc&apiKey={self.__api_key__}"
        print(url)
        response = self._http.request("GET", url)
        print(f"Response for {response.geturl()}: {response.status} ... ")
        # print(response.data)

        decoded = response.data.decode("utf-8")
        return json.loads(decoded)