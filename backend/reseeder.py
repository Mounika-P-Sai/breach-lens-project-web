"""Quick script to force re-seed demo data with fixes."""
from services.mongodb_service import connect_mongodb, get_db, is_connected
from seed_data import seed_all

db = connect_mongodb()
if db is None or not is_connected():
    print("ERROR: Could not connect to MongoDB")
    exit(1)

# Find demo users
demo = db.users.find_one({"email": "demo.breachlens@gmail.com"})
admin = db.users.find_one({"email": "admin.breachlens@gmail.com"})

if demo:
    uid = demo["_id"]
    r1 = db.scans.delete_many({"user_id": uid})
    r2 = db.vulnerabilities.delete_many({"user_id": uid})
    r3 = db.reports.delete_many({"user_id": uid})
    print(f"Deleted {r1.deleted_count} scans, {r2.deleted_count} vulns, {r3.deleted_count} reports for demo")

if admin:
    uid = admin["_id"]
    r1 = db.scans.delete_many({"user_id": uid})
    r2 = db.vulnerabilities.delete_many({"user_id": uid})
    r3 = db.reports.delete_many({"user_id": uid})
    print(f"Deleted {r1.deleted_count} scans, {r2.deleted_count} vulns, {r3.deleted_count} reports for admin")

print("Re-seeding...")
seed_all()
print("Done!")
