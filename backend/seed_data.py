"""
BreachLens Seed Data Script
Creates demo users and preloads sample scan data for immediate demo.
Seeds data into MongoDB Atlas collections.
"""

from passlib.hash import bcrypt
from database import MockDB
from services.scanner import scan_website
import random


def seed_all():
    """Seed demo users and sample scan data into MongoDB."""
    print("Seeding BreachLens demo data...")

    # Seed users (with correct demo emails from spec)
    demo_user = _seed_user("Demo User", "demo.breachlens@gmail.com", "Demo@123", role="user")
    admin_user = _seed_user("Admin User", "admin.breachlens@gmail.com", "Admin@123", role="admin")

    # Seed sample scans for demo user (only if none exist yet)
    existing_scans = MockDB.get_scans_by_user(demo_user["id"])
    if len(existing_scans) == 0:
        sample_urls = [
            "https://example.com",
            "https://testsite.org",
            "https://demoapp.io",
            "https://shopify-test.myshopify.com",
            "https://wordpress-test.local",
        ]

        for url in sample_urls:
            _seed_scan(demo_user["id"], url)

        # Seed a couple scans for admin
        for url in sample_urls[:2]:
            _seed_scan(admin_user["id"], url)

        print(f"Seeded {len(sample_urls)} scans for demo user")
        print("Seeded 2 scans for admin user")
    else:
        print(f"  Scans already exist ({len(existing_scans)} found), skipping seed")
    print("Demo data ready!")


def _seed_user(name, email, password, role="user"):
    """Create user if not exists. Returns user dict."""
    existing = MockDB.get_user_by_email(email)
    if existing:
        print(f"  User {email} already exists")
        return existing

    hashed = bcrypt.hash(password)

    # Use MockDB to create user, then update role if needed
    user = MockDB.create_user(name, email, hashed)

    # Set role via direct MongoDB update (MockDB defaults to "user")
    if role != "user":
        from database import MockDB as DB
        from services.mongodb_service import get_db
        db = get_db()
        db.users.update_one({"_id": user["id"]}, {"$set": {"role": role}})
        user["role"] = role

    print(f"  Created user: {email} (role: {role})")
    return user


def _seed_scan(user_id, url):
    """Run a scan and store results, ensuring deterministic output for demo."""
    random.seed(hash(url) % (2**32))

    scan_data = scan_website(url)
    scan = MockDB.create_scan(
        user_id=user_id,
        url=url,
        results=scan_data["results"],
        stats=scan_data["stats"],
    )
    print(f"  Scan created: {url} ({scan_data['stats']['total_vulnerabilities']} vulns)")
    return scan


if __name__ == "__main__":
    seed_all()
