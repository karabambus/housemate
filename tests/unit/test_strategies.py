import pytest
from src.strategies.equal_distribution import EqualDistributionStrategy
from src.strategies.percentage_distribution_strategy import PercentageDistributionStrategy
from src.strategies.fixed_distribution_strategy import FixedDistributionStrategy


class TestEqualDistributionStrategy:
    """Unit tests for EqualDistributionStrategy."""

    def test_equal_distribution_basic(self):
        """Test basic equal distribution among participants."""
        # Arrange
        strategy = EqualDistributionStrategy()
        total_amount = 300.0
        participants = [1, 2, 3]

        # Act
        result = strategy.calculate(total_amount, participants)

        # Assert
        assert len(result) == 3
        assert result[1] == 100.0
        assert result[2] == 100.0
        assert result[3] == 100.0
        assert sum(result.values()) == total_amount

    def test_equal_distribution_with_rounding(self):
        """Test equal distribution handles rounding correctly."""
        # Arrange
        strategy = EqualDistributionStrategy()
        total_amount = 100.0
        participants = [1, 2, 3]  # 100 / 3 = 33.33...

        # Act
        result = strategy.calculate(total_amount, participants)

        # Assert
        assert len(result) == 3
        # First participant gets rounding difference
        assert result[1] == 33.34  # 33.33 + 0.01
        assert result[2] == 33.33
        assert result[3] == 33.33
        assert sum(result.values()) == total_amount

    def test_equal_distribution_single_participant(self):
        """Test equal distribution with single participant."""
        # Arrange
        strategy = EqualDistributionStrategy()
        total_amount = 150.0
        participants = [1]

        # Act
        result = strategy.calculate(total_amount, participants)

        # Assert
        assert len(result) == 1
        assert result[1] == 150.0

    def test_equal_distribution_negative_amount_fails(self):
        """Test equal distribution fails with negative amount."""
        # Arrange
        strategy = EqualDistributionStrategy()
        total_amount = -50.0
        participants = [1, 2]

        # Act & Assert
        with pytest.raises(ValueError, match="cannot be negative"):
            strategy.calculate(total_amount, participants)

    def test_equal_distribution_empty_participants_fails(self):
        """Test equal distribution fails with empty participants."""
        # Arrange
        strategy = EqualDistributionStrategy()
        total_amount = 100.0
        participants = []

        # Act & Assert
        with pytest.raises(ValueError, match="at least one participant"):
            strategy.calculate(total_amount, participants)

    def test_get_strategy_name(self):
        """Test strategy name is correct."""
        # Arrange
        strategy = EqualDistributionStrategy()

        # Act
        name = strategy.get_strategy_name()

        # Assert
        assert name == "equal"


class TestPercentageDistributionStrategy:
    """Unit tests for PercentageDistributionStrategy."""

    def test_percentage_distribution_basic(self):
        """Test basic percentage distribution."""
        # Arrange
        strategy = PercentageDistributionStrategy()
        total_amount = 200.0
        participants = [1, 2, 3]
        distribution_params = {1: 50.0, 2: 30.0, 3: 20.0}

        # Act
        result = strategy.calculate(total_amount, participants, distribution_params)

        # Assert
        assert len(result) == 3
        assert result[1] == 100.0  # 50% of 200
        assert result[2] == 60.0   # 30% of 200
        assert result[3] == 40.0   # 20% of 200

    def test_percentage_distribution_equal_shares(self):
        """Test percentage distribution with equal shares."""
        # Arrange
        strategy = PercentageDistributionStrategy()
        total_amount = 300.0
        participants = [1, 2]
        distribution_params = {1: 50.0, 2: 50.0}

        # Act
        result = strategy.calculate(total_amount, participants, distribution_params)

        # Assert
        assert result[1] == 150.0
        assert result[2] == 150.0

    def test_percentage_distribution_missing_params_fails(self):
        """Test percentage distribution fails without parameters."""
        # Arrange
        strategy = PercentageDistributionStrategy()
        total_amount = 100.0
        participants = [1, 2]

        # Act & Assert
        with pytest.raises(ValueError, match="must be provided"):
            strategy.calculate(total_amount, participants, None)

    def test_percentage_distribution_missing_participant_fails(self):
        """Test percentage distribution fails if participant missing."""
        # Arrange
        strategy = PercentageDistributionStrategy()
        total_amount = 100.0
        participants = [1, 2, 3]
        distribution_params = {1: 50.0, 2: 50.0}  # Missing participant 3

        # Act & Assert
        with pytest.raises(ValueError, match="not specified for participant"):
            strategy.calculate(total_amount, participants, distribution_params)

    def test_percentage_distribution_not_100_fails(self):
        """Test percentage distribution fails if percentages don't sum to 100."""
        # Arrange
        strategy = PercentageDistributionStrategy()
        total_amount = 100.0
        participants = [1, 2]
        distribution_params = {1: 40.0, 2: 40.0}  # Sum = 80, not 100

        # Act & Assert
        with pytest.raises(ValueError, match="must equal 100"):
            strategy.calculate(total_amount, participants, distribution_params)

    def test_percentage_distribution_negative_amount_fails(self):
        """Test percentage distribution fails with negative amount."""
        # Arrange
        strategy = PercentageDistributionStrategy()
        total_amount = -100.0
        participants = [1, 2]
        distribution_params = {1: 50.0, 2: 50.0}

        # Act & Assert
        with pytest.raises(ValueError, match="cannot be negative"):
            strategy.calculate(total_amount, participants, distribution_params)

    def test_get_strategy_name(self):
        """Test strategy name is correct."""
        # Arrange
        strategy = PercentageDistributionStrategy()

        # Act
        name = strategy.get_strategy_name()

        # Assert
        assert name == "percentage"


class TestFixedDistributionStrategy:
    """Unit tests for FixedDistributionStrategy."""

    def test_fixed_distribution_exact_match(self):
        """Test fixed distribution with exact match."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = 380.0
        participants = [1, 2, 3]
        distribution_params = {1: 100.0, 2: 150.0, 3: 130.0}  # Sum = 380

        # Act
        result = strategy.calculate(total_amount, participants, distribution_params)

        # Assert
        assert len(result) == 3
        assert result[1] == 100.0
        assert result[2] == 150.0
        assert result[3] == 130.0

    def test_fixed_distribution_scaling_down(self):
        """Test fixed distribution with scaling (discount applied)."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = 270.0
        participants = [1, 2, 3]
        distribution_params = {1: 100.0, 2: 150.0, 3: 50.0}  # Sum = 300

        # Act
        result = strategy.calculate(total_amount, participants, distribution_params)

        # Assert
        assert len(result) == 3
        assert result[1] == 90.0   # 100 * (270/300)
        assert result[2] == 135.0  # 150 * (270/300)
        assert result[3] == 45.0   # 50 * (270/300)
        assert sum(result.values()) == total_amount

    def test_fixed_distribution_single_participant(self):
        """Test fixed distribution with single participant."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = 100.0
        participants = [1]
        distribution_params = {1: 100.0}

        # Act
        result = strategy.calculate(total_amount, participants, distribution_params)

        # Assert
        assert result[1] == 100.0

    def test_fixed_distribution_missing_params_fails(self):
        """Test fixed distribution fails without parameters."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = 100.0
        participants = [1, 2]

        # Act & Assert
        with pytest.raises(ValueError, match="must be provided"):
            strategy.calculate(total_amount, participants, None)

    def test_fixed_distribution_missing_participant_fails(self):
        """Test fixed distribution fails if participant missing."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = 100.0
        participants = [1, 2, 3]
        distribution_params = {1: 50.0, 2: 50.0}  # Missing participant 3

        # Act & Assert
        with pytest.raises(ValueError, match="not specified for participant"):
            strategy.calculate(total_amount, participants, distribution_params)

    def test_fixed_distribution_insufficient_amount_fails(self):
        """Test fixed distribution fails if fixed amounts can't cover total."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = 300.0
        participants = [1, 2]
        distribution_params = {1: 100.0, 2: 100.0}  # Sum = 200, less than 300

        # Act & Assert
        with pytest.raises(ValueError, match="cannot cover"):
            strategy.calculate(total_amount, participants, distribution_params)

    def test_fixed_distribution_negative_amount_fails(self):
        """Test fixed distribution fails with negative amount."""
        # Arrange
        strategy = FixedDistributionStrategy()
        total_amount = -100.0
        participants = [1, 2]
        distribution_params = {1: 50.0, 2: 50.0}

        # Act & Assert
        with pytest.raises(ValueError, match="cannot be negative"):
            strategy.calculate(total_amount, participants, distribution_params)

    def test_get_strategy_name(self):
        """Test strategy name is correct."""
        # Arrange
        strategy = FixedDistributionStrategy()

        # Act
        name = strategy.get_strategy_name()

        # Assert
        assert name == "fixed"
