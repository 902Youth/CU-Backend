from werkzeug.security import generate_password_hash, check_password_hash

def test_password_hashing():
    # Password to be hashed
    password = "example_password"

    # Generate a password hash
    hashed_password = generate_password_hash(password, salt_length=8)
    print(f"Password hash generated: {hashed_password}")
    hashed_password = hashed_password.encode()
    print(f"Hashed Password: {hashed_password}")
    hashed_password = hashed_password.decode()
    # Verify the hashed password
    is_correct_password = check_password_hash(hashed_password.decode(), password)
    print(f"Password verification (correct): {is_correct_password}")

    # Verify with an incorrect password
    is_incorrect_password = check_password_hash(hashed_password, "wrong_password")
    print(f"Password verification (incorrect): {is_incorrect_password}")

if __name__ == "__main__":
    test_password_hashing()
