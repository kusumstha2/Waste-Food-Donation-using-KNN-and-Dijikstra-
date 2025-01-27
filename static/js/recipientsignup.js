document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');

    signupForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        // Get form field values
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const address = document.getElementById('address').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('re_password').value; // Get confirm password value

        // Basic validation for empty fields
        if (!username || !email || !phone || !address || !password || !confirmPassword) {
            alert('All fields are required!');
            return;
        }

        // Check if passwords match
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        // Create an object for request data
        const requestData = {
            username: username,
            email: email,
            phone: phone,
            address: address,
            password: password,
            re_password: confirmPassword // Include the re_password field here
        };

        // Get CSRF token from the form
        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

        try {
            // Send the data to the backend
            const response = await fetch('/recipient/signup/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Ensure content type is JSON
                    'X-CSRFToken': csrfToken, // CSRF token in headers
                },
                body: JSON.stringify(requestData), // Send the requestData as JSON
            });

            // Handle the response
            if (response.ok) {
                const result = await response.json();
                alert('Signup successful!');
                console.log(result);
                window.location.href = '/recipient/login/'; // Redirect to login page after successful signup
            } else {
                const errorData = await response.json();
                console.log(errorData); // Log error response to console
                alert(`Error: ${errorData.error || 'Signup failed!'}`);
            }
        } catch (error) {
            console.error('Error during sign-up:', error);
            alert('An unexpected error occurred. Please try again later.');
        }
    });
});
