from core.account import Account
from core.market import MarketData
from core.orders import Order
from core.strategy import IStrategy

class LemonClient():
    def __init__:
        self.token = token


@classmethod
   def from_yaml():
    import yaml
    with open(key_path(), "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)["lemon-markets"]['api_key']


@classmethod
   def from_env():
    import os
    credential_file = os.environ.get("LEMON_CREDENTIALS")


  def account_api(self) -> Account:

  def market_api(self) -> MarketData:

  def orders_api(self): -> Order:

  def strategy_api(self): -> IStrategy:

 
