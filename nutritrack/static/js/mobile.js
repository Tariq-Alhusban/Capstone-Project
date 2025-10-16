// Mobile-specific enhancements
document.addEventListener('DOMContentLoaded', function() {

    // Detect if device is truly mobile/touch-enabled
    function isMobileDevice() {
        return (
            ('ontouchstart' in window) ||
            (navigator.maxTouchPoints > 0) ||
            (navigator.msMaxTouchPoints > 0) ||
            (window.innerWidth <= 768)
        );
    }

    // Mobile Navigation Toggle - Implementation
    const navMenu = document.querySelector('.nav-menu');
    const navContainer = document.querySelector('.nav-container');
    let navToggle;

    if (navContainer && navMenu) {
        // Create toggle button
        navToggle = document.createElement('button');
        navToggle.className = 'nav-toggle';
        navToggle.innerHTML = '☰';
        navToggle.setAttribute('aria-label', 'Toggle navigation menu');

        // Insert toggle button before nav-menu
        navContainer.insertBefore(navToggle, navMenu);

        // Toggle menu on click
        navToggle.addEventListener('click', function(e) {
            navMenu.classList.toggle('active');
            navToggle.innerHTML = navMenu.classList.contains('active') ? '✕' : '☰';
            const isExpanded = navMenu.classList.contains('active');
            navToggle.setAttribute('aria-expanded', isExpanded);
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navContainer.contains(e.target) && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.innerHTML = '☰';
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Close menu when clicking on nav links (mobile)
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    navMenu.classList.remove('active');
                    navToggle.innerHTML = '☰';
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });
        });

        // Handle window resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                navMenu.classList.remove('active');
                navToggle.innerHTML = '☰';
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Show mobile navigation toggle on small screens
        function checkScreenSize() {
            if (!navToggle || !navMenu) return;
            
            if (window.innerWidth <= 768) {
                navToggle.style.display = 'block';
            } else {
                navToggle.style.display = 'none';
                navMenu.classList.remove('active');
                navToggle.innerHTML = '☰';
            }
        }

        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);
    }

    // Touch-friendly quantity adjustments (MOBILE ONLY)
    if (isMobileDevice()) {
        const quantityInputs = document.querySelectorAll('input[type="number"]');
        quantityInputs.forEach(input => {
            const wrapper = document.createElement('div');
            wrapper.className = 'quantity-wrapper';
            wrapper.style.cssText = 'display: flex; align-items: center; gap: 0.5rem;';

            const decreaseBtn = document.createElement('button');
            decreaseBtn.type = 'button';
            decreaseBtn.className = 'btn btn-outline btn-small';
            decreaseBtn.innerHTML = '−';
            decreaseBtn.style.cssText = 'min-width: 40px; height: 40px; padding: 0;';

            const increaseBtn = document.createElement('button');
            increaseBtn.type = 'button';
            increaseBtn.className = 'btn btn-outline btn-small';
            increaseBtn.innerHTML = '+';
            increaseBtn.style.cssText = 'min-width: 40px; height: 40px; padding: 0;';

            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(decreaseBtn);
            wrapper.appendChild(input);
            wrapper.appendChild(increaseBtn);

            input.style.cssText = 'text-align: center; -moz-appearance: textfield;';
            input.setAttribute('readonly', 'readonly');

            decreaseBtn.addEventListener('click', function() {
                const currentValue = parseFloat(input.value) || 0;
                const step = parseFloat(input.step) || 1;
                const min = parseFloat(input.min) || 0;
                if (currentValue > min) {
                    input.value = Math.max(min, currentValue - step);
                    input.dispatchEvent(new Event('input'));
                }
            });

            increaseBtn.addEventListener('click', function() {
                const currentValue = parseFloat(input.value) || 0;
                const step = parseFloat(input.step) || 1;
                const max = parseFloat(input.max) || Infinity;
                if (currentValue < max) {
                    input.value = Math.min(max, currentValue + step);
                    input.dispatchEvent(new Event('input'));
                }
            });
        });
    }

    // Swipe to delete for meal entries (MOBILE ONLY)
    if (isMobileDevice()) {
        let swipeStartX, swipeStartY, currentX, currentY;
        const swipeThreshold = 100;

        document.querySelectorAll('.meal-entry').forEach(entry => {
            entry.style.position = 'relative';

            const deleteAction = document.createElement('div');
            deleteAction.className = 'swipe-actions';
            deleteAction.innerHTML = '🗑️ Delete';
            entry.appendChild(deleteAction);

            entry.addEventListener('touchstart', function(e) {
                swipeStartX = e.touches[0].clientX;
                swipeStartY = e.touches[0].clientY;
            });

            entry.addEventListener('touchmove', function(e) {
                if (!swipeStartX || !swipeStartY) return;

                currentX = e.touches[0].clientX;
                currentY = e.touches[0].clientY;

                const diffX = swipeStartX - currentX;
                const diffY = swipeStartY - currentY;

                if (Math.abs(diffX) > Math.abs(diffY) && diffX > 0) {
                    e.preventDefault();
                    const translateX = Math.min(diffX, swipeThreshold);
                    entry.style.transform = `translateX(-${translateX}px)`;
                }
            });

            entry.addEventListener('touchend', function(e) {
                const diffX = swipeStartX - currentX;
                if (diffX > swipeThreshold) {
                    entry.classList.add('swiped');
                    entry.style.transform = `translateX(-${swipeThreshold}px)`;
                    deleteAction.addEventListener('click', function() {
                        if (confirm('Delete this food item?')) {
                            entry.style.animation = 'slideOutRight 0.3s ease forwards';
                            setTimeout(() => entry.remove(), 300);
                        }
                    });
                } else {
                    entry.style.transform = 'translateX(0)';
                    entry.classList.remove('swiped');
                }
                swipeStartX = swipeStartY = currentX = currentY = null;
            });
        });
    }

    // Pull to refresh (MOBILE ONLY)
    if (isMobileDevice()) {
        let pullstartY, pullDistance;
        const pullThreshold = 100;

        const pullIndicator = document.createElement('div');
        pullIndicator.className = 'pull-indicator';
        pullIndicator.innerHTML = '↓ Pull to refresh';
        document.body.appendChild(pullIndicator);

        document.addEventListener('touchstart', function(e) {
            if (window.scrollY === 0) {
                pullstartY = e.touches[0].clientY;
            }
        });

        document.addEventListener('touchmove', function(e) {
            if (pullstartY && window.scrollY === 0) {
                pullDistance = e.touches[0].clientY - pullstartY;
                if (pullDistance > 0) {
                    e.preventDefault();
                    const progress = Math.min(pullDistance / pullThreshold, 1);
                    pullIndicator.style.top = `${-50 + (50 * progress)}px`;
                    if (progress >= 1) {
                        pullIndicator.innerHTML = '↑ Release to refresh';
                    } else {
                        pullIndicator.innerHTML = '↓ Pull to refresh';
                    }
                }
            }
        }, { passive: false });

        document.addEventListener('touchend', function(e) {
            if (pullDistance > pullThreshold) {
                pullIndicator.innerHTML = '🔄 Refreshing...';
                pullIndicator.classList.add('active');
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                pullIndicator.style.top = '-50px';
                pullIndicator.classList.remove('active');
            }
            pullstartY = pullDistance = null;
        });
    }

    // Offline detection (works on all devices)
    const offlineIndicator = document.createElement('div');
    offlineIndicator.className = 'offline-indicator';
    offlineIndicator.innerHTML = 'You are offline';
    document.body.appendChild(offlineIndicator);

    window.addEventListener('online', function() {
        offlineIndicator.classList.remove('show');
    });

    window.addEventListener('offline', function() {
        offlineIndicator.classList.add('show');
    });

});

// CSS animations for mobile
const mobileAnimations = `
@keyframes slideOutRight {
    to { transform: translateX(100%); opacity: 0; }
}
`;

const style = document.createElement('style');
style.textContent = mobileAnimations;
document.head.appendChild(style);
