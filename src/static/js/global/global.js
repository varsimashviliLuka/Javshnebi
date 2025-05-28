function showAlert(divID, category, message) {
    const alertPlaceholder = document.getElementById(divID);
    
    // Create a new alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${category} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add the alert to the placeholder
    alertPlaceholder.appendChild(alertDiv);
    
    // Optional: Auto-close the alert after a timeout
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000); // 5000 milliseconds = 5 seconds
}

function clearSessionData(redirect = true) {
    // Remove all session-related data
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email');
    
    // Optionally redirect the user to the login page or another page
    if (redirect) {
        window.location.href = '/'; // Redirect to the login page
    }
}

function isTokenExpired(token) {
    if (!token) return true;

    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Date.now() / 1000; // Current time in seconds

    return currentTime > payload.exp;
}

// Define the refreshToken function globally
function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');

    if (!refreshToken) {
        clearSessionData(); // Clear session data and redirect to login
        return Promise.reject('No refresh token available');
    }

    return fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${refreshToken}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401) {
            // alert("გთხოვთ ხელახლა გაიაროთ ავტორიზაცია.");
            clearSessionData(); // Clear session data and redirect to login
            return Promise.reject('Unauthorized');
        }
        if (!response.ok) {
            throw new Error('Failed to refresh token');
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token); // Save new access token
            return data.access_token;
        } else {
            throw new Error('Failed to refresh token');
        }
    })
    .catch(error => {
        console.error('Error refreshing token:', error);
        clearSessionData(); // Clear session data and redirect to login
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('access_token');

    // Check if the token is expired and redirect to login if necessary
    if (token && isTokenExpired(token)) {
        refreshToken(); // Clear session data and redirect to login
    }
});