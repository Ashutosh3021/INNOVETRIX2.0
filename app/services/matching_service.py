"""
Matching service using TF-IDF and cosine similarity for skill matching
"""
from typing import List
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models.internship import InternshipInDB, MatchedInternship
from app.models.user import UserInDB

logger = logging.getLogger(__name__)


class MatchingService:
    """Service class for matching students to internships based on skills"""
    
    @staticmethod
    def calculate_match_score(
        user: UserInDB,
        internships: List[InternshipInDB]
    ) -> List[MatchedInternship]:
        """
        Calculate match scores between user skills and internship requirements
        using TF-IDF and cosine similarity
        
        Args:
            user: User object with skills
            internships: List of internship objects
            
        Returns:
            List of internships with match scores, sorted by score (highest first)
        """
        if not internships:
            logger.warning("No internships provided for matching")
            return []
        
        # Prepare user skills as a single string
        user_skills_text = " ".join(user.skills).lower() if user.skills else ""
        
        # If user has no skills, return internships with 0 match score
        if not user.skills or not user_skills_text.strip():
            logger.info(f"User {user.id} has no skills, returning 0 match scores")
            return [
                MatchedInternship(
                    _id=internship.id,
                    title=internship.title,
                    company=internship.company,
                    domain=internship.domain,
                    required_skills=internship.required_skills,
                    description=internship.description,
                    location=internship.location,
                    duration=internship.duration,
                    stipend=internship.stipend,
                    created_at=internship.created_at,
                    match_score=0.0,
                    matched_skills=[]
                )
                for internship in internships
            ]
        
        # Prepare internship skills as strings
        internship_skills_texts = [
            " ".join(internship.required_skills).lower() if internship.required_skills else ""
            for internship in internships
        ]
        
        # Filter out empty internship skills
        valid_internships = [
            (i, internship) for i, internship in enumerate(internships)
            if internship.required_skills and internship_skills_texts[i].strip()
        ]
        
        if not valid_internships:
            logger.warning("No internships with valid skills found")
            return [
                MatchedInternship(
                    _id=internship.id,
                    title=internship.title,
                    company=internship.company,
                    domain=internship.domain,
                    required_skills=internship.required_skills,
                    description=internship.description,
                    location=internship.location,
                    duration=internship.duration,
                    stipend=internship.stipend,
                    created_at=internship.created_at,
                    match_score=0.0,
                    matched_skills=[]
                )
                for internship in internships
            ]
        
        # Combine all texts for TF-IDF vectorization
        valid_indices = [i for i, _ in valid_internships]
        valid_skills_texts = [internship_skills_texts[i] for i in valid_indices]
        all_texts = [user_skills_text] + valid_skills_texts
        
        # Create TF-IDF vectors with improved configuration
        vectorizer = TfidfVectorizer(
            lowercase=True,
            token_pattern=r'[a-zA-Z0-9+#.]+',  # Handle special chars in tech skills
            max_features=500,
            stop_words=None,  # Don't remove stop words for technical skills
            ngram_range=(1, 2)  # Support single words and bigrams
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            logger.info(f"TF-IDF matrix created: {tfidf_matrix.shape}")
        except ValueError as e:
            logger.error(f"TF-IDF vectorization failed: {e}")
            # Return internships with 0 match score on failure
            return [
                MatchedInternship(
                    _id=internship.id,
                    title=internship.title,
                    company=internship.company,
                    domain=internship.domain,
                    required_skills=internship.required_skills,
                    description=internship.description,
                    location=internship.location,
                    duration=internship.duration,
                    stipend=internship.stipend,
                    created_at=internship.created_at,
                    match_score=0.0,
                    matched_skills=[]
                )
                for internship in internships
            ]
        
        # User vector is the first one
        user_vector = tfidf_matrix[0:1]
        
        # Internship vectors are the rest
        internship_vectors = tfidf_matrix[1:]
        
        # Calculate cosine similarity between user and each internship
        similarity_scores = cosine_similarity(user_vector, internship_vectors)[0]
        
        # Create matched internship objects with scores
        matched_internships = []
        
        # First, add all valid internships with their scores
        for idx, (original_idx, internship) in enumerate(valid_internships):
            score = float(similarity_scores[idx])
            
            # Find matched skills (skills that appear in both user and internship)
            user_skills_lower = [skill.lower() for skill in user.skills]
            internship_skills_lower = [skill.lower() for skill in internship.required_skills]
            matched_skills = [
                skill for skill in user.skills
                if skill.lower() in internship_skills_lower
            ]
            
            matched_internship = MatchedInternship(
                _id=internship.id,
                title=internship.title,
                company=internship.company,
                domain=internship.domain,
                required_skills=internship.required_skills,
                description=internship.description,
                location=internship.location,
                duration=internship.duration,
                stipend=internship.stipend,
                created_at=internship.created_at,
                match_score=round(score, 4),
                matched_skills=matched_skills
            )
            matched_internships.append(matched_internship)
        
        # Add internships that were skipped (no skills) with 0 score
        skipped_indices = set(range(len(internships))) - set(valid_indices)
        for idx in skipped_indices:
            internship = internships[idx]
            matched_internship = MatchedInternship(
                _id=internship.id,
                title=internship.title,
                company=internship.company,
                domain=internship.domain,
                required_skills=internship.required_skills,
                description=internship.description,
                location=internship.location,
                duration=internship.duration,
                stipend=internship.stipend,
                created_at=internship.created_at,
                match_score=0.0,
                matched_skills=[]
            )
            matched_internships.append(matched_internship)
        
        # Sort by match score (highest first)
        matched_internships.sort(key=lambda x: x.match_score, reverse=True)
        
        logger.info(f"Matched {len(matched_internships)} internships for user {user.id}")
        return matched_internships
    
    @staticmethod
    def get_top_matches(
        matched_internships: List[MatchedInternship],
        top_n: int = 10,
        min_score: float = 0.0
    ) -> List[MatchedInternship]:
        """
        Filter and return top N matches above a minimum score
        
        Args:
            matched_internships: List of matched internships
            top_n: Number of top matches to return
            min_score: Minimum match score threshold
            
        Returns:
            List of top matched internships
        """
        # Filter by minimum score
        filtered = [
            internship for internship in matched_internships
            if internship.match_score >= min_score
        ]
        
        # Return top N
        return filtered[:top_n]