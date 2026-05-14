from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DerivativesPortfolio:
    initial_cash: float = 100_000_000
    contract_multiplier: float = 100_000
    margin_rate: float = 0.15
    fee_per_contract: float = 3000

    cash: float = field(init=False)
    position: int = field(default=0, init=False)
    entry_price: Optional[float] = field(default=None, init=False)

    trades: list = field(default_factory=list, init=False)
    equity_curve: list = field(default_factory=list, init=False)

    def __post_init__(self):
        self.cash = float(self.initial_cash)

    def unrealized_pnl(self, current_price: float) -> float:
        if self.position == 0 or self.entry_price is None:
            return 0.0

        return (current_price - self.entry_price) * self.position * self.contract_multiplier

    def total_equity(self, current_price: float) -> float:
        return self.cash + self.unrealized_pnl(current_price)

    def required_margin(self, price: float, quantity: int) -> float:
        notional_value = price * self.contract_multiplier * quantity
        return notional_value * self.margin_rate

    def can_open_position(self, price: float, quantity: int) -> bool:
        margin = self.required_margin(price, quantity)
        fee = quantity * self.fee_per_contract
        return self.cash >= margin + fee

    def open_long(self, date, price: float, quantity: int = 1, reason: str = "OPEN_LONG"):
        if self.position != 0:
            return None

        if not self.can_open_position(price, quantity):
            return None

        fee = quantity * self.fee_per_contract

        self.cash -= fee
        self.position = quantity
        self.entry_price = price

        trade = {
            "date": date,
            "action": "OPEN_LONG",
            "price": price,
            "quantity": quantity,
            "position_after": self.position,
            "fee": fee,
            "realized_pnl": 0,
            "cash_after": self.cash,
            "reason": reason
        }

        self.trades.append(trade)
        return trade

    def open_short(self, date, price: float, quantity: int = 1, reason: str = "OPEN_SHORT"):
        if self.position != 0:
            return None

        if not self.can_open_position(price, quantity):
            return None

        fee = quantity * self.fee_per_contract

        self.cash -= fee
        self.position = -quantity
        self.entry_price = price

        trade = {
            "date": date,
            "action": "OPEN_SHORT",
            "price": price,
            "quantity": quantity,
            "position_after": self.position,
            "fee": fee,
            "realized_pnl": 0,
            "cash_after": self.cash,
            "reason": reason
        }

        self.trades.append(trade)
        return trade

    def close_position(self, date, price: float, reason: str = "CLOSE_POSITION"):
        if self.position == 0 or self.entry_price is None:
            return None

        quantity = abs(self.position)
        fee = quantity * self.fee_per_contract

        realized_pnl = (price - self.entry_price) * self.position * self.contract_multiplier

        self.cash += realized_pnl
        self.cash -= fee

        action = "CLOSE_LONG" if self.position > 0 else "CLOSE_SHORT"

        trade = {
            "date": date,
            "action": action,
            "price": price,
            "quantity": quantity,
            "position_after": 0,
            "fee": fee,
            "realized_pnl": realized_pnl,
            "cash_after": self.cash,
            "reason": reason
        }

        self.trades.append(trade)

        self.position = 0
        self.entry_price = None

        return trade

    def mark_to_market(self, date, close_price: float):
        unrealized = self.unrealized_pnl(close_price)
        equity = self.total_equity(close_price)

        record = {
            "date": date,
            "close": close_price,
            "cash": self.cash,
            "position": self.position,
            "entry_price": self.entry_price,
            "unrealized_pnl": unrealized,
            "total_equity": equity
        }

        self.equity_curve.append(record)
        return record