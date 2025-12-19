"""
Quick test script to verify authentication works
"""
from src.infrastructure.database import DatabaseConnection
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService
import config

# Setup
db = DatabaseConnection(config.DATABASE_PATH)
user_repo = UserRepository(db)
auth_service = AuthService(user_repo)

# Test 1: Login with correct credentials
print("Test 1: Login with correct credentials (marin@test.com / test123)")
user = auth_service.login('marin@test.com', 'test123')
if user:
    print(f"✓ SUCCESS: Logged in as {user.get_full_name()} (ID: {user.user_id})")
else:
    print("✗ FAILED: Login unsuccessful")

# Test 2: Login with wrong password
print("\nTest 2: Login with wrong password (marin@test.com / wrongpass)")
user = auth_service.login('marin@test.com', 'wrongpass')
if user:
    print("✗ FAILED: Should not have logged in with wrong password")
else:
    print("✓ SUCCESS: Correctly rejected wrong password")

# Test 3: Login with non-existent email
print("\nTest 3: Login with non-existent email")
user = auth_service.login('nonexistent@test.com', 'test123')
if user:
    print("✗ FAILED: Should not have logged in with non-existent email")
else:
    print("✓ SUCCESS: Correctly rejected non-existent email")

# Test 4: Check all test users can login
print("\nTest 4: Check all test users can login with 'test123'")
test_emails = ['marin@test.com', 'ana@test.com', 'ivan@test.com', 'marija@test.com']
for email in test_emails:
    user = auth_service.login(email, 'test123')
    if user:
        print(f"✓ {email}: {user.get_full_name()}")
    else:
        print(f"✗ {email}: FAILED")

print("\n" + "="*50)
print("Authentication test complete!")
