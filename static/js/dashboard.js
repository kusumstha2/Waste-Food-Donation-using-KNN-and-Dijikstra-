// Get elements
const logoutLink = document.querySelector('a[href="#logout"]');
const logoutModal = document.getElementById('logoutModal');
const confirmLogout = document.getElementById('confirmLogout');
const cancelLogout = document.getElementById('cancelLogout');

const donateButton = document.querySelector('.donate-btn');
const donateModal = document.getElementById('donateModal');
const modalBody = document.getElementById('modalBody');

const profileLink = document.querySelector('a[href="#profile"]');
const profileModal = document.getElementById('profileModal');
const profileModalBody = document.getElementById('profileModalBody');

// Function to disable/enable body scroll
// const disableBodyScroll = () => (document.body.style.overflow = 'hidden');
// const enableBodyScroll = () => (document.body.style.overflow = '');

// Initialize Donate Form Logic
const initializeDonateForm = () => {
  const form = document.querySelector('.donate-form');
  const foodImageInput = document.getElementById('foodImage');
  const expiryDateInput = document.getElementById('expiryDate');

  if (!form || !foodImageInput || !expiryDateInput) return;

  // Set minimum expiry date
  expiryDateInput.setAttribute('min', new Date().toISOString().split('T')[0]);

  // Preview image logic
  foodImageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const previewContainer = document.getElementById('image-preview');
    previewContainer.innerHTML = '';

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

  // Form submit logic
  form.addEventListener('submit', (e) => {
    e.preventDefault();
  
    // Validate file size
    const file = foodImageInput.files[0];
    if (file && file.size > 10 * 1024 * 1024) {
      alert('Food image size must be less than 10MB');
      return;
    }
  
    // Convert file to Base64 if it exists
    let imageData = '';
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        imageData = reader.result; // Base64 encoded image
        // Collect and store data
        const donation = {
          donorName: form.donorName.value,
          donorNumber: form.donorNumber.value,
          foodName: form.foodName.value,
          foodType: form.foodType.value,
          foodImage: imageData, // Store Base64 image
          description: form.description.value,
          expiryDate: form.expiryDate.value,
          location: form.location.value,
        };
  
        const donations = JSON.parse(localStorage.getItem('donations')) || [];
        donations.push(donation);
        localStorage.setItem('donations', JSON.stringify(donations));
  
        alert('Thank you for your donation!');
        form.reset();
        document.getElementById('image-preview').innerHTML = '';
      };
      reader.readAsDataURL(file); // Convert image to Base64
    }
  });
  
};

// Handle Donate Button Click
donateButton.addEventListener('click', () => {
  // Fetch content from donate.html
  fetch('/donate/')
    .then((response) => response.text())
    .then((html) => {
      modalBody.innerHTML = html; // Inject HTML
      donateModal.style.display = 'flex'; // Show modal
      disableBodyScroll(); // Disable scrolling

      initializeDonateForm(); // Reinitialize logic
    })
    .catch((error) => console.error('Error loading donate.html:', error));
});

// Close the modal when clicking outside the modal content
window.addEventListener('click', (event) => {
  if (event.target === donateModal) {
    donateModal.style.display = 'none';
    modalBody.innerHTML = ''; // Clear content
    enableBodyScroll(); // Enable scrolling
  }
});

// Handle Profile Modal
profileLink.addEventListener('click', (event) => {
  event.preventDefault();
  fetch('profile.html')
    .then((response) => response.text())
    .then((html) => {
      profileModalBody.innerHTML = html;

      const userData = JSON.parse(localStorage.getItem('userData')) || {};
      const profilePic = document.getElementById('profilePic');

      // Populate user data
      profilePic.src = userData.profileImage || '../photo/profile.jpg';
      document.getElementById('userName').textContent = userData.name || 'Guest';
      document.getElementById('userEmail').textContent = userData.email || '';
      document.getElementById('userPhone').textContent = userData.phone || '';
      document.getElementById('userAddress').textContent = userData.address || '';

      // Handle profile picture update
      const fileInput = document.getElementById('changeProfilePic');
      profilePic.addEventListener('click', () => fileInput.click());
      fileInput.addEventListener('change', (event) => {
        const newPic = event.target.files[0];
        if (newPic) {
          const reader = new FileReader();
          reader.onloadend = () => {
            profilePic.src = reader.result;
            userData.profileImage = reader.result;
            localStorage.setItem('userData', JSON.stringify(userData));
          };
          reader.readAsDataURL(newPic);
        }
      });

      profileModal.style.display = 'flex';
    })
    .catch((error) => console.error('Error loading profile.html:', error));
});

// Close the profile modal when clicking outside
window.addEventListener('click', (event) => {
  if (event.target === profileModal) {
    profileModal.style.display = 'none';
    profileModalBody.innerHTML = ''; // Clear content
    enableBodyScroll();
  }
});

// Logout Modal Logic
logoutLink.addEventListener('click', (event) => {
  event.preventDefault();
  logoutModal.style.display = 'flex';
});

cancelLogout.addEventListener('click', () => {
  logoutModal.style.display = 'none';
});

confirmLogout.addEventListener('click', () => {
  logoutModal.style.display = 'none';
  window.location.href = 'login.html';
});
// // Get elements
// if (typeof logoutLink === 'undefined') {
// const logoutLink = document.querySelector('a[href="#logout"]');
// const logoutModal = document.getElementById('logoutModal');
// const confirmLogout = document.getElementById('confirmLogout');
// const cancelLogout = document.getElementById('cancelLogout');

// const donateButton = document.querySelector('.donate-btn');
// const donateModal = document.getElementById('donateModal');
// const modalBody = document.getElementById('modalBody');

// const profileLink = document.querySelector('a[href="#profile"]');
// const profileModal = document.getElementById('profileModal');
// const profileModalBody = document.getElementById('profileModalBody');

const chooseLocationLink = document.querySelector('a[href="#choose-location"]');
const locationModal = document.getElementById('locationModal');
const locationModalBody = document.getElementById('locationModalBody');

// Function to disable/enable body scroll
const disableBodyScroll = () => (document.body.style.overflow = 'hidden');
const enableBodyScroll = () => (document.body.style.overflow = '');

// Handle Location Modal
if (chooseLocationLink) {
  chooseLocationLink.addEventListener('click', (event) => {
    event.preventDefault();
    locationModal.style.display = 'flex';
    disableBodyScroll();
  });

  // Close the location modal when clicking outside
  window.addEventListener('click', (event) => {
    if (event.target === locationModal) {
      locationModal.style.display = 'none';
      enableBodyScroll();
    }
  });

  // Handle location form submission
  const locationForm = document.getElementById('locationForm');
  locationForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const location = document.getElementById('location').value;
    alert(`Location set to: ${location}`);
    localStorage.setItem('userLocation', location);
    locationModal.style.display = 'none';
    enableBodyScroll();
  });
}

// Other modals (Donate, Profile, Logout) remain unchanged...
// logoutLink.addEventListener('click', (event) => {
//   event.preventDefault();
//   logoutModal.style.display = 'flex';
// });

// cancelLogout.addEventListener('click', () => {
//   logoutModal.style.display = 'none';
// });

// confirmLogout.addEventListener('click', () => {
//   logoutModal.style.display = 'none';
//   window.location.href = 'login.html';
// });
