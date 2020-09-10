import matplotlib.pyplot as plt
from src.week3.Investar.Analyzer import Analyzer

if __name__ == '__main__':
    market_db = Analyzer()
    stock_dataframe = market_db.get_daily_price_with_name('SK하이닉스', '2018-11-01', '2019-09-10')

    stock_dataframe['MA20'] = stock_dataframe['close'].rolling(window=20).mean()
    stock_dataframe['stddev'] = stock_dataframe['close'].rolling(window=20).std()
    stock_dataframe['upper'] = stock_dataframe['MA20'] + (stock_dataframe['stddev'] * 2)
    stock_dataframe['lower'] = stock_dataframe['MA20'] - (stock_dataframe['stddev'] * 2)
    stock_dataframe['PB'] = (stock_dataframe['close'] - stock_dataframe['lower']) / \
                            (stock_dataframe['upper'] - stock_dataframe['lower'])

    stock_dataframe['II'] = (2 * stock_dataframe['close'] - stock_dataframe['high'] - stock_dataframe['low']) / \
                            (stock_dataframe['high'] - stock_dataframe['low']) * \
                            (stock_dataframe['volume'])

    stock_dataframe['IIP21'] = (stock_dataframe['II'].rolling(window=21).sum()) / (stock_dataframe['volume'].rolling(window=21).sum()) * 100

    stock_dataframe = stock_dataframe.dropna()

    plt.figure(figsize=(9, 9))
    plt.subplot(3, 1, 1)
    plt.title('SK 하이닉스 Bollinger Band(20 day, 2 std) - Reversals')
    plt.plot(stock_dataframe.index, stock_dataframe['close'], 'm', label='close')
    plt.plot(stock_dataframe.index, stock_dataframe['upper'], 'r--', label='upper band')
    plt.plot(stock_dataframe.index, stock_dataframe['MA20'], 'k--', label='Moving average 20')
    plt.plot(stock_dataframe.index, stock_dataframe['lower'], 'c--', label='lower band')
    plt.fill_between(stock_dataframe.index, stock_dataframe['upper'], stock_dataframe['lower'], color='0.9')

    for i in range(0, len(stock_dataframe['close'])):
        if stock_dataframe.PB.values[i] < .05 and stock_dataframe.IIP21.values[i] > 0:
            plt.plot(stock_dataframe.index.values[i], stock_dataframe.close.values[i], 'r^')
        elif stock_dataframe.PB.values[i] > .95 and stock_dataframe.IIP21.values[i] < 0:
            plt.plot(stock_dataframe.index.values[i], stock_dataframe.close.values[i], 'bv')
    plt.legend(loc='best')

    plt.subplot(3, 1, 2)
    plt.plot(stock_dataframe.index, stock_dataframe['PB'], 'b', label='%b')
    plt.grid(True)
    plt.legend(loc='best')

    plt.subplot(3, 1, 3)
    plt.bar(stock_dataframe.index, stock_dataframe.IIP21, color='g', label='II% 21 day')

    for i in range(len(stock_dataframe.close)):
        if stock_dataframe.PB.values[i] < .05 and stock_dataframe.IIP21.values[i] > 0:
            plt.plot(stock_dataframe.index.values[i], 0, 'r^')
        elif stock_dataframe.PB.values[i] > .95 and stock_dataframe.IIP21.values[i] < 0:
            plt.plot(stock_dataframe.index.values[i], 0, 'bv')
    plt.grid(True)
    plt.legend(loc='best')

    plt.show()
