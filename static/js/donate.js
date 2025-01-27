document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.donate-form');
  const foodImageInput = document.getElementById('foodImage');
  const expiryDateInput = document.getElementById('expiryDate');
  const today = new Date().toISOString().split('T')[0];

  // Set minimum expiry date to today
  expiryDateInput.setAttribute('min', today);

  // Form submit event
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Validate file size (max 5MB)document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.donate-form');
  const foodImageInput = document.getElementById('foodImage');
  const expiryDateInput = document.getElementById('expiryDate');
  const today = new Date().toISOString().split('T')[0];

  // Set minimum expiry date to today
  expiryDateInput.setAttribute('min', today);

  // Form submit event
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Validate file size (max 5MB)
    const file = foodImageInput.files[0];
    if (file && file.size > 10 * 1024 * 1024) {
      alert('Food image size must be less than 10MB');
      return;
    }

    // Ensure all fields are filled
    const inputs = form.querySelectorAll('input, select, textarea');
    for (const input of inputs) {
      if (!input.value) {
        alert(`Please fill out the ${input.previousElementSibling.textContent} field`);
        input.focus();
        return;
      }
    }

    // Collect form data
    const donorName = document.getElementById('donorName').value;
    const donorNumber = document.getElementById('donorNumber').value;
    const foodName = document.getElementById('foodName').value;
    const foodType = document.getElementById('foodType').value;
    const foodImage = foodImageInput.files[0] ? URL.createObjectURL(foodImageInput.files[0]) : '';
    const description = document.getElementById('description').value;
    const expiryDate = document.getElementById('expiryDate').value;
    const location = document.getElementById('location').value;

    // Create a donation object
    const donation = {
      donorName,
      donorNumber,
      foodName,
      foodType,
      foodImage,
      description,
      expiryDate,
      location
    };

    // Save the donation to localStorage
    let donations = JSON.parse(localStorage.getItem('donations')) || [];
    donations.push(donation);
    localStorage.setItem('donations', JSON.stringify(donations));

    // Display success message
    alert('Thank you for your donation!');
    form.reset();
    document.getElementById('image-preview').innerHTML = ''; // Clear image preview
  });

  // Preview image after selection
  foodImageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const previewContainer = document.getElementById('image-preview');
    previewContainer.innerHTML = ''; // Clear previous preview

    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const img = document.createElement('img');
        img.src = reader.result;
        previewContainer.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });
});

    const file = foodImageInput.files[0];
    if (file && file.size > 10 * 1024 * 1024) {
      alert('Food image size must be less than 10MB');
      return;
    }

    // Ensure all fields are filled
    const inputs = form.querySelectorAll('input, select, textarea');
    for (const input of inputs) {
      if (!input.value) {
        alert(`Please fill out the ${input.previousElementSibling.textContent} field`);
        input.focus();
        return;
      }
    }

    // Collect form data
    const donorName = document.getElementById('donorName').value;
    const donorNumber = document.getElementById('donorNumber').value;
    const foodName = document.getElementById('foodName').value;
    const foodType = document.getElementById('foodType').value;
    const foodImage = foodImageInput.files[0] ? URL.createObjectURL(foodImageInput.files[0]) : '';
    const description = document.getElementById('description').value;
    const expiryDate = document.getElementById('expiryDate').value;
    const location = document.getElementById('location').value;

    // Create a donation object
    const donation = {
      donorName,
      donorNumber,
      foodName,
      foodType,
      foodImage,
      description,
      expiryDate,
      location
    };

    // Save the donation to localStorage
    let donations = JSON.parse(localStorage.getItem('donations')) || [];
    donations.push(donation);
    localStorage.setItem('donations', JSON.stringify(donations));

    // Display success message
    alert('Thank you for your donation!');
    form.reset();
    document.getElementById('image-preview').innerHTML = ''; // Clear image preview
  });

  // Preview image after selection
  foodImageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const previewContainer = document.getElementById('image-preview');
    previewContainer.innerHTML = ''; // Clear previous preview

    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const img = document.createElement('img');
        img.src = reader.result;
        previewContainer.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });
