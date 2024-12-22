document.addEventListener('DOMContentLoaded', function () {
    const togglePwd = document.querySelector('.togglePWD'); // Select the toggle element
    const passwordField = document.querySelector('#passwordField'); // Select the password field

    if (togglePwd && passwordField) {
        togglePwd.addEventListener('click', function () {
            // Toggle the password field's type between "password" and "text"
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                togglePwd.textContent = 'HIDE'; // Change text to "HIDE"
            } else {
                passwordField.type = 'password';
                togglePwd.textContent = 'SHOW'; // Change text back to "SHOW"
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const togglePwd = document.querySelector('.toggleConfirm'); // Select the toggle element
    const passwordField = document.querySelector('#confirmField'); // Select the password field

    if (togglePwd && passwordField) {
        togglePwd.addEventListener('click', function () {
            // Toggle the password field's type between "password" and "text"
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                togglePwd.textContent = 'HIDE'; // Change text to "HIDE"
            } else {
                passwordField.type = 'password';
                togglePwd.textContent = 'SHOW'; // Change text back to "SHOW"
            }
        });
    }
});
