import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SPX = pd.read_csv("SPX-I.csv")
NDX = pd.read_csv("NDX-I.csv")

df1 = pd.DataFrame({
    "dates" : NDX.iloc[:, 0],
    "NDX" : NDX.iloc[:, 4]
})
df2 = pd.DataFrame({
    "dates" : SPX.iloc[:, 0],
    "SPX" : SPX.iloc[:, 4]
})

newdf = pd.merge(df1, df2, on='dates')

dfDate = pd.DataFrame(newdf["dates"])

dfClosePrices = pd.DataFrame({
    "NDX": newdf["NDX"],
    "SPX": newdf["SPX"]
})

dfPctChange = pd.DataFrame(dfClosePrices.pct_change())

dfAvg50 = pd.DataFrame(dfClosePrices.rolling(50).mean())

dfAvg200 = pd.DataFrame(dfClosePrices.rolling(200).mean())

dfSignals = pd.DataFrame(index = dfClosePrices.index, columns = dfClosePrices.columns)

dfSignals.values[(dfAvg50>dfAvg200)] = 1

dfSignals.values[(dfAvg50<=dfAvg200)] = 0

dfPNL = pd.DataFrame(dfSignals.shift(2) * dfPctChange)

dfCumPNL = pd.DataFrame(dfPNL.cumsum())

dfSignals.to_csv("golden.csv")

x = pd.to_datetime(newdf["dates"], format = '%Y%m%d')

y = dfCumPNL["NDX"]

plt.plot(x,y, color="red")

plt.show()