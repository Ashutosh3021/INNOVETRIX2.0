"""
Test script for Phase 4 & 5 Analytics Features
This script creates test data and validates the new analytics endpoints
"""
import asyncio
import sys
from datetime import datetime
from bson import ObjectId
from app.database.db import get_database
from app.services.auth_service import AuthService


async def create_test_data():
    """Create comprehensive test data for analytics"""
    db = get_database()
    
    print("=" * 60)
    print("Creating Test Data for Phase 4 & 5 Analytics")
    print("=" * 60)
    
    # Clear existing test data (optional - comment out if you want to keep existing data)
    # await db.users.delete_many({"email": {"$regex": "test"}})
    
    auth_service = AuthService()
    
    # Create Admin User
    print("\n1. Creating Admin User...")
    try:
        admin_data = {
            "name": "School Admin",
            "email": "admin@bput.edu",
            "password": "Admin@123",
            "role": "admin",
            "skills": [],
            "projects": []
        }
        admin = await auth_service.register_user(admin_data)
        print(f"✓ Admin created: {admin['email']}")
    except Exception as e:
        print(f"Admin might already exist: {e}")
    
    # Create Students with varying placement status
    print("\n2. Creating Students with Placement Data...")
    
    students_data = [
        # CSE Students - Placed
        {
            "name": "Rahul Kumar",
            "email": "rahul@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "CSE",
            "semester": 8,
            "cgpa": 8.9,
            "skills": ["Python", "Java", "React", "MongoDB"],
            "projects": ["E-commerce Platform", "ML Model"],
            "placement_status": "placed",
            "company_placed": "Google",
            "salary_package": 18.5,
            "placement_type": "job"
        },
        {
            "name": "Priya Sharma",
            "email": "priya@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "CSE",
            "semester": 8,
            "cgpa": 9.2,
            "skills": ["JavaScript", "Node.js", "AWS", "Docker"],
            "projects": ["Cloud Dashboard", "API Gateway"],
            "placement_status": "placed",
            "company_placed": "Microsoft",
            "salary_package": 22.0,
            "placement_type": "job"
        },
        {
            "name": "Amit Patel",
            "email": "amit@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "CSE",
            "semester": 6,
            "cgpa": 7.8,
            "skills": ["Python", "Django", "PostgreSQL"],
            "projects": ["Student Portal"],
            "placement_status": "placed",
            "company_placed": "Infosys",
            "salary_package": 4.5,
            "placement_type": "internship"
        },
        # ECE Students - Searching
        {
            "name": "Sneha Reddy",
            "email": "sneha@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "ECE",
            "semester": 7,
            "cgpa": 8.2,
            "skills": ["Embedded Systems", "C++", "VLSI Design"],
            "projects": ["IoT Project", "FPGA Design"],
            "placement_status": "searching"
        },
        {
            "name": "Vikram Singh",
            "email": "vikram@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "ECE",
            "semester": 8,
            "cgpa": 7.5,
            "skills": ["Signal Processing", "MATLAB", "Python"],
            "projects": ["Signal Analysis Tool"],
            "placement_status": "searching"
        },
        # ME Students - Not Placed
        {
            "name": "Rajesh Verma",
            "email": "rajesh@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "ME",
            "semester": 6,
            "cgpa": 6.8,
            "skills": ["CAD", "AutoCAD", "SolidWorks"],
            "projects": ["Engine Design"],
            "placement_status": "not_placed"
        },
        {
            "name": "Anjali Gupta",
            "email": "anjali@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "ME",
            "semester": 4,
            "cgpa": 7.0,
            "skills": ["Thermodynamics", "CAD"],
            "projects": [],
            "placement_status": "not_placed"
        },
        # EE Students - Mixed
        {
            "name": "Karthik Rao",
            "email": "karthik@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "EE",
            "semester": 8,
            "cgpa": 8.5,
            "skills": ["Power Systems", "MATLAB", "Python"],
            "projects": ["Smart Grid Project"],
            "placement_status": "placed",
            "company_placed": "TCS",
            "salary_package": 3.5,
            "placement_type": "job"
        },
        {
            "name": "Deepika Iyer",
            "email": "deepika@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "EE",
            "semester": 5,
            "cgpa": 7.2,
            "skills": ["Circuit Design", "PCB Design"],
            "projects": [],
            "placement_status": "not_placed"
        },
        # More students for better analytics
        {
            "name": "Suresh Menon",
            "email": "suresh@student.bput.edu",
            "password": "Student@123",
            "role": "student",
            "branch": "CSE",
            "semester": 7,
            "cgpa": 8.0,
            "skills": ["Java", "Spring Boot", "MySQL"],
            "projects": ["Banking System"],
            "placement_status": "placed",
            "company_placed": "Wipro",
            "salary_package": 3.8,
            "placement_type": "job"
        }
    ]
    
    created_count = 0
    for student_data in students_data:
        try:
            student = await auth_service.register_user(student_data)
            created_count += 1
            status = student_data.get('placement_status', 'not_placed')
            company = student_data.get('company_placed', 'N/A')
            print(f"✓ Student created: {student['email']} - {status} - {company}")
        except Exception as e:
            print(f"Student might already exist: {student_data['email']}")
    
    print(f"\n✓ Created {created_count} new students")
    
    # Create Company Users
    print("\n3. Creating Company Users...")
    companies_data = [
        {
            "name": "Google India",
            "email": "hr@google.com",
            "password": "Company@123",
            "role": "company",
            "skills": [],
            "projects": []
        },
        {
            "name": "Microsoft",
            "email": "hr@microsoft.com",
            "password": "Company@123",
            "role": "company",
            "skills": [],
            "projects": []
        }
    ]
    
    for company_data in companies_data:
        try:
            company = await auth_service.register_user(company_data)
            print(f"✓ Company created: {company['email']}")
        except Exception as e:
            print(f"Company might already exist: {company_data['email']}")
    
    print("\n" + "=" * 60)
    print("Test Data Creation Complete!")
    print("=" * 60)
    print("\nYou can now test the following features:")
    print("1. Login as admin: admin@bput.edu / Admin@123")
    print("2. View placement analytics")
    print("3. Filter students by branch, semester, placement status")
    print("4. View company hiring statistics")
    print("5. Export unplaced students list")
    print("6. Sort company hiring stats")
    print("=" * 60)


async def validate_analytics():
    """Validate analytics endpoints"""
    from app.services.admin_service import AdminService
    
    print("\n" + "=" * 60)
    print("Validating Analytics Endpoints")
    print("=" * 60)
    
    admin_service = AdminService()
    
    # Test 1: Placement Analytics
    print("\n1. Testing Placement Analytics...")
    try:
        placement_data = await admin_service.get_placement_analytics()
        print(f"✓ Placement Rate: {placement_data['placement_rate']}%")
        print(f"  - Placed: {placement_data['placed_students']}")
        print(f"  - Searching: {placement_data['searching_students']}")
        print(f"  - Not Placed: {placement_data['not_placed_students']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Company Hiring Stats
    print("\n2. Testing Company Hiring Stats...")
    try:
        company_stats = await admin_service.get_company_hiring_stats()
        print(f"✓ Found {len(company_stats)} companies with placements:")
        for company in company_stats[:5]:
            print(f"  - {company['company']}: {company['students_hired']} students @ ₹{company['avg_salary_offered']} LPA")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Unplaced Students
    print("\n3. Testing Unplaced Students List...")
    try:
        unplaced = await admin_service.get_unplaced_students()
        print(f"✓ Found {len(unplaced)} unplaced students")
        for student in unplaced[:3]:
            print(f"  - {student['name']} ({student['branch']}) - CGPA: {student.get('cgpa', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 4: Students by Branch
    print("\n4. Testing Students by Branch...")
    try:
        branch_stats = await admin_service.get_students_by_branch()
        print(f"✓ Found {len(branch_stats)} branches:")
        for branch in branch_stats:
            print(f"  - {branch['branch']}: {branch['student_count']} students (Avg CGPA: {branch['avg_cgpa']})")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Validation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    print("\nPhase 4 & 5 Analytics Test Suite")
    print("=" * 60)
    
    choice = input("\nChoose an option:\n1. Create Test Data\n2. Validate Analytics\n3. Both\n\nEnter choice (1/2/3): ")
    
    if choice == "1":
        asyncio.run(create_test_data())
    elif choice == "2":
        asyncio.run(validate_analytics())
    elif choice == "3":
        asyncio.run(create_test_data())
        asyncio.run(validate_analytics())
    else:
        print("Invalid choice!")
