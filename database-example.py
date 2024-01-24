import threading
import time
import yfinance as yf
import sqlalchemy
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
import pytz

# Database setup
Base = sqlalchemy.orm.declarative_base()

# Configure logging to write to a file
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

global symbol, current_price, quantity, purchase_date, avg_price

class TradeHistory(Base):
    __tablename__ = 'trade_history'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    action = Column(String)  # 'buy' or 'sell'
    quantity = Column(Integer)
    price = Column(Float)
    date = Column(String)

class Position(Base):
    __tablename__ = 'positions'
    symbol = Column(String, primary_key=True)
    quantity = Column(Integer)
    avg_price = Column(Float)
    purchase_date = Column(String)

# Initialize SQLAlchemy
engine = create_engine('sqlite:///trading_bot.db')
Session = sessionmaker(bind=engine)

# Create tables if not exist
Base.metadata.create_all(engine)

# Buy and fake trailing stop order lock
buy_sell_lock = threading.Lock()

def calculate_cash_on_hand():
    # Placeholder function, replace with actual implementation
    return 10000.0

def allocate_cash_equally(cash_available, total_symbols):
    # Placeholder function, replace with actual implementation
    return cash_available / total_symbols

def get_current_price(symbol):
    # Placeholder function, replace with actual implementation
    return 150.0

def track_price_changes(symbol):
    # Placeholder function, replace with actual implementation
    return 'increase'

def end_time_reached():
    # Placeholder function, replace with actual implementation
    return False

def run_schedule():
    # Placeholder function, replace with actual implementation
    pass

def place_trailing_stop_sell_order(symbol, quantity, current_price):
    # Placeholder function, replace with actual implementation
    return 'fake_stop_order_id'

def refresh_after_buy():
    # Placeholder function, replace with actual implementation
    pass

def remove_symbol_from_trade_list(symbol):
    # Placeholder function, replace with actual implementation
    pass

def print_technical_indicators(symbol, data):
    # Placeholder function, replace with actual implementation
    pass

def calculate_technical_indicators(symbol, lookback_days):
    # Placeholder function, replace with actual implementation
    pass

def status_printer_buy_stocks():
    # Placeholder function, replace with actual implementation
    pass

def buy_stock(symbol, quantity, avg_price, purchase_date):
    with buy_sell_lock:
        try:
            print("Buying stock...")
            stocks_to_remove = []

            global start_time, end_time, original_start_time, price_changes

            extracted_date_from_today_date = datetime.today().date()
            today_date_str = extracted_date_from_today_date.strftime("%Y-%m-%d")

            now = datetime.now(pytz.timezone('US/Eastern'))
            current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")

            current_date = datetime.today().strftime("%Y-%m-%d")

            # Adjust this line to use the correct parameters
            # e.g., buy_stock('SPXL', 10, 150.0, time.strftime("%Y-%m-%d %H:%M:%S"))
            # Removed the recursive call to avoid infinite recursion
            #buy_stock(symbol, quantity, avg_price, purchase_date)

            print("Database Information After Buying:")
            print_database_info()

            time.sleep(5)

            day_trade_count = 2

            if day_trade_count < 3:
                print("")
                print("Waiting 2 minutes before placing a trailing stop sell order.....")
                print("")
                time.sleep(120)

                qty_of_one_stock = 1

                current_price = avg_price

                print("Placing trailing stop sell order...")
                stop_order_id = place_trailing_stop_sell_order(symbol, qty_of_one_stock, current_price)

                if stop_order_id:
                    print(f"Trailing stop sell order placed for {symbol} with ID: {stop_order_id}")
                    print("")
                else:
                    print(f"Failed to place trailing stop sell order for {symbol}")
                    print("")

            print("Buying stock section completed.")

        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred during database update: {str(e)}")
            logging.error(f"An error occurred during database update: {str(e)}")


def test_example_trailing_stop_order(symbol):
    with buy_sell_lock:
        print(f"Test example trailing stop order triggered for {symbol}. Removing stock from the database.")
        session = Session()
        position = session.query(Position).filter_by(symbol=symbol).first()
        if position:
            session.delete(position)
            session.commit()
        session.close()

def print_database_info():
    with buy_sell_lock:
        session = Session()
        positions = session.query(Position).all()
        for position in positions:
            print(f"Symbol: {position.symbol}, Quantity: {position.quantity}, Avg Price: {position.avg_price}, Purchase Date: {position.purchase_date}")
        session.close()

def print_database_info():
    try:
        print("Printing database information...")
        with Session() as session:
            positions = session.query(Position).all()
            for position in positions:
                print(f"Symbol: {position.symbol}, Quantity: {position.quantity}, Avg Price: {position.avg_price}, Purchase Date: {position.purchase_date}")
    except SQLAlchemyError as e:
        print(f"An error occurred while printing database information: {str(e)}")


def stock_trading_script():
    while True:
        try:
            print("Executing stock trading script loop...")

            # Buy stock
            buy_stock('SPXL', 10, 150.0, time.strftime("%Y-%m-%d %H:%M:%S"))

            # Print database information
            print("Database Information After Buying:")
            print_database_info()

            # Wait for 5 seconds
            time.sleep(5)

            # Test example trailing stop order
            test_example_trailing_stop_order('SPXL')

            # Print database information after test example trailing stop order
            print("Database Information After Test Example Trailing Stop Order:")
            print_database_info()

            # Wait for 5 seconds before repeating
            time.sleep(5)

        except Exception as e:
            print(f"An error occurred in the stock trading script: {str(e)}")
            logging.error(f"An error occurred in the stock trading script: {str(e)}")

if __name__ == "__main__":
    # Run the stock trading script
    stock_trading_thread = threading.Thread(target=stock_trading_script)
    stock_trading_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stock_trading_thread.join()
