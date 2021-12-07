#from lemon.core.account import Account
#from lemon.core.market import MarketData
#from lemon.core.orders import Order
#from lemon.core.strategy import Strategy

class LemonBase():
    def __init__(self, token: str):
        self._token = token


    @classmethod
    def from_yaml(cls, config_file: str):
        import yaml
        with open(config_file, "r") as yamlfile:
            return cls(token=yaml.load(yamlfile, Loader=yaml.FullLoader)["lemon-markets"]['api_key'])



    @classmethod
    def from_env(cls):
        import os
        credential_file = os.environ.get("LEMON_CREDENTIALS")



