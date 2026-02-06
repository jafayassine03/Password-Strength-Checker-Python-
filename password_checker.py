import string
import random

def check_password_strength(password):
    score = 0
    feedback = []

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

    if score <= 2:
        strength = "WEAK "
    elif score <= 4:
        strength = "MEDIUM "
    else:
        strength = "STRONG "

    return strength, feedback, {
        "lower": has_lower,
        "upper": has_upper,
        "digit": has_digit,
        "symbol": has_symbol
    }


def generate_strong_password(base_password, checks):
    chars = list(base_password)

    if not checks["lower"]:
        chars.append(random.choice(string.ascii_lowercase))
    if not checks["upper"]:
        chars.append(random.choice(string.ascii_uppercase))
    if not checks["digit"]:
        chars.append(random.choice(string.digits))
    if not checks["symbol"]:
        chars.append(random.choice(string.punctuation))

    while len(chars) < 8:
        chars.append(random.choice(
            string.ascii_letters + string.digits + string.punctuation
        ))

    random.shuffle(chars)
    return "".join(chars)


def main():
    print(" Password Strength Checker\n")

    password = input("Enter a password: ")
    strength, feedback, checks = check_password_strength(password)

    print("\nStrength:", strength)

    if feedback:
        print("\nSuggestions:")
        for tip in feedback:
            print("-", tip)

        print("\n Tip: Let the computer generate a stronger version.")
        choice = input("Generate strong password? (y/n): ").lower()

        if choice == "y":
            strong_password = generate_strong_password(password, checks)
            print("\n Suggested strong password:")
            print(strong_password)


if __name__ == "__main__":
    main()
