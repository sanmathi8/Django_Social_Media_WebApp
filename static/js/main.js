document.addEventListener('DOMContentLoaded', () => {
    // 1. AJAX Likes
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const postId = button.dataset.postId;
            const likeIcon = button.querySelector('i');
            const likeCountSpan = document.getElementById(`like-count-${postId}`);
            
            try {
                // Send AJAX request
                const response = await fetch(`/like/${postId}/?ajax=true`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    
                    // Toggle heart classes and play subtle scale animation
                    if (data.liked) {
                        likeIcon.classList.remove('bi-heart');
                        likeIcon.classList.add('bi-heart-fill');
                        likeIcon.style.transform = 'scale(1.3)';
                        likeIcon.style.transition = 'transform 0.15s ease';
                        setTimeout(() => {
                            likeIcon.style.transform = 'scale(1)';
                        }, 150);
                    } else {
                        likeIcon.classList.remove('bi-heart-fill');
                        likeIcon.classList.add('bi-heart');
                        likeIcon.style.transform = 'scale(0.8)';
                        likeIcon.style.transition = 'transform 0.15s ease';
                        setTimeout(() => {
                            likeIcon.style.transform = 'scale(1)';
                        }, 150);
                    }
                    
                    // Update likes count label
                    if (likeCountSpan) {
                        likeCountSpan.textContent = `${data.likes_count} like${data.likes_count !== 1 ? 's' : ''}`;
                    }
                }
            } catch (error) {
                console.error('Error toggling like:', error);
            }
        });
    });

    // Helper function to get the CSRF token cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Theme toggle persistence
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const savedTheme = localStorage.getItem('socialize-theme');

    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = body.classList.toggle('dark-mode');
            localStorage.setItem('socialize-theme', isDark ? 'dark' : 'light');
        });
    }

    // 2. Auto-dismiss toast messages
    const toastMessages = document.querySelectorAll('.toast-msg');
    toastMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
            message.style.opacity = '0';
            message.style.transform = 'translateX(20px)';
            setTimeout(() => message.remove(), 400);
        }, 4200);
    });
});
