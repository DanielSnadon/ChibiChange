from sqlalchemy import create_engine
import pandas
import requests as rq
from datetime import datetime

pandas.set_option('display.max_columns', None)

def GetData(what, interval, count, to="USDT", start = '', end = ''): # Кастомная функция
    if end != "":
        end = f"&endTime={end}"
    if start !="":
        start = f"&startTime={start}"
    v1 = rq.get(f"https://api.binance.com/api/v1/klines?symbol={what}{to}&interval={interval}{start}{end}&limit={count}").json()
    return [temp[4] for temp in v1]

# snadon

engine = create_engine('sqlite:///prices.db')

btc1 = GetData(what="BTC", interval="1m", count=60)
btc2 = GetData(what="BTC", interval="1m", count=960)
btc3 = GetData(what="BTC", interval="1h", count=720)
btc4 = GetData(what="BTC", interval="1d", count=360)

eth1 = GetData(what="ETH", interval="1m", count=60)
eth2 = GetData(what="ETH", interval="1m", count=960)
eth3 = GetData(what="ETH", interval="1h", count=720)
eth4 = GetData(what="ETH", interval="1d", count=360)

bnb1 = GetData(what="BNB", interval="1m", count=60)
bnb2 = GetData(what="BNB", interval="1m", count=960)
bnb3 = GetData(what="BNB", interval="1h", count=720)
bnb4 = GetData(what="BNB", interval="1d", count=360)

xrp1 = GetData(what="XRP", interval="1m", count=60)
xrp2 = GetData(what="XRP", interval="1m", count=960)
xrp3 = GetData(what="XRP", interval="1h", count=720)
xrp4 = GetData(what="XRP", interval="1d", count=360)

sol1 = GetData(what="SOL", interval="1m", count=60)
sol2 = GetData(what="SOL", interval="1m", count=960)
sol3 = GetData(what="SOL", interval="1h", count=720)
sol4 = GetData(what="SOL", interval="1d", count=360)

ada1 = GetData(what="ADA", interval="1m", count=60)
ada2 = GetData(what="ADA", interval="1m", count=960)
ada3 = GetData(what="ADA", interval="1h", count=720)
ada4 = GetData(what="ADA", interval="1d", count=360)

doge1 = GetData(what="DOGE", interval="1m", count=60)
doge2 = GetData(what="DOGE", interval="1m", count=960)
doge3 = GetData(what="DOGE", interval="1h", count=720)
doge4 = GetData(what="DOGE", interval="1d", count=360)

dot1 = GetData(what="DOT", interval="1m", count=60)
dot2 = GetData(what="DOT", interval="1m", count=960)
dot3 = GetData(what="DOT", interval="1h", count=720)
dot4 = GetData(what="DOT", interval="1d", count=360)

eur1 = GetData(what="EUR", interval="1m", count=60)
eur2 = GetData(what="EUR", interval="1m", count=960)
eur3 = GetData(what="EUR", interval="1h", count=720)
eur4 = GetData(what="EUR", interval="1d", count=360)

amp1 = GetData(what="AMP", interval="1m", count=60)
amp2 = GetData(what="AMP", interval="1m", count=960)
amp3 = GetData(what="AMP", interval="1h", count=720)
amp4 = GetData(what="AMP", interval="1d", count=360)

pepe1 = GetData(what="PEPE", interval="1m", count=60)
pepe2 = GetData(what="PEPE", interval="1m", count=960)
pepe3 = GetData(what="PEPE", interval="1h", count=720)
pepe4 = GetData(what="PEPE", interval="1d", count=360)

ltc1 = GetData(what="LTC", interval="1m", count=60)
ltc2 = GetData(what="LTC", interval="1m", count=960)
ltc3 = GetData(what="LTC", interval="1h", count=720)
ltc4 = GetData(what="LTC", interval="1d", count=360)

print(len(btc1), len(btc2), len(btc3), len(btc4), len(eth1), len(eth2), len(eth3), len(eth4), len(bnb1), len(bnb2), len(bnb3), len(bnb4), len(xrp1), len(xrp2), len(xrp3), len(xrp4), len(sol1), len(sol2), len(sol3), len(sol4), len(ada1), len(ada2), len(ada3), len(ada4), len(doge1), len(doge2), len(doge3), len(doge4), len(dot1), len(dot2), len(dot3), len(dot4), len(eur1), len(eur2), len(eur3), len(eur4), len(amp1), len(amp2), len(amp3), len(amp4), len(pepe1), len(pepe2), len(pepe3), len(pepe4), len(ltc1), len(ltc2), len(ltc3), len(ltc4))

btc2 = [btc2[date] for date in range(len(btc2)) if (date + 1) % 16 == 0]
btc3 = [btc3[date] for date in range(len(btc3)) if (date + 1) % 12 == 0]
btc4 = [btc4[date] for date in range(len(btc4)) if (date + 1) % 6 == 0]


eth2 = [eth2[date] for date in range(len(eth2)) if (date + 1) % 16 == 0]
eth3 = [eth3[date] for date in range(len(eth3)) if (date + 1) % 12 == 0]
eth4 = [eth4[date] for date in range(len(eth4)) if (date + 1) % 6 == 0]

bnb2 = [bnb2[date] for date in range(len(bnb2)) if (date + 1) % 16 == 0]
bnb3 = [bnb3[date] for date in range(len(bnb3)) if (date + 1) % 12 == 0]
bnb4 = [bnb4[date] for date in range(len(bnb4)) if (date + 1) % 6 == 0]

xrp2 = [xrp2[date] for date in range(len(xrp2)) if (date + 1) % 16 == 0]
xrp3 = [xrp3[date] for date in range(len(xrp3)) if (date + 1) % 12 == 0]
xrp4 = [xrp4[date] for date in range(len(xrp4)) if (date + 1) % 6 == 0]

sol2 = [sol2[date] for date in range(len(sol2)) if (date + 1) % 16 == 0]
sol3 = [sol3[date] for date in range(len(sol3)) if (date + 1) % 12 == 0]
sol4 = [sol4[date] for date in range(len(sol4)) if (date + 1) % 6 == 0]

ada2 = [ada2[date] for date in range(len(ada2)) if (date + 1) % 16 == 0]
ada3 = [ada3[date] for date in range(len(ada3)) if (date + 1) % 12 == 0]
ada4 = [ada4[date] for date in range(len(ada4)) if (date + 1) % 6 == 0]

doge2 = [doge2[date] for date in range(len(doge2)) if (date + 1) % 16 == 0]
doge3 = [doge3[date] for date in range(len(doge3)) if (date + 1) % 12 == 0]
doge4 = [doge4[date] for date in range(len(doge4)) if (date + 1) % 6 == 0]

dot2 = [dot2[date] for date in range(len(dot2)) if (date + 1) % 16 == 0]
dot3 = [dot3[date] for date in range(len(dot3)) if (date + 1) % 12 == 0]
dot4 = [dot4[date] for date in range(len(dot4)) if (date + 1) % 6 == 0]

eur2 = [eur2[date] for date in range(len(eur2)) if (date + 1) % 16 == 0]
eur3 = [eur3[date] for date in range(len(eur3)) if (date + 1) % 12 == 0]
eur4 = [eur4[date] for date in range(len(eur4)) if (date + 1) % 6 == 0]

amp2 = [amp2[date] for date in range(len(amp2)) if (date + 1) % 16 == 0]
amp3 = [amp3[date] for date in range(len(amp3)) if (date + 1) % 12 == 0]
amp4 = [amp4[date] for date in range(len(amp4)) if (date + 1) % 6 == 0]

pepe2 = [pepe2[date] for date in range(len(pepe2)) if (date + 1) % 16 == 0]
pepe3 = [pepe3[date] for date in range(len(pepe3)) if (date + 1) % 12 == 0]
pepe4 = [pepe4[date] for date in range(len(pepe4)) if (date + 1) % 6 == 0]

ltc2 = [ltc2[date] for date in range(len(ltc2)) if (date + 1) % 16 == 0]
ltc3 = [ltc3[date] for date in range(len(ltc3)) if (date + 1) % 12 == 0]
ltc4 = [ltc4[date] for date in range(len(ltc4)) if (date + 1) % 6 == 0]

print(len(btc1), len(btc2), len(btc3), len(btc4), len(eth1), len(eth2), len(eth3), len(eth4), len(bnb1), len(bnb2), len(bnb3), len(bnb4), len(xrp1), len(xrp2), len(xrp3), len(xrp4), len(sol1), len(sol2), len(sol3), len(sol4), len(ada1), len(ada2), len(ada3), len(ada4), len(doge1), len(doge2), len(doge3), len(doge4), len(dot1), len(dot2), len(dot3), len(dot4), len(eur1), len(eur2), len(eur3), len(eur4), len(amp1), len(amp2), len(amp3), len(amp4), len(pepe1), len(pepe2), len(pepe3), len(pepe4), len(ltc1), len(ltc2), len(ltc3), len(ltc4))

toaster = pandas.DataFrame({"BTC/USDT/1h" : btc1,
                            "BTC/USDT/1d" : btc2,
                            "BTC/USDT/1m" : btc3,
                            "BTC/USDT/1y" : btc4,


                            "ETH/USDT/1h" : eth1,
                            "ETH/USDT/1d" : eth2,
                            "ETH/USDT/1m" : eth3,
                            "ETH/USDT/1y" : eth4,
                            
                            "BNB/USDT/1h" : bnb1,
                            "BNB/USDT/1d" : bnb2,
                            "BNB/USDT/1m" : bnb3,
                            "BNB/USDT/1y" : bnb4,
                            
                            "XRP/USDT/1h" : xrp1,
                            "XRP/USDT/1d" : xrp2,
                            "XRP/USDT/1m" : xrp3,
                            "XRP/USDT/1y" : xrp4,
                            
                            "SOL/USDT/1h" : sol1,
                            "SOL/USDT/1d" : sol2,
                            "SOL/USDT/1m" : sol3,
                            "SOL/USDT/1y" : sol4,
                            
                            "ADA/USDT/1h" : ada1,
                            "ADA/USDT/1d" : ada2,
                            "ADA/USDT/1m" : ada3,
                            "ADA/USDT/1y" : ada4,
                            
                            "DOGE/USDT/1h" : doge1,
                            "DOGE/USDT/1d" : doge2,
                            "DOGE/USDT/1m" : doge3,
                            "DOGE/USDT/1y" : doge4,

                            "DOT/USDT/1h" : dot1,
                            "DOT/USDT/1d" : dot2,
                            "DOT/USDT/1m" : dot3,
                            "DOT/USDT/1y" : dot4,
                            
                            "EUR/USDT/1h" : eur1,
                            "EUR/USDT/1d" : eur2,
                            "EUR/USDT/1m" : eur3,
                            "EUR/USDT/1y" : eur4,
                            
                            "AMP/USDT/1h" : amp1,
                            "AMP/USDT/1d" : amp2,
                            "AMP/USDT/1m" : amp3,
                            "AMP/USDT/1y" : amp4,
                            
                            "PEPE/USDT/1h" : pepe1,
                            "PEPE/USDT/1d" : pepe2,
                            "PEPE/USDT/1m" : pepe3,
                            "PEPE/USDT/1y" : pepe4,
                            
                            "LTC/USDT/1h" : ltc1,
                            "LTC/USDT/1d" : ltc2,
                            "LTC/USDT/1m" : ltc3,
                            "LTC/USDT/1y" : ltc4})

toaster.to_sql(name='table', con=engine, if_exists='replace')

print(pandas.read_sql('table', con=engine))