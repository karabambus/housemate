# HouseMate Development with Claude Code

## Project Context

**Course**: Programsko inženjerstvo (Software Engineering)
**Project**: HouseMate - Student Housing Management System
**Team**: Solo development

## Assignment Status

### ✅ Assignment 1: SOLID Principles (COMPLETED)

From `Class Documents/2025_8_SOLID-Principi.pdf`:

**Status**: ✅ DONE - All requirements met

- ✅ Implement ALL 5 SOLID principles in project code
- ✅ Each team member must demonstrate all principles in their code section
- ✅ Use feature branches for development
- ✅ Merge all changes to master branch
- ✅ Deploy application to accessible server (Docker + docker-compose.yml)
- ✅ Comprehensive documentation (`docs/SOLID_EXAMPLES.md`)
- **Points**: I3 - 1 bod ✅; I8 - 1 bod ✅

**SOLID Principles Implemented:**
- ✅ **S** - Single Responsibility: BillRepository, BillValidator, BillService
- ✅ **O** - Open/Closed: Strategy Pattern (3 distribution strategies)
- ✅ **L** - Liskov Substitution: All strategies substitutable at runtime
- ✅ **I** - Interface Segregation: 4 small, focused interfaces
- ✅ **D** - Dependency Inversion: Constructor injection throughout

---

### 🔄 Assignment 2: Design Patterns (IN PROGRESS)

From `Class Documents/PI-Vjezbe-Design-Patterns-2025-1.pdf`:

**Requirements**:
- Implement minimum **3 design patterns** from different categories:
  - **1x Creational** (Singleton, Factory Method, Builder, Prototype)
  - **1x Structural** (Adapter, Decorator, Facade, Proxy, Composite, Bridge)
  - **1x Behavioral** (Observer, Strategy, Template, Command, State, Iterator, Mediator, Chain)
- Each team member implements one pattern from each category
- **Points**: I3 - 1 bod; I8 - 1 bod

**Key Difference from SOLID Assignment**:
- ❌ **DON'T** explicitly show patterns everywhere in the code
- ❌ **DON'T** add comments like "// CREATIONAL: Singleton pattern"
- ✅ **DO** implement patterns naturally where they make sense
- ✅ **DO** demonstrate patterns by showing the code during presentation
- ✅ **DO** keep code clean and simple

**Approach**:
- **Marin codes, Claude guides**
- Ask Claude for questions, setup help, and direction
- Claude provides examples and explains concepts
- Marin implements the actual code

## Technology Decisions

### Why Flask?
**Decision**: Use Flask web framework
**Reasoning**:
- Simplest Python web framework (2-hour learning curve)
- Minimal boilerplate code
- Full control over architecture (perfect for demonstrating SOLID)
- Excellent documentation
- Ideal for 1-2 day timeline

**Alternatives considered**:
- **Django**: Too heavy, requires learning ORM, migrations, admin interface (2-3 days learning)
- **FastAPI**: Modern but async patterns add complexity, overkill for demo

**Verdict**: Flask wins on speed and simplicity

### Why SQLite?
**Decision**: Use SQLite database
**Reasoning**:
- Zero configuration (just a file: `housemate.db`)
- Comes with Python standard library
- Perfect for development and demo
- Can migrate to PostgreSQL later if needed
- Teammates' ER diagram maps directly to SQL tables

**Alternatives considered**:
- **PostgreSQL**: Requires Docker setup, connection management, adds unnecessary complexity
- **MySQL**: Similar complexity to PostgreSQL

**Verdict**: SQLite for speed, can upgrade later

### Why Bootstrap 5?
**Decision**: Use Bootstrap 5 + Jinja2 templates
**Reasoning**:
- No JavaScript framework needed
- Professional UI out of the box
- Faster than writing custom CSS
- Responsive by default
- 30-minute learning curve

**Alternatives considered**:
- **React/Vue**: Overkill, requires bundler, state management (adds 1-2 days)
- **Plain HTML/CSS**: Takes longer than using Bootstrap

**Verdict**: Bootstrap for professional look with minimal effort

### Why Docker?
**Decision**: Deploy with Docker
**Reasoning**:
- Assignment requires "accessible server"
- You already have Docker installed
- Simple Dockerfile + docker-compose.yml
- Portable across systems
- Easy to demonstrate

**Alternatives considered**:
- **Heroku/Railway**: External dependencies, may have deployment delays
- **Local dev server**: Less professional, harder to share

**Verdict**: Docker for portability and professionalism

## Module Selection Strategy

### Primary Module: Cost Distribution (Module 2)
**Why this module is perfect for SOLID**:

The Cost Distribution module naturally demonstrates ALL 5 SOLID principles:

1. **Single Responsibility (S)**:
   - `BillRepository` - only database operations
   - `BillValidator` - only validation logic
   - `BillService` - only business logic coordination
   - `CostCalculator` - only cost calculations
   - `BillController` - only HTTP request handling

2. **Open/Closed (O)**:
   - **Strategy Pattern** for cost distribution
   - `ICostDistributionStrategy` interface
   - Three implementations:
     - `EqualDistributionStrategy` - split equally
     - `PercentageDistributionStrategy` - split by percentages
     - `FixedAmountDistributionStrategy` - fixed amounts
   - Adding new strategy (e.g., weighted by income) requires ZERO changes to existing code

3. **Liskov Substitution (L)**:
   - Any `ICostDistributionStrategy` can substitute another
   - `BillService.set_strategy()` works with all implementations
   - Runtime strategy switching works transparently

4. **Interface Segregation (I)**:
   - Small, focused interfaces:
     - `INotificationSender` - only sending notifications
     - `IFileStorage` - only file storage
     - `IValidator` - only validation
     - `ICostCalculator` - only calculation
   - No "fat" interfaces with 20+ methods

5. **Dependency Inversion (D)**:
   - `BillService` depends on abstractions (interfaces)
   - Constructor injection of dependencies
   - Easy to swap implementations (e.g., MockRepository for testing)

### Secondary Module: Shopping List (Module 3)
**Purpose**: Show SOLID in simpler context
- Demonstrates SRP with separate Repository/Service/Controller
- Demonstrates DIP with interface-based design
- Quick to implement (2-3 hours)

### Tertiary Module: Task List (Module 4)
**Purpose**: Additional SOLID examples
- Shows different applications of same principles
- Demonstrates OCP with task priority strategies
- Time permitting

## Project Structure Philosophy

```
housemate/
├── src/
│   ├── interfaces/     # ISP (I) - Small, focused interfaces
│   ├── repositories/   # SRP (S) - Database access only
│   ├── validators/     # SRP (S) - Validation only
│   ├── services/       # DIP (D) - Business logic with injected dependencies
│   ├── strategies/     # OCP (O), LSP (L) - Pluggable implementations
│   ├── controllers/    # SRP (S) - HTTP handling only
│   └── models/         # Domain entities
```

**Design Philosophy**: Clear separation of concerns, each directory represents a SOLID principle in action

## Development Process

### Phase 1: Document Cleanup ✓
**Completed**: Fixed typos in `MyPart/Marin/Zadatak2/zad2.md`
- Fixed: "Nefukcionalni" → "Nefunkcionalni"
- Fixed: "suculje" → "sučelje"
- Standardized module names (Croatian + English)
- Added implementation priorities

### Phase 2: Project Setup (In Progress)
**Next Steps**:
1. Create directory structure
2. Initialize Git with feature branches
3. Create `requirements.txt`
4. Create `.gitignore`

### Phase 3: Database Setup
**Approach**:
- Use teammates' ER diagram from `Otherspart/ERDijagram(Modul_1,2,3).drawio`
- Convert to SQL schema
- Create seed data for testing

### Phase 4: Implementation Strategy

**Day 1 Morning** (4 hours):
- Hour 1: Documentation (✓ Done)
- Hour 2: Project setup
- Hour 3: Database setup
- Hour 4: Basic Flask app

**Day 1 Afternoon** (4 hours):
- Hours 5-6: Basic authentication
- Hours 7-8: SOLID interfaces + cost distribution strategies

**Day 2 Morning** (4 hours):
- Hours 9-10: Complete Cost Distribution module
- Hours 11-12: Cost Distribution UI

**Day 2 Afternoon** (4 hours):
- Hours 13-14: Shopping List + Task List
- Hours 15-16: Documentation + Deployment

## SOLID Implementation Strategy

### Single Responsibility (S)

**Pattern**: One class = one responsibility = one reason to change

**Examples**:
```python
# ✗ BAD - Multiple responsibilities
class BillManager:
    def save_to_database(self)    # Database
    def validate_bill(self)        # Validation
    def send_notification(self)    # Notification
    def calculate_distribution(self) # Calculation

# ✓ GOOD - Single responsibilities
class BillRepository:        # Only database
    def save(self, bill)

class BillValidator:         # Only validation
    def validate(self, bill)

class NotificationService:   # Only notifications
    def send(self, user, message)
```

**Feature Branch**: `feature/srp-repositories`

### Open/Closed (O)

**Pattern**: Open for extension, closed for modification

**Implementation**: Strategy pattern for cost distribution

```python
# Interface (closed for modification)
class ICostDistributionStrategy(ABC):
    @abstractmethod
    def calculate(self, total_amount, participants):
        pass

# Extensions (open for extension)
class EqualDistributionStrategy(ICostDistributionStrategy):
    def calculate(self, total_amount, participants):
        return total_amount / len(participants)

class PercentageDistributionStrategy(ICostDistributionStrategy):
    def calculate(self, total_amount, participants):
        # Custom logic

# Adding new strategy requires ZERO changes to existing code
class WeightedByIncomeStrategy(ICostDistributionStrategy):  # NEW!
    def calculate(self, total_amount, participants):
        # New logic
```

**Feature Branch**: `feature/ocp-strategies`

### Liskov Substitution (L)

**Pattern**: Subclasses must be substitutable for base classes

**Implementation**: All strategy implementations are fully substitutable

```python
# Service works with ANY strategy
class BillService:
    def __init__(self, strategy: ICostDistributionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ICostDistributionStrategy):
        self.strategy = strategy  # Can swap at runtime

    def distribute_bill(self, bill, participants):
        return self.strategy.calculate(bill.amount, participants)

# All these work identically
service = BillService(EqualDistributionStrategy())
service = BillService(PercentageDistributionStrategy())
service = BillService(FixedAmountDistributionStrategy())

# Runtime substitution works
service.set_strategy(EqualDistributionStrategy())
service.set_strategy(PercentageDistributionStrategy())
```

**Feature Branch**: `feature/lsp-substitution`

### Interface Segregation (I)

**Pattern**: Many small interfaces > one large interface

**Implementation**: Separate interfaces for different concerns

```python
# ✗ BAD - Fat interface
class IBillManager(ABC):
    @abstractmethod
    def save(self, bill)
    @abstractmethod
    def validate(self, bill)
    @abstractmethod
    def send_notification(self, user)
    @abstractmethod
    def calculate_distribution(self, amount)
    @abstractmethod
    def store_receipt(self, file)
    # ... 15 more methods

# ✓ GOOD - Segregated interfaces
class IRepository(ABC):
    @abstractmethod
    def save(self, entity)
    @abstractmethod
    def find_by_id(self, id)

class IValidator(ABC):
    @abstractmethod
    def validate(self, data)

class INotificationSender(ABC):
    @abstractmethod
    def send(self, recipient, message)

class ICostCalculator(ABC):
    @abstractmethod
    def calculate(self, amount, participants)

class IFileStorage(ABC):
    @abstractmethod
    def save_file(self, file, path)
```

**Feature Branch**: `feature/isp-interfaces`

### Dependency Inversion (D)

**Pattern**: Depend on abstractions, not concretions

**Implementation**: Constructor injection with interfaces

```python
# ✗ BAD - Depends on concrete implementations
class BillService:
    def __init__(self):
        self.repository = BillRepository()  # Concrete!
        self.validator = BillValidator()    # Concrete!

# ✓ GOOD - Depends on abstractions
class BillService:
    def __init__(
        self,
        repository: IRepository,         # Abstraction
        validator: IValidator,           # Abstraction
        calculator: ICostCalculator,     # Abstraction
        notifier: INotificationSender    # Abstraction
    ):
        self.repository = repository
        self.validator = validator
        self.calculator = calculator
        self.notifier = notifier

# Dependency Injection in app.py
def create_bill_service():
    # Wire up concrete implementations
    repo = BillRepository(db_connection)
    validator = BillValidator()
    calculator = CostCalculator()
    notifier = EmailSender()

    # Inject dependencies
    return BillService(
        repository=repo,
        validator=validator,
        calculator=calculator,
        notifier=notifier
    )
```

**Feature Branch**: `feature/dip-injection`

## Git Workflow

### Feature Branch Strategy

```bash
# Create feature branches for each SOLID principle
git checkout -b feature/srp-repositories
git checkout -b feature/ocp-strategies
git checkout -b feature/lsp-substitution
git checkout -b feature/isp-interfaces
git checkout -b feature/dip-injection

# Merge to main when complete
git checkout main
git merge feature/srp-repositories
git merge feature/ocp-strategies
# ... etc
```

### Commit Message Format

```
feat: implement <SOLID principle> in <module>

<Description of implementation and why it demonstrates the principle>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Risk Mitigation

### If Running Out of Time

**Priority 1** (MUST DO): Cost Distribution module only
- Demonstrates ALL 5 SOLID principles
- Better one perfect module than three incomplete

**Priority 2** (SHOULD DO): Add Shopping List
- Simple CRUD, 2-3 hours

**Priority 3** (NICE TO HAVE): Add Task List
- Only if time permits

### If Stuck on Flask

**Solution**: Use simplest patterns
- No blueprints initially
- All routes in `app.py`
- Focus on SOLID in business logic

### If Stuck on Deployment

**Quick Win**: Run with `python app.py`
- Docker is nice-to-have
- Local dev server acceptable for demo

## Success Metrics

### Functional Requirements
- [ ] User can log in
- [ ] User can create/view bills
- [ ] Bills can be distributed using 3 different strategies
- [ ] User can switch strategies at runtime
- [ ] Application accessible via Docker

### SOLID Requirements
- [ ] S: 5+ classes with single responsibility
- [ ] O: 3+ strategy implementations, extensible
- [ ] L: Strategies substitutable at runtime
- [ ] I: 4+ small interfaces
- [ ] D: Services use constructor injection

### Documentation Requirements
- [ ] `/docs/SOLID_EXAMPLES.md` with code examples
- [ ] `/docs/CLAUDE.md` (this file) with process
- [ ] Inline code comments explaining SOLID
- [ ] `README.md` with setup instructions

### Git Requirements
- [ ] Feature branches for each principle
- [ ] All merged to main
- [ ] Clear commit messages

## Design Patterns Implementation Guide

### Current Status: What Already Exists

**Already Implemented (from SOLID assignment)**:
- ✅ **Strategy Pattern** (Behavioral) - Cost distribution strategies
  - `EqualDistributionStrategy`
  - `PercentageDistributionStrategy`
  - `FixedDistributionStrategy`
  - **Counts toward Behavioral requirement!**

### Pattern Recommendations for HouseMate Modules

Based on existing code structure, here are natural fits for design patterns:

#### CREATIONAL Patterns (Pick 1)

**Option 1: Singleton Pattern** ⭐ RECOMMENDED
- **Where**: Database connection (`src/infrastructure/database.py`)
- **Why**: Already partially implemented - `get_db()` returns same connection
- **Current code**: Function-based singleton
- **What to do**: Convert to proper Singleton class with private constructor
- **Difficulty**: Easy (1-2 hours)
- **Files to modify**: `src/infrastructure/database.py`

**Option 2: Factory Method Pattern**
- **Where**: Notification system (email, SMS, push notifications)
- **Why**: Create different notification types based on user preference
- **What to add**: `NotificationFactory` that creates `EmailNotifier`, `SmsNotifier`, etc.
- **Difficulty**: Medium (2-3 hours)
- **Files to create**: `src/factories/notification_factory.py`, `src/notifiers/`

**Option 3: Builder Pattern**
- **Where**: Bill creation with many optional fields
- **Why**: Bill has many optional parameters (category, is_recurring, frequency, due_date)
- **What to do**: Create `BillBuilder` class for fluent API
- **Difficulty**: Medium (2-3 hours)
- **Files to modify**: `src/models/bill.py`

#### STRUCTURAL Patterns (Pick 1)

**Option 1: Facade Pattern** ⭐ RECOMMENDED
- **Where**: HouseMate management (wraps User, Bill, Shopping, Tasks)
- **Why**: Simplify complex subsystem interactions
- **What to add**: `HouseMate Facade` class with simple methods like `create_household()`, `split_bill()`, `add_shopping_item()`
- **Difficulty**: Easy (2-3 hours)
- **Files to create**: `src/facades/housemate_facade.py`
- **Example**: Instead of calling 5 different services, call one facade method

**Option 2: Decorator Pattern**
- **Where**: Bill validation (add logging, caching, or audit trail)
- **Why**: Add functionality to existing validators without changing them
- **What to add**: `LoggingValidator`, `CachingValidator` decorators
- **Difficulty**: Medium (3-4 hours)
- **Files to create**: `src/decorators/validator_decorators.py`

**Option 3: Adapter Pattern**
- **Where**: Export bills to different formats (PDF, CSV, JSON)
- **Why**: Adapt different export libraries to common interface
- **What to add**: `IExporter` interface, `PdfAdapter`, `CsvAdapter`
- **Difficulty**: Medium (3-4 hours)
- **Files to create**: `src/adapters/export_adapters.py`

#### BEHAVIORAL Patterns (Pick 1)

**Option 1: Strategy Pattern** ✅ ALREADY DONE
- **Status**: Already implemented in cost distribution
- **No additional work needed** - this counts!

**Option 2: Observer Pattern** ⭐ RECOMMENDED (if you want a 2nd behavioral)
- **Where**: Bill payment notifications
- **Why**: Notify multiple observers (users, email, dashboard) when bill is paid
- **What to add**: `BillObserver` interface, observers like `EmailObserver`, `DashboardObserver`
- **Difficulty**: Medium (3-4 hours)
- **Files to create**: `src/observers/bill_observers.py`

**Option 3: Template Method Pattern**
- **Where**: Data export process (open file → extract data → format → close file)
- **Why**: Define skeleton of export algorithm, let subclasses override steps
- **What to add**: `AbstractExporter` with template method, subclasses for PDF/CSV
- **Difficulty**: Medium (2-3 hours)
- **Files to create**: `src/exporters/abstract_exporter.py`

**Option 4: Command Pattern**
- **Where**: Undo/redo functionality for bills or shopping list
- **Why**: Encapsulate actions as objects
- **What to add**: `Command` interface, `CreateBillCommand`, `DeleteBillCommand`, `CommandHistory`
- **Difficulty**: Hard (4-5 hours)
- **Files to create**: `src/commands/`

### Recommended Combination (Minimum Effort)

**Easiest path to meet requirements:**

1. **CREATIONAL**: ✅ Singleton Pattern (Database connection)
   - Modify existing `database.py` to proper Singleton class
   - Time: 1-2 hours

2. **STRUCTURAL**: ✅ Facade Pattern (HouseMate operations)
   - Create simple facade wrapping existing services
   - Time: 2-3 hours

3. **BEHAVIORAL**: ✅ Strategy Pattern (ALREADY DONE!)
   - Just point to existing cost distribution strategies
   - Time: 0 hours

**Total time**: 3-5 hours

### How to Demonstrate Patterns

During presentation, you'll show:

1. **Singleton**: Point to `database.py` and explain how only one instance exists
2. **Facade**: Show facade class and how it simplifies complex operations
3. **Strategy**: Show cost distribution strategies (already done!)

**No need** for:
- Explicit comments in every file
- Separate documentation like SOLID_EXAMPLES.md
- Over-explanation in code

**Just** show clean code that happens to use design patterns.

### Questions to Ask Claude

When implementing, ask Claude:
- "How do I implement Singleton pattern in Python?"
- "What's the best way to structure a Facade for my services?"
- "Can you explain how Observer pattern would work for bill notifications?"
- "Show me an example of Builder pattern for Bill class"
- "Help me debug this Factory Method implementation"

Claude will provide examples and explain, **you write the actual code**.

---

## Lessons Learned

### Assignment 1: SOLID Principles

**What Worked Well**:
- Starting with document cleanup ensured clarity
- Flask choice was correct for speed
- SQLite eliminated configuration overhead
- Focus on Cost Distribution module for SOLID demonstration
- Strategy pattern implementation was clean and extensible

**Challenges Faced**:
- Over-documentation - added too many explicit SOLID comments
- Could have been more subtle with pattern demonstration

**Key Takeaway**:
- Less is more - clean code speaks for itself

### Assignment 2: Design Patterns

**Approach**:
- Marin codes, Claude guides
- Focus on patterns that fit naturally into existing architecture
- No over-documentation - let code demonstrate patterns

**What to Avoid**:
- Don't add patterns just to add patterns
- Don't over-comment with pattern names
- Don't create unnecessary complexity

## Timeline Tracking

| Phase | Estimated | Actual | Status |
|-------|-----------|--------|--------|
| Document cleanup | 2-3h | [TBD] | In Progress ✓ |
| Project setup | 2h | [TBD] | Pending |
| Database setup | 1h | [TBD] | Pending |
| Basic Flask app | 1h | [TBD] | Pending |
| Authentication | 2h | [TBD] | Pending |
| Cost Distribution | 6-8h | [TBD] | Pending |
| Shopping List | 2-3h | [TBD] | Pending |
| Task List | 2-3h | [TBD] | Pending |
| Documentation | 2-3h | [TBD] | Pending |
| Deployment | 1-2h | [TBD] | Pending |
| **Total** | **19-26h** | **[TBD]** | **In Progress** |

---

**Last Updated**: 2026-01-01
**Development Tool**: Claude Code (Claude Sonnet 4.5)
**Developer**: Marin
**Course**: Programsko inženjerstvo

---

## Summary

**Assignment 1 (SOLID)**: ✅ Complete - All 5 principles implemented and documented
**Assignment 2 (Design Patterns)**: 🔄 In Progress - Marin codes, Claude guides
