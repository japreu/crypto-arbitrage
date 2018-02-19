import ccxt
import json
from tqdm import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
import scipy as sp
import scipy.stats
import requests

binance = ccxt.binance() # USDT
bitfinex = ccxt.bitfinex() # USD
kraken = ccxt.kraken() # USD
okex = ccxt.okex() # USDT
bittrex = ccxt.bittrex() # USDT
hitbtc = ccxt.hitbtc() # USDT
gdax = ccxt.gdax() # USD
poloniex = ccxt.poloniex() # USDT
southxchange = ccxt.southxchange() # USD
independentreserve = ccxt.independentreserve() # USD
coingi = ccxt.coingi() # USD
quadrigacx = ccxt.quadrigacx() # USD
bibox = ccxt.bibox() # USDT
gateio = ccxt.gateio() # USDT
huobi = ccxt.huobi() # USDT
okcoinusd = ccxt.okcoinusd() # USD
okex = ccxt.okex() # USDT
cex = ccxt.cex() # USD
bitbay = ccxt.bitbay() # USD
bitlish = ccxt.bitlish() # USD
bl3p = ccxt.bl3p() # EUR
ccex = ccxt.ccex() # USD
paymium = ccxt.paymium() # USD
virwox = ccxt.virwox() # USD
paymium = ccxt.paymium() # USD
ccex = ccxt.ccex() # USD
anxpro = ccxt.anxpro() # USD
bitz = ccxt.bitz() # USD
gatecoin = ccxt.gatecoin() # USD
kucoin = ccxt.kucoin() # USD
mixcoins = ccxt.mixcoins() # USD
btcx = ccxt.btcx() # USD
coinexchange = ccxt.coinexchange() # USD
coinsecure = ccxt.coinsecure() # USD
bitcoincoid = ccxt.bitcoincoid() # USD
coincheck = ccxt.coincheck() # USD
bit2c = ccxt.bit2c() # USD
anxpro = ccxt.anxpro() # USD
binance = ccxt.binance() # USD
bitflyer = ccxt.bitflyer() # USD
btcbox = ccxt.btcbox() # USD
coincheck = ccxt.coincheck() # USD
coinexchange = ccxt.coinexchange() # USD
quoinex = ccxt.quoinex() # USD
zaif = ccxt.zaif() # USD
therock = ccxt.therock() # USD
bitso = ccxt.bitso() # USD
bl3p = ccxt.bl3p() # USD
anxpro = ccxt.anxpro() # USD
cryptopia = ccxt.cryptopia() # USD
independentreserve = ccxt.independentreserve() # USD
wex = ccxt.wex() # USD
urdubit = ccxt.urdubit() # USD
_1btcxe = ccxt._1btcxe() # USD
coingi = ccxt.coingi() # USD
btcexchange = ccxt.btcexchange() # USD
bitbay = ccxt.bitbay() # USD
bitmarket = ccxt.bitmarket() # USD
bitlish = ccxt.bitlish() # USD
cex = ccxt.cex() # USD
exmo = ccxt.exmo() # USD
getbtc = ccxt.getbtc() # USD
livecoin = ccxt.livecoin() # USD
xbtce = ccxt.xbtce() # USD
yobit = ccxt.yobit() # USD
bitmex = ccxt.bitmex() # USD
anxpro = ccxt.anxpro() # USD
fybsg = ccxt.fybsg() # USD
luno = ccxt.luno() # EUR
quoinex = ccxt.quoinex() # USD
bibox = ccxt.bibox() # USDT
lykke = ccxt.lykke() # USD
cobinhood = ccxt.cobinhood() # USD
bitlish = ccxt.bitlish() # USD
bitstamp = ccxt.bitstamp() # USD
coinfloor = ccxt.coinfloor() # USD
dsx = ccxt.dsx() # USD
livecoin = ccxt.livecoin() # USD
tidex = ccxt.tidex() # USDT
liqui = ccxt.liqui() # USDT
gemini = ccxt.gemini() # USD
itbit = ccxt.itbit() # USD

#huobi = ccxt.huobi() # USDT
#coinone = ccxt.coinone() # KRW
#bithumb = ccxt.bithumb() # KRW


def check_vola(exchange, coin, opportunity):

    r = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=' + coin + '&tsym=BTC&limit=101&e=' + exchange)
    response = r.json()
    exchange_price_data = response['Data']

    r = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=' + coin + '&tsym=BTC&limit=101&e=Binance')
    response = r.json()
    binance_price_data = response['Data']
    
    
    #########################################
    
    ex_avg = []
    for ex in exchange_price_data:
        ex_avg.append((ex['high']+ex['low']) / 2)
    
    bi_avg = []
    for bi in binance_price_data:
        bi_avg.append((bi['high']+bi['low']) / 2)
        
    ex_change = []
    for i in range(len(ex_avg)-1):
        yesterday = ex_avg[i]
        today = ex_avg[i + 1]
        ex_change.append(((today - yesterday) / yesterday) * 100)
    
    bi_change = []
    for i in range(len(bi_avg)-1):
        yesterday = bi_avg[i]
        today = bi_avg[i + 1]
        bi_change.append(((today - yesterday) / yesterday) * 100)
        
        
    #########################################
    
    
    if opportunity < 0: # negative percentages ; buy on binance; check exchange price vola
        prices = ex_change
        buy_signal = 'buy on binance'
    else: # positive percentages
        prices = bi_change
        buy_signal = 'buy on ' + exchange
        

    # select "receiving' exchange and check volatility 
    confidence = mean_confidence_interval(prices)
    confidence_left = confidence[0]
    confidence_right = confidence[1]
    
    if abs(opportunity) >= abs(confidence_left) and abs(opportunity) >= abs(confidence_right):
        if get_volume(coin, exchange) >= 3 and get_volume(coin, 'binance') >= 3:
            print()
            print(exchange, coin)
            print('Opportunity:', opportunity)
            print('Confidence:', confidence)
            print(buy_signal)
            plot_standard_dist(prices)
            print()
        
        else:
            print(coin, 'volume lower than 3 BTC/hour')
    else:
        print(coin, exchange, 'opportunity not in confidence interval')
    
def plot_standard_dist(change):
    plt.hist(change,99)
    plt.show()
    
def get_volume(coin, exchange):
    try:
        r = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=' + coin + '&tsym=BTC&limit=1&aggregate=1&e=' + exchange)
        response = r.json()
        return response['Data'][0]['volumeto']
    except:
        return 0
    
def get_fiat(exchange):
    
    if exchange == 'okex':
        fiat = 'USDT'
    elif exchange == 'bitfinex':
        fiat = 'USD'
    elif exchange == 'bittrex':
        fiat = 'USDT'
    elif exchange == 'huobi':
        fiat = 'USD'
    elif exchange == 'hitbtc':
        fiat = 'USDT'
    elif exchange == 'gdax':
        fiat = 'USD'
    elif exchange == 'poloniex':
        fiat = 'USDT'
    elif exchange == 'kraken':
        fiat = 'USD'

elif exchange == 'southxchange': fiat = 'USD'
elif exchange == 'acx': fiat = 'AUD'
elif exchange == 'btcmarkets': fiat = 'AUD'
elif exchange == 'coinspot': fiat = 'AUD'
elif exchange == 'independentreserve': fiat = 'USD'
elif exchange == 'braziliex': fiat = 'BRL'
elif exchange == 'flowbtc': fiat = 'BRL'
elif exchange == 'foxbit': fiat = 'BRL'
elif exchange == 'mercado': fiat = 'BRL'
elif exchange == 'coingi': fiat = 'USD'
elif exchange == 'quadrigacx': fiat = 'USD'
elif exchange == 'chilebit': fiat = 'CLP'
elif exchange == 'bibox': fiat = 'USDT'
elif exchange == 'gateio': fiat = 'USDT'
elif exchange == 'huobi': fiat = 'USDT'
elif exchange == 'okcoinusd': fiat = 'USD'
elif exchange == 'okex': fiat = 'USDT'
elif exchange == 'cex': fiat = 'USD'
elif exchange == 'coinmate': fiat = 'CZK'
elif exchange == 'bitbay': fiat = 'USD'
elif exchange == 'bitlish': fiat = 'USD'
elif exchange == 'bitmarket': fiat = 'PLN'
elif exchange == 'bl3p': fiat = 'EUR'
elif exchange == 'ccex': fiat = 'USD'
elif exchange == 'paymium': fiat = 'USD'
elif exchange == 'virwox': fiat = 'USD'
elif exchange == 'paymium': fiat = 'USD'
elif exchange == 'ccex': fiat = 'USD'
elif exchange == 'anxpro': fiat = 'USD'
elif exchange == 'bitz': fiat = 'USD'
elif exchange == 'gatecoin': fiat = 'USD'
elif exchange == 'kucoin': fiat = 'USD'
elif exchange == 'mixcoins': fiat = 'USD'
elif exchange == 'btcx': fiat = 'USD'
elif exchange == 'coinexchange': fiat = 'USD'
elif exchange == 'coinsecure': fiat = 'USD'
elif exchange == 'bitcoincoid': fiat = 'USD'
elif exchange == 'coincheck': fiat = 'USD'
elif exchange == 'bit2c': fiat = 'USD'
elif exchange == 'anxpro': fiat = 'USD'
elif exchange == 'binance': fiat = 'USD'
elif exchange == 'bitflyer': fiat = 'USD'
elif exchange == 'btcbox': fiat = 'USD'
elif exchange == 'coincheck': fiat = 'USD'
elif exchange == 'coinexchange': fiat = 'USD'
elif exchange == 'quoinex': fiat = 'USD'
elif exchange == 'zaif': fiat = 'USD'
elif exchange == 'therock': fiat = 'USD'
elif exchange == 'bitso': fiat = 'USD'
elif exchange == 'bl3p': fiat = 'USD'
elif exchange == 'anxpro': fiat = 'USD'
elif exchange == 'cryptopia': fiat = 'USD'
elif exchange == 'independentreserve': fiat = 'USD'
elif exchange == 'wex': fiat = 'USD'
elif exchange == 'urdubit': fiat = 'USD'
elif exchange == '_1btcxe': fiat = 'USD'
elif exchange == 'coingi': fiat = 'USD'
elif exchange == 'btcexchange': fiat = 'USD'
elif exchange == 'bitbay': fiat = 'USD'
elif exchange == 'bitmarket': fiat = 'USD'
elif exchange == 'bitlish': fiat = 'USD'
elif exchange == 'cex': fiat = 'USD'
elif exchange == 'exmo': fiat = 'USD'
elif exchange == 'getbtc': fiat = 'USD'
elif exchange == 'livecoin': fiat = 'USD'
elif exchange == 'xbtce': fiat = 'USD'
elif exchange == 'yobit': fiat = 'USD'
elif exchange == 'bitmex': fiat = 'USD'
elif exchange == 'anxpro': fiat = 'USD'
elif exchange == 'fybsg': fiat = 'USD'
elif exchange == 'luno': fiat = 'EUR'
elif exchange == 'quoinex': fiat = 'USD'
elif exchange == 'bibox': fiat = 'USDT'
elif exchange == 'lykke': fiat = 'USD'
elif exchange == 'cobinhood': fiat = 'USD'
elif exchange == 'bitlish': fiat = 'USD'
elif exchange == 'bitstamp': fiat = 'USD'
elif exchange == 'coinfloor': fiat = 'USD'
elif exchange == 'dsx': fiat = 'USD'
elif exchange == 'livecoin': fiat = 'USD'
elif exchange == 'tidex': fiat = 'USDT'
elif exchange == 'liqui': fiat = 'USDT'
elif exchange == 'gemini': fiat = 'USD'
elif exchange == 'itbit': fiat = 'USD'
        
    return fiat

def get_ticker(exchange):
    
    fiat = get_fiat(exchange)
    
    if exchange == 'okex':
        ticker = okex.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'bitfinex':
        ticker = bitfinex.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'bittrex':
        ticker = bittrex.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'huobi':
        ticker = huobi.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'hitbtc':
        ticker = hitbtc.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'gdax':
        ticker = gdax.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'poloniex':
        ticker = poloniex.fetch_ticker('BTC/' + fiat)['last']
    elif exchange == 'kraken':
        ticker = kraken.fetch_ticker('BTC/' + fiat)['last']

if exchange == 'southxchange':
        ticker = southxchange.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'acx':
        ticker = acx.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'btcmarkets':
        ticker = btcmarkets.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coinspot':
        ticker = coinspot.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'independentreserve':
        ticker = independentreserve.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'braziliex':
        ticker = braziliex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'flowbtc':
        ticker = flowbtc.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'foxbit':
        ticker = foxbit.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'mercado':
        ticker = mercado.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coingi':
        ticker = coingi.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'quadrigacx':
        ticker = quadrigacx.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'chilebit':
        ticker = chilebit.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bibox':
        ticker = bibox.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'gateio':
        ticker = gateio.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'huobi':
        ticker = huobi.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'okcoinusd':
        ticker = okcoinusd.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'okex':
        ticker = okex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'cex':
        ticker = cex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coinmate':
        ticker = coinmate.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitbay':
        ticker = bitbay.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitlish':
        ticker = bitlish.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitmarket':
        ticker = bitmarket.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bl3p':
        ticker = bl3p.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'ccex':
        ticker = ccex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'paymium':
        ticker = paymium.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'virwox':
        ticker = virwox.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'paymium':
        ticker = paymium.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'ccex':
        ticker = ccex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'anxpro':
        ticker = anxpro.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitz':
        ticker = bitz.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'gatecoin':
        ticker = gatecoin.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'kucoin':
        ticker = kucoin.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'mixcoins':
        ticker = mixcoins.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'btcx':
        ticker = btcx.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coinexchange':
        ticker = coinexchange.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coinsecure':
        ticker = coinsecure.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitcoincoid':
        ticker = bitcoincoid.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coincheck':
        ticker = coincheck.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bit2c':
        ticker = bit2c.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'anxpro':
        ticker = anxpro.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'binance':
        ticker = binance.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitflyer':
        ticker = bitflyer.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'btcbox':
        ticker = btcbox.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coincheck':
        ticker = coincheck.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coinexchange':
        ticker = coinexchange.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'quoinex':
        ticker = quoinex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'zaif':
        ticker = zaif.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'therock':
        ticker = therock.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitso':
        ticker = bitso.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bl3p':
        ticker = bl3p.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'anxpro':
        ticker = anxpro.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'cryptopia':
        ticker = cryptopia.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'independentreserve':
        ticker = independentreserve.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'wex':
        ticker = wex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'urdubit':
        ticker = urdubit.fetch_ticker('BTC/' + fiat)['last']
if exchange == '_1btcxe':
        ticker = _1btcxe.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coingi':
        ticker = coingi.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'btcexchange':
        ticker = btcexchange.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitbay':
        ticker = bitbay.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitmarket':
        ticker = bitmarket.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitlish':
        ticker = bitlish.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'cex':
        ticker = cex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'exmo':
        ticker = exmo.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'getbtc':
        ticker = getbtc.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'livecoin':
        ticker = livecoin.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'xbtce':
        ticker = xbtce.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'yobit':
        ticker = yobit.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitmex':
        ticker = bitmex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'anxpro':
        ticker = anxpro.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'fybsg':
        ticker = fybsg.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'luno':
        ticker = luno.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'quoinex':
        ticker = quoinex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bibox':
        ticker = bibox.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'lykke':
        ticker = lykke.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'cobinhood':
        ticker = cobinhood.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitlish':
        ticker = bitlish.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'bitstamp':
        ticker = bitstamp.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'coinfloor':
        ticker = coinfloor.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'dsx':
        ticker = dsx.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'livecoin':
        ticker = livecoin.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'tidex':
        ticker = tidex.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'liqui':
        ticker = liqui.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'gemini':
        ticker = gemini.fetch_ticker('BTC/' + fiat)['last']
if exchange == 'itbit':
        ticker = itbit.fetch_ticker('BTC/' + fiat)['last']
        
    return ticker

def get_pair(exchange, pair):
    
    if exchange == 'okex':
        pair = okex.fetch_ticker(pair)['last']
    elif exchange == 'bitfinex':
        pair = bitfinex.fetch_ticker(pair)['last']
    elif exchange == 'bittrex':
        pair = bittrex.fetch_ticker(pair)['last']
    elif exchange == 'huobi':
        pair = huobi.fetch_ticker(pair)['last']
    elif exchange == 'hitbtc':
        pair = hitbtc.fetch_ticker(pair)['last']
    elif exchange == 'gdax':
        pair = gdax.fetch_ticker(pair)['last']
    elif exchange == 'poloniex':
        pair = poloniex.fetch_ticker(pair)['last']
    elif exchange == 'kraken':
        pair = kraken.fetch_ticker(pair)['last']

elif exchange == 'southxchange':
        pair = southxchange.fetch_ticker(pair)['last']
elif exchange == 'acx':
        pair = acx.fetch_ticker(pair)['last']
elif exchange == 'btcmarkets':
        pair = btcmarkets.fetch_ticker(pair)['last']
elif exchange == 'coinspot':
        pair = coinspot.fetch_ticker(pair)['last']
elif exchange == 'independentreserve':
        pair = independentreserve.fetch_ticker(pair)['last']
elif exchange == 'braziliex':
        pair = braziliex.fetch_ticker(pair)['last']
elif exchange == 'flowbtc':
        pair = flowbtc.fetch_ticker(pair)['last']
elif exchange == 'foxbit':
        pair = foxbit.fetch_ticker(pair)['last']
elif exchange == 'mercado':
        pair = mercado.fetch_ticker(pair)['last']
elif exchange == 'coingi':
        pair = coingi.fetch_ticker(pair)['last']
elif exchange == 'quadrigacx':
        pair = quadrigacx.fetch_ticker(pair)['last']
elif exchange == 'chilebit':
        pair = chilebit.fetch_ticker(pair)['last']
elif exchange == 'bibox':
        pair = bibox.fetch_ticker(pair)['last']
elif exchange == 'gateio':
        pair = gateio.fetch_ticker(pair)['last']
elif exchange == 'huobi':
        pair = huobi.fetch_ticker(pair)['last']
elif exchange == 'okcoinusd':
        pair = okcoinusd.fetch_ticker(pair)['last']
elif exchange == 'okex':
        pair = okex.fetch_ticker(pair)['last']
elif exchange == 'cex':
        pair = cex.fetch_ticker(pair)['last']
elif exchange == 'coinmate':
        pair = coinmate.fetch_ticker(pair)['last']
elif exchange == 'bitbay':
        pair = bitbay.fetch_ticker(pair)['last']
elif exchange == 'bitlish':
        pair = bitlish.fetch_ticker(pair)['last']
elif exchange == 'bitmarket':
        pair = bitmarket.fetch_ticker(pair)['last']
elif exchange == 'bl3p':
        pair = bl3p.fetch_ticker(pair)['last']
elif exchange == 'ccex':
        pair = ccex.fetch_ticker(pair)['last']
elif exchange == 'paymium':
        pair = paymium.fetch_ticker(pair)['last']
elif exchange == 'virwox':
        pair = virwox.fetch_ticker(pair)['last']
elif exchange == 'paymium':
        pair = paymium.fetch_ticker(pair)['last']
elif exchange == 'ccex':
        pair = ccex.fetch_ticker(pair)['last']
elif exchange == 'anxpro':
        pair = anxpro.fetch_ticker(pair)['last']
elif exchange == 'bitz':
        pair = bitz.fetch_ticker(pair)['last']
elif exchange == 'gatecoin':
        pair = gatecoin.fetch_ticker(pair)['last']
elif exchange == 'kucoin':
        pair = kucoin.fetch_ticker(pair)['last']
elif exchange == 'mixcoins':
        pair = mixcoins.fetch_ticker(pair)['last']
elif exchange == 'btcx':
        pair = btcx.fetch_ticker(pair)['last']
elif exchange == 'coinexchange':
        pair = coinexchange.fetch_ticker(pair)['last']
elif exchange == 'coinsecure':
        pair = coinsecure.fetch_ticker(pair)['last']
elif exchange == 'bitcoincoid':
        pair = bitcoincoid.fetch_ticker(pair)['last']
elif exchange == 'coincheck':
        pair = coincheck.fetch_ticker(pair)['last']
elif exchange == 'bit2c':
        pair = bit2c.fetch_ticker(pair)['last']
elif exchange == 'anxpro':
        pair = anxpro.fetch_ticker(pair)['last']
elif exchange == 'binance':
        pair = binance.fetch_ticker(pair)['last']
elif exchange == 'bitflyer':
        pair = bitflyer.fetch_ticker(pair)['last']
elif exchange == 'btcbox':
        pair = btcbox.fetch_ticker(pair)['last']
elif exchange == 'coincheck':
        pair = coincheck.fetch_ticker(pair)['last']
elif exchange == 'coinexchange':
        pair = coinexchange.fetch_ticker(pair)['last']
elif exchange == 'quoinex':
        pair = quoinex.fetch_ticker(pair)['last']
elif exchange == 'zaif':
        pair = zaif.fetch_ticker(pair)['last']
elif exchange == 'therock':
        pair = therock.fetch_ticker(pair)['last']
elif exchange == 'bitso':
        pair = bitso.fetch_ticker(pair)['last']
elif exchange == 'bl3p':
        pair = bl3p.fetch_ticker(pair)['last']
elif exchange == 'anxpro':
        pair = anxpro.fetch_ticker(pair)['last']
elif exchange == 'cryptopia':
        pair = cryptopia.fetch_ticker(pair)['last']
elif exchange == 'independentreserve':
        pair = independentreserve.fetch_ticker(pair)['last']
elif exchange == 'wex':
        pair = wex.fetch_ticker(pair)['last']
elif exchange == 'urdubit':
        pair = urdubit.fetch_ticker(pair)['last']
elif exchange == '_1btcxe':
        pair = _1btcxe.fetch_ticker(pair)['last']
elif exchange == 'coingi':
        pair = coingi.fetch_ticker(pair)['last']
elif exchange == 'btcexchange':
        pair = btcexchange.fetch_ticker(pair)['last']
elif exchange == 'bitbay':
        pair = bitbay.fetch_ticker(pair)['last']
elif exchange == 'bitmarket':
        pair = bitmarket.fetch_ticker(pair)['last']
elif exchange == 'bitlish':
        pair = bitlish.fetch_ticker(pair)['last']
elif exchange == 'cex':
        pair = cex.fetch_ticker(pair)['last']
elif exchange == 'exmo':
        pair = exmo.fetch_ticker(pair)['last']
elif exchange == 'getbtc':
        pair = getbtc.fetch_ticker(pair)['last']
elif exchange == 'livecoin':
        pair = livecoin.fetch_ticker(pair)['last']
elif exchange == 'xbtce':
        pair = xbtce.fetch_ticker(pair)['last']
elif exchange == 'yobit':
        pair = yobit.fetch_ticker(pair)['last']
elif exchange == 'bitmex':
        pair = bitmex.fetch_ticker(pair)['last']
elif exchange == 'anxpro':
        pair = anxpro.fetch_ticker(pair)['last']
elif exchange == 'fybsg':
        pair = fybsg.fetch_ticker(pair)['last']
elif exchange == 'luno':
        pair = luno.fetch_ticker(pair)['last']
elif exchange == 'quoinex':
        pair = quoinex.fetch_ticker(pair)['last']
elif exchange == 'bibox':
        pair = bibox.fetch_ticker(pair)['last']
elif exchange == 'lykke':
        pair = lykke.fetch_ticker(pair)['last']
elif exchange == 'cobinhood':
        pair = cobinhood.fetch_ticker(pair)['last']
elif exchange == 'bitlish':
        pair = bitlish.fetch_ticker(pair)['last']
elif exchange == 'bitstamp':
        pair = bitstamp.fetch_ticker(pair)['last']
elif exchange == 'coinfloor':
        pair = coinfloor.fetch_ticker(pair)['last']
elif exchange == 'dsx':
        pair = dsx.fetch_ticker(pair)['last']
elif exchange == 'livecoin':
        pair = livecoin.fetch_ticker(pair)['last']
elif exchange == 'tidex':
        pair = tidex.fetch_ticker(pair)['last']
elif exchange == 'liqui':
        pair = liqui.fetch_ticker(pair)['last']
elif exchange == 'gemini':
        pair = gemini.fetch_ticker(pair)['last']
elif exchange == 'itbit':
        pair = itbit.fetch_ticker(pair)['last']
        
    return pair

exchanges = ['okex',
             'poloniex', 
             'kraken',
             'bitfinex',
             'bittrex',  
             'hitbtc', 
             'gdax'
            , 'southxchange'
            , 'acx'
            , 'btcmarkets'
            , 'coinspot'
            , 'independentreserve'
            , 'braziliex'
            , 'flowbtc'
            , 'foxbit'
            , 'mercado'
            , 'coingi'
            , 'quadrigacx'
            , 'chilebit'
            , 'bibox'
            , 'gateio'
            , 'huobi'
            , 'okcoinusd'
            , 'okex'
            , 'cex'
            , 'coinmate'
            , 'bitbay'
            , 'bitlish'
            , 'bitmarket'
            , 'bl3p'
            , 'ccex'
            , 'paymium'
            , 'virwox'
            , 'paymium'
            , 'ccex'
            , 'anxpro'
            , 'bitz'
            , 'gatecoin'
            , 'kucoin'
            , 'mixcoins'
            , 'btcx'
            , 'coinexchange'
            , 'coinsecure'
            , 'bitcoincoid'
            , 'coincheck'
            , 'bit2c'
            , 'anxpro'
            , 'binance'
            , 'bitflyer'
            , 'btcbox'
            , 'coincheck'
            , 'coinexchange'
            , 'quoinex'
            , 'zaif'
            , 'therock'
            , 'bitso'
            , 'bl3p'
            , 'anxpro'
            , 'cryptopia'
            , 'independentreserve'
            , 'wex'
            , 'urdubit'
            , '_1btcxe'
            , 'coingi'
            , 'btcexchange'
            , 'bitbay'
            , 'bitmarket'
            , 'bitlish'
            , 'cex'
            , 'exmo'
            , 'getbtc'
            , 'livecoin'
            , 'xbtce'
            , 'yobit'
            , 'bitmex'
            , 'anxpro'
            , 'fybsg'
            , 'luno'
            , 'quoinex'
            , 'bibox'
            , 'lykke'
            , 'cobinhood'
            , 'bitlish'
            , 'bitstamp'
            , 'coinfloor'
            , 'dsx'
            , 'livecoin'
            , 'tidex'
            , 'liqui'
            , 'gemini'
            , 'itbit'
]

def get_pairs(exchange):
    if exchange == 'okex':
        btc_pairs = ['BCD/BTC', 'ETH/BTC', 'EOS/BTC', 'TRX/BTC', 'WTC/BTC', 'BTG/BTC', 'NEO/BTC', 'ICX/BTC', 'XLM/BTC', 'LTC/BTC', 'IOTA/BTC', 'ELF/BTC', 'QTUM/BTC', 'HSR/BTC', 'ETC/BTC', 'ZRX/BTC', 'OMG/BTC', 'LRC/BTC', 'MDA/BTC', 'SNT/BTC', 'SUB/BTC', 'BRD/BTC', 'DNT/BTC', 'EDO/BTC', 'XMR/BTC', 'LEND/BTC', 'CTR/BTC', 'LINK/BTC', 'EVX/BTC', 'ZEC/BTC', 'AST/BTC', 'FUN/BTC', 'ENG/BTC', 'REQ/BTC', 'KNC/BTC', 'DASH/BTC', 'MANA/BTC', 'MCO/BTC', 'MTL/BTC', 'DGD/BTC', 'OAX/BTC', 'ARK/BTC', 'NULS/BTC', 'GAS/BTC', 'SALT/BTC', 'ICN/BTC', 'RCN/BTC', 'MTH/BTC', 'RDN/BTC', 'VIB/BTC', 'STORJ/BTC', 'SNGLS/BTC', 'SNM/BTC', 'BNT/BTC', 'PPT/BTC']
    elif exchange == 'bitfinex':
        btc_pairs = ['ETH/BTC', 'EOS/BTC', 'XRP/BTC', 'BTG/BTC', 'NEO/BTC', 'BCH/BTC', 'LTC/BTC', 'IOTA/BTC', 'QTUM/BTC', 'ETC/BTC', 'ZRX/BTC', 'TNB/BTC', 'OMG/BTC', 'SNT/BTC', 'EDO/BTC', 'XMR/BTC', 'ZEC/BTC', 'FUN/BTC', 'DASH/BTC']
    elif exchange == 'bittrex':
        btc_pairs = ['ETH/BTC', 'ADA/BTC', 'XRP/BTC', 'BTG/BTC', 'NEO/BTC', 'BCH/BTC', 'XLM/BTC', 'LTC/BTC', 'XVG/BTC', 'QTUM/BTC', 'RLC/BTC', 'ETC/BTC', 'OMG/BTC', 'SNT/BTC', 'DNT/BTC', 'XMR/BTC', 'POWR/BTC', 'ZEC/BTC', 'NAV/BTC', 'FUN/BTC', 'LSK/BTC', 'ENG/BTC', 'STRAT/BTC', 'DASH/BTC', 'MANA/BTC', 'MCO/BTC', 'BAT/BTC', 'WINGS/BTC', 'LUN/BTC', 'ARK/BTC', 'SALT/BTC', 'KMD/BTC', 'XZC/BTC', 'RCN/BTC', 'WAVES/BTC', 'VIB/BTC', 'STORJ/BTC', 'ADX/BTC', 'BNT/BTC']
    elif exchange == 'hitbtc':
        btc_pairs = ['ETH/BTC', 'EOS/BTC', 'TRX/BTC', 'WTC/BTC', 'XRP/BTC', 'VEN/BTC', 'BTG/BTC', 'NEO/BTC', 'BCH/BTC', 'ICX/BTC', 'LTC/BTC', 'XVG/BTC', 'QTUM/BTC', 'HSR/BTC', 'VIBE/BTC', 'RLC/BTC', 'ETC/BTC', 'ZRX/BTC', 'NEBL/BTC', 'ENJ/BTC', 'OMG/BTC', 'LRC/BTC', 'SNT/BTC', 'SUB/BTC', 'DNT/BTC', 'POE/BTC', 'EDO/BTC', 'FUEL/BTC', 'XMR/BTC', 'LEND/BTC', 'CTR/BTC', 'ARN/BTC', 'EVX/BTC', 'CDT/BTC', 'ZEC/BTC', 'FUN/BTC', 'LSK/BTC', 'STRAT/BTC', 'CND/BTC', 'DASH/BTC', 'MANA/BTC', 'MCO/BTC', 'WINGS/BTC', 'TNT/BTC', 'AMB/BTC', 'LUN/BTC', 'BQX/BTC', 'DGD/BTC', 'OAX/BTC', 'KMD/BTC', 'DLT/BTC', 'ICN/BTC', 'MTH/BTC', 'WAVES/BTC', 'VIB/BTC', 'SNGLS/BTC', 'BNT/BTC', 'PPT/BTC']
    elif exchange == 'gdax':
        btc_pairs = ['ETH/BTC', 'LTC/BTC']
    elif exchange == 'poloniex':
        btc_pairs = ['ETH/BTC', 'XRP/BTC', 'BCH/BTC', 'XLM/BTC', 'LTC/BTC', 'ETC/BTC', 'ZRX/BTC', 'OMG/BTC', 'XMR/BTC', 'ZEC/BTC', 'BTS/BTC', 'NAV/BTC', 'LSK/BTC', 'STRAT/BTC', 'DASH/BTC', 'GAS/BTC', 'STORJ/BTC']
    elif exchange == 'kraken':
        btc_pairs = ['ETH/BTC', 'EOS/BTC', 'XRP/BTC', 'BCH/BTC', 'XLM/BTC', 'LTC/BTC', 'ETC/BTC', 'XMR/BTC', 'ZEC/BTC', 'DASH/BTC', 'ICN/BTC']
        
    elif exchange == 'southxchange': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'acx': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'btcmarkets': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coinspot': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'independentreserve': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'braziliex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'flowbtc': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'foxbit': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'mercado': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coingi': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'quadrigacx': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'chilebit': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bibox': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'gateio': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'huobi': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'okcoinusd': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'okex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'cex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coinmate': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitbay': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitlish': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitmarket': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bl3p': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'ccex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'paymium': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'virwox': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'paymium': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'ccex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'anxpro': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitz': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'gatecoin': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'kucoin': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'mixcoins': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'btcx': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coinexchange': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coinsecure': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitcoincoid': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coincheck': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bit2c': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'anxpro': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'binance': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitflyer': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'btcbox': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coincheck': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coinexchange': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'quoinex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'zaif': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'therock': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitso': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bl3p': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'anxpro': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'cryptopia': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'independentreserve': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'wex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'urdubit': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == '_1btcxe': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coingi': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'btcexchange': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitbay': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitmarket': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitlish': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'cex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'exmo': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'getbtc': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'livecoin': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'xbtce': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'yobit': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitmex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'anxpro': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'fybsg': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'luno': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'quoinex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bibox': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'lykke': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'cobinhood': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitlish': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'bitstamp': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'coinfloor': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'dsx': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'livecoin': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'tidex': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'liqui': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'gemini': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
        elif exchange == 'itbit': 
                btc_pairs = ['BTC/USDT', 'TRX/BTC', 'ETH/BTC', 'XRP/BTC', 'BNB/BTC', 'NANO/BTC', 'ADA/BTC', 'ICX/BTC', 'NEO/BTC', 'BCC/BTC', 'LSK/BTC', 'VEN/BTC', 'HSR/BTC', 'ETC/BTC', 'XLM/BTC', 'EOS/BTC', 'LTC/BTC', 'BLZ/BTC', 'IOST/BTC', 'ENG/BTC', 'DGD/BTC', 'XVG/BTC', 'IOTA/BTC', 'WTC/BTC', 'QTUM/BTC', 'MTL/BTC', 'PPT/BTC', 'POE/BTC', 'ZEC/BTC', 'XMR/BTC', 'BTG/BTC', 'SUB/BTC', 'BRD/BTC', 'KNC/BTC', 'TRIG/BTC', 'FUN/BTC', 'VIBE/BTC', 'CND/BTC', 'ELF/BTC', 'BCD/BTC', 'BQX/BTC', 'OMG/BTC', 'APPC/BTC', 'INS/BTC', 'SNT/BTC', 'STRAT/BTC', 'BTS/BTC', 'DASH/BTC', 'ZRX/BTC', 'AE/BTC', 'QSP/BTC', 'POWR/BTC', 'GXS/BTC', 'GAS/BTC', 'AION/BTC', 'LEND/BTC', 'MANA/BTC', 'CTR/BTC', 'ADX/BTC', 'NULS/BTC', 'TNT/BTC', 'OST/BTC', 'PIVX/BTC', 'STEEM/BTC', 'ENJ/BTC', 'NEBL/BTC', 'CMT/BTC', 'ARK/BTC', 'VIB/BTC', 'WABI/BTC', 'GTO/BTC', 'REQ/BTC', 'DNT/BTC', 'SALT/BTC', 'LINK/BTC', 'TNB/BTC', 'GVT/BTC', 'MCO/BTC', 'BAT/BTC', 'CDT/BTC', 'WAVES/BTC', 'ARN/BTC', 'LRC/BTC', 'AMB/BTC', 'XZC/BTC', 'AST/BTC', 'MOD/BTC', 'BCPT/BTC', 'CHAT/BTC', 'MTH/BTC', 'LUN/BTC', 'STORJ/BTC', 'KMD/BTC', 'RDN/BTC', 'NAV/BTC', 'FUEL/BTC', 'RCN/BTC', 'VIA/BTC', 'RLC/BTC', 'YOYO/BTC', 'EVX/BTC', 'EDO/BTC', 'SNGLS/BTC', 'MDA/BTC', 'WINGS/BTC', 'ICN/BTC', 'SNM/BTC', 'DLT/BTC', 'OAX/BTC', 'BNT/BTC']
    return btc_pairs
    
def opportunities(exchange): # fiat = USD or USDT
    
    count = 0
    deltas = []
    pairs = []
    
    btc_pairs = get_pairs(exchange)
    
    for pair in tqdm(btc_pairs):

        if count == 0:
            binance_usd = binance.fetch_ticker('BTC/USDT')['last']
            exchange_usd = get_ticker(exchange)
            count += 1

        binance_pair = binance.fetch_ticker(pair)['last']

        try:
            exchange_pair = get_pair(exchange, pair)
        except Exception as e:
            continue

        delta = ((binance_pair / exchange_pair) - 1) * 100
        deltas.append(delta)
        pairs.append(pair)
    
    for final_delta, pair in zip(deltas, pairs):
        if abs(final_delta) >= 2:
            coin = pair.replace('/BTC', '')
            check_vola(exchange, coin, final_delta)
        else:
            print(pair, exchange, 'no opp: lower than 2%')

def mean_confidence_interval(data):
    a = 1.0*np.array(data)
    n = len(a)
    std = np.std(a)
    m = np.mean(a)
    h = std * 1.68
    return m-h, m+h
            
for exchange in exchanges:
    print('EXCHANGE:', exchange)
    opportunities(exchange)
    print('DONE')
