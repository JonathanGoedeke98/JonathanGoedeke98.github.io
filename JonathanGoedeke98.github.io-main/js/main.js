// Modern interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Variables
    const header = document.querySelector('header');
    const backToTop = document.querySelector('.back-to-top');
    const themeToggle = document.querySelector('.theme-toggle');
    const progressBar = document.querySelector('.progress-bar');
    const loader = document.querySelector('.loader');
    const revealElements = document.querySelectorAll('.reveal');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    // Initialize loader
    if (loader) {
        window.addEventListener('load', () => {
            loader.classList.add('hidden');
        });
    }
    
    // Mobile menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('show-menu');
            hamburger.querySelector('i').classList.toggle('fa-bars');
            hamburger.querySelector('i').classList.toggle('fa-times');
        });
    }
    
    // Scroll event listener
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        // Header scroll effect
        if (header) {
            if (scrollPosition > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
        
        // Back to top button
        if (backToTop) {
            if (scrollPosition > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        }
        
        // Progress bar
        if (progressBar) {
            const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (scrollPosition / windowHeight) * 100;
            progressBar.style.width = scrolled + '%';
        }
        
        // Reveal animations
        if (revealElements.length > 0) {
            revealElements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementTop < windowHeight - 100) {
                    element.classList.add('active');
                }
            });
        }
    });
    
    // Back to top functionality
    if (backToTop) {
        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Theme toggle functionality
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            
            // Update icon
            const icon = themeToggle.querySelector('i');
            if (icon) {
                if (document.body.classList.contains('dark-theme')) {
                    icon.classList.remove('fa-moon');
                    icon.classList.add('fa-sun');
                    localStorage.setItem('theme', 'dark');
                } else {
                    icon.classList.remove('fa-sun');
                    icon.classList.add('fa-moon');
                    localStorage.setItem('theme', 'light');
                }
            }
        });
        
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            }
        }
    }
    
    // Keyboard navigation detection
    function handleFirstTab(e) {
        if (e.keyCode === 9) { // Tab key
            document.body.classList.add('user-is-tabbing');
            window.removeEventListener('keydown', handleFirstTab);
        }
    }
    window.addEventListener('keydown', handleFirstTab);
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Tabs functionality
    const tabLinks = document.querySelectorAll('.tab-link');
    if (tabLinks.length > 0) {
        tabLinks.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.target;
                
                // Remove active class from all tabs and content
                document.querySelectorAll('.tab-link').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                tab.classList.add('active');
                document.getElementById(target).classList.add('active');
            });
        });
        
        // Activate first tab by default
        tabLinks[0].click();
    }
    
    // Accordion functionality
    const accordions = document.querySelectorAll('.accordion-header');
    if (accordions.length > 0) {
        accordions.forEach(accordion => {
            accordion.addEventListener('click', () => {
                const parent = accordion.parentElement;
                parent.classList.toggle('active');
            });
        });
    }
    
    // Typing effect
    const typingElement = document.querySelector('.typing-effect');
    if (typingElement) {
        const text = typingElement.dataset.text.split(',');
        let index = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;
        
        function type() {
            const currentText = text[index];
            
            if (isDeleting) {
                typingElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                typingSpeed = 50;
            } else {
                typingElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                typingSpeed = 100;
            }
            
            if (!isDeleting && charIndex === currentText.length) {
                isDeleting = true;
                typingSpeed = 1000; // Pause at end
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                index = (index + 1) % text.length;
                typingSpeed = 500; // Pause before starting new word
            }
            
            setTimeout(type, typingSpeed);
        }
        
        setTimeout(type, 1000);
    }
    
    // Form validation
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let isValid = true;
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const messageInput = document.getElementById('message');
            
            // Reset errors
            document.querySelectorAll('.form-error').forEach(error => error.remove());
            document.querySelectorAll('.error').forEach(field => field.classList.remove('error'));
            
            // Validate name
            if (!nameInput.value.trim()) {
                isValid = false;
                showError(nameInput, 'Name is required');
            }
            
            // Validate email
            if (!emailInput.value.trim()) {
                isValid = false;
                showError(emailInput, 'Email is required');
            } else if (!isValidEmail(emailInput.value)) {
                isValid = false;
                showError(emailInput, 'Please enter a valid email');
            }
            
            // Validate message
            if (!messageInput.value.trim()) {
                isValid = false;
                showError(messageInput, 'Message is required');
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        function showError(input, message) {
            input.classList.add('error');
            const errorElement = document.createElement('div');
            errorElement.className = 'form-error';
            errorElement.textContent = message;
            input.parentElement.appendChild(errorElement);
        }
        
        function isValidEmail(email) {
            const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(String(email).toLowerCase());
        }
    }
    
    // Counter animation
    const counters = document.querySelectorAll('.counter-number');
    if (counters.length > 0) {
        counters.forEach(counter => {
            const target = +counter.dataset.target;
            const duration = 2000; // ms
            const step = target / (duration / 16); // 60fps
            
            function updateCounter() {
                const current = +counter.textContent;
                if (current < target) {
                    counter.textContent = Math.ceil(current + step);
                    setTimeout(updateCounter, 16);
                } else {
                    counter.textContent = target;
                }
            }
            
            // Start counter when in viewport
            const observer = new IntersectionObserver(entries => {
                if (entries[0].isIntersecting) {
                    updateCounter();
                    observer.disconnect();
                }
            });
            
            observer.observe(counter);
        });
    }
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('.tooltip');
    if (tooltips.length > 0) {
        tooltips.forEach(tooltip => {
            const text = tooltip.dataset.tooltip;
            const tooltipText = document.createElement('span');
            tooltipText.className = 'tooltip-text';
            tooltipText.textContent = text;
            tooltip.appendChild(tooltipText);
        });
    }
    
    // Skill bars animation
    const skillBars = document.querySelectorAll('.skill-percent');
    if (skillBars.length > 0) {
        skillBars.forEach(bar => {
            const percent = bar.dataset.percent;
            bar.style.width = '0%';
            
            const observer = new IntersectionObserver(entries => {
                if (entries[0].isIntersecting) {
                    setTimeout(() => {
                        bar.style.width = percent + '%';
                    }, 300);
                    observer.disconnect();
                }
            });
            
            observer.observe(bar);
        });
    }
});
