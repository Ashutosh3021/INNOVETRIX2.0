"""
Admin service for administrative operations and analytics
"""
from datetime import datetime
from typing import List, Dict, Optional, Any
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from app.database.db import get_database, is_db_ready


class AdminService:
    """Service class for admin-related operations"""
    
    def __init__(self):
        if not is_db_ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not ready. Please try again later."
            )
        self.db = get_database()
        if self.db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available."
            )
        self.users_collection = self.db.users
        self.internships_collection = self.db.internships
        self.applications_collection = self.db.applications
    
    async def verify_admin(self, user_id: str) -> bool:
        """
        Verify if user is an admin
        
        Args:
            user_id: User ID to verify
            
        Returns:
            True if user is admin, False otherwise
        """
        try:
            object_id = ObjectId(user_id)
            user = await self.users_collection.find_one({"_id": object_id})
            return user is not None and user.get("role") == "admin"
        except InvalidId:
            return False
    
    async def get_analytics_overview(self) -> Dict[str, Any]:
        """
        Get comprehensive analytics overview
        
        Returns:
            Dictionary with analytics data
        """
        # Count totals
        total_students = await self.users_collection.count_documents({"role": "student"})
        total_companies = await self.users_collection.count_documents({"role": "company"})
        total_internships = await self.internships_collection.count_documents({})
        total_applications = await self.applications_collection.count_documents({})
        
        # Count by application status
        pending_applications = await self.applications_collection.count_documents({"status": "pending"})
        accepted_applications = await self.applications_collection.count_documents({"status": "accepted"})
        rejected_applications = await self.applications_collection.count_documents({"status": "rejected"})
        
        return {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_internships": total_internships,
            "total_applications": total_applications,
            "pending_applications": pending_applications,
            "accepted_applications": accepted_applications,
            "rejected_applications": rejected_applications
        }
    
    async def get_students_by_branch(self) -> List[Dict[str, Any]]:
        """
        Get student count grouped by branch
        
        Returns:
            List of branch statistics
        """
        pipeline = [
            {"$match": {"role": "student", "branch": {"$exists": True, "$ne": None}}},
            {"$group": {
                "_id": "$branch",
                "count": {"$sum": 1},
                "avg_cgpa": {"$avg": "$cgpa"}
            }},
            {"$sort": {"count": -1}}
        ]
        
        cursor = self.users_collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        return [
            {
                "branch": item["_id"],
                "student_count": item["count"],
                "avg_cgpa": round(item.get("avg_cgpa", 0.0), 2) if item.get("avg_cgpa") else 0.0
            }
            for item in results
        ]
    
    async def get_students_by_semester(self) -> List[Dict[str, Any]]:
        """
        Get student count grouped by semester
        
        Returns:
            List of semester statistics
        """
        pipeline = [
            {"$match": {"role": "student", "semester": {"$exists": True, "$ne": None}}},
            {"$group": {
                "_id": "$semester",
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        cursor = self.users_collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        return [
            {
                "semester": item["_id"],
                "student_count": item["count"]
            }
            for item in results
        ]
    
    async def get_top_performing_students(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top performing students by CGPA
        
        Args:
            limit: Number of students to return
            
        Returns:
            List of top students
        """
        cursor = self.users_collection.find(
            {"role": "student", "cgpa": {"$exists": True, "$ne": None}},
            {"name": 1, "email": 1, "branch": 1, "semester": 1, "cgpa": 1, "skills": 1}
        ).sort("cgpa", -1).limit(limit)
        
        students = await cursor.to_list(length=limit)
        
        return [
            {
                "id": str(student["_id"]),
                "name": student.get("name"),
                "email": student.get("email"),
                "branch": student.get("branch"),
                "semester": student.get("semester"),
                "cgpa": student.get("cgpa"),
                "skills_count": len(student.get("skills", []))
            }
            for student in students
        ]
    
    async def get_all_students(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all students with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List of student details
        """
        cursor = self.users_collection.find(
            {"role": "student"},
            {"hashed_password": 0}
        ).skip(skip).limit(limit).sort("created_at", -1)
        
        students = await cursor.to_list(length=limit)
        
        return [
            {
                "id": str(student["_id"]),
                "name": student.get("name"),
                "email": student.get("email"),
                "branch": student.get("branch"),
                "semester": student.get("semester"),
                "cgpa": student.get("cgpa"),
                "skills": student.get("skills", []),
                "projects": student.get("projects", []),
                "is_blocked": student.get("is_blocked", False),
                "created_at": student.get("created_at")
            }
            for student in students
        ]
    
    async def get_all_internships_admin(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all internships for admin view
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List of internship details
        """
        cursor = self.internships_collection.find({}).skip(skip).limit(limit).sort("created_at", -1)
        internships = await cursor.to_list(length=limit)
        
        result = []
        for internship in internships:
            # Get application count for this internship
            app_count = await self.applications_collection.count_documents(
                {"internship_id": str(internship["_id"])}
            )
            
            result.append({
                "id": str(internship["_id"]),
                "title": internship.get("title"),
                "company": internship.get("company"),
                "domain": internship.get("domain"),
                "required_skills": internship.get("required_skills", []),
                "posted_by": internship.get("posted_by"),
                "application_count": app_count,
                "created_at": internship.get("created_at")
            })
        
        return result
    
    async def block_student(self, student_id: str) -> bool:
        """
        Block a student account
        
        Args:
            student_id: Student ID to block
            
        Returns:
            True if successful, False otherwise
        """
        try:
            object_id = ObjectId(student_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid student ID format: {student_id}"
            )
        
        result = await self.users_collection.update_one(
            {"_id": object_id, "role": "student"},
            {"$set": {"is_blocked": True, "updated_at": datetime.utcnow()}}
        )
        
        return result.modified_count > 0
    
    async def unblock_student(self, student_id: str) -> bool:
        """
        Unblock a student account
        
        Args:
            student_id: Student ID to unblock
            
        Returns:
            True if successful, False otherwise
        """
        try:
            object_id = ObjectId(student_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid student ID format: {student_id}"
            )
        
        result = await self.users_collection.update_one(
            {"_id": object_id, "role": "student"},
            {"$set": {"is_blocked": False, "updated_at": datetime.utcnow()}}
        )
        
        return result.modified_count > 0
    
    async def delete_internship_admin(self, internship_id: str) -> bool:
        """
        Delete an internship (admin can delete any internship)
        
        Args:
            internship_id: Internship ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            object_id = ObjectId(internship_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid internship ID format: {internship_id}"
            )
        
        # Delete all applications for this internship first
        await self.applications_collection.delete_many({"internship_id": internship_id})
        
        # Delete the internship
        result = await self.internships_collection.delete_one({"_id": object_id})
        
        return result.deleted_count > 0
    
    async def get_internship_analytics(self) -> List[Dict[str, Any]]:
        """
        Get internship analytics by domain
        
        Returns:
            List of domain statistics
        """
        pipeline = [
            {"$group": {
                "_id": "$domain",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        
        cursor = self.internships_collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        return [
            {
                "domain": item["_id"],
                "internship_count": item["count"]
            }
            for item in results
        ]
    
    async def get_application_analytics(self) -> Dict[str, Any]:
        """
        Get detailed application analytics
        
        Returns:
            Application statistics
        """
        # Get top applied internships
        pipeline = [
            {"$group": {
                "_id": "$internship_id",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        cursor = self.applications_collection.aggregate(pipeline)
        top_internships = await cursor.to_list(length=10)
        
        # Enrich with internship details
        top_applied = []
        for item in top_internships:
            try:
                internship_obj_id = ObjectId(item["_id"])
                internship = await self.internships_collection.find_one({"_id": internship_obj_id})
                if internship:
                    top_applied.append({
                        "internship_id": item["_id"],
                        "title": internship.get("title"),
                        "company": internship.get("company"),
                        "application_count": item["count"]
                    })
            except:
                continue
        
        return {
            "top_applied_internships": top_applied
        }
    
    async def get_placement_analytics(self) -> Dict[str, Any]:
        """
        Get placement tracking analytics
        
        Returns:
            Placement statistics
        """
        # Count students by placement status
        total_students = await self.users_collection.count_documents({"role": "student"})
        placed_students = await self.users_collection.count_documents({
            "role": "student",
            "placement_status": "placed"
        })
        searching_students = await self.users_collection.count_documents({
            "role": "student",
            "placement_status": "searching"
        })
        not_placed = total_students - placed_students - searching_students
        
        # Get placement type distribution
        placement_type_pipeline = [
            {"$match": {"role": "student", "placement_status": "placed"}},
            {"$group": {
                "_id": "$placement_type",
                "count": {"$sum": 1}
            }}
        ]
        cursor = self.users_collection.aggregate(placement_type_pipeline)
        placement_types = await cursor.to_list(length=None)
        
        # Get average salary by placement type
        salary_pipeline = [
            {"$match": {"role": "student", "placement_status": "placed", "salary_package": {"$exists": True, "$ne": None}}},
            {"$group": {
                "_id": "$placement_type",
                "avg_salary": {"$avg": "$salary_package"},
                "min_salary": {"$min": "$salary_package"},
                "max_salary": {"$max": "$salary_package"}
            }}
        ]
        cursor = self.users_collection.aggregate(salary_pipeline)
        salary_stats = await cursor.to_list(length=None)
        
        return {
            "total_students": total_students,
            "placed_students": placed_students,
            "searching_students": searching_students,
            "not_placed_students": not_placed,
            "placement_rate": round((placed_students / total_students * 100), 2) if total_students > 0 else 0,
            "placement_types": [
                {"type": item["_id"], "count": item["count"]}
                for item in placement_types
            ],
            "salary_statistics": [
                {
                    "type": item["_id"],
                    "avg_salary": round(item["avg_salary"], 2),
                    "min_salary": item["min_salary"],
                    "max_salary": item["max_salary"]
                }
                for item in salary_stats
            ]
        }
    
    async def get_company_hiring_stats(self) -> List[Dict[str, Any]]:
        """
        Get company hiring statistics
        
        Returns:
            List of companies with hiring counts
        """
        # Count students placed by company
        pipeline = [
            {"$match": {"role": "student", "placement_status": "placed", "company_placed": {"$exists": True, "$ne": None}}},
            {"$group": {
                "_id": "$company_placed",
                "students_hired": {"$sum": 1},
                "avg_salary_offered": {"$avg": "$salary_package"}
            }},
            {"$sort": {"students_hired": -1}}
        ]
        
        cursor = self.users_collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        return [
            {
                "company": item["_id"],
                "students_hired": item["students_hired"],
                "avg_salary_offered": round(item.get("avg_salary_offered", 0), 2) if item.get("avg_salary_offered") else 0
            }
            for item in results
        ]
    
    async def get_unplaced_students(self) -> List[Dict[str, Any]]:
        """
        Get list of unplaced students
        
        Returns:
            List of students without placements
        """
        cursor = self.users_collection.find(
            {
                "role": "student",
                "$or": [
                    {"placement_status": "not_placed"},
                    {"placement_status": {"$exists": False}},
                    {"placement_status": None}
                ]
            },
            {"name": 1, "email": 1, "branch": 1, "semester": 1, "cgpa": 1, "skills": 1}
        ).sort("cgpa", -1)
        
        students = await cursor.to_list(length=None)
        
        return [
            {
                "id": str(student["_id"]),
                "name": student.get("name"),
                "email": student.get("email"),
                "branch": student.get("branch"),
                "semester": student.get("semester"),
                "cgpa": student.get("cgpa"),
                "skills": student.get("skills", [])
            }
            for student in students
        ]
