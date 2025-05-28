document.addEventListener("DOMContentLoaded", () => {
  const accessToken = localStorage.getItem("access_token");
  const userEmail = localStorage.getItem("user_email");
  const navbarUserArea = document.getElementById("navbarUserArea");

  if (accessToken && userEmail && navbarUserArea) {
    navbarUserArea.innerHTML = `
      <span class="text-white me-3">👋 Hello, ${userEmail}</span>
      <button class="btn btn-danger" onclick="clearSessionData()">Log Out</button>
    `;
  }
});