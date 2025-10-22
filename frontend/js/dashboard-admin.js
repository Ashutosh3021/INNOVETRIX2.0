// ============================================
// ADMIN DASHBOARD MODULE
// ============================================

const AdminDashboard = {
    currentUser: null,
    analytics: null,
    filters: {
        branch: 'all',
        semester: 'all',
        placementStatus: 'all'
    },
    
    /**
     * Initialize admin dashboard
     */
    async init() {
        this.currentUser = Auth.getCurrentUser();
        if (!this.currentUser) {
            Auth.logout();
            return;
        }
        
        this.render();
        await this.loadAnalytics();
    },
    
    /**
     * Render dashboard structure
     */
    render() {
        const dashboard = document.getElementById('admin-dashboard');
        dashboard.innerHTML = `
            <div class="dashboard-container">
                <!-- Header -->
                <div class="dashboard-header fade-in">
                    <div class="dashboard-title">
                        <h1>Admin Dashboard</h1>
                        <p>School Analytics & Management</p>
                    </div>
                    <div class="dashboard-actions">
                        <button class="btn btn-secondary" id="refresh-analytics-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
                            </svg>
                            Refresh
                        </button>
                        <button class="btn btn-secondary" id="admin-logout-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
                            </svg>
                            Logout
                        </button>
                    </div>
                </div>
                
                <!-- Filters Section -->
                <div class="filters-section fade-in">
                    <div class="filter-group">
                        <label>Branch:</label>
                        <select id="filter-branch" class="filter-select">
                            <option value="all">All Branches</option>
                            <option value="CSE">CSE</option>
                            <option value="ECE">ECE</option>
                            <option value="ME">ME</option>
                            <option value="EE">EE</option>
                            <option value="CE">CE</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Semester:</label>
                        <select id="filter-semester" class="filter-select">
                            <option value="all">All Semesters</option>
                            <option value="1">Semester 1</option>
                            <option value="2">Semester 2</option>
                            <option value="3">Semester 3</option>
                            <option value="4">Semester 4</option>
                            <option value="5">Semester 5</option>
                            <option value="6">Semester 6</option>
                            <option value="7">Semester 7</option>
                            <option value="8">Semester 8</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Placement Status:</label>
                        <select id="filter-placement" class="filter-select">
                            <option value="all">All Status</option>
                            <option value="placed">Placed</option>
                            <option value="searching">Searching</option>
                            <option value="not_placed">Not Placed</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" id="apply-filters-btn">Apply Filters</button>
                    <button class="btn btn-secondary" id="reset-filters-btn">Reset</button>
                </div>
                
                <!-- Overview Stats -->
                <div class="stats-grid" id="overview-stats">
                    <div class="loading-container">
                        <div class="loading-spinner"></div>
                    </div>
                </div>
                
                <!-- Charts Section -->
                <div class="dashboard-content">
                    <!-- Placement Tracking Charts -->
                    <div class="card slide-in-left">
                        <div class="card-header">
                            <h3 class="card-title">Placement Overview</h3>
                        </div>
                        <div id="placement-overview" class="chart-container"></div>
                    </div>
                    
                    <!-- Placement Type Distribution -->
                    <div class="card slide-in-right">
                        <div class="card-header">
                            <h3 class="card-title">Placement Type Distribution</h3>
                        </div>
                        <div id="placement-type-chart" class="chart-container"></div>
                    </div>
                    
                    <!-- Salary Statistics -->
                    <div class="card scale-in">
                        <div class="card-header">
                            <h3 class="card-title">Salary Statistics by Type</h3>
                        </div>
                        <div id="salary-stats" class="stats-details"></div>
                    </div>
                    
                    <!-- Company Hiring Stats -->
                    <div class="card scale-in">
                        <div class="card-header">
                            <h3 class="card-title">Company Hiring Statistics</h3>
                            <button class="btn btn-sm btn-secondary" id="sort-companies-btn">Sort by Hired</button>
                        </div>
                        <div id="company-hiring-stats" class="table-container"></div>
                    </div>
                    
                    <!-- Unplaced Students List -->
                    <div class="card slide-in-left">
                        <div class="card-header">
                            <h3 class="card-title">Unplaced Students</h3>
                            <button class="btn btn-sm btn-primary" id="export-unplaced-btn">Export CSV</button>
                        </div>
                        <div id="unplaced-students-list" class="students-list"></div>
                    </div>
                    
                    <!-- Students by Branch Chart -->
                    <div class="card slide-in-left">
                        <div class="card-header">
                            <h3 class="card-title">Students by Branch</h3>
                        </div>
                        <div id="students-by-branch-chart" class="chart-container"></div>
                    </div>
                    
                    <!-- Students by Semester Chart -->
                    <div class="card slide-in-right">
                        <div class="card-header">
                            <h3 class="card-title">Students by Semester</h3>
                        </div>
                        <div id="students-by-semester-chart" class="chart-container"></div>
                    </div>
                    
                    <!-- Top Students -->
                    <div class="card scale-in">
                        <div class="card-header">
                            <h3 class="card-title">Top Performing Students</h3>
                        </div>
                        <div id="top-students-list" class="students-list"></div>
                    </div>
                    
                    <!-- Internship Analytics -->
                    <div class="card scale-in">
                        <div class="card-header">
                            <h3 class="card-title">Internships by Domain</h3>
                        </div>
                        <div id="internships-chart" class="chart-container"></div>
                    </div>
                    
                    <!-- Application Status -->
                    <div class="card slide-in-left">
                        <div class="card-header">
                            <h3 class="card-title">Application Statistics</h3>
                        </div>
                        <div id="application-stats" class="stats-details"></div>
                    </div>
                    
                    <!-- All Students Management -->
                    <div class="card slide-in-right">
                        <div class="card-header">
                            <h3 class="card-title">Student Management</h3>
                        </div>
                        <div id="all-students-list" class="management-list"></div>
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
        const logoutBtn = document.getElementById('admin-logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => Auth.logout());
        }
        
        const refreshBtn = document.getElementById('refresh-analytics-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadAnalytics());
        }
        
        // Filter event listeners
        const applyFiltersBtn = document.getElementById('apply-filters-btn');
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', () => this.applyFilters());
        }
        
        const resetFiltersBtn = document.getElementById('reset-filters-btn');
        if (resetFiltersBtn) {
            resetFiltersBtn.addEventListener('click', () => this.resetFilters());
        }
        
        const exportUnplacedBtn = document.getElementById('export-unplaced-btn');
        if (exportUnplacedBtn) {
            exportUnplacedBtn.addEventListener('click', () => this.exportUnplacedStudents());
        }
        
        const sortCompaniesBtn = document.getElementById('sort-companies-btn');
        if (sortCompaniesBtn) {
            sortCompaniesBtn.addEventListener('click', () => this.toggleCompanySort());
        }
    },
    
    /**
     * Load all analytics
     */
    async loadAnalytics() {
        await Promise.all([
            this.loadOverview(),
            this.loadPlacementAnalytics(),
            this.loadCompanyHiringStats(),
            this.loadUnplacedStudents(),
            this.loadStudentsByBranch(),
            this.loadStudentsBySemester(),
            this.loadTopStudents(),
            this.loadInternshipAnalytics(),
            this.loadApplicationStats(),
            this.loadAllStudents()
        ]);
    },
    
    /**
     * Load overview statistics
     */
    async loadOverview() {
        const container = document.getElementById('overview-stats');
        if (!container) return;
        
        try {
            const overview = await API.getAdminOverview();
            
            const stats = [
                {
                    icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
                    label: 'Total Students',
                    value: overview.total_students,
                    color: 'var(--accent-cyan)'
                },
                {
                    icon: '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
                    label: 'Companies',
                    value: overview.total_companies,
                    color: 'var(--accent-pink)'
                },
                {
                    icon: '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
                    label: 'Internships',
                    value: overview.total_internships,
                    color: 'var(--accent-purple)'
                },
                {
                    icon: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
                    label: 'Applications',
                    value: overview.total_applications,
                    color: 'var(--accent-green)'
                }
            ];
            
            container.innerHTML = stats.map(stat => `
                <div class="stat-card">
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
            
            Animations.staggerChildren(container, 100);
            
        } catch (error) {
            console.error('Error loading overview:', error);
            container.innerHTML = '<p class="error-state">Failed to load overview</p>';
        }
    },
    
    /**
     * Load students by branch
     */
    async loadStudentsByBranch() {
        const container = document.getElementById('students-by-branch-chart');
        if (!container) return;
        
        try {
            const data = await API.getStudentsByBranch();
            this.renderBarChart(container, data, 'branch', 'count', 'Students');
        } catch (error) {
            console.error('Error loading students by branch:', error);
            container.innerHTML = '<p class="error-state">Failed to load data</p>';
        }
    },
    
    /**
     * Load students by semester
     */
    async loadStudentsBySemester() {
        const container = document.getElementById('students-by-semester-chart');
        if (!container) return;
        
        try {
            const data = await API.getStudentsBySemester();
            this.renderBarChart(container, data, 'semester', 'count', 'Students');
        } catch (error) {
            console.error('Error loading students by semester:', error);
            container.innerHTML = '<p class="error-state">Failed to load data</p>';
        }
    },
    
    /**
     * Load top students
     */
    async loadTopStudents() {
        const container = document.getElementById('top-students-list');
        if (!container) return;
        
        try {
            const students = await API.getTopStudents(10);
            
            container.innerHTML = students.map((student, index) => `
                <div class="student-item">
                    <div class="rank">#${index + 1}</div>
                    <div class="student-info">
                        <h4>${student.name}</h4>
                        <p>${student.email}</p>
                        <p class="branch-sem">${student.branch || 'N/A'} | Semester ${student.semester || 'N/A'}</p>
                    </div>
                    <div class="cgpa-badge">
                        ${student.cgpa ? student.cgpa.toFixed(2) : 'N/A'}
                    </div>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Error loading top students:', error);
            container.innerHTML = '<p class="error-state">Failed to load data</p>';
        }
    },
    
    /**
     * Load internship analytics
     */
    async loadInternshipAnalytics() {
        const container = document.getElementById('internships-chart');
        if (!container) return;
        
        try {
            const data = await API.getInternshipAnalytics();
            this.renderBarChart(container, data, 'domain', 'count', 'Internships');
        } catch (error) {
            console.error('Error loading internship analytics:', error);
            container.innerHTML = '<p class="error-state">Failed to load data</p>';
        }
    },
    
    /**
     * Load application statistics
     */
    async loadApplicationStats() {
        const container = document.getElementById('application-stats');
        if (!container) return;
        
        try {
            const stats = await API.getApplicationAnalytics();
            
            container.innerHTML = `
                <div class="stat-detail-grid">
                    <div class="stat-detail">
                        <span class="label">Total Applications:</span>
                        <span class="value">${stats.total}</span>
                    </div>
                    <div class="stat-detail">
                        <span class="label">Pending:</span>
                        <span class="value status-pending">${stats.by_status?.pending || 0}</span>
                    </div>
                    <div class="stat-detail">
                        <span class="label">Reviewed:</span>
                        <span class="value status-reviewed">${stats.by_status?.reviewed || 0}</span>
                    </div>
                    <div class="stat-detail">
                        <span class="label">Accepted:</span>
                        <span class="value status-accepted">${stats.by_status?.accepted || 0}</span>
                    </div>
                    <div class="stat-detail">
                        <span class="label">Rejected:</span>
                        <span class="value status-rejected">${stats.by_status?.rejected || 0}</span>
                    </div>
                </div>
            `;
            
        } catch (error) {
            console.error('Error loading application stats:', error);
            container.innerHTML = '<p class="error-state">Failed to load data</p>';
        }
    },
    
    /**
     * Load all students for management
     */
    async loadAllStudents() {
        const container = document.getElementById('all-students-list');
        if (!container) return;
        
        try {
            const students = await API.getAllStudents(0, 50);
            
            container.innerHTML = students.map(student => `
                <div class="management-item">
                    <div class="student-info">
                        <h4>${student.name}</h4>
                        <p>${student.email}</p>
                        <p class="branch-sem">${student.branch || 'N/A'} | Sem ${student.semester || 'N/A'} | CGPA: ${student.cgpa?.toFixed(2) || 'N/A'}</p>
                    </div>
                    <div class="management-actions">
                        ${student.is_blocked 
                            ? `<button class="btn btn-sm btn-success unblock-btn" data-id="${student._id}">Unblock</button>`
                            : `<button class="btn btn-sm btn-danger block-btn" data-id="${student._id}">Block</button>`
                        }
                    </div>
                </div>
            `).join('');
            
            // Add event listeners
            container.querySelectorAll('.block-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.dataset.id;
                    if (confirm('Block this student?')) {
                        await this.blockStudent(id);
                    }
                });
            });
            
            container.querySelectorAll('.unblock-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.dataset.id;
                    await this.unblockStudent(id);
                });
            });
            
        } catch (error) {
            console.error('Error loading students:', error);
            container.innerHTML = '<p class="error-state">Failed to load data</p>';
        }
    },
    
    /**
     * Render simple bar chart
     */
    renderBarChart(container, data, labelKey, valueKey, label) {
        if (!data || data.length === 0) {
            container.innerHTML = '<p class="empty-state">No data available</p>';
            return;
        }
        
        const maxValue = Math.max(...data.map(item => item[valueKey]));
        
        container.innerHTML = data.map(item => {
            const percentage = (item[valueKey] / maxValue) * 100;
            return `
                <div class="chart-bar-item">
                    <div class="bar-label">${item[labelKey] || 'Unknown'}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: ${percentage}%"></div>
                    </div>
                    <div class="bar-value">${item[valueKey]}</div>
                </div>
            `;
        }).join('');
        
        // Animate bars
        setTimeout(() => {
            container.querySelectorAll('.bar-fill').forEach(bar => {
                bar.style.transition = 'width 1s ease-out';
            });
        }, 100);
    },
    
    /**
     * Block student
     */
    async blockStudent(studentId) {
        try {
            await API.blockStudent(studentId);
            await this.loadAllStudents();
        } catch (error) {
            alert('Failed to block student');
        }
    },
    
    /**
     * Unblock student
     */
    async unblockStudent(studentId) {
        try {
            await API.unblockStudent(studentId);
            await this.loadAllStudents();
        } catch (error) {
            alert('Failed to unblock student');
        }
    },
    
    /**
     * Load placement analytics
     */
    async loadPlacementAnalytics() {
        const overviewContainer = document.getElementById('placement-overview');
        const typeContainer = document.getElementById('placement-type-chart');
        const salaryContainer = document.getElementById('salary-stats');
        
        if (!overviewContainer || !typeContainer || !salaryContainer) return;
        
        try {
            const data = await API.getPlacementAnalytics();
            
            // Render placement overview
            overviewContainer.innerHTML = `
                <div class="placement-stats-grid">
                    <div class="placement-stat">
                        <div class="stat-value" style="color: var(--accent-green);">${data.placed_students}</div>
                        <div class="stat-label">Placed</div>
                    </div>
                    <div class="placement-stat">
                        <div class="stat-value" style="color: var(--accent-cyan);">${data.searching_students}</div>
                        <div class="stat-label">Searching</div>
                    </div>
                    <div class="placement-stat">
                        <div class="stat-value" style="color: var(--accent-orange);">${data.not_placed_students}</div>
                        <div class="stat-label">Not Placed</div>
                    </div>
                    <div class="placement-stat">
                        <div class="stat-value" style="color: var(--primary);">${data.placement_rate}%</div>
                        <div class="stat-label">Placement Rate</div>
                    </div>
                </div>
                <div class="placement-bar" style="margin-top: 1.5rem;">
                    <div class="bar-segment" style="width: ${(data.placed_students/data.total_students*100)}%; background: var(--accent-green);"></div>
                    <div class="bar-segment" style="width: ${(data.searching_students/data.total_students*100)}%; background: var(--accent-cyan);"></div>
                    <div class="bar-segment" style="width: ${(data.not_placed_students/data.total_students*100)}%; background: var(--accent-orange);"></div>
                </div>
            `;
            
            // Render placement type distribution
            if (data.placement_types && data.placement_types.length > 0) {
                this.renderBarChart(typeContainer, data.placement_types, 'type', 'count', 'Students');
            } else {
                typeContainer.innerHTML = '<p class="empty-state">No placement type data available</p>';
            }
            
            // Render salary statistics
            if (data.salary_statistics && data.salary_statistics.length > 0) {
                salaryContainer.innerHTML = `
                    <div class="salary-stats-grid">
                        ${data.salary_statistics.map(stat => `
                            <div class="salary-stat-card">
                                <h4>${stat.type || 'Unknown'}</h4>
                                <div class="salary-details">
                                    <div class="salary-item">
                                        <span class="label">Average:</span>
                                        <span class="value">₹${stat.avg_salary} LPA</span>
                                    </div>
                                    <div class="salary-item">
                                        <span class="label">Min:</span>
                                        <span class="value">₹${stat.min_salary} LPA</span>
                                    </div>
                                    <div class="salary-item">
                                        <span class="label">Max:</span>
                                        <span class="value">₹${stat.max_salary} LPA</span>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
            } else {
                salaryContainer.innerHTML = '<p class="empty-state">No salary data available</p>';
            }
            
        } catch (error) {
            console.error('Error loading placement analytics:', error);
            overviewContainer.innerHTML = '<p class="error-state">Failed to load placement data</p>';
            typeContainer.innerHTML = '<p class="error-state">Failed to load placement types</p>';
            salaryContainer.innerHTML = '<p class="error-state">Failed to load salary data</p>';
        }
    },
    
    /**
     * Load company hiring stats
     */
    async loadCompanyHiringStats() {
        const container = document.getElementById('company-hiring-stats');
        if (!container) return;
        
        try {
            const data = await API.getCompanyHiringStats();
            
            if (!data || data.length === 0) {
                container.innerHTML = '<p class="empty-state">No company hiring data available</p>';
                return;
            }
            
            container.innerHTML = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Students Hired</th>
                            <th>Avg Salary (LPA)</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(company => `
                            <tr>
                                <td><strong>${company.company || 'Unknown'}</strong></td>
                                <td><span class="badge">${company.students_hired}</span></td>
                                <td>₹${company.avg_salary_offered ? company.avg_salary_offered.toFixed(2) : 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            
        } catch (error) {
            console.error('Error loading company hiring stats:', error);
            container.innerHTML = '<p class="error-state">Failed to load company hiring data</p>';
        }
    },
    
    /**
     * Load unplaced students
     */
    async loadUnplacedStudents() {
        const container = document.getElementById('unplaced-students-list');
        if (!container) return;
        
        try {
            const students = await API.getUnplacedStudents();
            
            if (!students || students.length === 0) {
                container.innerHTML = '<p class="empty-state">No unplaced students found</p>';
                return;
            }
            
            container.innerHTML = students.map((student, index) => `
                <div class="student-item">
                    <div class="rank">#${index + 1}</div>
                    <div class="student-info">
                        <h4>${student.name}</h4>
                        <p>${student.email}</p>
                        <p class="branch-sem">${student.branch || 'N/A'} | Semester ${student.semester || 'N/A'}</p>
                        ${student.skills && student.skills.length > 0 ? 
                            `<div class="skills-tags" style="margin-top: 0.5rem;">
                                ${student.skills.slice(0, 3).map(skill => 
                                    `<span class="skill-tag-sm">${skill}</span>`
                                ).join('')}
                                ${student.skills.length > 3 ? `<span class="skill-tag-sm">+${student.skills.length - 3} more</span>` : ''}
                            </div>` : ''
                        }
                    </div>
                    <div class="cgpa-badge">
                        ${student.cgpa ? student.cgpa.toFixed(2) : 'N/A'}
                    </div>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Error loading unplaced students:', error);
            container.innerHTML = '<p class="error-state">Failed to load unplaced students</p>';
        }
    },
    
    /**
     * Apply filters
     */
    applyFilters() {
        this.filters.branch = document.getElementById('filter-branch').value;
        this.filters.semester = document.getElementById('filter-semester').value;
        this.filters.placementStatus = document.getElementById('filter-placement').value;
        
        this.loadFilteredStudents();
    },
    
    /**
     * Reset filters
     */
    resetFilters() {
        this.filters = {
            branch: 'all',
            semester: 'all',
            placementStatus: 'all'
        };
        
        document.getElementById('filter-branch').value = 'all';
        document.getElementById('filter-semester').value = 'all';
        document.getElementById('filter-placement').value = 'all';
        
        this.loadAllStudents();
    },
    
    /**
     * Load filtered students
     */
    async loadFilteredStudents() {
        const container = document.getElementById('all-students-list');
        if (!container) return;
        
        try {
            const allStudents = await API.getAllStudents(0, 200);
            
            // Apply filters
            let filteredStudents = allStudents.filter(student => {
                if (this.filters.branch !== 'all' && student.branch !== this.filters.branch) {
                    return false;
                }
                if (this.filters.semester !== 'all' && student.semester !== parseInt(this.filters.semester)) {
                    return false;
                }
                if (this.filters.placementStatus !== 'all') {
                    const status = student.placement_status || 'not_placed';
                    if (status !== this.filters.placementStatus) {
                        return false;
                    }
                }
                return true;
            });
            
            if (filteredStudents.length === 0) {
                container.innerHTML = '<p class="empty-state">No students match the selected filters</p>';
                return;
            }
            
            container.innerHTML = filteredStudents.map(student => `
                <div class="management-item">
                    <div class="student-info">
                        <h4>${student.name}</h4>
                        <p>${student.email}</p>
                        <p class="branch-sem">${student.branch || 'N/A'} | Sem ${student.semester || 'N/A'} | CGPA: ${student.cgpa?.toFixed(2) || 'N/A'}</p>
                        ${student.placement_status ? `<span class="badge" style="background: ${student.placement_status === 'placed' ? 'var(--success)' : student.placement_status === 'searching' ? 'var(--accent-cyan)' : 'var(--accent-orange)'}">${student.placement_status}</span>` : ''}
                    </div>
                    <div class="management-actions">
                        ${student.is_blocked 
                            ? `<button class="btn btn-sm btn-success unblock-btn" data-id="${student.id}">Unblock</button>`
                            : `<button class="btn btn-sm btn-danger block-btn" data-id="${student.id}">Block</button>`
                        }
                    </div>
                </div>
            `).join('');
            
            // Add event listeners
            container.querySelectorAll('.block-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.dataset.id;
                    if (confirm('Block this student?')) {
                        await this.blockStudent(id);
                    }
                });
            });
            
            container.querySelectorAll('.unblock-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.dataset.id;
                    await this.unblockStudent(id);
                });
            });
            
        } catch (error) {
            console.error('Error loading filtered students:', error);
            container.innerHTML = '<p class="error-state">Failed to load students</p>';
        }
    },
    
    /**
     * Toggle company sorting
     */
    companySortDescending: true,
    
    async toggleCompanySort() {
        this.companySortDescending = !this.companySortDescending;
        const container = document.getElementById('company-hiring-stats');
        
        try {
            const data = await API.getCompanyHiringStats();
            const sorted = [...data].sort((a, b) => {
                return this.companySortDescending 
                    ? b.students_hired - a.students_hired
                    : a.students_hired - b.students_hired;
            });
            
            container.innerHTML = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Students Hired ${this.companySortDescending ? '↓' : '↑'}</th>
                            <th>Avg Salary (LPA)</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${sorted.map(company => `
                            <tr>
                                <td><strong>${company.company || 'Unknown'}</strong></td>
                                <td><span class="badge">${company.students_hired}</span></td>
                                <td>₹${company.avg_salary_offered ? company.avg_salary_offered.toFixed(2) : 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } catch (error) {
            console.error('Error sorting companies:', error);
        }
    },
    
    /**
     * Export unplaced students to CSV
     */
    async exportUnplacedStudents() {
        try {
            const students = await API.getUnplacedStudents();
            
            if (!students || students.length === 0) {
                alert('No unplaced students to export');
                return;
            }
            
            // Create CSV content
            const headers = ['Name', 'Email', 'Branch', 'Semester', 'CGPA', 'Skills'];
            const csvContent = [
                headers.join(','),
                ...students.map(student => [
                    `"${student.name}"`,
                    student.email,
                    student.branch || 'N/A',
                    student.semester || 'N/A',
                    student.cgpa || 'N/A',
                    `"${student.skills ? student.skills.join('; ') : 'N/A'}"`
                ].join(','))
            ].join('\n');
            
            // Create download link
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `unplaced_students_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
        } catch (error) {
            console.error('Error exporting unplaced students:', error);
            alert('Failed to export data');
        }
    }
};
