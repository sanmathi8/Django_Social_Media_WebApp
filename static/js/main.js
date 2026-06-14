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

    // 2. Auto-dismiss Alert Messages
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            // Check if bootstrap is defined before calling
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Fallback fade out
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 4000);
    });
});
