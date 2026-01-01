# SOLID Principles Demonstration - HouseMate

This document demonstrates all 5 SOLID principles implemented in the HouseMate application, specifically in the Cost Distribution module (Module 2).

## Table of Contents
1. [S - Single Responsibility Principle](#s---single-responsibility-principle)
2. [O - Open/Closed Principle](#o---openclosed-principle)
3. [L - Liskov Substitution Principle](#l---liskov-substitution-principle)
4. [I - Interface Segregation Principle](#i---interface-segregation-principle)
5. [D - Dependency Inversion Principle](#d---dependency-inversion-principle)
6. [How to View SOLID in Git History](#how-to-view-solid-in-git-history)

---

## S - Single Responsibility Principle

> **A class should have one, and only one, reason to change.**

### Demonstration

The Bill management module is split into multiple classes, each with a single responsibility:

#### ❌ BAD (Violates SRP)
```python
class BillManager:
    def save_to_database(self, bill):
        # Database logic here (reason to change #1: database changes)
        pass

    def validate_bill(self, bill):
        # Validation logic here (reason to change #2: validation rules change)
        pass

    def send_notification(self, user, bill):
        # Notification logic here (reason to change #3: notification system changes)
        pass

    def calculate_distribution(self, bill, participants):
        # Calculation logic here (reason to change #4: calculation rules change)
        pass
```

**Problems:**
- 4 different reasons to change this class
- If database changes, must touch this file
- If validation rules change, must touch this file
- If notification system changes, must touch this file
- Hard to test (must mock everything)
- Hard to understand (too many responsibilities)

#### ✓ GOOD (Follows SRP)

**File: `src/repositories/bill_repository.py`**
```python
class BillRepository:
    """Single Responsibility: Database operations only"""

    def __init__(self, db_connection):
        self.db = db_connection

    def save(self, bill):
        # ONLY database operations
        # Reason to change: database schema changes
        pass

    def find_by_id(self, bill_id):
        # ONLY database retrieval
        pass
```

**File: `src/validators/bill_validator.py`**
```python
class BillValidator:
    """Single Responsibility: Validation only"""

    def validate(self, bill_data):
        # ONLY validation logic
        # Reason to change: validation rules change
        pass
```

**File: `src/services/bill_service.py`**
```python
class BillService:
    """Single Responsibility: Coordinate operations only"""

    def __init__(self, repository, validator, calculator):
        self.repository = repository
        self.validator = validator
        self.calculator = calculator

    def create_bill(self, bill_data):
        # ONLY coordination - delegates to other classes
        # 1. Validate using validator
        # 2. Save using repository
        # Reason to change: business process changes
        pass
```

**Benefits:**
- Each class has exactly ONE reason to change
- Easy to test (mock one dependency at a time)
- Easy to understand (clear, focused responsibility)
- Changes isolated to appropriate class

### Code Examples in Project

| Class | Responsibility | File |
|-------|---------------|------|
| `BillRepository` | Database operations only | `src/repositories/bill_repository.py` |
| `BillValidator` | Validation only | `src/validators/bill_validator.py` |
| `BillService` | Coordinate bill operations | `src/services/bill_service.py` |
| `CostCalculator` | Calculate cost distributions | `src/services/cost_calculator.py` |
| `EqualDistributionStrategy` | Equal distribution calculation | `src/strategies/equal_distribution.py` |

---

## O - Open/Closed Principle

> **Software entities should be open for extension, but closed for modification.**

### Demonstration

The cost distribution system uses the Strategy Pattern to enable adding new distribution methods WITHOUT modifying existing code.

#### ❌ BAD (Violates OCP)

**File: `src/services/cost_calculator.py` (BEFORE refactoring - see commit 93e79de)**
```python
class CostCalculator:
    def calculate(self, strategy_type: str, total_amount: float, participants: List[int]):
        """
        Problem: Adding new strategy requires MODIFYING this method
        """
        if strategy_type == "equal":
            # 15 lines of equal distribution logic
            num_participants = len(participants)
            equal_share = total_amount / num_participants
            return {user_id: equal_share for user_id in participants}

        elif strategy_type == "percentage":
            # 12 lines of percentage distribution logic
            # ...

        elif strategy_type == "fixed":
            # 10 lines of fixed distribution logic
            # ...

        else:
            raise ValueError(f"Unknown strategy: {strategy_type}")
```

**To add new strategy (e.g., weighted by income):**
```python
# Must MODIFY CostCalculator.calculate() method
elif strategy_type == "weighted":
    # Add 15 more lines here
    # MODIFIED existing code! Violates OCP!
```

**Problems:**
- Must modify `CostCalculator` every time new strategy is added
- if/else chain grows longer
- Violates Open/Closed Principle
- Risk of breaking existing strategies

#### ✓ GOOD (Follows OCP)

**File: `src/interfaces/i_cost_strategy.py`**
```python
class ICostDistributionStrategy(ABC):
    """
    Interface defines contract.
    CLOSED for modification - interface doesn't change.
    """

    @abstractmethod
    def calculate(self, total_amount: float, participants: List[int],
                  distribution_params: Dict = None) -> Dict[int, float]:
        pass
```

**File: `src/services/cost_calculator.py` (AFTER refactoring - see commit 9f85f97)**
```python
class CostCalculator:
    def calculate_with_strategy(
        self,
        strategy: ICostDistributionStrategy,  # Accepts ANY strategy
        total_amount: float,
        participants: List[int],
        distribution_params: Dict = None
    ) -> Dict[int, float]:
        """
        OPEN for extension - accepts new strategies
        CLOSED for modification - this method never changes
        """
        return strategy.calculate(total_amount, participants, distribution_params)
```

**File: `src/strategies/equal_distribution.py`**
```python
class EqualDistributionStrategy(ICostDistributionStrategy):
    """EXTENSION: Implements equal distribution"""

    def calculate(self, total_amount, participants, distribution_params=None):
        num_participants = len(participants)
        equal_share = total_amount / num_participants
        return {user_id: equal_share for user_id in participants}
```

**File: `src/strategies/percentage_distribution_strategy.py`**
```python
class PercentageDistributionStrategy(ICostDistributionStrategy):
    """EXTENSION: Implements percentage distribution"""

    def calculate(self, total_amount, participants, distribution_params=None):
        # Percentage distribution logic
        pass
```

**File: `src/strategies/fixed_distribution_strategy.py`**
```python
class FixedDistributionStrategy(ICostDistributionStrategy):
    """EXTENSION: Implements fixed amount distribution"""

    def calculate(self, total_amount, participants, distribution_params=None):
        # Fixed amount distribution logic
        pass
```

**To add new strategy (e.g., weighted by income):**
```python
# Create NEW file: src/strategies/weighted_distribution_strategy.py
class WeightedDistributionStrategy(ICostDistributionStrategy):
    """EXTENSION: New strategy - NO modifications to existing code!"""

    def calculate(self, total_amount, participants, distribution_params=None):
        # New weighted distribution logic
        incomes = distribution_params.get('incomes', {})
        total_income = sum(incomes.values())

        result = {}
        for user_id in participants:
            income_ratio = incomes[user_id] / total_income
            result[user_id] = total_amount * income_ratio

        return result

# Use it immediately - NO changes to CostCalculator or other strategies!
strategy = WeightedDistributionStrategy()
calculator.calculate_with_strategy(strategy, 300.00, [1, 2, 3],
                                   {'incomes': {1: 30000, 2: 50000, 3: 40000}})
```

**Benefits:**
- Adding new strategy = creating ONE new file
- ZERO modifications to existing code
- Existing strategies continue working unchanged
- No risk of breaking existing functionality

### Git History Demonstration

View the transformation from BEFORE (violates OCP) to AFTER (follows OCP):

```bash
# View BEFORE code (violates OCP)
git show 93e79de:src/services/cost_calculator.py

# View AFTER code (follows OCP)
git show 9f85f97:src/services/cost_calculator.py

# View the diff
git diff 93e79de 9f85f97 src/services/cost_calculator.py
```

---

## L - Liskov Substitution Principle

> **Objects of a superclass should be replaceable with objects of a subclass without breaking the application.**

### Demonstration

All `ICostDistributionStrategy` implementations are fully substitutable for one another.

#### ✓ GOOD (Follows LSP)

**All strategies implement the same interface:**
```python
# All these are SUBSTITUTABLE - work identically from caller's perspective
strategy1 = EqualDistributionStrategy()
strategy2 = PercentageDistributionStrategy()
strategy3 = FixedDistributionStrategy()

# Can swap at any time without breaking code
calculator.calculate_with_strategy(strategy1, 300.00, [1, 2, 3])
calculator.calculate_with_strategy(strategy2, 300.00, [1, 2, 3])
calculator.calculate_with_strategy(strategy3, 300.00, [1, 2, 3])
```

**Runtime substitution works:**
```python
class BillService:
    def distribute_bill(self, bill_id, strategy: ICostDistributionStrategy, participants):
        """
        Accepts ANY strategy - they're all substitutable
        LSP: Can substitute any ICostDistributionStrategy without breaking
        """
        bill = self.repository.find_by_id(bill_id)

        # This works with ALL strategies
        distribution = self.calculator.calculate_with_strategy(
            strategy=strategy,  # ANY strategy works here
            total_amount=bill.amount,
            participants=participants
        )

        return distribution

# All these work identically:
service.distribute_bill(1, EqualDistributionStrategy(), [1, 2, 3])
service.distribute_bill(1, PercentageDistributionStrategy(), [1, 2, 3])
service.distribute_bill(1, FixedDistributionStrategy(), [1, 2, 3])

# Can even swap at runtime
user_choice = request.form['strategy_type']
if user_choice == 'equal':
    strategy = EqualDistributionStrategy()
elif user_choice == 'percentage':
    strategy = PercentageDistributionStrategy()
else:
    strategy = FixedDistributionStrategy()

# Works regardless of which strategy was chosen
service.distribute_bill(bill_id, strategy, participants)
```

**Contract enforcement:**

All strategies follow the same contract:
- Accept same parameters: `total_amount`, `participants`, `distribution_params`
- Return same structure: `Dict[int, float]` (user_id -> amount_owed)
- Raise `ValueError` for invalid inputs
- Guarantee total distributed equals total_amount (within rounding tolerance)

#### ❌ BAD (Violates LSP)

Example of LSP violation (NOT in our code):
```python
class BrokenStrategy(ICostDistributionStrategy):
    def calculate(self, total_amount, participants, distribution_params=None):
        # Violates LSP: Returns string instead of Dict[int, float]
        return "User 1: $100, User 2: $200"  # Wrong type!

class AnotherBrokenStrategy(ICostDistributionStrategy):
    def calculate(self, total_amount, participants, distribution_params=None):
        # Violates LSP: Requires distribution_params (not optional)
        if distribution_params is None:
            raise TypeError("distribution_params is required!")  # Breaks substitutability
```

**Our code follows LSP:**
- All strategies return `Dict[int, float]`
- All strategies accept optional `distribution_params`
- All strategies validate inputs consistently
- All strategies can be substituted without code changes

---

## I - Interface Segregation Principle

> **Many client-specific interfaces are better than one general-purpose interface.**

### Demonstration

Instead of one large "fat" interface, we use multiple small, focused interfaces.

#### ❌ BAD (Violates ISP)

```python
class IBillManager(ABC):
    """
    FAT INTERFACE - forces classes to implement methods they don't need
    """

    # Database operations
    @abstractmethod
    def save(self, bill): pass

    @abstractmethod
    def find_by_id(self, id): pass

    @abstractmethod
    def delete(self, id): pass

    # Validation
    @abstractmethod
    def validate(self, data): pass

    # Notifications
    @abstractmethod
    def send_email(self, user, message): pass

    @abstractmethod
    def send_sms(self, user, message): pass

    # Cost calculation
    @abstractmethod
    def calculate_equal(self, amount, participants): pass

    @abstractmethod
    def calculate_percentage(self, amount, participants): pass

    # File handling
    @abstractmethod
    def save_receipt(self, file): pass

    @abstractmethod
    def delete_receipt(self, file): pass

    # ... 20 more methods ...
```

**Problems:**
- Classes forced to implement methods they don't use
- Tight coupling
- Hard to test
- Hard to maintain

#### ✓ GOOD (Follows ISP)

**Multiple small, focused interfaces:**

**File: `src/interfaces/i_repository.py`**
```python
class IRepository(ABC):
    """
    FOCUSED: Only repository operations
    Client only needs database operations? Use this interface.
    """

    @abstractmethod
    def save(self, entity): pass

    @abstractmethod
    def find_by_id(self, id): pass

    @abstractmethod
    def delete(self, id): pass
```

**File: `src/interfaces/i_validator.py`**
```python
class IValidator(ABC):
    """
    FOCUSED: Only validation
    Client only needs validation? Use this interface.
    """

    @abstractmethod
    def validate(self, data) -> List[ValidationError]: pass
```

**File: `src/interfaces/i_cost_strategy.py`**
```python
class ICostDistributionStrategy(ABC):
    """
    FOCUSED: Only cost calculation
    Client only needs cost calculation? Use this interface.
    """

    @abstractmethod
    def calculate(self, total_amount, participants, distribution_params): pass

    @abstractmethod
    def get_strategy_name(self) -> str: pass
```

**File: `src/interfaces/i_notification.py`**
```python
class INotificationSender(ABC):
    """
    FOCUSED: Only notification sending
    Client only needs to send notifications? Use this interface.
    """

    @abstractmethod
    def send(self, recipient, message): pass
```

**Benefits:**
- Classes only implement what they need
- Clear, focused interfaces
- Easy to test (mock only what's needed)
- Loose coupling

**Usage in BillService:**
```python
class BillService:
    def __init__(
        self,
        repository: IRepository,        # Only needs database operations
        validator: IValidator,          # Only needs validation
        calculator: CostCalculator      # Only needs calculation
    ):
        """
        ISP: BillService only depends on the specific interfaces it needs
        Doesn't depend on fat interface with 20+ methods
        """
        self.repository = repository
        self.validator = validator
        self.calculator = calculator
```

---

## D - Dependency Inversion Principle

> **Depend upon abstractions, not concretions.**

### Demonstration

High-level modules (BillService) depend on abstractions (interfaces), not low-level modules (concrete implementations).

#### ❌ BAD (Violates DIP)

```python
from src.repositories.bill_repository import BillRepository  # Concrete!
from src.validators.bill_validator import BillValidator      # Concrete!

class BillService:
    def __init__(self):
        """
        Problem: Depends on CONCRETE implementations
        Tightly coupled to specific classes
        """
        self.repository = BillRepository()  # Hard-coded dependency!
        self.validator = BillValidator()    # Hard-coded dependency!

    def create_bill(self, data):
        # Now stuck with BillRepository forever
        # Can't swap for MockRepository in tests
        # Can't use PostgresRepository in production
        pass
```

**Problems:**
- Tightly coupled to concrete implementations
- Hard to test (can't inject mocks)
- Hard to swap implementations
- Violates DIP

#### ✓ GOOD (Follows DIP)

**File: `src/services/bill_service.py`**
```python
from src.interfaces.i_repository import IBillRepository  # Abstraction!
from src.interfaces.i_validator import IValidator        # Abstraction!

class BillService:
    def __init__(
        self,
        repository: IBillRepository,  # Depends on ABSTRACTION
        validator: IValidator,         # Depends on ABSTRACTION
        calculator: CostCalculator
    ):
        """
        DIP: Depends on abstractions (interfaces), not concretions
        Dependencies INJECTED via constructor
        """
        self.repository = repository  # Could be ANY implementation
        self.validator = validator    # Could be ANY implementation
        self.calculator = calculator

# Dependency Injection in app.py
def create_bill_service():
    """
    Wire up concrete implementations here
    BillService doesn't know or care which implementations are used
    """

    # Development: Use SQLite
    db = get_db()
    repo = BillRepository(db)           # Concrete implementation
    validator = BillValidator()          # Concrete implementation
    calculator = CostCalculator()

    # Inject dependencies
    return BillService(
        repository=repo,      # Injected
        validator=validator,  # Injected
        calculator=calculator # Injected
    )

# Testing: Swap for mocks
def create_test_bill_service():
    """
    Same BillService code works with mocks
    DIP enables easy testing
    """
    mock_repo = MockBillRepository()      # Test implementation
    mock_validator = MockValidator()      # Test implementation
    calculator = CostCalculator()

    return BillService(
        repository=mock_repo,
        validator=mock_validator,
        calculator=calculator
    )

# Production: Swap for production implementations
def create_production_bill_service():
    """
    Same BillService code works with production implementations
    DIP enables easy configuration changes
    """
    db = get_postgres_connection()
    repo = PostgresBillRepository(db)    # Different implementation
    validator = StrictBillValidator()     # Different implementation
    calculator = CostCalculator()

    return BillService(
        repository=repo,
        validator=validator,
        calculator=calculator
    )
```

**Benefits:**
- Loose coupling
- Easy to test (inject mocks)
- Easy to swap implementations
- BillService doesn't know concrete types

**File: `app.py` - Dependency Injection Container**
```python
# Initialize repositories and services (Dependency Injection - SOLID D)
db = get_db()

# Authentication
user_repository = UserRepository(db)
auth_service = AuthService(user_repository)

# Bills (SOLID demonstration)
bill_repository = BillRepository(db)
bill_validator = BillValidator()
cost_calculator = CostCalculator()
bill_service = BillService(bill_repository, bill_validator, cost_calculator)
```

---

## How to View SOLID in Git History

The project deliberately created "bad" code violating SOLID, then refactored to "good" code following SOLID. This creates a clear before/after comparison.

### View Commit History

```bash
cd housemate
git log --oneline --graph -10
```

### View BEFORE Code (Violates SOLID)

```bash
# Show the commit with "bad" code
git show 93e79de
```

### View AFTER Code (Follows SOLID)

```bash
# Show the commit with refactored "good" code
git show 9f85f97
```

### View the Transformation

```bash
# See exactly what changed
git diff 93e79de 9f85f97
```

### Key Commits

| Commit | Description | SOLID Principle |
|--------|-------------|----------------|
| `93e79de` | BEFORE: if/else chain (violates OCP) | Violates O, L, S, D |
| `9f85f97` | AFTER: Strategy Pattern (follows OCP) | Follows O, L, S |
| `32277f7` | Separate BillRepository and BillValidator | Follows S |
| `16f25cb` | Add BillService with Dependency Injection | Follows D |
| `46aff11` | Create SOLID interfaces | Follows I |

---

## Summary

### All 5 SOLID Principles Demonstrated

| Principle | Implementation | Files |
|-----------|---------------|-------|
| **S** - Single Responsibility | Separate classes for repository, validator, service, calculator | `bill_repository.py`, `bill_validator.py`, `bill_service.py` |
| **O** - Open/Closed | Strategy Pattern for cost distribution | `i_cost_strategy.py`, `equal_distribution.py`, `percentage_distribution_strategy.py`, `fixed_distribution_strategy.py` |
| **L** - Liskov Substitution | All strategies substitutable at runtime | All strategy implementations |
| **I** - Interface Segregation | Small, focused interfaces | `i_repository.py`, `i_validator.py`, `i_cost_strategy.py`, `i_notification.py` |
| **D** - Dependency Inversion | Constructor injection of interfaces | `bill_service.py`, `app.py` |

### Benefits of SOLID in This Project

1. **Maintainability**: Each class has one clear purpose
2. **Extensibility**: Adding new cost distribution strategy = one new file
3. **Testability**: Easy to inject mocks for testing
4. **Flexibility**: Can swap implementations without code changes
5. **Clarity**: Code structure clearly communicates intent

---

**Date**: 2025-12-18
**Author**: Marin
**Course**: Programsko inženjerstvo
**Assignment**: SOLID Principles Demonstration
