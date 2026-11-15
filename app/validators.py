"""Server-side input validation. Each function returns (clean_value, error_message)."""
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,59}$")
SEAT_RE = re.compile(r"^[A-E][1-8]$")
PAYMENT_METHODS = ("UPI", "Card", "Wallet")


def validate_name(value):
    value = (value or "").strip()
    if not NAME_RE.match(value):
        return None, "Name must be 2-60 letters (spaces, . ' - allowed)."
    return value, None


def validate_email(value):
    value = (value or "").strip().lower()
    if not EMAIL_RE.match(value):
        return None, "Enter a valid email address."
    return value, None


def validate_password(value):
    value = value or ""
    if len(value) < 8 or not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
        return None, "Password must be at least 8 characters with a letter and a digit."
    return value, None


def validate_seats(values, max_seats=6):
    seats = sorted(set(v.strip().upper() for v in values or []))
    if not seats:
        return None, "Select at least one seat."
    if len(seats) > max_seats:
        return None, f"You can book at most {max_seats} seats at a time."
    if any(not SEAT_RE.match(s) for s in seats):
        return None, "Invalid seat selected."
    return seats, None


def validate_payment(value):
    if value not in PAYMENT_METHODS:
        return None, "Choose a valid payment method."
    return value, None


def validate_review(stars, comment):
    try:
        stars = int(stars)
    except (TypeError, ValueError):
        return None, None, "Rating must be a number from 1 to 5."
    if not 1 <= stars <= 5:
        return None, None, "Rating must be between 1 and 5."
    comment = (comment or "").strip()
    if not comment or len(comment) > 300:
        return None, None, "Review must be 1-300 characters."
    return stars, comment, None
