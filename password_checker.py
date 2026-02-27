import string
import secrets
import math


COMMON_PASSWORDS = {"123456", "password", "qwerty", "admin", "letmein"}


def calculate_entropy(password):
    pool = 0

    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in COMMON_PASSWORDS:
        return "VERY WEAK", 0, ["This is a very common password!"], 0

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if has_lower:
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if has_upper:
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if has_digit:
        score += 1
    else:
        feedback.append("Add numbers")

    if has_symbol:
        score += 1
    else:
        feedback.append("Add symbols")

    entropy = calculate_entropy(password)

    score_percent = int((score / 5) * 100)

    if score_percent < 40:
        strength = "WEAK"
    elif score_percent < 80:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    return strength, score_percent, feedback, entropy


def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(characters) for _ in range(length))


def improve_password(base_password):
    chars = list(base_password)

    if not any(c.islower() for c in base_password):
        chars.append(secrets.choice(string.ascii_lowercase))
    if not any(c.isupper() for c in base_password):
        chars.append(secrets.choice(string.ascii_uppercase))
    if not any(c.isdigit() for c in base_password):
        chars.append(secrets.choice(string.digits))
    if not any(c in string.punctuation for c in base_password):
        chars.append(secrets.choice(string.punctuation))

    while len(chars) < 12:
        chars.append(secrets.choice(
            string.ascii_letters + string.digits + string.punctuation
        ))

    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main():
    print("🔐 Advanced Password Strength Checker\n")

    while True:
        password = input("Enter a password (or type 'exit'): ")

        if password.lower() == "exit":
            print("Goodbye 👋")
            break

        strength, score, feedback, entropy = check_password_strength(password)

        print(f"\nStrength: {strength}")
        print(f"Score: {score}/100")
        print(f"Entropy: {entropy} bits")

        if feedback:
            print("\nSuggestions:")
            for tip in feedback:
                print("-", tip)

            choice = input("\nGenerate improved version? (y/n): ").lower()
            if choice == "y":
                improved = improve_password(password)
                print("\nSuggested improved password:")
                print(improved)

        print("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    main()