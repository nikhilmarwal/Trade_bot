#!/usr/bin/env python
# coding: utf-8

# In[3]:


from binance.client import Client
import logging
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_log.log"), # Log into bot_log.log
        logging.StreamHandler()             # Log into console
    ]
)

class Basic_bot():
    def __init__(self,api_key,secret_key, testnet = True ):
        base_url = "https://testnet.binancefuture.com"
        self.client = Client(api_key,
                            secret_key,
                            testnet= True)
        self.futures_url = "https://testnet.binancefuture.com"
        
        if testnet :
            # self.client.API_URL = "https://testnet.binancefuture.com"
            logging.info(f"BOT initialised in Testnet {self.futures_url}")
        else:
            logging.warning(f"BOT initialised in LIVE")

    def _create_order(self, symbol, side, order_type, quantity, price=None,):
        params = {
            'symbol' : symbol,
            'side' : side,
            'type' : order_type,
            'quantity': quantity,
        }
        if order_type == ORDER_TYPE_LIMIT:
            if not price:
                logging.error(f'Price is required for LIMIT orders')
                return None
            params['price'] = price
            params['timeInForce'] = TIME_IN_FORCE_GTC
            logging.info(f"Attempting to place LIMIT order {params}")
        try :
            order = self.client.futures_create_order(**params)
            logging.info(f"Order successful: Symbol={order.get('symbol')}, Status={order.get('status')}, OrderId={order.get('orderId')}")
            print(f"\n--- Order Details (ID: {order.get('orderId')}) ---")
            print(f"SYMBOL: {order.get('symbol')} | SIDE: {order.get('side')} | TYPE: {order.get('type')}")
            print(f"QUANTITY: {order.get('origQty')} | PRICE: {order.get('price')}")
            print(f"STATUS: {order.get('status')}\n")
            return order
        except BinanceAPIException as e:
            logging.info(f"Binance API error (Code {e.code} : {e.message}) ")
            print(f"Binance API error occured (Code {e.code} : {e.message}) ")
        except BinanceOrderException as e:
            logging.info(f"Binary Order error {e}) ")
            print(f"Binary Order error  {e} ) ") 
        except Exception as e:
            logging.info(f"Unexpected error occured  {e})")
            print(f"Unexpected error occured  {e})")
        return None

    def place_market_order(self, symbol: str , side: str, quantity : float):
        side = side.upper()  # converted side into Uppercase
        if side not in['BUY', 'SELL']:
            raise ValueError("Side must be either BUY or SELL")

        return self._create_order(symbol=symbol.upper(),
                            side=side,
                            order_type = ORDER_TYPE_MARKET,
                            quantity=quantity)
    def place_limit_order(self, symbol: str , side: str, quantity : float, price : float):
        side = side.upper() 
        if side not in['BUY', 'SELL']:
            raise ValueError("Side must be either BUY or SELL")

        return self._create_order(symbol=symbol.upper(),
                            side=side,
                            order_type = ORDER_TYPE_LIMIT,
                            quantity=quantity,
                            price = price)
    def get_symbol_info(self, symbol):
        try : 
            info = self.client.futures_exchange_info()
            for s in info['symbols']:
                if s == symbol.upper():
                    return s
            logging.warning(f"{symbol} is not a valid FUTURE symbol")
            return None
        except Exception as e:
            logging.info(f"Unexpected error occured  {e})")
            print(f"Unexpected error occured  {e})")
            return None


def run_cli():
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        api_key = os.getenv("YOUR_API_KEY")
        secret_key = os.getenv("SECRET_KEY")
    except ImportError :
        print("python dotenv is not installed. API keys are not HARDCODED , For first time you can paste your API and SECRET KEY in run_cli method  ")
        api_key = 'PASTE API KEY HERE '
        secret_key = 'PASTE SECRET KEY HERE'

    bot = Basic_bot(api_key, secret_key, testnet = True)

    while True:
        print("\n" + "="*50)
        print("Simple Futures Bot CLI")
        print("1. Place MARKET Order")
        print("2. Place LIMIT Order")
        print("3. Exit")
        print("="*50)

        choice = input("Enter choice (1/2/3): ")

        if choice == '3':
            print("Exiting Bot.")
            break
        
        if choice in ['1', '2']:
            try:
                symbol = input("Enter SYMBOL (e.g., BTCUSDT): ").upper()
                side = input("Enter SIDE (BUY or SELL): ").upper()
                quantity = float(input("Enter QUANTITY (e.g., 0.001): "))

                if choice == '1':
                    bot.place_market_order(symbol, side, quantity)
                
                elif choice == '2':
                    price = float(input("Enter LIMIT PRICE (e.g., 60000.00): "))
                    bot.place_limit_order(symbol, side, quantity, price)
                
            except ValueError as ve:
                print(f"Input Error: {ve}. Please enter valid numbers/strings.")
            except Exception as e:
                print(f"General Error during input: {e}")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    run_cli()

