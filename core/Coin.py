import requests
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt
import numpy as np
import os


class Coin:
    def __init__(self, name: str, currency: str):
        self.name = name
        self.price = None
        self.history = []
        self.currency = currency

    def get_price(self):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.name}&vs_currencies={self.currency}"
        response = requests.get(url).json()
        price = response[self.name][self.currency]
        self.price = price

    def get_historical_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0"}
        url = f"https://www.coingecko.com/en/coins/{self.name}/historical_data/{self.currency}#panel"
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "lxml")

        rows = [row for row in soup.find_all("tr")][1:]

        for row in rows:
            date = row.find("th").text
            market_cap = row.find_all("td")[0].text.replace(
                "\n", "").replace("$", "").replace(",", "").replace(self.currency.upper(), "")
            volume = row.find_all("td")[1].text.replace(
                "\n", "").replace("$", "").replace(",", "").replace(self.currency.upper(), "")
            open_price = row.find_all("td")[2].text.replace(
                "\n", "").replace("$", "").replace(",", "").replace(self.currency.upper(), "")
            close_price = row.find_all("td")[3].text.replace(
                "\n", "").replace("$", "").replace(",", "").replace(self.currency.upper(), "")

            if close_price == "N/A":
                close_price = np.nan

            out = {
                "date": date,
                "market_cap": market_cap,
                "volume": volume,
                "open_price": open_price,
                "close_price": close_price
            }

            self.history.append(out)

    def generate_chart(self):
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
        x_axis = [x["date"] for x in self.history]
        x_axis.reverse()

        # AX1
        open_price_y_axis = [float(x["open_price"]) for x in self.history]
        close_price_y_axis = [float(x["close_price"]) for x in self.history]
        open_price_y_axis.reverse()
        close_price_y_axis.reverse()

        ax1.plot(x_axis, open_price_y_axis, label="Open")
        ax1.plot(x_axis, close_price_y_axis, label="Close")
        ax1.set_title(f"30 days historical data for {self.name}")
        ax1.axes.xaxis.set_visible(False)
        ax1.legend()

        # AX2
        volume_y_axis = [float(x["volume"]) for x in self.history]
        market_cap_y_axis = [float(x["market_cap"]) for x in self.history]
        volume_y_axis.reverse()
        market_cap_y_axis.reverse()
        ax2.plot(x_axis, volume_y_axis, label="Volume")
        ax2.plot(x_axis, market_cap_y_axis, label="Market Cap")
        ax2.legend()

        # PLT
        plt.setp(ax1.get_xticklabels(), rotation=90, fontsize=6)
        plt.setp(ax2.get_xticklabels(), rotation=90, fontsize=6)
        plt.ylabel(self.currency.upper())
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.12)
        path = "./src/img/"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig('./src/img/chart.png')
        plt.close()
