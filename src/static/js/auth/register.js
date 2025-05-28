function register(event) {
    event.preventDefault();  // Prevent the form from submitting
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('register-password').value;
    const password_repeat = document.getElementById('confirmPassword').value;
    const registerBtn = document.getElementById('registerBtn');
    registerBtn.disabled = true;
    // Create a JSON object with the form values
    const formData = {
        email: email,
        password: password,
        password_repeat: password_repeat
    };


    fetch('/api/registration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if(data.error){
            showAlert('alertPlaceholderRegister', 'danger', data.error || 'Invalid Registration');
            registerBtn.disabled = false;
        }else {
            showAlert('alertPlaceholderRegister', 'success', data.message || 'Please Check Your Mail');
            registerBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener("DOMContentLoaded", () => {
// Password strength meter
  const strengthBar = document.getElementById("password-strength");
  const passwordInput = document.getElementById("register-password");

  if (passwordInput && strengthBar) {
    passwordInput.addEventListener("input", () => {
      const val = passwordInput.value;
      let score = 0;
      if (val.length >= 6) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[a-z]/.test(val)) score++;
      if (/\d/.test(val)) score++;
      if (/[\W_]/.test(val)) score++;

      const percent = (score / 5) * 100;
      strengthBar.style.width = `${percent}%`;
      strengthBar.className = "progress-bar";

      if (percent < 40) {
        strengthBar.classList.add("bg-danger");
      } else if (percent < 80) {
        strengthBar.classList.add("bg-warning");
      } else {
        strengthBar.classList.add("bg-success");
      }
    });
  }

document.getElementById('registerForm').onsubmit = register;

});