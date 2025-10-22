// ============================================
// OCR MODULE - Resume Auto-Fill
// ============================================

const OCR = {
    /**
     * Handle resume upload and OCR processing
     */
    async handleResumeUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Display filename
        const filenameDisplay = document.getElementById('resume-filename');
        if (filenameDisplay) {
            filenameDisplay.textContent = file.name;
        }
        
        // Show processing indicator
        this.showProcessingIndicator();
        
        try {
            // For now, simulate OCR processing
            // In production, you would use Tesseract.js or send to a backend OCR service
            await this.simulateOCRProcessing(file);
            
        } catch (error) {
            console.error('OCR Error:', error);
            this.showOCRError('Failed to process resume. Please fill in manually.');
        } finally {
            this.hideProcessingIndicator();
        }
    },
    
    /**
     * Simulate OCR processing (placeholder for actual OCR implementation)
     */
    async simulateOCRProcessing(file) {
        return new Promise((resolve) => {
            setTimeout(() => {
                // Simulate extracted data
                const extractedData = {
                    skills: ['Python', 'JavaScript', 'React', 'Node.js', 'Machine Learning'],
                    projects: ['E-commerce Platform', 'ML Classification System', 'Portfolio Website']
                };
                
                this.autoFillForm(extractedData);
                resolve();
            }, 2000);
        });
    },
    
    /**
     * Auto-fill form with extracted data
     */
    autoFillForm(data) {
        if (data.skills && data.skills.length > 0) {
            const skillsInput = document.getElementById('register-skills');
            if (skillsInput) {
                skillsInput.value = data.skills.join(', ');
                Animations.pulse(skillsInput);
            }
        }
        
        if (data.projects && data.projects.length > 0) {
            const projectsInput = document.getElementById('register-projects');
            if (projectsInput) {
                projectsInput.value = data.projects.join(', ');
                Animations.pulse(projectsInput);
            }
        }
        
        this.showSuccess('Resume processed! Please review the auto-filled information.');
    },
    
    /**
     * Show processing indicator
     */
    showProcessingIndicator() {
        const filenameDisplay = document.getElementById('resume-filename');
        if (filenameDisplay) {
            filenameDisplay.innerHTML = '<span class="shimmer">Processing resume...</span>';
        }
    },
    
    /**
     * Hide processing indicator
     */
    hideProcessingIndicator() {
        // Processing complete - filename already updated
    },
    
    /**
     * Show success message
     */
    showSuccess(message) {
        const filenameDisplay = document.getElementById('resume-filename');
        if (filenameDisplay) {
            filenameDisplay.style.color = 'var(--success)';
            setTimeout(() => {
                filenameDisplay.style.color = '';
            }, 3000);
        }
        
        // You could also show a toast notification here
        console.log('OCR Success:', message);
    },
    
    /**
     * Show error message
     */
    showOCRError(message) {
        const filenameDisplay = document.getElementById('resume-filename');
        if (filenameDisplay) {
            filenameDisplay.textContent = message;
            filenameDisplay.style.color = 'var(--error)';
        }
    },
    
    /**
     * Advanced OCR implementation with Tesseract.js (optional enhancement)
     * Uncomment and use if you include Tesseract.js library
     */
    /*
    async processWithTesseract(file) {
        const { createWorker } = Tesseract;
        const worker = createWorker();
        
        await worker.load();
        await worker.loadLanguage('eng');
        await worker.initialize('eng');
        
        const { data: { text } } = await worker.recognize(file);
        await worker.terminate();
        
        return this.extractDataFromText(text);
    },
    
    extractDataFromText(text) {
        // Parse extracted text to find skills, projects, etc.
        const skills = [];
        const projects = [];
        
        // Add your parsing logic here
        // Example: look for skill keywords, project sections, etc.
        
        return { skills, projects };
    }
    */
};
