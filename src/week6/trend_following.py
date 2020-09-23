import matplotlib.pyplot as plt
from src.week3.Investar.Analyzer import Analyzer

if __name__ == '__main__':
    market_db = Analyzer()
    stock_dataframe = market_db.get_daily_price_with_name('SK하이닉스', '2018-11-01', '2019-09-10')
    stock_dataframe = stock_dataframe.dropna()

    stock_dataframe['MA20'] = stock_dataframe['close'].rolling(window=20).mean()
    stock_dataframe['stddev'] = stock_dataframe['close'].rolling(window=20).std()
    stock_dataframe['upper'] = stock_dataframe['MA20'] + (stock_dataframe['stddev'] * 2)
    stock_dataframe['lower'] = stock_dataframe['MA20'] - (stock_dataframe['stddev'] * 2)
    stock_dataframe['bandwidth'] = (stock_dataframe['upper'] - stock_dataframe['lower']) / stock_dataframe['MA20'] * 100
    stock_dataframe['PB'] = (stock_dataframe['close'] - stock_dataframe['lower']) / \
                            (stock_dataframe['upper'] - stock_dataframe['lower'])

    # Type Price - (고가 + 저가 + 종가)/3
    stock_dataframe['TP'] = (stock_dataframe['high'] + stock_dataframe['low'] + stock_dataframe['close']) / 3
    # Positive/Negative Money Flow
    stock_dataframe['PMF'] = 0
    stock_dataframe['NMF'] = 0
    # 1 뺀 이유는 내부에서 +1 한 값이랑 비교해서...
    for i in range(len(stock_dataframe) - 1):
        tp_current = stock_dataframe.TP.values[i]
        tp_next = stock_dataframe.TP.values[i + 1]
        target_mf = 'PMF' if tp_current < tp_next else 'NMF'
        stock_dataframe[target_mf].values[i+1] = tp_next * stock_dataframe.volume.values[i+1]

    # Money Flow ratio - window 동안의 상대적 현금 흐름 RSI
    mf_window=10
    stock_dataframe['MFR'] = stock_dataframe.PMF.rolling(window=mf_window).sum() / stock_dataframe.NMF.rolling(window=mf_window).sum()
    stock_dataframe['MFI10'] = 100 - (100 / (1 + stock_dataframe.MFR))

    up_trend_threshold = .8
    down_trend_threshold = .2
    mfi_up_trend_threshold = 80
    mfi_down_trend_threshold = 20


    plt.figure(figsize=(9, 8))
    plt.subplot(2, 1, 1)
    plt.title('SK 하이닉스 Bollinger Band(20 day, 2 std) - Trend Following')
    plt.plot(stock_dataframe.index, stock_dataframe['close'], '#0000ff', label='close')
    plt.plot(stock_dataframe.index, stock_dataframe['upper'], 'r--', label='upper band')
    plt.plot(stock_dataframe.index, stock_dataframe['MA20'], 'k--', label='Moving average 20')
    plt.plot(stock_dataframe.index, stock_dataframe['lower'], 'c--', label='lower band')
    plt.fill_between(stock_dataframe.index, stock_dataframe['upper'], stock_dataframe['lower'], color='0.9')

    for i in range(0, len(stock_dataframe['close'])):
        if stock_dataframe.PB.values[i] > up_trend_threshold and stock_dataframe.MFI10.values[i] > mfi_up_trend_threshold:
            plt.plot(stock_dataframe.index.values[i], stock_dataframe.close.values[i], 'r^')
        elif stock_dataframe.PB.values[i] < down_trend_threshold and stock_dataframe.MFI10.values[i] < mfi_down_trend_threshold:
            plt.plot(stock_dataframe.index.values[i], stock_dataframe.close.values[i], 'bv')
    plt.legend(loc='best')

    plt.subplot(2, 1, 2)
    plt.plot(stock_dataframe.index, stock_dataframe['PB'] * 100, 'b', label='%b*100')  # bollinger index 백분률
    plt.plot(stock_dataframe.index, stock_dataframe['MFI10'], 'g--', label=f'MFI({mf_window} days)')
    plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])  # y틱 고정

    for i in range(len(stock_dataframe.close)):
        if stock_dataframe.PB.values[i] > up_trend_threshold and stock_dataframe.MFI10.values[i] > mfi_up_trend_threshold:
            plt.plot(stock_dataframe.index.values[i], 0, 'r^')
        elif stock_dataframe.PB.values[i] < down_trend_threshold and stock_dataframe.MFI10.values[i] < mfi_down_trend_threshold:
            plt.plot(stock_dataframe.index.values[i], 0, 'bv')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()
