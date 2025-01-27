document.addEventListener('DOMContentLoaded', () => {
  const tableBody = document.getElementById('historyTable');
  const history = JSON.parse(localStorage.getItem('donationHistory')) || [];
  const now = new Date();

  // Clean old history
  const recentHistory = history.filter((entry) => {
    const deleteDate = new Date(entry.deletedDate);
    return now - deleteDate <= 5 * 24 * 60 * 60 * 1000; // 5 days in milliseconds
  });

  localStorage.setItem('donationHistory', JSON.stringify(recentHistory));

  // Populate table
  recentHistory.forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.foodName}</td>
      <td>${entry.foodType}</td>
      <td>${entry.description}</td>
      <td>${new Date(entry.deletedDate).toLocaleDateString()}</td>
    `;
    tableBody.appendChild(row);
  });
});
