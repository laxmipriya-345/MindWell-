// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Initialize scroll reveal animations
    initScrollReveal();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validation
    initFormValidation();
    
    // Auto-hide alerts
    initAlerts();
    
    // Smooth scroll for anchor links
    initSmoothScroll();
});

// Scroll Reveal Animation
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');
    
    function checkReveal() {
        for (let i = 0; i < revealElements.length; i++) {
            const windowHeight = window.innerHeight;
            const revealTop = revealElements[i].getBoundingClientRect().top;
            const revealPoint = 150;
            
            if (revealTop < windowHeight - revealPoint) {
                revealElements[i].classList.add('active');
            }
        }
    }
    
    window.addEventListener('scroll', checkReveal);
    checkReveal(); // Check on initial load
}

// Initialize Bootstrap Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Auto-hide Alerts
function initAlerts() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

// Smooth Scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Parallax Effect for Hero Section
window.addEventListener('scroll', function() {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const scrolled = window.pageYOffset;
        heroSection.style.transform = 'translateY(' + (scrolled * 0.5) + 'px)';
    }
});

// Typing Animation for Hero Title
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing animation on hero title
const heroTitle = document.querySelector('.hero-title');
if (heroTitle) {
    typeWriter(heroTitle, heroTitle.textContent, 100);
}

// Counter Animation for Statistics
function animateCounter(element, start, end, duration = 2000) {
    let startTimestamp = null;
    
    function step(timestamp) {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    }
    
    window.requestAnimationFrame(step);
}

// Initialize counters when they come into view
const counters = document.querySelectorAll('.counter');
if (counters.length > 0) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const endValue = parseInt(target.getAttribute('data-target'));
                animateCounter(target, 0, endValue);
                observer.unobserve(target);
            }
        });
    });
    
    counters.forEach(counter => observer.observe(counter));
}

// Mood Tracker Chart Initialization
function initMoodChart() {
    const ctx = document.getElementById('moodChart');
    if (ctx) {
        fetch('/api/mood-data')
            .then(response => response.json())
            .then(data => {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.dates,
                        datasets: [{
                            label: 'Mood Level',
                            data: data.levels,
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            tension: 0.4,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: {
                            duration: 2000,
                            easing: 'easeInOutQuart'
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 5,
                                grid: {
                                    display: true,
                                    color: 'rgba(0,0,0,0.05)'
                                }
                            },
                            x: {
                                grid: {
                                    display: false
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            });
    }
}

// Call mood chart initialization
initMoodChart();

// Mental Health Assessment Form
const assessmentForm = document.getElementById('assessmentForm');
if (assessmentForm) {
    assessmentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const answers = [];
        for (let i = 1; i <= 10; i++) {
            const selected = document.querySelector(`input[name="q${i}"]:checked`);
            if (selected) {
                answers.push(parseInt(selected.value));
            }
        }
        
        if (answers.length < 10) {
            showNotification('Please answer all questions', 'warning');
            return;
        }
        
        // Show loading
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Analyzing...';
        submitBtn.disabled = true;
        
        fetch('/api/submit-assessment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers: answers })
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            showNotification('An error occurred', 'error');
        })
        .finally(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    });
}

// Display Assessment Results
function displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) return;
    
    let alertClass = 'success';
    if (data.level === 'High') alertClass = 'danger';
    else if (data.level === 'Moderate') alertClass = 'warning';
    
    let html = `
        <div class="alert alert-${alertClass} animate__animated animate__fadeIn">
            <h5 class="alert-heading">Risk Level: ${data.level}</h5>
            <p>${data.message}</p>
            <hr>
            <p class="mb-0">Score: ${data.score}/30</p>
        </div>
    `;
    
    if (data.resources && data.resources.length > 0) {
        html += `
            <div class="mt-3">
                <h6>Resources:</h6>
                <ul class="list-group">
        `;
        data.resources.forEach(resource => {
            html += `<li class="list-group-item">${resource}</li>`;
        });
        html += '</ul></div>';
    }
    
    resultsContainer.innerHTML = html;
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Show Notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Lazy Loading Images
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.add('fade-in');
            observer.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));

// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize chatbot state from localStorage
    const chatbotState = localStorage.getItem('chatbotOpen');
    if (chatbotState === 'false') {
        toggleChatbot();
    }
    
    // Save chatbot state when toggled
    const originalToggle = toggleChatbot;
    toggleChatbot = function() {
        originalToggle();
        localStorage.setItem('chatbotOpen', isChatbotOpen);
    };
    
    // Auto-focus input when chatbot opens
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'style' && 
                mutation.target.style.display !== 'none') {
                document.getElementById('chatInput').focus();
            }
        });
    });
    
    const chatbotBody = document.getElementById('chatbotBody');
    if (chatbotBody) {
        observer.observe(chatbotBody, { attributes: true });
    }
});
// ===============================
// AI CHATBOT INTEGRATION
// ===============================

const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.innerText = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message when user presses ENTER
if (chatInput) {
    chatInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();

            const message = chatInput.value.trim();
            if (!message) return;

            addMessage(message, "user");
            chatInput.value = "";

            fetch("/api/chat", {
                method: "POST",
                credentials: "include",   // ⭐ FIXES 401
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            })
            .then(res => res.json())
            .then(data => {
                addMessage(data.reply, "bot");
            })
            .catch(() => {
                addMessage("AI server error.", "bot");
            });
        }
    });
}