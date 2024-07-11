def clear(etf, stocks):
    if etf not in stocks:
        for stock in stocks:
            order_target_percent(stock, 0)

def handle_bar(context, bar_dict):
    CHECK_RANGE = 22
    etf0 = '513100.XSHG'
    etf1 = '162411.XSHE'
    etf2 = '159915.XSHE'

    etf0_index = history_bars(etf0, CHECK_RANGE, '1d', 'close')
    etf1_index = history_bars(etf1, CHECK_RANGE, '1d', 'close')
    etf2_index = history_bars(etf2, CHECK_RANGE, '1d', 'close')

    etf0_return = (etf0_index[CHECK_RANGE-1]-etf0_index[0])/etf0_index[0]
    etf1_return = (etf1_index[CHECK_RANGE-1]-etf1_index[0])/etf1_index[0]
    etf2_return = (etf2_index[CHECK_RANGE-1]-etf2_index[0])/etf2_index[0]

    signal = max(etf0_return, etf1_return, etf2_return, 0)#

    stocks = context.portfolio.positions

    if signal==0:
        clear('159912.XSHE', stocks)
    elif signal == etf0_return:
        clear(etf0, stocks)
        order_target_percent(etf0, 1)
    elif signal == etf1_return:
        clear(etf1, stocks)
        order_target_percent(etf1, 1)
    elif signal == etf2_return:
        clear(etf2, stocks)
        order_target_percent(etf2, 1)