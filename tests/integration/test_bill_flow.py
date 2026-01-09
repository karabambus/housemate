"""
Integration tests for Bill flow.

These tests use a real database (no mocks) and test the full stack:
- Repository -> Service -> Business Logic
- Database interactions
- Full bill lifecycle

IMPORTANT: These are integration tests without mocks (I8 - 1 bod requirement)
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
class TestBillFlowIntegration:
    """Integration tests for complete bill flow without mocks."""

    def test_create_and_retrieve_bill(self, test_db, sample_household, sample_users):
        """Test creating a bill and retrieving it from database."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Act - Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Electricity Bill',
            amount=150.0,
            category='utilities',
            due_date='2024-12-31'
        )

        # Act - Retrieve bill
        bill = service.get_bill(bill_id)

        # Assert
        assert bill is not None
        assert bill.bill_id == bill_id
        assert bill.title == 'Electricity Bill'
        assert bill.amount == 150.0
        assert bill.category == 'utilities'
        assert bill.household_id == sample_household
        assert bill.payer_id == sample_users['user1_id']
        assert bill.payment_status == 'pending'

    def test_create_bill_with_validation_error(self, test_db, sample_household, sample_users):
        """Test that bill creation fails with invalid data."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Act & Assert - Try to create bill with negative amount
        with pytest.raises(ValueError, match="Validation failed"):
            service.create_bill(
                household_id=sample_household,
                payer_id=sample_users['user1_id'],
                title='Invalid Bill',
                amount=-50.0  # Invalid negative amount
            )

        # Verify no bill was created in database
        bills = repository.find_by_household(sample_household)
        assert len(bills) == 0

    def test_update_bill_status(self, test_db, sample_household, sample_users):
        """Test updating bill payment status."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Rent',
            amount=500.0,
            category='rent'
        )

        # Act - Update status to paid
        result = service.update_bill_status(bill_id, 'paid')

        # Assert
        assert result is True
        updated_bill = service.get_bill(bill_id)
        assert updated_bill.payment_status == 'paid'

    def test_delete_bill(self, test_db, sample_household, sample_users):
        """Test deleting a bill."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Temporary Bill',
            amount=25.0
        )

        # Act - Delete bill
        result = service.delete_bill(bill_id)

        # Assert
        assert result is True
        deleted_bill = service.get_bill(bill_id)
        assert deleted_bill is None

    def test_get_household_bills(self, test_db, sample_household, sample_users):
        """Test retrieving all bills for a household."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create multiple bills
        service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Water',
            amount=30.0,
            category='utilities'
        )
        service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user2_id'],
            title='Internet',
            amount=60.0,
            category='utilities'
        )
        service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user3_id'],
            title='Groceries',
            amount=100.0,
            category='food'
        )

        # Act
        bills = service.get_household_bills(sample_household)

        # Assert
        assert len(bills) == 3
        bill_titles = [bill.title for bill in bills]
        assert 'Water' in bill_titles
        assert 'Internet' in bill_titles
        assert 'Groceries' in bill_titles

    def test_distribute_bill_equal_strategy(self, test_db, sample_household, sample_users):
        """Test bill distribution with equal strategy - full integration."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Shared Groceries',
            amount=300.0,
            category='food'
        )

        # Act - Distribute using equal strategy
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

        # Assert
        assert len(distribution) == 3
        assert distribution[sample_users['user1_id']] == 100.0
        assert distribution[sample_users['user2_id']] == 100.0
        assert distribution[sample_users['user3_id']] == 100.0
        assert sum(distribution.values()) == 300.0

    def test_distribute_bill_percentage_strategy(self, test_db, sample_household, sample_users):
        """Test bill distribution with percentage strategy."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Utilities',
            amount=200.0,
            category='utilities'
        )

        # Act - Distribute using percentage strategy
        strategy = PercentageDistributionStrategy()
        distribution = service.distribute_bill(
            bill_id=bill_id,
            strategy=strategy,
            participants=[
                sample_users['user1_id'],
                sample_users['user2_id'],
                sample_users['user3_id']
            ],
            distribution_params={
                sample_users['user1_id']: 50.0,
                sample_users['user2_id']: 30.0,
                sample_users['user3_id']: 20.0
            }
        )

        # Assert
        assert distribution[sample_users['user1_id']] == 100.0  # 50%
        assert distribution[sample_users['user2_id']] == 60.0   # 30%
        assert distribution[sample_users['user3_id']] == 40.0   # 20%

    def test_distribute_bill_fixed_strategy(self, test_db, sample_household, sample_users):
        """Test bill distribution with fixed amount strategy."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Shopping',
            amount=250.0,
            category='food'
        )

        # Act - Distribute using fixed strategy
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
                sample_users['user2_id']: 100.0,
                sample_users['user3_id']: 50.0
            }
        )

        # Assert
        assert distribution[sample_users['user1_id']] == 100.0
        assert distribution[sample_users['user2_id']] == 100.0
        assert distribution[sample_users['user3_id']] == 50.0
        assert sum(distribution.values()) == 250.0

    def test_strategy_switching(self, test_db, sample_household, sample_users):
        """Test switching between different distribution strategies for same bill."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Create bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Monthly Bill',
            amount=300.0
        )

        participants = [
            sample_users['user1_id'],
            sample_users['user2_id'],
            sample_users['user3_id']
        ]

        # Act - Try equal distribution
        equal_strategy = EqualDistributionStrategy()
        equal_dist = service.distribute_bill(bill_id, equal_strategy, participants)

        # Act - Switch to percentage distribution
        percentage_strategy = PercentageDistributionStrategy()
        percentage_dist = service.distribute_bill(
            bill_id,
            percentage_strategy,
            participants,
            {
                sample_users['user1_id']: 50.0,
                sample_users['user2_id']: 30.0,
                sample_users['user3_id']: 20.0
            }
        )

        # Assert - Both strategies work on same bill
        assert sum(equal_dist.values()) == 300.0
        assert sum(percentage_dist.values()) == 300.0
        assert equal_dist != percentage_dist  # Different distributions

    def test_recurring_bill_creation(self, test_db, sample_household, sample_users):
        """Test creating a recurring bill."""
        # Arrange
        repository = BillRepository(test_db)
        validator = BillValidator()
        calculator = CostCalculator()
        service = BillService(repository, validator, calculator)

        # Act - Create recurring bill
        bill_id = service.create_bill(
            household_id=sample_household,
            payer_id=sample_users['user1_id'],
            title='Monthly Rent',
            amount=1000.0,
            category='rent',
            is_recurring=True,
            frequency='monthly',
            due_date='2024-01-01'
        )

        # Retrieve and assert
        bill = service.get_bill(bill_id)
        assert bill.is_recurring is True
        assert bill.frequency == 'monthly'
        assert bill.amount == 1000.0
