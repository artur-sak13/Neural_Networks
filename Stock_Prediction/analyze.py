import json, time, os, math
from datetime import datetime
from time import mktime
from yahoo_finance import Share
from pprint import pprint
from Activations import *
import matplotlib.pyplot as plt
from matplotlib import style

style.use('bmh')

def normalize(close, high, low):
    h = 1.0
    l = -1.0
    return (((close - low)/ (high - low)) * (h - l)) + l
    # return ((2.0 * close - (high + low)) / (high - low))

def un_normalize(price, high, low):
    h = 1.0
    l = -1.0
    return (((price - l) / (h - l)) * (high - low)) + low
    #  return (((price * (high - low)) / 2.0) + (high + low)) / 2.0

def rollingWindow(seq, size):
    it = iter(seq)
    next(it)
    win = [it.next() for curr in xrange(size)]
    yield win
    for elem in it:
        win[:-1] = win[1:]
        win[-1] = elem
        yield win

def makeTrainingSets(size):
    hist = getHistoricalData()
    del hist[20:]

    training_set = []
    for win in rollingWindow(hist, size):
        window = []
        for price in win:
            # window.append(price)
            window.append(normalize(price, max(win), min(win)))
        training_set.append(window)
    return training_set

def getDesired(num):
    hist = getHistoricalData()
    desired = []
    del hist[40:]

    for i in range(num):
        desired.append([hist[i]])
    return desired

def getTestData(size):
    hist = getHistoricalData()
    hist.reverse()

    test_set = []
    for win in rollingWindow(hist, size):
        window = []
        for price in win:
            window.append(price)
        test_set.append(window)
    return test_set

def getActualPrice(test):
    close = []
    for i in range(len(test) - 1):
        close.append(test[i + 1][0])
    return close

def getHistoricalData():
    historicalPrices = []
    stock = Share('^VIX')
    data = stock.get_historical('2015-01-01', '2016-01-01')
    data.reverse()
    for elem in data:
        historicalPrices.append(float(elem['Adj_Close']))
    return historicalPrices

def normalize_all(pattern):
    ret = []
    for price in pattern:
        ret.append(normalize(price, max(pattern), min(pattern)))
    return ret

def calculate_SSR(actuals, predicted):
    ssr = 0.0
    for p1, p2 in zip(actuals, predicted):
        ssr += (p1 - p2)**2
    return ssr

def f_sst(data, mean):
    sst = 0.0
    for prd in data:
        sst += (prd-mean)**2
    return sst


def calculate_mean(data):
    add = 0.0
    for price in data:
        add += abs(price)
    return (1/(len(data)))* add

def analyze():
    patterns = makeTrainingSets(5)
    # pprint(patterns)
    desired = getDesired(len(patterns))
    net = Network([5,100,50,1])
    net.train(patterns, desired)

    test = getTestData(5)
    data = []
    for pattern in test:
        n_pattern = normalize_all(pattern)
        data.append(un_normalize(net.test(n_pattern), max(pattern), min(pattern)))
    data.reverse()

    price = getHistoricalData()
    ssr = calculate_SSR(price, data)
    sst = f_sst(data, calculate_mean(data))
    r_square = 1.0 - (ssr/sst)



    print "SSR: \n", ssr
    print "SST: \n", sst
    print "R-square: \n", r_square
    print "R: \n", math.sqrt(r_square)
    print "Max Actual: \n", max(price)
    print "Mean Actual: ", calculate_mean(price)
    print "Min Actual: \n", min(price)
    print "Max Predicted: \n", max(data)
    print "Mean Predicted: ", calculate_mean(data)
    print "Min Predicted: \n", min(data)
    print "Observations: \n", len(price)



    pdata = list(enumerate(data, start=4))
    prices = list(enumerate(getHistoricalData()))

    plt.plot(*zip(*prices), label='Actual')
    plt.plot(*zip(*pdata), label='Predicted')
    plt.title('Actual and Forecasted ^VIX TS')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


analyze()
