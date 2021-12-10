# ![](https://www.lemon.markets/images/logo.svg?auto=format&fit=max&w=3840) 

# Unoffical Python SDK for lemon.markets trading API

## What features are currently included in this SDK?
- [x] Management of account properties and spaces
- [x] Creating, deleting and executing market orders
- [x] Receiving historical (m1, h1, d1) market data  
- [x] Searching for instruments, funds, etfs, etc. 
- [x] Creating and executing strategies in separate spaces  
- [x] Pagination handling
- [ ] Backtesting of strategies

## Install

Running following command will install all project dependencies. You have to install python and poetry first or using pip by default.
```python
$ poetry install
```
or 
```python
$ pip install -r requirements.txt
```
## How to start? 

1. Grab your api key on dashboard.lemon.markets 

2. Configure LemonMarketsClient

* via YAML file
  Create a credentials yml file with the following structure (by default it uses `credentials.yml`):

```yaml
lemon-markets:
    api_key: ************************eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsIweVBkVkRESkp0bk5RS0p3aDFWNlBKTExGa3MwWFREZjVWIn0.elT8WO-wati-pSP3eMxVqgOBZCmOhykyRQru36mWsng*************************

```

``` 
from lemon.client.lemon_client import LemonMarketsClient

client = LemonMarketsClient.from_yaml()
```

* via environment variables

export your Lemon Markets api key as follows:


```shell
export LEMON_CREDENTIALS=<YOUR-API-KEY>
```

then:

```

from lemon.client.lemon_client import LemonMarketsClient

client = LemonMarketsClient.from_env()
```

* as an argument

```

from lemon.client.lemon_client import LemonMarketsClient

client = LemonMarketsClient('YOUR-API-KEY')
```


## How to use?
For a detailed example usage please open up the example_usage.ipynb notebook.

Use the client to commnunicate with any of the APIs (Account, Order, Market)

### Account API

```Python

from lemon.client.lemon_client import LemonMarketsClient

client = LemonMarketsClient.from_yaml()

acc = client.account_api()


# list your spaces
$ acc.spaces
[Space(Name: MasterStrategy, Buying_power: 500000000.0, Risk_limit: 500000000.0, Trading_type: paper,
 Space(Name: Default, Buying_power: 100000000.0, Risk_limit: 100000000.0, Trading_type: paper]
```

### Market API

```python

m = client.market_api()

# 
$ m = MarketData()
$ m.search_instrument("MSCI")
Collecting 504 results....
             isin     wkn                       name  \
0    LU1291100664  A2ADBR   BNPPE-MSCI EXUKXCW UECEO   
1    DE000ETFL086  ETFL08          DK MSCI EUROPE LC   
2    DE000ETFL102  ETFL10           DK MSCI JAPAN LC   
3    DE000ETFL268  ETFL26                DK MSCI USA   
4    DE000ETFL284  ETFL28             DK MSCI EUROPE   
..            ...     ...                        ...   
499  LU1753045415  A2JFSU    BNPPE-M.EUR.SRI SS5 DIS   
500  LU1923627332  LYX01C  MUL-LYX.MSCI RUSSI.DIS.LS   
501  LU2109787049  A2PZC5  AIS-A.MSCI WESGUS UETFDRC   
502  LU2153616326  A2P22T  AMUNDI MUSESGLS ETFDR HEO   
503  LU2233156749  A2QEUK  AIS-I.M.JAP.SRI UC.E.DRYN   

                              title symbol type  \
0    BNP P.EASY-MSCI EU.EX UK EX CW   EEXU  etf   
1     DEKA MSCI EUROPE LC UCITS ETF   EL4H  etf   
2      DEKA MSCI JAPAN LC UCITS ETF   EL4J  etf   
3           DEKA MSCI USA UCITS ETF   EL4Z  etf   
4        DEKA MSCI EUROPE UCITS ETF   EL42  etf   
..                              ...    ...  ...   
499   BNPPE-MSCI EUR.SRI S-SER.5%C.   ZSRI  etf   
500  M.U.L.-LYXOR MSCI RUSSI.UC.ETF   RUSL  etf   
501   AIS-AMUNDI MSCI EM.ESG U.SEL.   SBIM  etf   
502  AIS-AMUNDI MSCI US.ESG LD.SEL.   SADH  etf   
503        AIS-INDEX MSCI JAPAN SRI   JARI  etf
show more (open the raw output data in a text editor) ...

500  [{'name': 'Börse München - Gettex', 'title': '...  
501  [{'name': 'Börse München - Gettex', 'title': '...  
502  [{'name': 'Börse München - Gettex', 'title': '...  
503  [{'name': 'Börse München - Gettex', 'title': '...  


$ m.ohlc(isin="DE0005933931",timespan="h", start="2021-11-01",end="2021-11-26")
         isin       o       h       l       c  \
0   DE0005933931  133.60  133.66  133.46  133.60   
1   DE0005933931  133.84  134.30  133.80  134.26   
2   DE0005933931  134.26  134.40  134.20  134.20   
3   DE0005933931  134.32  134.32  134.12  134.12   
4   DE0005933931  134.12  134.12  133.96  134.10   
5   DE0005933931  133.90  133.94  133.90  133.90   
6   DE0005933931  133.90  133.90  133.80  133.86   
7   DE0005933931  133.70  133.88  133.70  133.88   
8   DE0005933931  134.12  134.16  134.08  134.16  
...

$ m.quotes(isin="DE0005933931",mic="XMUN")
  isin	        b_v	a_v	  b	      a	              t	                mic
	DE0005933931	160	160	130.04	130.1	2021-11-29T17:20:55.000+00:00	XMUN
```

### Order API


```Python

from lemon.client.lemonmarkets_client import LemonMarketsClient
client = LemonMarketsClient.from_yaml()

# The space has to be passed so we have to read it from the Account API

account = client.account_api()
space = account.space_by_name('Test')[0]._uuid
order = client.order_api(space) # Or paste it directly here

order.create(isin="US19260Q1076",quantity=1,side="buy",venue="XMUN",expires_at="p2d")


order.activate()

```
