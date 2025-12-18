"""
HouseMate Flask Application

Main application entry point.
Demonstrates SOLID principles through clean architecture.
"""

from flask import Flask, render_template, session, redirect, url_for, flash, request
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.infrastructure.database import get_db
from pathlib import Path
import config

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Ensure upload folder exists
Path(config.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# Initialize repositories and services (Dependency Injection - SOLID D)
db = get_db()

# Authentication
user_repository = UserRepository(db)
auth_service = AuthService(user_repository)

# Bills (SOLID demonstration)
from src.repositories.bill_repository import BillRepository
from src.validators.bill_validator import BillValidator
from src.services.cost_calculator import CostCalculator
from src.services.bill_service import BillService
from src.strategies import EqualDistributionStrategy, PercentageDistributionStrategy, FixedDistributionStrategy

bill_repository = BillRepository(db)
bill_validator = BillValidator()
cost_calculator = CostCalculator()
bill_service = BillService(bill_repository, bill_validator, cost_calculator)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = auth_service.login(email, password)

        if user:
            session['user_id'] = user.user_id
            session['user_name'] = user.get_full_name()
            session['user_email'] = user.email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/')
def index():
    """
    Landing page / dashboard.
    Shows different content for logged in vs logged out users.
    """
    if 'user_id' in session:
        # User is logged in - show dashboard
        return render_template('dashboard.html',
                             user_name=session.get('user_name'),
                             household_name=session.get('household_name'))
    else:
        # User not logged in - show landing page
        return render_template('index.html')


@app.route('/about')
def about():
    """About page explaining SOLID principles in this project."""
    return render_template('about.html')


# ============================================================================
# Bills Routes (Cost Distribution Module - SOLID Demonstration)
# ============================================================================

@app.route('/bills')
def bills_list():
    """
    List all bills for user's household.
    Demonstrates SOLID principles working together.
    """
    if 'user_id' not in session:
        flash('Please log in to view bills.', 'warning')
        return redirect(url_for('login'))

    # Get user's household (from seed data, user 1 is in household 1)
    household_id = 1  # TODO: Get from user's household membership
    bills = bill_service.get_household_bills(household_id)

    return render_template('bills/list.html', bills=bills)


@app.route('/bills/create', methods=['GET', 'POST'])
def bills_create():
    """
    Create a new bill and distribute costs.
    Demonstrates all SOLID principles.
    """
    if 'user_id' not in session:
        flash('Please log in to create bills.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Get form data
            title = request.form['title']
            amount = float(request.form['amount'])
            category = request.form.get('category', 'other')
            strategy_type = request.form['strategy']

            # Create bill (SOLID S, D: BillService coordinates)
            bill_id = bill_service.create_bill(
                household_id=1,  # TODO: Get from user's household
                payer_id=session['user_id'],
                title=title,
                amount=amount,
                category=category
            )

            # Distribute costs using selected strategy (SOLID O, L)
            participants = [1, 2, 3]  # TODO: Get from household members

            if strategy_type == 'equal':
                strategy = EqualDistributionStrategy()
                distribution = bill_service.distribute_bill(bill_id, strategy, participants)
            elif strategy_type == 'percentage':
                # Get percentages from form
                params = {
                    1: float(request.form.get('percent_1', 33.33)),
                    2: float(request.form.get('percent_2', 33.33)),
                    3: float(request.form.get('percent_3', 33.34))
                }
                strategy = PercentageDistributionStrategy()
                distribution = bill_service.distribute_bill(bill_id, strategy, participants, params)
            else:  # fixed
                # Get fixed amounts from form
                params = {
                    1: float(request.form.get('fixed_1', amount/3)),
                    2: float(request.form.get('fixed_2', amount/3)),
                    3: float(request.form.get('fixed_3', amount/3))
                }
                strategy = FixedDistributionStrategy()
                distribution = bill_service.distribute_bill(bill_id, strategy, participants, params)

            flash(f'Bill "{title}" created and distributed successfully!', 'success')
            return redirect(url_for('bills_detail', bill_id=bill_id))

        except ValueError as e:
            flash(f'Error creating bill: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Unexpected error: {str(e)}', 'danger')

    return render_template('bills/create.html')


@app.route('/bills/<int:bill_id>')
def bills_detail(bill_id):
    """
    Show bill details and cost distribution.
    """
    if 'user_id' not in session:
        flash('Please log in to view bill details.', 'warning')
        return redirect(url_for('login'))

    bill = bill_service.get_bill(bill_id)

    if not bill:
        flash('Bill not found.', 'danger')
        return redirect(url_for('bills_list'))

    return render_template('bills/detail.html', bill=bill)


@app.route('/bills/<int:bill_id>/delete', methods=['POST'])
def bills_delete(bill_id):
    """
    Delete a bill.
    """
    if 'user_id' not in session:
        flash('Please log in to delete bills.', 'warning')
        return redirect(url_for('login'))

    bill = bill_service.get_bill(bill_id)

    if not bill:
        flash('Bill not found.', 'danger')
        return redirect(url_for('bills_list'))

    bill_service.delete_bill(bill_id)
    flash(f'Bill "{bill.title}" deleted successfully.', 'success')
    return redirect(url_for('bills_list'))


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """500 error handler."""
    return render_template('500.html'), 500


# Context processor to make config available in all templates
@app.context_processor
def inject_config():
    """Inject configuration variables into all templates."""
    return {
        'app_name': config.APP_NAME,
        'version': config.VERSION,
    }


if __name__ == '__main__':
    # Initialize database if it doesn't exist
    from src.infrastructure.database import init_db
    db_path = Path(config.DATABASE_PATH)
    if not db_path.exists():
        print("Database not found. Initializing...")
        init_db()

    # Run the application
    print(f"\n{'='*60}")
    print(f"  {config.APP_NAME} v{config.VERSION}")
    print(f"{'='*60}")
    print(f"\n  Running on: http://127.0.0.1:5000")
    print(f"  Database: {config.DATABASE_PATH}")
    print(f"\n  Test login:")
    print(f"    Email: marin@test.com")
    print(f"    Password: test123")
    print(f"\n{'='*60}\n")

    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
