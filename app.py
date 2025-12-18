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

# Initialize repositories and services
db = get_db()
user_repository = UserRepository(db)
auth_service = AuthService(user_repository)  # Token service not implemented yet

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
