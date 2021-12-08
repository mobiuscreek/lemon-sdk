from lemon.core.account import Account
from lemon.core.market import MarketData
from lemon.core.orders import Order
from lemon.core.strategy import Strategy

class LemonClient():
    def __init__(self, token: str):
        self._token = token


    @classmethod
    def from_yaml(cls, config_file: str = "credentials.yml"):
        import yaml
        with open(config_file, "r") as yamlfile:
            return cls(token=yaml.load(yamlfile, Loader=yaml.FullLoader)["lemon-markets"]['api_key'])


    @classmethod
    def from_env(cls):
        import os
        credential_file = os.environ.get("LEMON_CREDENTIALS")


    def account_api(self):
        return Account(self._token)

    def order_api(self, *args, **kwargs):
        return Order(self._token, *args, **kwargs)

    def market_api(self):
        return MarketData(self._token)
    
    def strategy_api(self):
        return Strategy(self._token)

