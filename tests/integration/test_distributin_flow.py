"""
Integration tests for Bill Distribution flow (NO MOCKS).
Tests full stack with real database, real calculations, all strategies.
"""
import pytest
from src.repositories.bill_repository import BillRepository
from src.validators.bill_validator import BillValidator
from src.services.bill_service import BillService
from src.services.cost_calculator import CostCalculator
from src.strategies.equal_distribution import EqualDistributionStrategy
from src.strategies.percentage_distribution_strategy import PercentageDistributionStrategy
from src.strategies.fixed_distribution_strategy import FixedDistributionStrategy


@pytest.mark.integration
class TestDistributionFlowIntegration:

    def test_end_to_end_equal_distribution(self, test_db, sample_household, sample_users):
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Pizza Night',
            amount=90.0,
            category='food'
        )

        strategy = EqualDistributionStrategy()
        distribution = service.distribute_bill(
            bill_id=bill_id,
            strategy=strategy,
            participants=[
                sample_users['user1_id'],
                sample_users['user2_id'],
                sample_users['user3_id']
            ]
        )

        assert sum(distribution.values()) == 90.0
        assert distribution[sample_users['user1_id']] == 30.0
        assert distribution[sample_users['user2_id']] == 30.0
        assert distribution[sample_users['user3_id']] == 30.0

    def test_end_to_end_percentage_distribution(self, test_db, sample_household, sample_users):
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Shared Expenses',
            amount=1000.0,
            category='other'
        )

        strategy = PercentageDistributionStrategy()
        distribution = service.distribute_bill(
            bill_id=bill_id,
            strategy=strategy,
            participants=[sample_users['user1_id'], sample_users['user2_id']],
            distribution_params={
                sample_users['user1_id']: 70.0,
                sample_users['user2_id']: 30.0
            }
        )

        assert distribution[sample_users['user1_id']] == 700.0
        assert distribution[sample_users['user2_id']] == 300.0

    def test_end_to_end_fixed_distribution(self, test_db, sample_household, sample_users):
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Groceries with discount',
            amount=180.0,
            category='food'
        )

        strategy = FixedDistributionStrategy()
        distribution = service.distribute_bill(
            bill_id=bill_id,
            strategy=strategy,
            participants=[
                sample_users['user1_id'],
                sample_users['user2_id'],
                sample_users['user3_id']
            ],
            distribution_params={
                sample_users['user1_id']: 100.0,
                sample_users['user2_id']: 80.0,
                sample_users['user3_id']: 20.0
            }
        )

        assert sum(distribution.values()) == 180.0
        assert distribution[sample_users['user1_id']] == 90.0
        assert distribution[sample_users['user2_id']] == 72.0
        assert distribution[sample_users['user3_id']] == 18.0

    def test_multiple_bills_different_strategies(self, test_db, sample_household, sample_users):
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        bill1_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Bill 1',
            amount=150.0
        )

        bill2_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user2_id'],
            title='Bill 2',
            amount=200.0
        )

        equal_strategy = EqualDistributionStrategy()
        dist1 = service.distribute_bill(
            bill1_id,
            equal_strategy,
            [sample_users['user1_id'], sample_users['user2_id'], sample_users['user3_id']]
        )

        percentage_strategy = PercentageDistributionStrategy()
        dist2 = service.distribute_bill(
            bill2_id,
            percentage_strategy,
            [sample_users['user1_id'], sample_users['user2_id'], sample_users['user3_id']],
            {
                sample_users['user1_id']: 40.0,
                sample_users['user2_id']: 40.0,
                sample_users['user3_id']: 20.0
            }
        )

        assert sum(dist1.values()) == 150.0
        assert sum(dist2.values()) == 200.0
        assert dist1[sample_users['user1_id']] == 50.0
        assert dist2[sample_users['user1_id']] == 80.0

    def test_create_bill_distribute_update_status(self, test_db, sample_household, sample_users):
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Full Lifecycle Bill',
            amount=300.0,
            category='utilities'
        )

        bill = service.get_bill(bill_id)
        assert bill.payment_status == 'pending'

        strategy = EqualDistributionStrategy()
        distribution = service.distribute_bill(
            bill_id,
            strategy,
            [sample_users['user1_id'], sample_users['user2_id'], sample_users['user3_id']]
        )
        assert len(distribution) == 3

        service.update_bill_status(bill_id, 'paid')
        updated_bill = service.get_bill(bill_id)
        assert updated_bill.payment_status == 'paid'

    def test_distribution_with_rounding(self, test_db, sample_household, sample_users):
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Odd Amount Bill',
            amount=100.0
        )

        strategy = EqualDistributionStrategy()
        distribution = service.distribute_bill(
            bill_id,
            strategy,
            [sample_users['user1_id'], sample_users['user2_id'], sample_users['user3_id']]
        )

        assert distribution[sample_users['user1_id']] == 33.34
        assert distribution[sample_users['user2_id']] == 33.33
        assert distribution[sample_users['user3_id']] == 33.33
        assert sum(distribution.values()) == 100.0
