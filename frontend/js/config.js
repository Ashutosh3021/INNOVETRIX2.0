// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    API_ENDPOINTS: {
        // Auth
        REGISTER: '/api/auth/register',
        LOGIN: '/api/auth/login',
        
        // Users
        USERS: '/api/users',
        PROFILE: '/api/users/me',
        
        // Internships
        INTERNSHIPS: '/api/internships',
        
        // Applications
        APPLICATIONS: '/api/applications',
        MY_APPLICATIONS: '/api/applications/my-applications',
        
        // Matching
        RECOMMENDATIONS: '/api/matching/recommendations',
        
        // Admin
        ADMIN_OVERVIEW: '/api/admin/analytics/overview',
        ADMIN_STUDENTS_BY_BRANCH: '/api/admin/analytics/students-by-branch',
        ADMIN_STUDENTS_BY_SEMESTER: '/api/admin/analytics/students-by-semester',
        ADMIN_TOP_STUDENTS: '/api/admin/analytics/top-students',
        ADMIN_INTERNSHIPS: '/api/admin/analytics/internships',
        ADMIN_APPLICATIONS: '/api/admin/analytics/applications',
        ADMIN_PLACEMENT: '/api/admin/analytics/placement',
        ADMIN_COMPANY_HIRING: '/api/admin/analytics/company-hiring',
        ADMIN_UNPLACED_STUDENTS: '/api/admin/students/unplaced',
        ADMIN_ALL_STUDENTS: '/api/admin/students',
        ADMIN_ALL_INTERNSHIPS: '/api/admin/internships',
        ADMIN_BLOCK_STUDENT: '/api/admin/students',
        ADMIN_UNBLOCK_STUDENT: '/api/admin/students',
    },
    
    STORAGE_KEYS: {
        AUTH_TOKEN: 'authToken',
        CURRENT_USER: 'currentUser',
        USER_ROLE: 'userRole',
        THEME: 'theme'
    },
    
    ROLES: {
        STUDENT: 'student',
        COMPANY: 'company',
        ADMIN: 'admin'
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
