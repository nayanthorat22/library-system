import os
from app import create_app
from app.models import db, User, Book, LibrarySettings

def seed_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database schema created.")

        # Ensure Library Settings exist
        settings = LibrarySettings.get_settings()
        print(f"Library settings confirmed: {settings.borrow_duration_days} days loan, Rs. {settings.daily_fine_rate}/day fine.")

        # Seed Default Administrator
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@library.com')
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(
                name="Library Administrator",
                email=admin_email,
                role="admin"
            )
            admin_user.set_password("Admin@12345")
            db.session.add(admin_user)
            print(f"Created Admin: {admin_email} (Password: Admin@12345)")

        # Seed Demo Student
        student_email = "student@library.com"
        demo_student = User.query.filter_by(email=student_email).first()
        if not demo_student:
            demo_student = User(
                name="Rahul Sharma",
                email=student_email,
                role="student"
            )
            demo_student.set_password("Student@12345")
            db.session.add(demo_student)
            print(f"Created Demo Student: {student_email} (Password: Student@12345)")

        # Seed Default Books using centralized catalog collection
        from app.books_data import BOOKS_COLLECTION

        for b_data in BOOKS_COLLECTION:
            if not Book.query.filter_by(isbn=b_data["isbn"]).first():
                b = Book(**b_data)
                db.session.add(b)

        db.session.commit()
        print(f"Database seeding completed successfully with {len(BOOKS_COLLECTION)} books!")

if __name__ == '__main__':
    seed_database()
