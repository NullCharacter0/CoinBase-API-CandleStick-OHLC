from requests import get 
from time import time
import pandas as pd 



baseurl = "https://api.coinbase.com/api/v3/brokerage/products/"


class Prices:
    # GET "https://api.coinbase.com/api/v3/brokerage/products/"

    def __init__(self, currency="ETH-USD") -> None:
        self.currency = currency
        self.data_frame = self.get_df()

    def get_df(self):
        """
        HARD-CODED TODO: Create more flexable func
        Function used to retrive and store candle stick data
        :return: Pandas,DataFrame
        """
        now = int(time())  # UNIX TimeStamp: Rounded off to SECONDS
        limit = 300  # Candle you want to Produce MAX: 300

        # granulatry set for 5 minutes
        t_window = (5 * limit) * 60  # (granlatry * limit) * ConversionIntoSeconds
        end = str(now)  # Convert to String
        start = str(now - t_window)  # Subtract 90000 seconds
        df = pd.DataFrame

        # .                                                   CoinBase: pkease stop this vvvvvvvvvvv
        fullurl = f"{baseurl}{self.currency}/candles?start={start}&end={end}&granularity=FIVE_MINUTE"
        try:  # .                                                                        ^^^^^^^^^^^

            r = get(fullurl, auth=CoinbaseWalletAuth(api, secretkey))
            df = df(data=r.json().get("candles")[::-1])  # [::-1] is to flip the data
        except Exception as e:
            print(e)
        df["start"] = pd.to_datetime(df["start"], unit="s")  # Convert timestamps into readable
        df = df.set_index("start", drop=True)  # set new index
        df = df[["open", "high", "low", "close", "volume"]]  # Correctly order the columns
        return df.astype(float)  # convert from string to float

