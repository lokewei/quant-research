import backtrader as bt
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import backtrader.analyzers as btanalyzers
import math
import tushare as ts
# import config


class MFI(bt.Indicator):
    lines = ("mfi", "raw_mf", "typical", "money_flow_pos", "money_flow_neg")

    plotlines = dict(
        raw_mf = dict(_plotskip=True),
        money_flow_pos = dict(_plotskip=True),
        money_flow_neg = dict(_plotskip=True),
        typical = dict(_plotskip=True),
    )

    params = (
        ('period', 14),
    )

    def next(self):
        typical_price = (self.data.close[0] + self.data.low[0]+self.data.high[0])/3
        raw_mf = typical_price * self.data.volume[0]

        self.lines.typical[0] = typical_price
        self.lines.raw_mf[0] = raw_mf

        self.lines.money_flow_pos[0] = raw_mf if self.lines.typical[0] >= self.lines.typical[-1] else 0
        self.lines.money_flow_neg[0] = raw_mf if self.lines.typical[0] <= self.lines.typical[-1] else 0

        pos_mf = math.fsum(self.lines.money_flow_pos.get(size=self.params.period))
        neg_mf = math.fsum(self.lines.money_flow_neg.get(size=self.params.period))

        if neg_mf == 0:
            self.lines.mfi[0] = 100
            return

        self.lines.mfi[0] = 100 - 100/(1+ pos_mf/neg_mf)



class Strategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.mfi = MFI()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: {:.2f}, Cost: {:.2f}, Comm {:.2f}'.format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: {:.2f}, Cost: {:.2f}, Comm {:.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        if not self.position:
            if self.mfi[0]<35:
                self.order = self.order_target_percent(target=0.95)
        else:
            if self.mfi[0] > 65:
                self.order = self.sell()



if __name__=='__main__':
    stock = '601318.SH'
    start_date = '20100701'
    end_date = '20201224'
    # ts.set_token(config.token)
    ts.set_token('xxxx')


    def aquire_data(stock, start_date, end_date):
        df = ts.pro_bar(ts_code=stock,adj='qfq', start_date=start_date, end_date=end_date)
        dates = pd.to_datetime(df['trade_date'])
        df = df[['open', 'high', 'low', 'close', 'vol']]
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df.index = dates
        df.sort_index(ascending=True, inplace=True)
        print(df)
        return df

    df = aquire_data(stock, start_date, end_date)
    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)

    cerebro.addstrategy(Strategy)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=98)

    back = cerebro.run()

    cerebro.plot(style='candle')
