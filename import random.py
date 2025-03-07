import random
import time
import threading


class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.next = None  # For linked list


class StockTradingEngine:
    def __init__(self):
        self.order_books = [None] * 1024  # One order book for each ticker (1024 total)
        self.lock = threading.Lock()

    def get_ticker_index(self, ticker):
        # Convert the ticker to an index based on the numeric suffix
        return int(ticker[3:]) - 1

    def add_order(self, order_type, ticker, quantity, price):
        """Handles a new order and attempts to match it."""
        ticker_index = self.get_ticker_index(ticker)
        new_order = Order(order_type, ticker, quantity, price)

        # Lock to avoid race conditions when modifying the order books
        with self.lock:
            # Try to match the order with existing orders
            self.match_order(ticker_index, new_order)

            # If there's remaining quantity, add the order to the order book
            if new_order.quantity > 0:
                self.add_to_order_book(ticker_index, new_order)

    def add_to_order_book(self, ticker_index, new_order):
        """Add the unmatched order to the linked list in order book."""
        if not self.order_books[ticker_index]:
            self.order_books[ticker_index] = new_order
        else:
            current = self.order_books[ticker_index]
            while current.next:
                current = current.next
            current.next = new_order

    def match_order(self, ticker_index, new_order):
        """Attempt to match the order with existing orders in the book."""
        current = self.order_books[ticker_index]
        prev = None

        while current:
            # If it's a BUY order
            if new_order.order_type == "BUY" and current.order_type == "SELL" and new_order.price >= current.price:
                matched_quantity = min(new_order.quantity, current.quantity)
                print(f"Matched {matched_quantity} shares of {new_order.ticker} at ${current.price}")
                new_order.quantity -= matched_quantity
                current.quantity -= matched_quantity

                if current.quantity == 0:
                    # Remove the order from the list if fully matched
                    if prev:
                        prev.next = current.next
                    else:
                        self.order_books[ticker_index] = current.next
                    current = current.next if prev is None else prev.next
                else:
                    current = current.next

            # If it's a SELL order
            elif new_order.order_type == "SELL" and current.order_type == "BUY" and new_order.price <= current.price:
                matched_quantity = min(new_order.quantity, current.quantity)
                print(f"Matched {matched_quantity} shares of {new_order.ticker} at ${current.price}")
                new_order.quantity -= matched_quantity
                current.quantity -= matched_quantity

                if current.quantity == 0:
                    # Remove the order from the list if fully matched
                    if prev:
                        prev.next = current.next
                    else:
                        self.order_books[ticker_index] = current.next
                    current = current.next if prev is None else prev.next
                else:
                    current = current.next
            else:
                # No match, proceed to the next order
                prev = current
                current = current.next

    def simulate_trading(self, num_orders=100):
        """Simulates stock trading with random buy/sell orders."""
        tickers = [f"STK{i}" for i in range(1, 1025)]
        orders = []

        # Generate random orders
        for _ in range(num_orders):
            order_type = random.choice(["BUY", "SELL"])
            ticker = random.choice(tickers)
            quantity = random.randint(1, 100)  # Random quantity between 1 and 100
            price = round(random.uniform(10, 500), 2)  # Price between $10 and $500
            orders.append((order_type, ticker, quantity, price))

        # Execute the orders in sequence with some delay to simulate real-time trading
        for order in orders:
            self.add_order(*order)
            time.sleep(random.uniform(0.1, 0.5))  # Simulate delays


# Example Usage
if __name__ == "__main__":
    trading_engine = StockTradingEngine()
    trading_engine.simulate_trading(50)  # Simulate trading with 50 orders
