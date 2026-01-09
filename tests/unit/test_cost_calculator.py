import pytest
from unittest.mock import Mock
from src.services.cost_calculator import CostCalculator
from src.strategies.equal_distribution import EqualDistributionStrategy
from src.strategies.percentage_distribution_strategy import PercentageDistributionStrategy
from src.strategies.fixed_distribution_strategy import FixedDistributionStrategy


class TestCostCalculator:
    """Unit tests for CostCalculator service."""

    def test_calculate_with_equal_strategy(self):
        """Test calculator with equal distribution strategy."""
        # Arrange
        calculator = CostCalculator()
        strategy = EqualDistributionStrategy()
        total_amount = 300.0
        participants = [1, 2, 3]

        # Act
        result = calculator.calculate_with_strategy(
            strategy=strategy,
            total_amount=total_amount,
            participants=participants
        )

        # Assert
        assert len(result) == 3
        assert result[1] == 100.0
        assert result[2] == 100.0
        assert result[3] == 100.0

    def test_calculate_with_percentage_strategy(self):
        """Test calculator with percentage distribution strategy."""
        # Arrange
        calculator = CostCalculator()
        strategy = PercentageDistributionStrategy()
        total_amount = 200.0
        participants = [1, 2]
        distribution_params = {1: 60.0, 2: 40.0}

        # Act
        result = calculator.calculate_with_strategy(
            strategy=strategy,
            total_amount=total_amount,
            participants=participants,
            distribution_params=distribution_params
        )

        # Assert
        assert result[1] == 120.0  # 60% of 200
        assert result[2] == 80.0   # 40% of 200

    def test_calculate_with_fixed_strategy(self):
        """Test calculator with fixed distribution strategy."""
        # Arrange
        calculator = CostCalculator()
        strategy = FixedDistributionStrategy()
        total_amount = 300.0
        participants = [1, 2]
        distribution_params = {1: 200.0, 2: 100.0}

        # Act
        result = calculator.calculate_with_strategy(
            strategy=strategy,
            total_amount=total_amount,
            participants=participants,
            distribution_params=distribution_params
        )

        # Assert
        assert result[1] == 200.0
        assert result[2] == 100.0

    def test_calculate_with_mocked_strategy(self):
        """Test calculator delegates correctly to strategy using mock."""
        # Arrange
        calculator = CostCalculator()
        mock_strategy = Mock()
        expected_result = {1: 150.0, 2: 150.0}
        mock_strategy.calculate.return_value = expected_result

        total_amount = 300.0
        participants = [1, 2]
        params = {'test': 'param'}

        # Act
        result = calculator.calculate_with_strategy(
            strategy=mock_strategy,
            total_amount=total_amount,
            participants=participants,
            distribution_params=params
        )

        # Assert
        assert result == expected_result
        mock_strategy.calculate.assert_called_once_with(
            total_amount, participants, params
        )

    def test_get_strategy_name_equal(self):
        """Test getting strategy name for equal distribution."""
        # Arrange
        calculator = CostCalculator()
        strategy = EqualDistributionStrategy()

        # Act
        name = calculator.get_strategy_name(strategy)

        # Assert
        assert name == "equal"

    def test_get_strategy_name_percentage(self):
        """Test getting strategy name for percentage distribution."""
        # Arrange
        calculator = CostCalculator()
        strategy = PercentageDistributionStrategy()

        # Act
        name = calculator.get_strategy_name(strategy)

        # Assert
        assert name == "percentage"

    def test_get_strategy_name_fixed(self):
        """Test getting strategy name for fixed distribution."""
        # Arrange
        calculator = CostCalculator()
        strategy = FixedDistributionStrategy()

        # Act
        name = calculator.get_strategy_name(strategy)

        # Assert
        assert name == "fixed"

    def test_get_strategy_name_with_mock(self):
        """Test getting strategy name with mocked strategy."""
        # Arrange
        calculator = CostCalculator()
        mock_strategy = Mock()
        mock_strategy.get_strategy_name.return_value = "custom"

        # Act
        name = calculator.get_strategy_name(mock_strategy)

        # Assert
        assert name == "custom"
        mock_strategy.get_strategy_name.assert_called_once()

    def test_strategy_substitution(self):
        """Test Liskov Substitution - strategies are interchangeable."""
        # Arrange
        calculator = CostCalculator()
        total_amount = 100.0
        participants = [1, 2]

        # Equal strategy
        equal_strategy = EqualDistributionStrategy()
        equal_result = calculator.calculate_with_strategy(
            equal_strategy, total_amount, participants
        )

        # Percentage strategy (50-50)
        percentage_strategy = PercentageDistributionStrategy()
        percentage_result = calculator.calculate_with_strategy(
            percentage_strategy, total_amount, participants,
            {1: 50.0, 2: 50.0}
        )

        # Assert - same result with different strategies (equal split)
        assert equal_result == percentage_result
        assert equal_result[1] == 50.0
        assert equal_result[2] == 50.0
