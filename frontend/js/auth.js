// ============================================
// AUTHENTICATION MODULE
// ============================================

const Auth = {
    selectedRole: CONFIG.ROLES.STUDENT,
    
    /**
     * Initialize auth module
     */
    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
    },
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Role selection on landing page
        document.querySelectorAll('.role-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const role = e.currentTarget.dataset.role;
                this.selectRole(role);
            });
        });
        
        // Back to landing
        const backButton = document.getElementById('back-to-landing');
        if (backButton) {
            backButton.addEventListener('click', () => {
                this.showPage('landing-page');
            });
        }
        
        // Form toggles
        const showRegister = document.getElementById('show-register');
        const showLogin = document.getElementById('show-login');
        
        if (showRegister) {
            showRegister.addEventListener('click', (e) => {
                e.preventDefault();
                this.showRegisterForm();
            });
        }
        
        if (showLogin) {
            showLogin.addEventListener('click', (e) => {
                e.preventDefault();
                this.showLoginForm();
            });
        }
        
        // Handle all show-login links (including from wizard)
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('show-login-link')) {
                e.preventDefault();
                this.showLoginForm();
            }
        });
        
        // Form submissions
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }
        
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister();
            });
        }
        
        // Resume upload for OCR
        const resumeUpload = document.getElementById('resume-upload');
        if (resumeUpload) {
            resumeUpload.addEventListener('change', (e) => {
                OCR.handleResumeUpload(e);
            });
        }
    },
    
    /**
     * Select role and navigate to auth page
     */
    selectRole(role) {
        this.selectedRole = role;
        
        // Update role indicator
        const roleDisplay = document.getElementById('selected-role-display');
        if (roleDisplay) {
            roleDisplay.textContent = role.charAt(0).toUpperCase() + role.slice(1);
        }
        
        // Show/hide student-specific fields
        const studentFields = document.getElementById('student-fields');
        if (studentFields) {
            if (role === CONFIG.ROLES.STUDENT) {
                studentFields.classList.add('active');
            } else {
                studentFields.classList.remove('active');
            }
        }
        
        // Navigate to auth page
        this.showPage('auth-page');
        this.showLoginForm();
    },
    
    /**
     * Show specific page
     */
    showPage(pageId) {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.classList.add('active');
        }
    },
    
    /**
     * Show login form
     */
    showLoginForm() {
        document.getElementById('login-form').classList.add('active');
        document.getElementById('register-form').classList.remove('active');
        const wizardForm = document.getElementById('wizard-form');
        if (wizardForm) {
            wizardForm.classList.remove('active');
            wizardForm.style.display = 'none';
        }
        document.getElementById('auth-title').textContent = 'Welcome Back';
        document.getElementById('auth-subtitle').textContent = 'Sign in to continue';
        this.hideError();
    },
    
    /**
     * Show register form
     */
    showRegisterForm() {
        document.getElementById('login-form').classList.remove('active');
        document.getElementById('auth-title').textContent = 'Create Account';
        document.getElementById('auth-subtitle').textContent = 'Join SkillMatchAI today';
        this.hideError();
        
        // For students, show wizard; for others, show simple form
        if (this.selectedRole === CONFIG.ROLES.STUDENT) {
            document.getElementById('register-form').classList.remove('active');
            const wizardForm = document.getElementById('wizard-form');
            if (wizardForm) {
                wizardForm.classList.add('active');
                wizardForm.style.display = 'block';
                // Initialize wizard
                Wizard.init();
            }
        } else {
            document.getElementById('register-form').classList.add('active');
            const wizardForm = document.getElementById('wizard-form');
            if (wizardForm) {
                wizardForm.classList.remove('active');
                wizardForm.style.display = 'none';
            }
        }
    },
    
    /**
     * Handle login
     */
    async handleLogin() {
        const usernameOrEmail = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const submitButton = document.querySelector('#login-form .submit-button');
        
        this.setLoading(submitButton, true);
        this.hideError();
        
        try {
            const response = await API.login({ username_or_email: usernameOrEmail, password });
            
            // Store auth data
            localStorage.setItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN, response.access_token);
            localStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_USER, JSON.stringify(response.user));
            localStorage.setItem(CONFIG.STORAGE_KEYS.USER_ROLE, response.user.role);
            
            // Navigate to appropriate dashboard
            this.navigateToDashboard(response.user.role);
            
        } catch (error) {
            this.showError(error.message || 'Login failed. Please check your credentials.');
        } finally {
            this.setLoading(submitButton, false);
        }
    },
    
    /**
     * Handle registration
     */
    async handleRegister() {
        const name = document.getElementById('register-name').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const submitButton = document.querySelector('#register-form .submit-button');
        
        this.setLoading(submitButton, true);
        this.hideError();
        
        try {
            const userData = {
                name,
                email,
                password,
                role: this.selectedRole
            };
            
            // Add student-specific fields
            if (this.selectedRole === CONFIG.ROLES.STUDENT) {
                const branch = document.getElementById('register-branch').value;
                const semester = document.getElementById('register-semester').value;
                const cgpa = document.getElementById('register-cgpa').value;
                const skillsInput = document.getElementById('register-skills').value;
                const projectsInput = document.getElementById('register-projects').value;
                
                userData.branch = branch || null;
                userData.semester = semester ? parseInt(semester) : null;
                userData.cgpa = cgpa ? parseFloat(cgpa) : null;
                userData.skills = skillsInput ? skillsInput.split(',').map(s => s.trim()) : [];
                userData.projects = projectsInput ? projectsInput.split(',').map(p => p.trim()) : [];
            } else {
                userData.skills = [];
                userData.projects = [];
            }
            
            const response = await API.register(userData);
            
            // Store auth data
            localStorage.setItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN, response.access_token);
            localStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_USER, JSON.stringify(response.user));
            localStorage.setItem(CONFIG.STORAGE_KEYS.USER_ROLE, response.user.role);
            
            // Navigate to appropriate dashboard
            this.navigateToDashboard(response.user.role);
            
        } catch (error) {
            this.showError(error.message || 'Registration failed. Please try again.');
        } finally {
            this.setLoading(submitButton, false);
        }
    },
    
    /**
     * Navigate to role-specific dashboard
     */
    navigateToDashboard(role) {
        const dashboardMap = {
            [CONFIG.ROLES.STUDENT]: 'student-dashboard',
            [CONFIG.ROLES.COMPANY]: 'company-dashboard',
            [CONFIG.ROLES.ADMIN]: 'admin-dashboard'
        };
        
        const dashboardId = dashboardMap[role];
        if (dashboardId) {
            this.showPage(dashboardId);
            
            // Trigger dashboard load
            if (role === CONFIG.ROLES.STUDENT) {
                StudentDashboard.init();
            } else if (role === CONFIG.ROLES.COMPANY) {
                CompanyDashboard.init();
            } else if (role === CONFIG.ROLES.ADMIN) {
                AdminDashboard.init();
            }
        }
    },
    
    /**
     * Check authentication status
     */
    checkAuthStatus() {
        const token = localStorage.getItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN);
        const role = localStorage.getItem(CONFIG.STORAGE_KEYS.USER_ROLE);
        
        if (token && role) {
            // User is authenticated, navigate to dashboard
            this.navigateToDashboard(role);
        } else {
            // Show landing page
            this.showPage('landing-page');
        }
    },
    
    /**
     * Logout
     */
    logout() {
        localStorage.removeItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.CURRENT_USER);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.USER_ROLE);
        
        this.showPage('landing-page');
    },
    
    /**
     * Get current user
     */
    getCurrentUser() {
        const userJson = localStorage.getItem(CONFIG.STORAGE_KEYS.CURRENT_USER);
        return userJson ? JSON.parse(userJson) : null;
    },
    
    /**
     * Show error message
     */
    showError(message) {
        const errorElement = document.getElementById('auth-error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }
    },
    
    /**
     * Hide error message
     */
    hideError() {
        const errorElement = document.getElementById('auth-error');
        if (errorElement) {
            errorElement.classList.remove('show');
        }
    },
    
    /**
     * Set loading state
     */
    setLoading(button, isLoading) {
        if (isLoading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }
};
