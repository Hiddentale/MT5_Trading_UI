import MetaTrader5 as mt5
import time

live_account_username = None
live_account_password = None
live_account_server = None
demo_account_username = None
demo_account_password = None
demo_account_server = None

def connected_to_server():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    login_details = [live_account_username, live_account_password, live_account_server]
    authorized = mt5.login(login=login_details[0], password=login_details[1], server=login_details[2])
    return authorized


def connect_to_demo_server():
    login_details = [demo_account_username, demo_account_password, demo_account_server]
    authorized = mt5.login(login=login_details[0], password=login_details[1], server=login_details[2])
    return authorized


def place_market_order(volume, symbol, order_type):
    market_order_request = {
        "action": mt5.TRADE_ACTION_DEAL,  # Market Order
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(market_order_request)  # Sending the order to the market
    return result._asdict()["order"]


def find_order_info(identifier):
    time.sleep(0.5)
    result = mt5.positions_get(position=identifier)
    return result[0][10]


def acquire_market_order_identifier_and_entry():
    identifier = mt5.positions_get()[0][7]
    market_order_entry = mt5.positions_get()[0][10]  # Need to find a way to change this, so it does not depend on tuple index, since that might change.
    return identifier, market_order_entry


def adjust_stop_loss(identifier, entry, symbol, order_type):
    points = 20
    if order_type == mt5.ORDER_TYPE_BUY:
        stop_loss_request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "sl": entry - points,
            "position": identifier
        }
    else:
        stop_loss_request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "sl": entry + points,
            "position": identifier
        }
    result = mt5.order_send(stop_loss_request)  # Adding a stop loss


def exit_all_trades():
    if connected_to_server():
        open_trades = mt5.positions_get()
        if open_trades == ():
            print("There are currently no active trades!")
            return
        symbol = open_trades[0].symbol
        lot = open_trades[0].volume
        order_type = open_trades[0].type
        if order_type == 0:
            order_type = mt5.ORDER_TYPE_SELL
        else:
            order_type = mt5.ORDER_TYPE_BUY
        position_id = open_trades[0].ticket
        price = mt5.symbol_info_tick(symbol).bid
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        # This code here makes it so that you log out of your session and into a demo account, thus you are unable to see your orders/how much profit you are making. Thus not affecting your mental game.
        # #result = mt5.Close(symbol=symbol, ticket=ticket)
        # #result = mt5.order_send(request={"action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": volume, "type": order_type, "price": price, "position": ticket, "type_filling": mt5.ORDER_FILLING_IOC})
        # #connect_to_demo_server()
    else:
        print(f"failed to connect, error code: {mt5.last_error()}")
    mt5.shutdown()


def place_trade(symbol, order_type):
    if connected_to_server():
        orders = mt5.positions_get()
        if orders == ():
            equity = mt5.account_info()._asdict()["equity"]
            volume = equity // 1000
            #volume = 0.1  <-- For testing purposes

            identifier = place_market_order(volume, symbol, order_type)
            entry = find_order_info(identifier)
            print(f"Market entry at: {entry}")
            adjust_stop_loss(identifier, entry, symbol, order_type)
            #connect_to_demo_server() <-- This code works together with the code at line 97.
            #exit()
        else:
            print("You currently already have a trade running!")
            return

    else:
        print(f"failed to connect, error code: {mt5.last_error()}")
    mt5.shutdown()
