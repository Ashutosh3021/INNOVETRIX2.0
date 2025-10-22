// ============================================
// ANIMATION HELPERS MODULE
// ============================================

const Animations = {
    /**
     * Add fade-in animation to elements
     */
    fadeIn(element, delay = 0) {
        setTimeout(() => {
            element.classList.add('fade-in');
        }, delay);
    },
    
    /**
     * Add stagger animation to children
     */
    staggerChildren(container, delay = 100) {
        const children = container.children;
        Array.from(children).forEach((child, index) => {
            setTimeout(() => {
                child.classList.add('fade-in');
            }, index * delay);
        });
    },
    
    /**
     * Add scale-in animation
     */
    scaleIn(element, delay = 0) {
        setTimeout(() => {
            element.classList.add('scale-in');
        }, delay);
    },
    
    /**
     * Add slide animation
     */
    slideIn(element, direction = 'left', delay = 0) {
        setTimeout(() => {
            element.classList.add(`slide-in-${direction}`);
        }, delay);
    },
    
    /**
     * Create loading spinner
     */
    createSpinner() {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        return spinner;
    },
    
    /**
     * Smooth scroll to element
     */
    smoothScrollTo(element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    },
    
    /**
     * Page transition effect
     */
    pageTransition(fromPage, toPage, callback) {
        fromPage.style.opacity = '0';
        fromPage.style.transform = 'translateX(-50px)';
        
        setTimeout(() => {
            fromPage.classList.remove('active');
            toPage.classList.add('active');
            toPage.style.opacity = '0';
            toPage.style.transform = 'translateX(50px)';
            
            setTimeout(() => {
                toPage.style.opacity = '1';
                toPage.style.transform = 'translateX(0)';
                if (callback) callback();
            }, 50);
        }, 300);
    },
    
    /**
     * Card flip animation
     */
    flipCard(card) {
        card.style.transform = 'rotateY(180deg)';
        setTimeout(() => {
            card.style.transform = 'rotateY(0deg)';
        }, 600);
    },
    
    /**
     * Pulse animation
     */
    pulse(element, duration = 2000) {
        element.classList.add('pulse');
        setTimeout(() => {
            element.classList.remove('pulse');
        }, duration);
    },
    
    /**
     * Shake animation for errors
     */
    shake(element) {
        element.style.animation = 'shake 0.5s';
        setTimeout(() => {
            element.style.animation = '';
        }, 500);
    },
    
    /**
     * Progress bar animation
     */
    animateProgress(progressBar, percentage, duration = 1000) {
        let current = 0;
        const increment = percentage / (duration / 16);
        
        const interval = setInterval(() => {
            current += increment;
            if (current >= percentage) {
                current = percentage;
                clearInterval(interval);
            }
            progressBar.style.width = `${current}%`;
        }, 16);
    },
    
    /**
     * Count up animation for numbers
     */
    countUp(element, target, duration = 1000) {
        let current = 0;
        const increment = target / (duration / 16);
        
        const interval = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            element.textContent = Math.floor(current);
        }, 16);
    },
    
    /**
     * Typewriter effect
     */
    typeWriter(element, text, speed = 50) {
        let index = 0;
        element.textContent = '';
        
        const interval = setInterval(() => {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
            } else {
                clearInterval(interval);
            }
        }, speed);
    },
    
    /**
     * Ripple effect on click
     */
    addRippleEffect(element) {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    }
};

// Add shake keyframe if not already in CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
