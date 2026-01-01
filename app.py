from flask import Flask, render_template, session, redirect, url_for, flash, request
from src.facades.housemate_facade import HouseMateFacade
from pathlib import Path
import config

app = Flask(__name__)
app.config.from_object(config)

Path(config.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

housemate = HouseMateFacade()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = housemate.login_user(email, password)

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
    if 'user_id' in session:
        return render_template('dashboard.html',
                             user_name=session.get('user_name'),
                             household_name=session.get('household_name'))
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/bills')
def bills_list():
    if 'user_id' not in session:
        flash('Please log in to view bills.', 'warning')
        return redirect(url_for('login'))

    household_id = 1
    bills = housemate.get_household_bills(household_id)

    return render_template('bills/list.html', bills=bills)


@app.route('/bills/create', methods=['GET', 'POST'])
def bills_create():
    if 'user_id' not in session:
        flash('Please log in to create bills.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            title = request.form['title']
            amount = float(request.form['amount'])
            category = request.form.get('category', 'other')
            strategy_type = request.form['strategy']

            bill_id = housemate.create_bill(
                household_id=1,
                payer_id=session['user_id'],
                title=title,
                amount=amount,
                category=category
            )

            participants = [1, 2, 3]
            params = None

            if strategy_type == 'percentage':
                params = {
                    1: float(request.form.get('percent_1', 33.33)),
                    2: float(request.form.get('percent_2', 33.33)),
                    3: float(request.form.get('percent_3', 33.34))
                }
            elif strategy_type == 'fixed':
                params = {
                    1: float(request.form.get('fixed_1', amount/3)),
                    2: float(request.form.get('fixed_2', amount/3)),
                    3: float(request.form.get('fixed_3', amount/3))
                }

            distribution = housemate.split_bill(
                bill_id=bill_id,
                participants=participants,
                strategy_type=strategy_type,
                params=params
            )

            flash(f'Bill "{title}" created and distributed successfully!', 'success')
            return redirect(url_for('bills_detail', bill_id=bill_id))

        except ValueError as e:
            flash(f'Error creating bill: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Unexpected error: {str(e)}', 'danger')

    return render_template('bills/create.html')


@app.route('/bills/<int:bill_id>')
def bills_detail(bill_id):
    if 'user_id' not in session:
        flash('Please log in to view bill details.', 'warning')
        return redirect(url_for('login'))

    bill = housemate.get_bill(bill_id)

    if not bill:
        flash('Bill not found.', 'danger')
        return redirect(url_for('bills_list'))

    return render_template('bills/detail.html', bill=bill)


@app.route('/bills/<int:bill_id>/delete', methods=['POST'])
def bills_delete(bill_id):
    if 'user_id' not in session:
        flash('Please log in to delete bills.', 'warning')
        return redirect(url_for('login'))

    bill = housemate.get_bill(bill_id)

    if not bill:
        flash('Bill not found.', 'danger')
        return redirect(url_for('bills_list'))

    housemate.delete_bill(bill_id)
    flash(f'Bill "{bill.title}" deleted successfully.', 'success')
    return redirect(url_for('bills_list'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def inject_config():
    return {
        'app_name': config.APP_NAME,
        'version': config.VERSION,
    }


if __name__ == '__main__':
    from src.infrastructure.database import init_db
    db_path = Path(config.DATABASE_PATH)
    if not db_path.exists():
        print("Database not found. Initializing...")
        init_db()

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
