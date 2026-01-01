# HouseMate - Student Housing Management System

A Flask-based web application for managing shared housing expenses, bills, and tasks. Built as a demonstration of SOLID software engineering principles.

## Course Information

**Course**: Programsko inženjerstvo (Software Engineering)
**Institution**: [Your University]
**Assignment**: SOLID Principles Demonstration
**Date**: December 2025

## Features

### Implemented Modules

#### 1. User Authentication
- Secure login/registration with bcrypt password hashing
- Session management
- User profile management

#### 2. Cost Distribution (Primary SOLID Demonstration)
- Create and manage household bills
- Multiple distribution strategies:
  - **Equal Distribution**: Split costs equally among participants
  - **Percentage Distribution**: Split by custom percentages
  - **Fixed Amount Distribution**: Assign fixed amounts per participant
- Runtime strategy switching
- Bill categorization (rent, utilities, food, other)
- Recurring bill support
- Payment status tracking

### SOLID Principles Demonstrated

All 5 SOLID principles are implemented in the Cost Distribution module:

- **S** - Single Responsibility Principle: Separate classes for repository, validator, service
- **O** - Open/Closed Principle: Strategy pattern for cost distribution
- **L** - Liskov Substitution Principle: Interchangeable distribution strategies
- **I** - Interface Segregation Principle: Small, focused interfaces
- **D** - Dependency Inversion Principle: Dependency injection throughout

See [docs/SOLID_EXAMPLES.md](docs/SOLID_EXAMPLES.md) for detailed examples and code explanations.

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite 3
- **Authentication**: bcrypt
- **Frontend**: Bootstrap 5 + Jinja2 templates
- **Deployment**: Docker + docker-compose

## Project Structure

```
housemate/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── database/
│   ├── schema.sql             # Database schema
│   ├── seed_data.sql          # Sample data
│   └── housemate.db           # SQLite database
├── src/
│   ├── interfaces/            # SOLID (I) - Interface Segregation
│   │   ├── i_repository.py
│   │   ├── i_validator.py
│   │   ├── i_cost_strategy.py
│   │   └── i_notification.py
│   ├── models/                # Domain entities
│   │   ├── user.py
│   │   └── bill.py
│   ├── repositories/          # SOLID (S) - Single Responsibility
│   │   ├── user_repository.py
│   │   └── bill_repository.py
│   ├── validators/            # SOLID (S) - Single Responsibility
│   │   └── bill_validator.py
│   ├── services/              # SOLID (D) - Dependency Inversion
│   │   ├── auth_service.py
│   │   ├── bill_service.py
│   │   └── cost_calculator.py
│   ├── strategies/            # SOLID (O,L) - Open/Closed, Liskov
│   │   ├── equal_distribution.py
│   │   ├── percentage_distribution_strategy.py
│   │   └── fixed_distribution_strategy.py
│   └── infrastructure/
│       └── database.py
├── templates/                 # Jinja2 HTML templates
├── static/                    # CSS, JS, images
├── docs/
│   ├── SOLID_EXAMPLES.md     # SOLID principles documentation
│   └── GIT_SOLID_DEMONSTRATION.md
└── tests/                     # Unit tests

```

## Setup Instructions

### Option 1: Docker (Recommended)

**Prerequisites**: Docker and docker-compose installed

```bash
# 1. Navigate to project directory
cd housemate

# 2. Build and run with docker-compose
docker-compose up --build

# 3. Access the application
# Open browser to: http://localhost:5000
```

### Option 2: Local Development

**Prerequisites**: Python 3.11+

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python3 app.py

# 5. Access the application
# Open browser to: http://localhost:5000
```

## Usage

### Default Login Credentials

The application comes with seed data for testing:

| Email | Password | Household |
|-------|----------|-----------|
| john@example.com | password123 | Tech House |
| jane@example.com | password123 | Tech House |
| bob@example.com | password123 | Green Villa |

### Creating a Bill

1. Log in with credentials above
2. Click "Dashboard" or "Manage Bills"
3. Click "Create New Bill"
4. Fill in bill details:
   - Title (e.g., "Electricity Bill")
   - Amount (e.g., 300.00)
   - Category (rent, utilities, food, other)
   - Recurring (optional)
5. Click "Create Bill"

### Distributing Bill Costs

1. View a bill from the bills list
2. Select distribution strategy:
   - **Equal**: Splits amount equally (e.g., 300/3 = 100 each)
   - **Percentage**: Specify percentages (e.g., 40%, 30%, 30%)
   - **Fixed Amount**: Specify exact amounts per person
3. Select participants
4. View calculated distribution

## Testing SOLID Principles

### View Git History

The project intentionally created "bad" code violating SOLID, then refactored to "good" code:

```bash
# View commit history showing SOLID refactoring
git log --oneline --graph -10

# View BEFORE code (violates SOLID)
git show 93e79de

# View AFTER code (follows SOLID)
git show 9f85f97

# View the transformation
git diff 93e79de 9f85f97
```

### Run Tests

```bash
# Run SOLID demonstration tests
python3 test_auth.py
```

## Documentation

- [SOLID Examples](docs/SOLID_EXAMPLES.md) - Comprehensive SOLID principles documentation
- [Git SOLID Demonstration](docs/GIT_SOLID_DEMONSTRATION.md) - How to view SOLID in git history
- [Python Code Explained](PYTHON_CODE_EXPLAINED.md) - Learning guide for Python code

## Development

### Database Schema

The database schema is defined in `database/schema.sql` based on the ER diagram.

To reset the database:

```bash
# Backup current database
cp database/housemate.db database/housemate.db.backup

# Reinitialize
rm database/housemate.db
sqlite3 database/housemate.db < database/schema.sql
sqlite3 database/housemate.db < database/seed_data.sql
```

### Adding a New Cost Distribution Strategy

Thanks to the Open/Closed Principle, adding a new strategy requires only creating a new file:

```python
# Create: src/strategies/weighted_distribution_strategy.py
from src.interfaces.i_cost_strategy import ICostDistributionStrategy

class WeightedDistributionStrategy(ICostDistributionStrategy):
    def calculate(self, total_amount, participants, distribution_params=None):
        # Implementation here
        pass

    def get_strategy_name(self):
        return "weighted"

# Use immediately - no changes to existing code needed!
strategy = WeightedDistributionStrategy()
calculator.calculate_with_strategy(strategy, 300.00, [1, 2, 3])
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t housemate:latest .

# Run container
docker run -d -p 5000:5000 --name housemate housemate:latest

# View logs
docker logs -f housemate

# Stop container
docker stop housemate
```

### Production Considerations

For production deployment:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Use environment variables** for sensitive data:
   ```bash
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='sqlite:///database/housemate.db'
   ```

3. **Use PostgreSQL** instead of SQLite for better concurrency

4. **Add SSL/TLS** with reverse proxy (nginx, Caddy)

5. **Enable logging** and monitoring

## Assignment Requirements Checklist

- [x] Implement all 5 SOLID principles
- [x] Use feature branches for development
- [x] Merge all changes to main branch
- [x] Deploy application (Docker)
- [x] Create comprehensive documentation

### SOLID Principles Coverage

- [x] **S** - Single Responsibility: Separate Repository, Validator, Service classes
- [x] **O** - Open/Closed: Strategy pattern with 3+ implementations
- [x] **L** - Liskov Substitution: All strategies fully substitutable
- [x] **I** - Interface Segregation: 4+ small, focused interfaces
- [x] **D** - Dependency Inversion: Constructor injection throughout

## License

This project was created for educational purposes as part of a university assignment.

## Author

**Marin**
Programsko inženjerstvo
December 2025

---

**Note**: This application demonstrates SOLID principles for educational purposes. For production use, additional security hardening, comprehensive testing, and scalability improvements would be recommended.
