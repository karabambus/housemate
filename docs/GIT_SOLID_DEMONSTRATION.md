# Git Commands to Demonstrate SOLID Principles

This document shows how to view the SOLID refactoring demonstration in git history.

## Overview

We intentionally created "bad" code that violates SOLID principles, then refactored it to "good" code that follows SOLID. This creates a clear before/after comparison visible in git history.

## Git History

```bash
# View recent commits
git log --oneline -5
```

**Output:**
```
9f85f97 refactor: apply Strategy Pattern to CostCalculator (SOLID demonstration)
93e79de feat: add cost distribution strategies and calculator (BEFORE SOLID refactoring)
46aff11 feat: create SOLID interfaces demonstrating I, O, L, D principles
d134007 feat: implement user authentication with bcrypt password hashing
58f6043 docs: add Python code explanation guide for learning
```

## View BEFORE Version (Violates SOLID)

```bash
# Show the "bad" code commit
git show 93e79de
```

**Key Problem:** Uses if/else chain - violates Open/Closed Principle

```python
def calculate(self, strategy_type: str, ...):
    if strategy_type == "equal":
        # Equal distribution logic here (15 lines)
    elif strategy_type == "percentage":
        # Percentage distribution logic here (12 lines)
    elif strategy_type == "fixed":
        # Fixed distribution logic here (10 lines)
    else:
        raise ValueError(f"Unknown strategy: {strategy_type}")
```

## View AFTER Version (Follows SOLID)

```bash
# Show the refactored "good" code commit
git show 9f85f97
```

**Solution:** Uses Strategy Pattern - follows SOLID principles

```python
def calculate_with_strategy(self, strategy: ICostDistributionStrategy, ...):
    # Delegate to strategy - doesn't know implementation details
    return strategy.calculate(total_amount, participants, distribution_params)
```

## View the Transformation (Diff)

```bash
# Show what changed between BEFORE and AFTER
git diff 93e79de 9f85f97
```

**Key Changes:**
- ❌ Removed: 64 lines of if/else logic
- ✓ Added: 56 lines of clean delegation
- Changed: `calculate(strategy_type: str)` → `calculate_with_strategy(strategy: ICostDistributionStrategy)`
- Result: Adding new strategy requires ZERO changes to this file

## Side-by-Side Comparison

```bash
# View BEFORE and AFTER side by side
git diff 93e79de 9f85f97 src/services/cost_calculator.py
```

## Full Commit Messages

```bash
# Show full commit message for BEFORE
git show 93e79de --stat

# Show full commit message for AFTER
git show 9f85f97 --stat
```

## SOLID Principles Demonstrated

### O - Open/Closed Principle

**BEFORE (❌ Violates):**
- Adding new strategy (e.g., "weighted") requires MODIFYING `calculate()` method
- Must add new `elif` branch to the if/else chain

**AFTER (✓ Follows):**
- Adding new strategy requires ZERO changes to `CostCalculator`
- Just create new class implementing `ICostDistributionStrategy`

**Example - Adding new strategy:**

```bash
# BEFORE: Must modify CostCalculator.calculate()
# Add this to the if/else chain:
elif strategy_type == "weighted":
    # 15 more lines of logic here...

# AFTER: Just create new file, no changes to CostCalculator
# Create: src/strategies/weighted_distribution.py
class WeightedDistributionStrategy(ICostDistributionStrategy):
    def calculate(self, ...):
        # Implementation here
```

### L - Liskov Substitution Principle

**BEFORE (❌ Violates):**
- Can't swap strategies at runtime
- Tightly coupled to string types

**AFTER (✓ Follows):**
- All strategies are interchangeable
- Can swap strategies at runtime without breaking code

```python
# All these work identically:
calculator.calculate_with_strategy(EqualDistributionStrategy(), ...)
calculator.calculate_with_strategy(PercentageDistributionStrategy(), ...)
calculator.calculate_with_strategy(FixedDistributionStrategy(), ...)
```

### S - Single Responsibility Principle

**BEFORE (❌ Violates):**
- `CostCalculator` has multiple responsibilities:
  1. Knows equal distribution logic
  2. Knows percentage distribution logic
  3. Knows fixed distribution logic
  4. Decides which to use

**AFTER (✓ Follows):**
- `CostCalculator` has ONE responsibility: coordinate strategies
- Each strategy has ONE responsibility: implement its distribution logic

### D - Dependency Inversion Principle

**BEFORE (❌ Violates):**
- Depends on concrete string values ("equal", "percentage", "fixed")
- Tightly coupled to implementation details

**AFTER (✓ Follows):**
- Depends on abstraction (`ICostDistributionStrategy` interface)
- Loose coupling - doesn't know concrete implementations

## For Demonstration/Presentation

```bash
# 1. Show commit history
git log --oneline --graph -5

# 2. Show the BEFORE code
git show 93e79de:src/services/cost_calculator.py | head -50

# 3. Show the AFTER code
git show 9f85f97:src/services/cost_calculator.py | head -50

# 4. Show the diff highlighting changes
git diff 93e79de 9f85f97 src/services/cost_calculator.py --color

# 5. Show statistics
git diff 93e79de 9f85f97 --stat
```

## Files Changed

```
src/services/cost_calculator.py | 120 ++++++++++++++++++---------------------
1 file changed, 56 insertions(+), 64 deletions(-)
```

**Translation:**
- 64 lines deleted (bad if/else code)
- 56 lines added (good Strategy Pattern code)
- Net reduction: 8 lines (simpler code!)

## Key Takeaways

1. **Intentional "Bad" Code**: We created code that violates SOLID on purpose
2. **Clear Refactoring**: Git history shows transformation from bad → good
3. **Visible in Diff**: Changes clearly show SOLID principles being applied
4. **Well Documented**: Commit messages explain exactly what changed and why

This demonstrates understanding of:
- What NOT to do (anti-patterns)
- How to recognize SOLID violations
- How to refactor to follow SOLID principles
- Git workflow for tracking architectural improvements

---

**Note**: This same approach can be used for Shopping List and Task List modules to demonstrate more SOLID principles.
