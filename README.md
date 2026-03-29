# Algorithmic Trading Python

This repository contains various trading algorithms that I have developed using QuantConnect

Here are the algorithms I have made so far:
- A [simple trading bot](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/SimpleTradingBot) which buys and holds SPY until a stop loss or take profit is reached, then waits a month before repeating.
- [Buy & Hold QQQ](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/BuyHoldQQQ) with 5% stop loss (updated based on highest price seen since fill) using limit and stop orders. Waits a month after stop loss before repeating.
- A simple [SPY strategy using SMA](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/SMASPY) which uses a basic SMA indicator and 52 week high and low. Uptrend and near high = long, downtrend and near low = short, else liquidate.
- A [simple intraday SPY bot](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/SimpleIntradaySPY) that at the start of each day goes long if open < yesterday's close, short if open > yesterday's close (both by 1%).
- A [size effect strategy](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/SizeEffectStrategy) which takes the 200 most liquid stocks that have a price above $10 and invests in the 10 stocks with the lowest market cap, rebalancing every month.
- An [X trading bot](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/XTradingBot) that performs sentiment analysis on Elon Musk's tweets to trade TSLA.
- Another [SMA strategy](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/SMASPYBND) using a 30 day SMA where if SMA < SPY, allocate 80% of portfolio to SPY, 20% BND. Else 20%/80%. Rebalance to 80%/20% if no trend change for 30 days.
- A [Forex trading bot](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/ForexTradingBot) that is a simple mean reversion strategy on EURUSD.
- An [options trading bot](https://github.com/Cole-Godfrey/AlgorithmicTradingPython/tree/main/OptionsTradingBot) that buys call options if the price breaks out of its one-month high.

The backtesting statistics for each algorithm can be found in STATS.md in each algorithm's folder.
