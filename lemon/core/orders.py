import datetime
import json
from lemon.common.requests import ApiRequest
from lemon.core.account import Account

class Order():
    status:str
    id:str
    regulatory_information:dict = None

    def __init__(self, credentials:str, space_id:str) -> None:
        self._token = credentials
        self.space_id = space_id

    def create(self, isin: str, side: str, quantity: int, venue: str, expires_at: str, stop_price: float=None, limit_price: float=None, notes: str=None):
        args = locals()
        args.pop('self')
        args['space_id'] = self.space_id

        if list(filter(lambda x: x._uuid == self.space_id, Account(self._token).spaces))[0].trading_type == "paper":
            type="paper"
        else:
            type="money"
        request = ApiRequest(type=type,
                             endpoint="/orders/",
                             method="POST",
                             body=args,
                             authorization_token=self._token
                             )
        if request.response['status'] == "ok":
            self.status = request.response['results']['status']
            self.id = request.response['results']['id']
            self.regulatory_information = request.response['results']['regulatory_information']
            self.estimated_price = request.response['results']['estimated_price']
            return f"Order with id: {self.id} created!"
        return f"Order cant be created!"


    def activate(self, pin:str=None)->str:
        if list(filter(lambda x: x._uuid == self.space_id, Account(self._token).spaces))[0].trading_type == "paper":
            type="paper"
        else:
            type="money"
            data = json.dumps({"pin": pin})


        request = ApiRequest(type=type,
                             endpoint="/orders/{}/activate/".format(self.id),
                             method="POST",
                             body=data if type=="money" else None,
                             authorization_token=self._token
                             )

        return request.response['status']

    def delete(self, pin:str=None)->str:
        if list(filter(lambda x: x._uuid == self.space_id, Account(self._token).spaces))[0].trading_type == "paper":
            type="paper"
        else:
            type="money"
            data = json.dumps({"pin": pin})


        request = ApiRequest(type=type,
                             endpoint="/orders/{}/".format(self.id),
                             method="DELETE",
                             body=data if type=="money" else None,
                             authorization_token=self._token
                             )

        return request.response['status']

    def retrieve(self, pin:str=None, *args, **kwargs)->str:
        if list(filter(lambda x: x._uuid == self.space_id, Account(self._token).spaces))[0].trading_type == "paper":
            type="paper"
        else:
            type="money"
            data = json.dumps({"pin": pin})
        request = ApiRequest(type=type,
                             endpoint="/orders/",
                             url_params = kwargs,
                             authorization_token=self._token)

        return request.response
