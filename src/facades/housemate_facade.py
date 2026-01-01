from typing import Optional, List, Dict
from src.infrastructure.database import get_db
from src.repositories.user_repository import UserRepository
from src.repositories.bill_repository import BillRepository
from src.services.auth_service import AuthService
from src.services.bill_service import BillService
from src.validators.bill_validator import BillValidator
from src.services.cost_calculator import CostCalculator
from src.strategies import (
    EqualDistributionStrategy,
    PercentageDistributionStrategy,
    FixedDistributionStrategy
)


class HouseMateFacade:

    def __init__(self):
        self.db = get_db()

        self.user_repository = UserRepository(self.db)
        self.bill_repository = BillRepository(self.db)

        self.bill_validator = BillValidator()

        self.auth_service = AuthService(self.user_repository)
        self.cost_calculator = CostCalculator()
        self.bill_service = BillService(
            self.bill_repository,
            self.bill_validator,
            self.cost_calculator
        )

    def login_user(self, email: str, password: str):
        return self.auth_service.login(email, password)

    def register_user(self, email: str, password: str,
                     first_name: str, last_name: str):
        return self.auth_service.register(email, password, first_name, last_name)

    def create_bill(self, household_id: int, payer_id: int,
                   title: str, amount: float, **kwargs):
        return self.bill_service.create_bill(
            household_id=household_id,
            payer_id=payer_id,
            title=title,
            amount=amount,
            **kwargs
        )

    def get_bill(self, bill_id: int):
        return self.bill_service.get_bill(bill_id)

    def get_household_bills(self, household_id: int):
        return self.bill_service.get_household_bills(household_id)

    def delete_bill(self, bill_id: int):
        return self.bill_service.delete_bill(bill_id)

    def split_bill(self, bill_id: int, participants: List[int],
                   strategy_type: str, params: Dict = None) -> Dict[int, float]:

        if strategy_type == 'equal':
            strategy = EqualDistributionStrategy()
        elif strategy_type == 'percentage':
            strategy = PercentageDistributionStrategy()
        elif strategy_type == 'fixed':
            strategy = FixedDistributionStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_type}")

        return self.bill_service.distribute_bill(
            bill_id=bill_id,
            strategy=strategy,
            participants=participants,
            distribution_params=params
        )
