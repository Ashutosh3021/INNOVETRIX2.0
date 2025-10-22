// ============================================
// MULTI-STEP WIZARD MODULE
// ============================================

const Wizard = {
    currentStep: 1,
    totalSteps: 5,
    formData: {},
    
    /**
     * Initialize wizard
     */
    init() {
        this.currentStep = 1;
        this.formData = {};
        this.showStep(1);
        this.setupEventListeners();
    },
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Navigation buttons
        const prevBtn = document.getElementById('wizard-prev');
        const nextBtn = document.getElementById('wizard-next');
        const submitBtn = document.getElementById('wizard-submit');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousStep());
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextStep());
        }
        
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitForm());
        }
        
        // Tags input for skills, certifications, languages
        this.setupTagsInput('wizard-skills-input', 'wizard-skills-container');
        this.setupTagsInput('wizard-certifications-input', 'wizard-certifications-container');
        this.setupTagsInput('wizard-languages-input', 'wizard-languages-container');
        this.setupTagsInput('wizard-projects-input', 'wizard-projects-container');
    },
    
    /**
     * Show specific step
     */
    showStep(stepNumber) {
        this.currentStep = stepNumber;
        
        // Hide all panels
        document.querySelectorAll('.wizard-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        
        // Show current panel
        const currentPanel = document.getElementById(`wizard-step-${stepNumber}`);
        if (currentPanel) {
            currentPanel.classList.add('active');
        }
        
        // Update step indicators
        document.querySelectorAll('.wizard-step').forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index + 1 < stepNumber) {
                step.classList.add('completed');
            } else if (index + 1 === stepNumber) {
                step.classList.add('active');
            }
        });
        
        // Update navigation buttons
        this.updateNavigation();
    },
    
    /**
     * Update navigation button states
     */
    updateNavigation() {
        const prevBtn = document.getElementById('wizard-prev');
        const nextBtn = document.getElementById('wizard-next');
        const submitBtn = document.getElementById('wizard-submit');
        
        if (prevBtn) {
            prevBtn.disabled = this.currentStep === 1;
        }
        
        if (nextBtn && submitBtn) {
            if (this.currentStep === this.totalSteps) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'flex';
            } else {
                nextBtn.style.display = 'flex';
                submitBtn.style.display = 'none';
            }
        }
    },
    
    /**
     * Go to next step
     */
    async nextStep() {
        // Validate current step
        if (!this.validateStep(this.currentStep)) {
            return;
        }
        
        // Save current step data
        this.saveStepData(this.currentStep);
        
        // Move to next step
        if (this.currentStep < this.totalSteps) {
            this.showStep(this.currentStep + 1);
        }
    },
    
    /**
     * Go to previous step
     */
    previousStep() {
        if (this.currentStep > 1) {
            this.showStep(this.currentStep - 1);
        }
    },
    
    /**
     * Validate current step
     */
    validateStep(stepNumber) {
        const panel = document.getElementById(`wizard-step-${stepNumber}`);
        if (!panel) return true;
        
        const requiredFields = panel.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                this.showFieldError(field, 'This field is required');
            } else {
                this.clearFieldError(field);
            }
        });
        
        // Step-specific validation
        if (stepNumber === 1) {
            const email = document.getElementById('wizard-email');
            const password = document.getElementById('wizard-password');
            
            if (email && !this.validateEmail(email.value)) {
                isValid = false;
                this.showFieldError(email, 'Please enter a valid email');
            }
            
            if (password && password.value.length < 8) {
                isValid = false;
                this.showFieldError(password, 'Password must be at least 8 characters');
            }
        }
        
        // Validate tags input for step 3 (skills required)
        if (stepNumber === 3) {
            const skills = this.getTagsFromContainer('wizard-skills-container');
            if (skills.length === 0) {
                isValid = false;
                const skillsContainer = document.getElementById('wizard-skills-container');
                skillsContainer.style.borderColor = 'var(--error)';
                // Add error message
                const existingError = skillsContainer.parentElement.querySelector('.wizard-error-text');
                if (!existingError) {
                    const errorText = document.createElement('div');
                    errorText.className = 'wizard-error-text';
                    errorText.textContent = 'Please add at least one skill';
                    skillsContainer.parentElement.appendChild(errorText);
                }
            } else {
                const skillsContainer = document.getElementById('wizard-skills-container');
                skillsContainer.style.borderColor = '';
                const errorText = skillsContainer.parentElement.querySelector('.wizard-error-text');
                if (errorText) errorText.remove();
            }
        }
        
        // Validate languages for step 5
        if (stepNumber === 5) {
            const languages = this.getTagsFromContainer('wizard-languages-container');
            if (languages.length === 0) {
                isValid = false;
                const languagesContainer = document.getElementById('wizard-languages-container');
                languagesContainer.style.borderColor = 'var(--error)';
                const existingError = languagesContainer.parentElement.querySelector('.wizard-error-text');
                if (!existingError) {
                    const errorText = document.createElement('div');
                    errorText.className = 'wizard-error-text';
                    errorText.textContent = 'Please add at least one language';
                    languagesContainer.parentElement.appendChild(errorText);
                }
            } else {
                const languagesContainer = document.getElementById('wizard-languages-container');
                languagesContainer.style.borderColor = '';
                const errorText = languagesContainer.parentElement.querySelector('.wizard-error-text');
                if (errorText) errorText.remove();
            }
        }
        
        return isValid;
    },
    
    /**
     * Save step data to formData object
     */
    saveStepData(stepNumber) {
        const panel = document.getElementById(`wizard-step-${stepNumber}`);
        if (!panel) return;
        
        const inputs = panel.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (input.type !== 'file' && input.id) {
                const fieldName = input.id.replace('wizard-', '');
                this.formData[fieldName] = input.value;
            }
        });
        
        // Save tags
        if (stepNumber === 3) {
            this.formData.skills = this.getTagsFromContainer('wizard-skills-container');
            this.formData.certifications = this.getTagsFromContainer('wizard-certifications-container');
        }
        
        if (stepNumber === 4) {
            this.formData.projects = this.getTagsFromContainer('wizard-projects-container');
        }
        
        if (stepNumber === 5) {
            this.formData.languages = this.getTagsFromContainer('wizard-languages-container');
        }
    },
    
    /**
     * Submit complete form
     */
    async submitForm() {
        // Validate last step
        if (!this.validateStep(this.totalSteps)) {
            return;
        }
        
        // Save last step data
        this.saveStepData(this.totalSteps);
        
        // Prepare registration data
        const registrationData = {
            name: this.formData.name,
            email: this.formData.email,
            password: this.formData.password,
            role: Auth.selectedRole,
            branch: this.formData.branch || null,
            semester: this.formData.semester ? parseInt(this.formData.semester) : null,
            cgpa: this.formData.cgpa ? parseFloat(this.formData.cgpa) : null,
            skills: this.formData.skills || [],
            certifications: this.formData.certifications || [],
            experience: this.formData.experience || null,
            projects: this.formData.projects || [],
            languages: this.formData.languages || []
        };
        
        // Show loading
        const submitBtn = document.getElementById('wizard-submit');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<div class="loading-spinner"></div> Creating Account...';
        submitBtn.disabled = true;
        
        try {
            const response = await API.register(registrationData);
            
            // Store auth data
            localStorage.setItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN, response.access_token);
            localStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_USER, JSON.stringify(response.user));
            localStorage.setItem(CONFIG.STORAGE_KEYS.USER_ROLE, response.user.role);
            
            // Show username notification
            alert(`Account created successfully!

Your username: ${response.user.username}

Please save this username for future logins.`);
            
            // Navigate to dashboard
            Auth.navigateToDashboard(response.user.role);
            
        } catch (error) {
            Auth.showError(error.message || 'Registration failed. Please try again.');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    },
    
    /**
     * Setup tags input field
     */
    setupTagsInput(inputId, containerId) {
        const input = document.getElementById(inputId);
        const container = document.getElementById(containerId);
        
        if (!input || !container) return;
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const value = input.value.trim();
                if (value) {
                    this.addTag(container, value);
                    input.value = '';
                }
            }
        });
        
        input.addEventListener('blur', () => {
            const value = input.value.trim();
            if (value) {
                this.addTag(container, value);
                input.value = '';
            }
        });
    },
    
    /**
     * Add tag to container
     */
    addTag(container, text) {
        const tag = document.createElement('span');
        tag.className = 'tag-item';
        tag.innerHTML = `
            ${text}
            <button type="button" class="tag-remove">&times;</button>
        `;
        
        tag.querySelector('.tag-remove').addEventListener('click', () => {
            tag.remove();
        });
        
        // Insert before input
        const input = container.querySelector('input');
        container.insertBefore(tag, input);
    },
    
    /**
     * Get all tags from container
     */
    getTagsFromContainer(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return [];
        
        const tags = [];
        container.querySelectorAll('.tag-item').forEach(tag => {
            const text = tag.textContent.replace('×', '').trim();
            if (text) tags.push(text);
        });
        
        return tags;
    },
    
    /**
     * Validate email format
     */
    validateEmail(email) {
        const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        return re.test(email);
    },
    
    /**
     * Show field error
     */
    showFieldError(field, message) {
        field.style.borderColor = 'var(--error)';
        
        // Remove existing error
        const existingError = field.parentElement.querySelector('.wizard-error-text');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorText = document.createElement('div');
        errorText.className = 'wizard-error-text';
        errorText.textContent = message;
        field.parentElement.appendChild(errorText);
    },
    
    /**
     * Clear field error
     */
    clearFieldError(field) {
        field.style.borderColor = '';
        const errorText = field.parentElement.querySelector('.wizard-error-text');
        if (errorText) {
            errorText.remove();
        }
    }
};
