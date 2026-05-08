import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Portfolio:
    initial_cash: float = 100_000_000
    lot_size: int = 100
    fee_rate: float = 0.001
    sell_tax_rate: float = 0.001

    cash: float = field(init=False)
    shares: int = field(default=0, init=False)
    avg_price: Optional[float] = field(default=None, init=False)

    trades: list = field(default_factory=list, init=False)
    equity_curve: list = field(default_factory=list, init=False)

    def __post_init__(self):
        self.cash = float(self.initial_cash)

    def total_value(self, current_price: float) -> float:
        return self.cash + self.shares * current_price

    def _round_lot(self, quantity: int) -> int:
        return quantity // self.lot_size * self.lot_size

    def buy(self, date, price: float, allocation_pct: float = 1.0, reason: str = "BUY"):
        """
        Mua cổ phiếu.
        Mặc định dùng 100% tiền mặt hiện có.
        """

        if price <= 0:
            return None

        available_cash = self.cash * allocation_pct

        quantity = math.floor(available_cash / (price * (1 + self.fee_rate)))
        quantity = self._round_lot(quantity)

        if quantity <= 0:
            return None

        value = quantity * price
        fee = value * self.fee_rate
        total_cost = value + fee

        if total_cost > self.cash:
            return None

        old_position_value = 0

        if self.shares > 0 and self.avg_price is not None:
            old_position_value = self.shares * self.avg_price

        self.cash -= total_cost
        self.shares += quantity
        self.avg_price = (old_position_value + value) / self.shares

        trade = {
            "date": date,
            "action": "BUY",
            "price": price,
            "quantity": quantity,
            "value": value,
            "fee": fee,
            "tax": 0,
            "cash_after": self.cash,
            "shares_after": self.shares,
            "avg_price_after": self.avg_price,
            "pnl": 0,
            "reason": reason
        }

        self.trades.append(trade)

        return trade

    def sell(self, date, price: float, quantity: Optional[int] = None, reason: str = "SELL"):
        """
        Bán cổ phiếu.
        Nếu không truyền quantity thì bán toàn bộ.
        """

        if price <= 0:
            return None

        if self.shares <= 0:
            return None

        if quantity is None:
            quantity = self.shares
        else:
            quantity = min(quantity, self.shares)
            quantity = self._round_lot(quantity)

        if quantity <= 0:
            return None

        value = quantity * price
        fee = value * self.fee_rate
        tax = value * self.sell_tax_rate
        net_received = value - fee - tax

        if self.avg_price is not None:
            pnl = (price - self.avg_price) * quantity - fee - tax
        else:
            pnl = 0

        self.cash += net_received
        self.shares -= quantity

        if self.shares == 0:
            self.avg_price = None

        trade = {
            "date": date,
            "action": "SELL",
            "price": price,
            "quantity": quantity,
            "value": value,
            "fee": fee,
            "tax": tax,
            "cash_after": self.cash,
            "shares_after": self.shares,
            "avg_price_after": self.avg_price,
            "pnl": pnl,
            "reason": reason
        }

        self.trades.append(trade)

        return trade

    def mark_to_market(self, date, close_price: float):
        """
        Ghi lại giá trị tài khoản theo từng ngày.
        """

        market_value = self.shares * close_price
        total_value = self.cash + market_value

        if self.shares > 0 and self.avg_price is not None:
            unrealized_pnl = (close_price - self.avg_price) * self.shares
        else:
            unrealized_pnl = 0

        record = {
            "date": date,
            "close": close_price,
            "cash": self.cash,
            "shares": self.shares,
            "market_value": market_value,
            "total_value": total_value,
            "unrealized_pnl": unrealized_pnl
        }

        self.equity_curve.append(record)

        return record