// ============================================
// COMPANY DASHBOARD MODULE
// ============================================

const CompanyDashboard = {
    currentUser: null,
    internships: [],
    
    /**
     * Initialize company dashboard
     */
    async init() {
        this.currentUser = Auth.getCurrentUser();
        if (!this.currentUser) {
            Auth.logout();
            return;
        }
        
        this.render();
        await this.loadInternships();
    },
    
    /**
     * Render dashboard structure
     */
    render() {
        const dashboard = document.getElementById('company-dashboard');
        dashboard.innerHTML = `
            <div class="dashboard-container">
                <!-- Header -->
                <div class="dashboard-header fade-in">
                    <div class="dashboard-title">
                        <h1>Company Dashboard</h1>
                        <p>Welcome, ${this.currentUser.name}</p>
                    </div>
                    <div class="dashboard-actions">
                        <button class="btn btn-primary" id="create-internship-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <line x1="12" y1="5" x2="12" y2="19"/>
                                <line x1="5" y1="12" x2="19" y2="12"/>
                            </svg>
                            Post Internship
                        </button>
                        <button class="btn btn-secondary" id="company-logout-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
                            </svg>
                            Logout
                        </button>
                    </div>
                </div>
                
                <!-- Stats -->
                <div class="stats-grid" id="company-stats">
                    <div class="stat-card">
                        <div class="stat-icon" style="color: var(--accent-cyan)">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="2" y="7" width="20" height="14" rx="2"/>
                                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                            </svg>
                        </div>
                        <div class="stat-content">
                            <div class="stat-value" id="total-internships">0</div>
                            <div class="stat-label">Posted Internships</div>
                        </div>
                    </div>
                </div>
                
                <!-- Internships List -->
                <div class="card scale-in">
                    <div class="card-header">
                        <h3 class="card-title">Your Internship Postings</h3>
                    </div>
                    <div id="internships-list" class="internships-container">
                        <div class="loading-container">
                            <div class="loading-spinner"></div>
                            <p>Loading internships...</p>
                        </div>
                    </div>
                </div>
                
                <!-- Create/Edit Modal -->
                <div id="internship-modal" class="modal">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3 id="modal-title">Post New Internship</h3>
                            <button class="modal-close" id="close-modal">&times;</button>
                        </div>
                        <form id="internship-form">
                            <div class="form-group">
                                <label>Title *</label>
                                <input type="text" id="internship-title" required>
                            </div>
                            <div class="form-group">
                                <label>Company *</label>
                                <input type="text" id="internship-company" required>
                            </div>
                            <div class="form-group">
                                <label>Domain *</label>
                                <input type="text" id="internship-domain" required placeholder="e.g., Software Development, Data Science">
                            </div>
                            <div class="form-group">
                                <label>Required Skills (comma-separated) *</label>
                                <input type="text" id="internship-skills" required placeholder="Python, Machine Learning, FastAPI">
                            </div>
                            <div class="form-group">
                                <label>Description *</label>
                                <textarea id="internship-description" rows="4" required></textarea>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Location</label>
                                    <input type="text" id="internship-location" placeholder="Remote / City">
                                </div>
                                <div class="form-group">
                                    <label>Duration</label>
                                    <input type="text" id="internship-duration" placeholder="3 months">
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Stipend</label>
                                <input type="text" id="internship-stipend" placeholder="₹10,000/month">
                            </div>
                            <button type="submit" class="btn btn-primary">
                                <span>Post Internship</span>
                            </button>
                        </form>
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
        const logoutBtn = document.getElementById('company-logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => Auth.logout());
        }
        
        const createBtn = document.getElementById('create-internship-btn');
        if (createBtn) {
            createBtn.addEventListener('click', () => this.showCreateModal());
        }
        
        const closeModal = document.getElementById('close-modal');
        if (closeModal) {
            closeModal.addEventListener('click', () => this.hideModal());
        }
        
        const form = document.getElementById('internship-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSubmit();
            });
        }
        
        // Close modal on outside click
        const modal = document.getElementById('internship-modal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.hideModal();
            });
        }
    },
    
    /**
     * Load internships
     */
    async loadInternships() {
        const container = document.getElementById('internships-list');
        if (!container) return;
        
        try {
            const allInternships = await API.getInternships();
            // Filter to show only internships posted by this user
            this.internships = allInternships.filter(i => i.posted_by === this.currentUser._id);
            
            // Update stats
            const totalEl = document.getElementById('total-internships');
            if (totalEl) totalEl.textContent = this.internships.length;
            
            if (this.internships.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="7" width="20" height="14" rx="2"/>
                            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                        </svg>
                        <p>No internships posted yet.</p>
                        <button class="btn btn-primary" onclick="CompanyDashboard.showCreateModal()">Post Your First Internship</button>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = this.internships.map(internship => `
                <div class="internship-card">
                    <div class="internship-header">
                        <h4>${internship.title}</h4>
                        <div class="internship-actions">
                            <button class="btn-icon edit-btn" data-id="${internship._id}" title="Edit">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                                </svg>
                            </button>
                            <button class="btn-icon delete-btn" data-id="${internship._id}" title="Delete">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                </svg>
                            </button>
                            <button class="btn-icon view-applicants-btn" data-id="${internship._id}" title="View Applicants">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                                    <circle cx="9" cy="7" r="4"/>
                                    <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="internship-body">
                        <p><strong>Company:</strong> ${internship.company}</p>
                        <p><strong>Domain:</strong> ${internship.domain}</p>
                        ${internship.location ? `<p><strong>Location:</strong> ${internship.location}</p>` : ''}
                        ${internship.duration ? `<p><strong>Duration:</strong> ${internship.duration}</p>` : ''}
                        ${internship.stipend ? `<p><strong>Stipend:</strong> ${internship.stipend}</p>` : ''}
                        <p class="description">${internship.description}</p>
                        <div class="skills-tags">
                            ${internship.required_skills.map(skill => `<span class="skill-tag-sm">${skill}</span>`).join('')}
                        </div>
                        <p class="posted-date">Posted: ${new Date(internship.created_at).toLocaleDateString()}</p>
                    </div>
                </div>
            `).join('');
            
            // Add event listeners
            container.querySelectorAll('.edit-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const id = e.currentTarget.dataset.id;
                    this.showEditModal(id);
                });
            });
            
            container.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.currentTarget.dataset.id;
                    if (confirm('Are you sure you want to delete this internship?')) {
                        await this.deleteInternship(id);
                    }
                });
            });
            
            container.querySelectorAll('.view-applicants-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const id = e.currentTarget.dataset.id;
                    this.viewApplicants(id);
                });
            });
            
        } catch (error) {
            console.error('Error loading internships:', error);
            container.innerHTML = '<p class="error-state">Failed to load internships.</p>';
        }
    },
    
    /**
     * Show create modal
     */
    showCreateModal() {
        this.currentEditId = null;
        document.getElementById('modal-title').textContent = 'Post New Internship';
        document.getElementById('internship-form').reset();
        document.getElementById('internship-modal').classList.add('active');
    },
    
    /**
     * Show edit modal
     */
    showEditModal(id) {
        const internship = this.internships.find(i => i._id === id);
        if (!internship) return;
        
        this.currentEditId = id;
        document.getElementById('modal-title').textContent = 'Edit Internship';
        document.getElementById('internship-title').value = internship.title;
        document.getElementById('internship-company').value = internship.company;
        document.getElementById('internship-domain').value = internship.domain;
        document.getElementById('internship-skills').value = internship.required_skills.join(', ');
        document.getElementById('internship-description').value = internship.description;
        document.getElementById('internship-location').value = internship.location || '';
        document.getElementById('internship-duration').value = internship.duration || '';
        document.getElementById('internship-stipend').value = internship.stipend || '';
        
        document.getElementById('internship-modal').classList.add('active');
    },
    
    /**
     * Hide modal
     */
    hideModal() {
        document.getElementById('internship-modal').classList.remove('active');
        this.currentEditId = null;
    },
    
    /**
     * Handle form submit
     */
    async handleSubmit() {
        const data = {
            title: document.getElementById('internship-title').value,
            company: document.getElementById('internship-company').value,
            domain: document.getElementById('internship-domain').value,
            required_skills: document.getElementById('internship-skills').value.split(',').map(s => s.trim()),
            description: document.getElementById('internship-description').value,
            location: document.getElementById('internship-location').value || null,
            duration: document.getElementById('internship-duration').value || null,
            stipend: document.getElementById('internship-stipend').value || null
        };
        
        try {
            if (this.currentEditId) {
                await API.updateInternship(this.currentEditId, data);
            } else {
                await API.createInternship(data);
            }
            
            this.hideModal();
            await this.loadInternships();
            
        } catch (error) {
            alert(error.message || 'Failed to save internship');
        }
    },
    
    /**
     * Delete internship
     */
    async deleteInternship(id) {
        try {
            await API.deleteInternship(id);
            await this.loadInternships();
        } catch (error) {
            alert(error.message || 'Failed to delete internship');
        }
    },
    
    /**
     * View applicants
     */
    async viewApplicants(id) {
        try {
            const applications = await API.getInternshipApplications(id);
            
            if (applications.length === 0) {
                alert('No applications yet for this internship.');
                return;
            }
            
            // Create modal to show applicants
            this.showApplicantsModal(applications, id);
            
        } catch (error) {
            alert('Failed to load applicants');
        }
    },
    
    /**
     * Show applicants modal
     */
    showApplicantsModal(applications, internshipId) {
        const modal = document.getElementById('internship-modal');
        const modalContent = modal.querySelector('.modal-content');
        
        modalContent.innerHTML = `
            <div class="modal-header">
                <h3>Applicants</h3>
                <button class="modal-close" onclick="CompanyDashboard.hideApplicantsModal()">&times;</button>
            </div>
            <div class="applicants-list">
                ${applications.map(app => `
                    <div class="applicant-card" data-app-id="${app._id}">
                        <div class="applicant-header">
                            <div class="applicant-info">
                                <h4>${app.student_name || 'Unknown'}</h4>
                                <p>${app.student_email || ''}</p>
                            </div>
                            <span class="status-badge status-${app.status}">${app.status}</span>
                        </div>
                        <div class="applicant-skills">
                            ${app.student_skills ? app.student_skills.slice(0, 5).map(skill => `
                                <span class="skill-tag-sm">${skill}</span>
                            `).join('') : ''}
                        </div>
                        <div class="applicant-actions" style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                            ${app.status === 'pending' || app.status === 'reviewing' ? `
                                <button class="btn btn-sm btn-success" onclick="CompanyDashboard.updateStatus('${app._id}', 'accepted')">
                                    ✓ Accept
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="CompanyDashboard.updateStatus('${app._id}', 'rejected')">
                                    × Reject
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="CompanyDashboard.updateStatus('${app._id}', 'reviewing')">
                                    👁 Review
                                </button>
                            ` : `
                                <p style="color: var(--text-secondary); font-size: 0.875rem;">Status: ${app.status}</p>
                            `}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        modal.classList.add('active');
    },
    
    /**
     * Hide applicants modal
     */
    hideApplicantsModal() {
        const modal = document.getElementById('internship-modal');
        modal.classList.remove('active');
        // Reload internships to get updated application counts
        this.loadInternships();
    },
    
    /**
     * Update application status
     */
    async updateStatus(applicationId, newStatus) {
        try {
            await API.put(`/api/applications/${applicationId}/status/${newStatus}`, {});
            
            alert(`Application ${newStatus} successfully!`);
            
            // Update the UI immediately
            const card = document.querySelector(`[data-app-id="${applicationId}"]`);
            if (card) {
                const statusBadge = card.querySelector('.status-badge');
                if (statusBadge) {
                    statusBadge.className = `status-badge status-${newStatus}`;
                    statusBadge.textContent = newStatus;
                }
                
                // Hide action buttons
                const actions = card.querySelector('.applicant-actions');
                if (actions) {
                    actions.innerHTML = `<p style="color: var(--text-secondary); font-size: 0.875rem;">Status: ${newStatus}</p>`;
                }
            }
            
        } catch (error) {
            console.error('Status update error:', error);
            alert(error.message || 'Failed to update status');
        }
    }
};
