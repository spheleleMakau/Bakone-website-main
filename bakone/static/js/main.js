// Smooth scroll for navigation links
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href').slice(1);
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            e.preventDefault();
            window.scrollTo({
                top: targetSection.offsetTop - 70,
                behavior: 'smooth'
            });
        }
    });
});

// Fade-in animation on scroll
function revealOnScroll() {
    const fadeEls = document.querySelectorAll('.fade-in');
    fadeEls.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 60) {
            el.classList.add('visible');
        }
    });
}
window.addEventListener('scroll', revealOnScroll);
window.addEventListener('DOMContentLoaded', revealOnScroll);

// Add fade-in class to sections
['hero', 'about', 'services', 'training', 'contact'].forEach(id => {
    const section = document.getElementById(id);
    if (section) section.classList.add('fade-in');
});

// Sticky navbar shadow on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 10) {
        navbar.style.boxShadow = '0 4px 16px rgba(0,0,0,0.08)';
    } else {
        navbar.style.boxShadow = '';
    }
});

// Phone number input restriction to 10 digits
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.querySelector('[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            // Remove all non-digit characters
            let value = e.target.value.replace(/\D/g, '');

            // Ensure starts with 0
            if (value.length > 0 && !value.startsWith('0')) {
                value = '0' + value;
            }

            // Limit to 10 digits
            if (value.length > 10) {
                value = value.substring(0, 10);
            }

            // Format as South African number: 0X XXX XXXX
            if (value.length >= 2) {
                value = value.substring(0, 2) + ' ' + value.substring(2);
            }
            if (value.length >= 6) {
                value = value.substring(0, 6) + ' ' + value.substring(6);
            }
            if (value.length >= 10) {
                value = value.substring(0, 10) + ' ' + value.substring(10);
            }

            e.target.value = value;
        });

        // Prevent non-numeric input and ensure starts with 0
        phoneInput.addEventListener('keypress', function(e) {
            if (!/[0-9]/.test(e.key) && !['Backspace', 'Delete', 'Tab', 'Enter'].includes(e.key)) {
                e.preventDefault();
            }
        });

        // On focus, ensure starts with 0
        phoneInput.addEventListener('focus', function(e) {
            if (!e.target.value.startsWith('0') && e.target.value.length === 0) {
                e.target.value = '0';
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.contact-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate form
            if (!validateForm(form)) {
                return;
            }

            // Collect form data
            const formData = new FormData(form);
            const data = {
                name: formData.get('name').trim(),
                company: formData.get('company').trim(),
                email: formData.get('email').trim(),
                phone: formData.get('phone').replace(/\s/g, '').trim(), // Remove spaces for clean number
                services: formData.getAll('services[]'), // Get all selected services
                message: formData.get('message').trim()
            };

            // Create service names mapping
            const serviceNames = {
                'farming': 'Agricultural Operations',
                'ohs': 'Occupational Health & Safety',
                'construction': 'Construction Management',
                'logistics': 'Logistics & Transportation',
                'training': 'Training & Certification',
                'other': 'Other'
            };

            // Format selected services
            let servicesText = 'No services selected';
            if (data.services && data.services.length > 0) {
                servicesText = data.services.map(service => serviceNames[service] || service).join(', ');
            }

            // Create comprehensive WhatsApp message
            const whatsappMessage = `🔔 *NEW BUSINESS INQUIRY - Bakone Trading & Projects*

👤 *CLIENT DETAILS:*
• *Name:* ${data.name}
• *Company:* ${data.company || 'Not specified'}
• *Email:* ${data.email}
• *Phone:* ${data.phone ? '+27 ' + data.phone : 'Not provided'}

🎯 *SERVICES REQUESTED:*
${servicesText}

📝 *PROJECT REQUIREMENTS:*
${data.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 *Bakone Trading & Projects*
🌐 Website Contact Form Submission
📅 ${new Date().toLocaleDateString('en-ZA', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
})}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Please respond promptly to this business inquiry.*`.trim();

            // Encode message for URL
            const encodedMessage = encodeURIComponent(whatsappMessage);

            // WhatsApp URL (South African format without +)
            const whatsappURL = `https://wa.me/27646871657?text=${encodedMessage}`;

            // Show success modal
            showSuccessModal(data.name, servicesText);

            // Open WhatsApp
            window.open(whatsappURL, '_blank');

            // Reset form
            form.reset();
        });
    }
});

// Comprehensive form validation
function validateForm(form) {
    const errors = [];
    let isValid = true;

    // Get form fields
    const name = form.querySelector('[name="name"]');
    const company = form.querySelector('[name="company"]');
    const email = form.querySelector('[name="email"]');
    const phone = form.querySelector('[name="phone"]');
    const services = form.querySelectorAll('[name="services[]"]:checked');
    const message = form.querySelector('[name="message"]');

    // Clear previous error states
    clearFieldErrors(form);

    // Validate name
    if (!name.value.trim()) {
        showFieldError(name, 'Full name is required');
        errors.push('Name is required');
        isValid = false;
    } else if (name.value.trim().length < 2) {
        showFieldError(name, 'Name must be at least 2 characters');
        errors.push('Name too short');
        isValid = false;
    }

    // Validate company
    if (!company.value.trim()) {
        showFieldError(company, 'Please enter your company name');
        errors.push('Company name is required');
        isValid = false;
    } else if (company.value.trim().length < 2) {
        showFieldError(company, 'Please enter a valid company name');
        errors.push('Company name too short');
        isValid = false;
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.value.trim()) {
        showFieldError(email, 'Email address is required');
        errors.push('Email is required');
        isValid = false;
    } else if (!emailRegex.test(email.value.trim())) {
        showFieldError(email, 'Please enter a valid email address');
        errors.push('Invalid email format');
        isValid = false;
    }

    // Validate phone number
    const phoneDigits = phone.value.replace(/\s/g, '');
    if (!phoneDigits) {
        showFieldError(phone, 'Phone number is required');
        errors.push('Phone number is required');
        isValid = false;
    } else if (phoneDigits.length !== 10) {
        showFieldError(phone, 'Phone number must be exactly 10 digits');
        errors.push('Phone number must be 10 digits');
        isValid = false;
    } else if (!/^0[6-8]/.test(phoneDigits)) {
        showFieldError(phone, 'Please enter a valid South African mobile number');
        errors.push('Invalid South African mobile number');
        isValid = false;
    }

    // Validate services selection
    if (services.length === 0) {
        const servicesContainer = form.querySelector('.services-checkboxes');
        showFieldError(servicesContainer, 'Please select at least one service of interest');
        errors.push('No services selected');
        isValid = false;
    }

    // Validate message
    if (!message.value.trim()) {
        showFieldError(message, 'Project details are required');
        errors.push('Message is required');
        isValid = false;
    } else if (message.value.trim().length < 10) {
        showFieldError(message, 'Please provide more details (at least 10 characters)');
        errors.push('Message too short');
        isValid = false;
    }

    // Show error modal if validation failed
    if (!isValid) {
        showErrorModal(errors);
    }

    return isValid;
}

// Show field error
function showFieldError(field, message) {
    field.style.borderColor = '#e74c3c';
    field.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.2)';

    // Add error message
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.color = '#e74c3c';
    errorElement.style.fontSize = '0.85rem';
    errorElement.style.marginTop = '4px';

    // Insert after field or its parent label
    const parent = field.closest('.form-field') || field.parentElement;
    parent.appendChild(errorElement);

    // Focus field
    field.focus();
}

// Show success modal
function showSuccessModal(name, services) {
    const modal = document.getElementById('successModal');
    const userName = document.getElementById('userName');
    const selectedServices = document.getElementById('selectedServices');
    
    if (modal) {
        userName.textContent = name;
        selectedServices.textContent = services;
        modal.classList.add('active');
        
        // Close button listener
        const closeBtn = document.getElementById('modalCloseBtn');
        if (closeBtn) {
            closeBtn.onclick = function() {
                modal.classList.remove('active');
            };
        }
        
        // Close on overlay click
        modal.onclick = function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        };
    }
}

// Show error modal
function showErrorModal(errors) {
    const modal = document.getElementById('errorModal');
    const errorList = document.getElementById('errorList');
    
    if (modal && errorList) {
        // Clear previous errors
        errorList.innerHTML = '';
        
        // Add new errors
        errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorList.appendChild(li);
        });
        
        modal.classList.add('active');
        
        // Close button listener
        const closeBtn = document.getElementById('errorModalCloseBtn');
        if (closeBtn) {
            closeBtn.onclick = function() {
                modal.classList.remove('active');
            };
        }
        
        // Close on overlay click
        modal.onclick = function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        };
    }
}

// Clear all field errors
function clearFieldErrors(form) {
    // Reset field styles
    const fields = form.querySelectorAll('input, textarea, .services-checkboxes');
    fields.forEach(field => {
        field.style.borderColor = '';
        field.style.boxShadow = '';
    });

    // Remove error messages
    const errorMessages = form.querySelectorAll('.field-error');
    errorMessages.forEach(error => error.remove());
}
