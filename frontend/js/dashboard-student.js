// ============================================
// STUDENT DASHBOARD MODULE
// ============================================

const StudentDashboard = {
    currentUser: null,
    recommendations: [],
    applications: [],
    
    /**
     * Initialize student dashboard
     */
    async init() {
        this.currentUser = Auth.getCurrentUser();
        if (!this.currentUser) {
            Auth.logout();
            return;
        }
        
        this.render();
        await this.loadData();
    },
    
    /**
     * Render dashboard structure
     */
    render() {
        const dashboard = document.getElementById('student-dashboard');
        dashboard.innerHTML = `
            <div class="dashboard-container">
                <!-- Header -->
                <div class="dashboard-header fade-in">
                    <div class="dashboard-title">
                        <h1>Welcome, ${this.currentUser.name}</h1>
                        <p>Your personalized internship recommendations</p>
                    </div>
                    <div class="dashboard-actions">
                        <button class="btn btn-secondary" id="view-profile-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                <circle cx="12" cy="7" r="4"/>
                            </svg>
                            Profile
                        </button>
                        <button class="btn btn-primary" id="refresh-recommendations-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
                            </svg>
                            Refresh
                        </button>
                        <button class="btn btn-secondary" id="logout-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
                            </svg>
                            Logout
                        </button>
                    </div>
                </div>
                
                <!-- Stats Cards -->
                <div class="stats-grid" id="stats-grid">
                    <!-- Stats will be loaded here -->
                </div>
                
                <!-- Main Content Grid -->
                <div class="dashboard-content">
                    <!-- Skills Visualization -->
                    <div class="card slide-in-left">
                        <div class="card-header">
                            <h3 class="card-title">Your Skills</h3>
                        </div>
                        <div id="skills-visualization" class="skills-container">
                            <!-- Skills will be rendered here -->
                        </div>
                    </div>
                    
                    <!-- AI Recommendations -->
                    <div class="card slide-in-right">
                        <div class="card-header">
                            <h3 class="card-title">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="vertical-align: middle;">
                                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                                </svg>
                                AI-Powered Recommendations
                            </h3>
                            <span class="badge">Top Matches</span>
                        </div>
                        <div id="recommendations-list" class="recommendations-container">
                            <div class="loading-container">
                                <div class="loading-spinner"></div>
                                <p>Loading recommendations...</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- My Applications -->
                    <div class="card scale-in">
                        <div class="card-header">
                            <h3 class="card-title">My Applications</h3>
                            <span class="badge" id="applications-count">0</span>
                        </div>
                        <div id="applications-list" class="applications-container">
                            <!-- Applications will be rendered here -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.setupEventListeners();
    },
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => Auth.logout());
        }
        
        const refreshBtn = document.getElementById('refresh-recommendations-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadRecommendations());
        }
        
        const profileBtn = document.getElementById('view-profile-btn');
        if (profileBtn) {
            profileBtn.addEventListener('click', () => this.showProfile());
        }
    },
    
    /**
     * Load dashboard data
     */
    async loadData() {
        await Promise.all([
            this.loadStats(),
            this.loadSkills(),
            this.loadRecommendations(),
            this.loadApplications()
        ]);
    },
    
    /**
     * Load statistics
     */
    async loadStats() {
        const statsGrid = document.getElementById('stats-grid');
        if (!statsGrid) return;
        
        const stats = [
            {
                icon: '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
                label: 'Skills',
                value: this.currentUser.skills?.length || 0,
                color: 'var(--accent-cyan)'
            },
            {
                icon: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
                label: 'Applications',
                value: '...',
                color: 'var(--accent-pink)',
                id: 'stat-applications'
            },
            {
                icon: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
                label: 'CGPA',
                value: this.currentUser.cgpa?.toFixed(2) || 'N/A',
                color: 'var(--accent-purple)'
            },
            {
                icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
                label: 'Semester',
                value: this.currentUser.semester || 'N/A',
                color: 'var(--accent-green)'
            }
        ];
        
        statsGrid.innerHTML = stats.map(stat => `
            <div class="stat-card" ${stat.id ? `id="${stat.id}"` : ''}>
                <div class="stat-icon" style="color: ${stat.color}">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        ${stat.icon}
                    </svg>
                </div>
                <div class="stat-content">
                    <div class="stat-value">${stat.value}</div>
                    <div class="stat-label">${stat.label}</div>
                </div>
            </div>
        `).join('');
    },
    
    /**
     * Load and visualize skills
     */
    loadSkills() {
        const container = document.getElementById('skills-visualization');
        if (!container || !this.currentUser.skills) return;
        
        const skills = this.currentUser.skills;
        
        if (skills.length === 0) {
            container.innerHTML = '<p class="empty-state">No skills added yet. Update your profile to add skills.</p>';
            return;
        }
        
        container.innerHTML = skills.map(skill => `
            <span class="skill-tag">
                ${skill}
            </span>
        `).join('');
        
        // Add stagger animation
        Animations.staggerChildren(container, 50);
    },
    
    /**
     * Load AI recommendations
     */
    async loadRecommendations() {
        const container = document.getElementById('recommendations-list');
        if (!container) return;
        
        try {
            this.recommendations = await API.getRecommendations(10);
            
            if (this.recommendations.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M16 16s-1.5-2-4-2-4 2-4 2M9 9h.01M15 9h.01"/>
                        </svg>
                        <p>No recommendations available yet.</p>
                        <p class="text-secondary">Add more skills to get personalized matches!</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = this.recommendations.map(rec => `
                <div class="recommendation-card">
                    <div class="recommendation-header">
                        <h4>${rec.internship.title}</h4>
                        <div class="match-score" style="--score: ${rec.match_score * 100}">
                            <svg width="48" height="48" viewBox="0 0 48 48">
                                <circle cx="24" cy="24" r="20" fill="none" stroke="var(--bg-tertiary)" stroke-width="4"/>
                                <circle cx="24" cy="24" r="20" fill="none" stroke="var(--accent-green)" stroke-width="4"
                                    stroke-dasharray="${rec.match_score * 125.6} 125.6" 
                                    stroke-dashoffset="0" 
                                    transform="rotate(-90 24 24)"/>
                            </svg>
                            <span class="score-text">${Math.round(rec.match_score * 100)}%</span>
                        </div>
                    </div>
                    <div class="recommendation-body">
                        <p class="company"><strong>${rec.internship.company}</strong></p>
                        <p class="domain">${rec.internship.domain}</p>
                        ${rec.internship.location ? `<p class="location">📍 ${rec.internship.location}</p>` : ''}
                        ${rec.internship.stipend ? `<p class="stipend">💰 ${rec.internship.stipend}</p>` : ''}
                        <div class="required-skills">
                            ${rec.internship.required_skills.slice(0, 5).map(skill => `
                                <span class="skill-tag-sm">${skill}</span>
                            `).join('')}
                        </div>
                        <div class="matching-skills">
                            <strong>Your matching skills:</strong>
                            ${rec.matching_skills.map(skill => `
                                <span class="matching-skill">${skill}</span>
                            `).join('')}
                        </div>
                    </div>
                    <div class="recommendation-footer">
                        <button class="btn btn-primary apply-btn" data-internship-id="${rec.internship._id}">
                            Apply Now
                        </button>
                        <button class="btn btn-secondary view-details-btn" data-internship-id="${rec.internship._id}">
                            View Details
                        </button>
                    </div>
                </div>
            `).join('');
            
            // Add event listeners to apply buttons
            container.querySelectorAll('.apply-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const internshipId = e.target.dataset.internshipId;
                    this.applyToInternship(internshipId, e.target);
                });
            });
            
        } catch (error) {
            console.error('Error loading recommendations:', error);
            container.innerHTML = '<p class="error-state">Failed to load recommendations. Please try again.</p>';
        }
    },
    
    /**
     * Load applications
     */
    async loadApplications() {
        const container = document.getElementById('applications-list');
        const countBadge = document.getElementById('applications-count');
        
        try {
            this.applications = await API.getMyApplications();
            
            if (countBadge) {
                countBadge.textContent = this.applications.length;
            }
            
            // Update stat
            const statCard = document.getElementById('stat-applications');
            if (statCard) {
                const valueEl = statCard.querySelector('.stat-value');
                if (valueEl) valueEl.textContent = this.applications.length;
            }
            
            if (this.applications.length === 0) {
                container.innerHTML = '<p class="empty-state">No applications yet. Start applying to internships!</p>';
                return;
            }
            
            container.innerHTML = this.applications.map(app => `
                <div class="application-card">
                    <div class="application-header">
                        <h4>${app.internship.title}</h4>
                        <div class="application-actions">
                            <span class="status-badge status-${app.status}">${app.status}</span>
                            ${app.status === 'pending' || app.status === 'reviewing' ? `
                                <button class="btn-icon withdraw-btn" data-id="${app._id}" title="Withdraw">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                        <line x1="18" y1="6" x2="6" y2="18"/>
                                        <line x1="6" y1="6" x2="18" y2="18"/>
                                    </svg>
                                </button>
                            ` : ''}
                        </div>
                    </div>
                    <p class="company">${app.internship.company}</p>
                    <p class="applied-date">Applied: ${new Date(app.applied_at).toLocaleDateString()}</p>
                </div>
            `).join('');
            
            // Add withdraw event listeners
            container.querySelectorAll('.withdraw-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const appId = e.currentTarget.dataset.id;
                    if (confirm('Are you sure you want to withdraw this application?')) {
                        await this.withdrawApplication(appId);
                    }
                });
            });
            
        } catch (error) {
            console.error('Error loading applications:', error);
            container.innerHTML = '<p class="error-state">Failed to load applications.</p>';
        }
    },
    
    /**
     * Apply to internship
     */
    async applyToInternship(internshipId, button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<div class="loading-spinner"></div> Applying...';
        button.disabled = true;
        
        try {
            await API.applyToInternship(internshipId);
            button.innerHTML = '✓ Applied';
            button.classList.remove('btn-primary');
            button.classList.add('btn-success');
            
            // Reload applications
            await this.loadApplications();
            
        } catch (error) {
            console.error('Application error:', error);
            button.innerHTML = originalText;
            button.disabled = false;
            alert(error.message || 'Failed to apply. You may have already applied.');
        }
    },
    
    /**
     * Withdraw application
     */
    async withdrawApplication(applicationId) {
        try {
            await API.delete(`/api/applications/${applicationId}`);
            
            // Show success message
            alert('Application withdrawn successfully');
            
            // Reload applications
            await this.loadApplications();
            
        } catch (error) {
            console.error('Withdraw error:', error);
            alert(error.message || 'Failed to withdraw application');
        }
    },
    
    /**
     * Show profile modal (simplified)
     */
    showProfile() {
        alert(`Profile:

Name: ${this.currentUser.name}
Email: ${this.currentUser.email}
Branch: ${this.currentUser.branch || 'N/A'}
Semester: ${this.currentUser.semester || 'N/A'}
CGPA: ${this.currentUser.cgpa || 'N/A'}

Skills: ${this.currentUser.skills?.join(', ') || 'None'}`);
    }
};
