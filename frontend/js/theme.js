// ============================================
// THEME TOGGLE MODULE
// ============================================

const Theme = {
    /**
     * Initialize theme module
     */
    init() {
        this.loadTheme();
        this.setupEventListeners();
    },
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    },
    
    /**
     * Load theme from storage
     */
    loadTheme() {
        const savedTheme = localStorage.getItem(CONFIG.STORAGE_KEYS.THEME);
        const theme = savedTheme || 'dark';
        this.applyTheme(theme);
    },
    
    /**
     * Apply theme
     */
    applyTheme(theme) {
        document.body.classList.remove('dark-theme', 'light-theme');
        document.body.classList.add(`${theme}-theme`);
        localStorage.setItem(CONFIG.STORAGE_KEYS.THEME, theme);
    },
    
    /**
     * Toggle theme
     */
    toggleTheme() {
        const isDark = document.body.classList.contains('dark-theme');
        const newTheme = isDark ? 'light' : 'dark';
        this.applyTheme(newTheme);
        
        // Add animation to button
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                toggleButton.style.transform = '';
            }, 300);
        }
    },
    
    /**
     * Get current theme
     */
    getCurrentTheme() {
        return document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    }
};
