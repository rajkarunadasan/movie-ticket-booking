# Movie Ticket Booking Application (CineBook)

A web-based movie ticket booking application built with **Flask and SQLite**, developed incrementally using the **Scrum framework** (four sprints) and managed with Git.

**Repository:** https://github.com/rajkarunadasan/movie-ticket-booking

**Team:** Raj Karunadasan (25039177205221084) and Mukesh Sundar (25039177205221072)
**Course:** B.Tech IT B, Thiagarajar College of Engineering, Madurai
**Subject:** Software Engineering (22IT331) &middot; **Instructor:** Dr. R. Kirubahari

## Problem Statement and Objectives

Booking movie tickets at the counter means queues, no visibility of free seats, and no record of past bookings. This project provides an online booking flow where users can browse movies, pick exact seats, pay and receive an e-ticket.

**Objectives**
- Deliver working features incrementally, sprint by sprint, using Scrum (see the Assignment 1 poster).
- Prevent double booking of seats.
- Validate all input and handle errors gracefully.
- Demonstrate Git practice: regular commits, branches per feature, merges, per-member contributions.

## Features / Modules (by Sprint)

| Sprint | Feature | Module |
|---|---|---|
| 1 | User registration and login (hashed passwords) | `app/auth.py` |
| 1 | Browse movies and showtimes | `app/movies.py` |
| 2 | Search and filter (title, genre, language) | `app/movies.py` |
| 2 | Seat selection with live seat map | `app/booking.py` |
| 3 | Payment (simulated), booking confirmation, e-ticket, booking history | `app/booking.py` |
| 4 | Ratings and reviews | `app/movies.py` |
| 4 | UI/UX improvements (responsive layout) | `app/static/style.css` |

Cross-cutting: SQLite schema and demo data (`app/db.py`), input validation (`app/validators.py`), custom error pages.

## Technology Stack and Tools

Python 3.10+, Flask 3 (Jinja2), SQLite, pytest, Git and GitHub. The Assignment 1 poster listed Android Studio, Figma, Firebase and Jira as the planned production toolset; this mini-project implements the same Scrum backlog as a web application for easy demonstration.

## Prerequisites and Installation

```bash
git clone https://github.com/rajkarunadasan/movie-ticket-booking.git
cd movie-ticket-booking
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

Open <http://127.0.0.1:5000>. The database `tickets.db` is created and filled with demo movies automatically on first run (git-ignored). Set the `SECRET_KEY` environment variable for any real deployment.

Run the tests with `python -m pytest -v`.

## Sample Inputs and Outputs

| Action | Input | Output |
|---|---|---|
| Register | `Asha Devi`, `asha@example.com`, `secret123` | Account created, redirected to login |
| Register (weak password) | `short` | "Password must be at least 8 characters with a letter and a digit." |
| Search | `galaxy` | Only *Galaxy Rangers* is listed |
| Filter | Genre `Drama`, Language `Tamil` | Only *The Last Lighthouse* |
| Select seats | `A1, A2` | Summary: 2 x price = total |
| Pay | UPI | E-ticket with booking ID such as `CB5F3A91C2` |
| Book a taken seat | `A1` again | "Some selected seats were just taken." |
| Review | 4 stars, "Gripping story" | Review shown, average rating updated |

Screenshots are in [`docs/screenshots`](docs/screenshots).

## Testing Performed and Results

**47 automated tests (pytest), all passing.**

| Area | Cases | Result |
|---|---|---|
| Validators | names, email, password, seats, payment, review | Pass |
| Authentication | register, duplicate email, wrong password, logout, open-redirect block | Pass |
| Browse and search | listing, detail, filters, no results, SQL-injection attempt | Pass |
| Seat selection | login required, 0 / >6 / invalid seats, checkout summary | Pass |
| Booking | e-ticket, seats become unavailable, double-booking prevented, invalid payment, ticket privacy | Pass |
| Reviews | login required, average, update instead of duplicate, invalid input | Pass |

Two defects were found and fixed on their own branches: a booking test that counted the reference text twice (`fix/booking-test-count`), and star ratings that rendered as escaped text instead of ★ symbols (`fix/star-rating-display`).

## Team Details and Individual Contributions

| Member | Register No. | Contribution (branch) |
|---|---|---|
| Raj Karunadasan | 25039177205221084 | Project setup, database schema and seed data, validators, movie browsing (`feature/browse-movies`), seat selection (`feature/seat-selection`), ratings and reviews (`feature/ratings-reviews`), README |
| Mukesh Sundar (GitHub: mumukeshsundar-dotcom) | 25039177205221072 | Authentication (`feature/user-auth`), search and filters (`feature/search-filter`), payment and e-ticket (`feature/payment-eticket`), UI improvements (`feature/ui-improvements`) |

## Git Workflow

`main` holds stable code. Each feature was developed on its own branch with small commits and tests, then merged with `--no-ff` so that merges are visible in the history (`git log --graph`).

## Known Limitations and Future Enhancements

- Payment is simulated; no real payment gateway.
- No CSRF tokens, email verification or password reset.
- No seat-hold timer while a user is paying (double booking is still prevented at the database level).
- Notifications and offers (planned in Sprint 4 of the poster) are not implemented.
- Future: payment gateway, QR-code tickets, admin panel to manage movies and shows, cancellation and refunds, mobile app.

## Acknowledgements

Flask, pytest and SQLite. No code was copied from other teams' repositories.
