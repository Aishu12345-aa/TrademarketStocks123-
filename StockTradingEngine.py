import heapq
import random
import time

class StockTradingEngine:
    def __init__(self):
        # Dictionary for each ticker symbol: {'BUY': max_heap, 'SELL': min_heap}
        self.order_book = {ticker: {'BUY': [], 'SELL': []} for ticker in self.generate_tickers()}

    def generate_tickers(self):
        # Generate 1,024 stock tickers like "STK1", "STK2", ..., "STK1024"
        return [f"STK{i}" for i in range(1, 1025)]

    def add_order(self, order_type, ticker, quantity, price):
        """Handles a new order and attempts to match it."""
        if order_type == "BUY":
            self.match_order(ticker, quantity, price, is_buy=True)
        else:  # SELL order
            self.match_order(ticker, quantity, price, is_buy=False)

    def match_order(self, ticker, quantity, price, is_buy):
        """Attempts to match the order; if no match, adds it to the book."""
        opposite_type = 'SELL' if is_buy else 'BUY'
        heap = self.order_book[ticker][opposite_type]

        while heap and quantity > 0:
            best_price, best_quantity = heapq.heappop(heap)
            if is_buy and best_price > price:  # Buy order can't afford the best sell price
                heapq.heappush(heap, (best_price, best_quantity))  # Put it back
                break
            if not is_buy and best_price < price:  # Sell order wants more than the best buy
                heapq.heappush(heap, (best_price, best_quantity))
                break

            matched_quantity = min(quantity, best_quantity)
            quantity -= matched_quantity
            best_quantity -= matched_quantity
            print(f"Matched {matched_quantity} shares of {ticker} at ${best_price}")

            if best_quantity > 0:
                heapq.heappush(heap, (best_price, best_quantity))  # Reinsert remaining quantity

        if quantity > 0:
            # Add remaining unmatched quantity to order book
            order_book_type = 'BUY' if is_buy else 'SELL'
            order_heap = self.order_book[ticker][order_book_type]
            heapq.heappush(order_heap, (-price, quantity) if is_buy else (price, quantity))

    def simulate_trading(self, num_orders=100):
        """Simulates stock trading with random buy/sell orders."""
        tickers = self.generate_tickers()
        orders = []
        for _ in range(num_orders):
            order_type = random.choice(["BUY", "SELL"])
            ticker = random.choice(tickers)
            quantity = random.randint(1, 100)  # Random quantity between 1 and 100
            price = round(random.uniform(10, 500), 2)  # Price between $10 and $500
            
            orders.append((order_type, ticker, quantity, price))
        
        for order in orders:
            self.add_order(*order)
            time.sleep(random.uniform(0.1, 0.5))  # Simulate real-time trading delays


# Example Usage
if __name__ == "__main__":
    trading_engine = StockTradingEngine()
    trading_engine.simulate_trading(50)  # Run sequentially without threads

