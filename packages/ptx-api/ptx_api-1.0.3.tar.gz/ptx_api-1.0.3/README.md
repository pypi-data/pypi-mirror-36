# ptx_api

A Python Module for get data from PTX.

## Install

```bash
pip install ptx-api
```

## Usage

Create a `PTX` object.
```python
>>> from ptx_api import PTX
>>> ptx = PTX("api_id", "api_key")
```

Use `get()` to get resource from PTX platform.
```python
>>> ptx.get("/v2/Bus/Route/city/Taipei", params={"$top": 5})
[{'RouteUID': 'TPE10132', 'RouteID': '10132', 'HasSubRoutes': True, 'Operators': [{'OperatorID': '100', 'OperatorName': {'Zh_tw': '臺北客運', 'En': 'Taipei Bus Co., Ltd.'}, 'OperatorCode': 'TaipeiBus', 'OperatorNo': '1407'}], 'AuthorityID': '004', 'ProviderID': '045', 'SubRoutes': [{'SubRouteUID': 'TPE101320', 'SubRouteID': '101320', 'OperatorIDs': ['100'], 'SubRouteName': {'Zh_tw': '234', 'En': '234'}, 'Direction': 0, 'FirstBusTime': '0450', 'LastBusTime': '2240', 'HolidayFirstBusTime': '0450'},
...
```

## Source
[![公共運輸整合資訊流通服務平臺（Public Transport data eXchange, PTX）](https://imgur.com/wp2gOeU.png)](http://ptx.transportdata.tw/PTX)