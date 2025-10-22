// ============================================
// API SERVICE - Centralized API Handling
// ============================================

const API = {
    /**
     * Make an authenticated API request
     */
    async request(endpoint, options = {}) {
        const token = localStorage.getItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN);
        
        const defaultHeaders = {
            'Content-Type': 'application/json',
        };
        
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }
        
        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers,
            },
        };
        
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, config);
            
            // Handle different response types
            if (response.status === 204) {
                return { success: true };
            }
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: 'GET' });
    },
    
    /**
     * POST request
     */
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },
    
    /**
     * PUT request
     */
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },
    
    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },
    
    // ============================================
    // AUTH ENDPOINTS
    // ============================================
    
    async register(userData) {
        return this.post(CONFIG.API_ENDPOINTS.REGISTER, userData);
    },
    
    async login(credentials) {
        return this.post(CONFIG.API_ENDPOINTS.LOGIN, credentials);
    },
    
    // ============================================
    // USER ENDPOINTS
    // ============================================
    
    async getProfile() {
        return this.get(CONFIG.API_ENDPOINTS.PROFILE);
    },
    
    async updateProfile(data) {
        return this.put(CONFIG.API_ENDPOINTS.PROFILE, data);
    },
    
    async getUser(userId) {
        return this.get(`${CONFIG.API_ENDPOINTS.USERS}/${userId}`);
    },
    
    // ============================================
    // INTERNSHIP ENDPOINTS
    // ============================================
    
    async getInternships(params = {}) {
        return this.get(CONFIG.API_ENDPOINTS.INTERNSHIPS, params);
    },
    
    async getInternship(internshipId) {
        return this.get(`${CONFIG.API_ENDPOINTS.INTERNSHIPS}/${internshipId}`);
    },
    
    async createInternship(data) {
        return this.post(CONFIG.API_ENDPOINTS.INTERNSHIPS, data);
    },
    
    async updateInternship(internshipId, data) {
        return this.put(`${CONFIG.API_ENDPOINTS.INTERNSHIPS}/${internshipId}`, data);
    },
    
    async deleteInternship(internshipId) {
        return this.delete(`${CONFIG.API_ENDPOINTS.INTERNSHIPS}/${internshipId}`);
    },
    
    // ============================================
    // APPLICATION ENDPOINTS
    // ============================================
    
    async applyToInternship(internshipId) {
        return this.post(CONFIG.API_ENDPOINTS.APPLICATIONS, { internship_id: internshipId });
    },
    
    async getMyApplications() {
        return this.get(CONFIG.API_ENDPOINTS.MY_APPLICATIONS);
    },
    
    async getInternshipApplications(internshipId) {
        return this.get(`${CONFIG.API_ENDPOINTS.APPLICATIONS}/internship/${internshipId}`);
    },
    
    async updateApplicationStatus(applicationId, status) {
        return this.put(
            `${CONFIG.API_ENDPOINTS.APPLICATIONS}/${applicationId}/status`,
            { status }
        );
    },
    
    // ============================================
    // MATCHING ENDPOINTS
    // ============================================
    
    async getRecommendations(limit = 10) {
        return this.get(CONFIG.API_ENDPOINTS.RECOMMENDATIONS, { limit });
    },
    
    // ============================================
    // ADMIN ENDPOINTS
    // ============================================
    
    async getAdminOverview() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_OVERVIEW);
    },
    
    async getStudentsByBranch() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_STUDENTS_BY_BRANCH);
    },
    
    async getStudentsBySemester() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_STUDENTS_BY_SEMESTER);
    },
    
    async getTopStudents(limit = 10) {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_TOP_STUDENTS, { limit });
    },
    
    async getInternshipAnalytics() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_INTERNSHIPS);
    },
    
    async getApplicationAnalytics() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_APPLICATIONS);
    },
    
    async getAllStudents(skip = 0, limit = 100) {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_ALL_STUDENTS, { skip, limit });
    },
    
    async getAllInternshipsAdmin(skip = 0, limit = 100) {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_ALL_INTERNSHIPS, { skip, limit });
    },
    
    async blockStudent(studentId) {
        return this.post(`${CONFIG.API_ENDPOINTS.ADMIN_BLOCK_STUDENT}/${studentId}/block`, {});
    },
    
    async unblockStudent(studentId) {
        return this.post(`${CONFIG.API_ENDPOINTS.ADMIN_UNBLOCK_STUDENT}/${studentId}/unblock`, {});
    },
    
    async deleteInternshipAdmin(internshipId) {
        return this.delete(`${CONFIG.API_ENDPOINTS.ADMIN_ALL_INTERNSHIPS}/${internshipId}`);
    },
    
    async getPlacementAnalytics() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_PLACEMENT);
    },
    
    async getCompanyHiringStats() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_COMPANY_HIRING);
    },
    
    async getUnplacedStudents() {
        return this.get(CONFIG.API_ENDPOINTS.ADMIN_UNPLACED_STUDENTS);
    }
};
