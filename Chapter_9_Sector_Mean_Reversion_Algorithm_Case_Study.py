# Chapter 9 - Sector Mean Reversion Algorithm Case Study
#
# Copy and paste this code to a new algorithm window
# Set start date = 10/01/2004 and end date = 05/29/2020
# Set initial capital to 100000
# Run a backtest with 'Build Algorithm'
# Ater that completes run another backtest with 'Run Full Backtest'

import talib as ta

def initialize(context):
    # uncomment the line below if you have trouble with AGG order fills
    set_slippage(slippage.FixedSlippage(spread = 0.0))

    schedule_function(entries, date_rules.every_day(), time_rules.market_close(minutes=10))
    schedule_function(exits, date_rules.every_day(), time_rules.market_close(minutes=15))
    schedule_function(trade_bonds, date_rules.every_day(), time_rules.market_close(minutes=9))

    context.sectors = [sid(19662), # XLY
                       sid(19658), # XLK
                       sid(19659), # XLP
                       sid(19656), # XLF
                       sid(19661), # XLV
                       sid(19660), # XLU
                       sid(19657), # XLI
                       sid(19654), # XLB
                       sid(19655), # XLE
                       sid(26669),] # VNQ
    context.bonds = sid(25485) # AGG

def entries(context, data):
    for x in context.sectors:
        current_price = data.current(x,'price')
        closes_history = data.history(x, 'close', 200, '1d')
        sma_200_day = closes_history.mean()
        rsi = ta.RSI(closes_history,4)[-1]

        if rsi < 20 and current_price > sma_200_day and context.portfolio.positions[x].amount == 0:
            order_percent(x, 0.10)

def exits(context, data):
    for x in context.sectors:
        closes_history = data.history(x, 'close', 200, '1d')
        rsi = ta.RSI(closes_history,4)[-1]

        if  context.portfolio.positions[x].amount > 0 and rsi > 70:
            order_target_percent(x, 0)

def trade_bonds(context, data):
    if context.portfolio.positions[context.bonds].amount == 0:
        amount_of_current_positions = len(context.portfolio.positions)
    if context.portfolio.positions[context.bonds].amount > 0:
        amount_of_current_positions = len(context.portfolio.positions) - 1

    percent_to_allocate_to_bonds = (10 - amount_of_current_positions) * 0.10

    order_target_percent(context.bonds, percent_to_allocate_to_bonds)
