#what i want to retrieve

from decimal import Decimal
from pydantic import BaseModel


#response
class DashboardSummary(BaseModel):
    # income: Decimal
    expenses: Decimal
    # net_cash_flow: Decimal
    # savings_rate: Decimal