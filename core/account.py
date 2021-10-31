import logging
from typing import List
from urllib.parse import urlencode
import pandas as pd
from requests.api import request
from requests.models import Response
from client.auth import credentials
from common.errors import *
from common.helpers import Singleton
from common.requests import ApiRequest


from core.models import Space


class AccountState:
    _balance: float = None
    _cash_accounts: int = None
    _securities_account_number: int = None

    def fetch_account_state(self):
        request = ApiRequest(type="trading",
                             endpoint="/state/",
                             method="GET",
                             authorization_token=Account().token
                             )

        self._balance = request.response['state']['balance']
        self._cash_accounts = request.response['cash_account_number'] if not None else None
        self._cash_accounts_securities_account_number = request.response[
            'securities_account_number'] if not None else None

    @property
    def balance(self) -> float:
        self.fetch_account_state()
        return self._balance

    @property
    def cash_accounts(self) -> int:
        self.fetch_account_state()
        return self._cash_accounts

    @property
    def securities_accounts(self) -> int:
        self.fetch_account_state()
        return self._securities_account_number


class Account(AccountState, metaclass=Singleton):
    _token: str

    def __init__(self) -> None:
        super().__init__()
        self.spaces = list()
        self.__create_spaces()
        self._token = self.spaces[0].session.token

    def __create_spaces(self):
        """ Creating objects for any spaces dedicated in the credential file
        """
        for s in credentials():
            self.spaces.append(Space(credentials=s))

    def space_by_name(self, name: str) -> List[Space]:
        """ Filter spaces by name 

        Args:
            name (str): 

        Returns:
            List[Space]: [description]
        """
        return list(filter(lambda x: x.name == name, self.spaces))

    def search_instrument(self, name: str, type: str = ["stock", "bond", "fond", "ETF", "warrant"], **kwargs):
        """[summary]

        Args:
            name (str): Could be a ISIN, WKN or stock name. At least 3 charakters are needed. Otherwise an error will occur.
            type (str, optional): One type of ["stock", "bond", "fond", "ETF", "warrant"].
            kwargs** (optional): optional keyword arguments

        Keyword arguments:
            mic (string):           Enter a Market Identifier Code (MIC) in there. Default is XMUN.
            isin (string):          Specify the ISIN you are interested in. You can also specify multiple ISINs. Maximum 10 ISINs per Request.
            currency (string):      letter abbreviation, e.g. "EUR" or "USD"
            tradeable (boolean):    true or false
            limit (integer):        Needed for pagination, default is 0.

        Raises:
            ValueError:  Parameter {type} is not a valid parameter!
        """
        if len(name) < 3:
            raise ValueError(f"Paramter {name} is too short (min 3 char)!")

        if type not in ["stock", "bond", "fond", "ETF", "warrant"]:
            raise ValueError(f"Parameter {type} is not a valid parameter!")

        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        query_str = urlencode({'search': name, 'type': type}, doseq=True)

        request = ApiRequest(type="market",
                             endpoint="/instruments?{}/".format(
                                 query_str + payload),
                             method="GET",
                             authorization_token=self._token)

        if request.response != None:
            df = pd.DataFrame()
            for item in request.response:
                df = df.append(item, ignore_index=True)
            return df
        else:
            return "No instrument found!"

    def trading_venues(self, **kwargs):
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        request = ApiRequest(type="market",
                             endpoint="/venues?{}/".format(payload),
                             method="GET",
                             authorization_token=self._token)
        return request.response

    def quotes(self, isin: str, **kwargs):
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        request = ApiRequest(type="market",
                             endpoint="/quotes?isin={}{}/".format(
                                 isin, payload),
                             method="GET",
                             authorization_token=self._token)
        return request.response

    def ohlc(self, isin: str, timespan: str = ["m", "h", "d"], **kwargs):

        if timespan not in ["m", "h", "d"]:
            raise ValueError(f"Parameter {type} is not a valid parameter!")

        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        request = ApiRequest(type="market",
                             endpoint="/ohlc/{}1/?isin={}{}/".format(
                                 timespan, isin, payload),
                             method="GET",
                             authorization_token=self._token)

        return request.response

    def trades(self, mic: str, isin: str, **kwargs):
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        request = ApiRequest(type="market",
                             endpoint="/trades/?isin={}{}/".format(
                                 isin, payload),
                             method="GET",
                             authorization_token=self._token)
        return request.response

    def run(self):
        for space in self.spaces:
            space.run()

    @property
    def token(self) -> str:
        self.refresh_token()
        return self._token

    def refresh_token(self):
        self._token = self.spaces[0].session.token
