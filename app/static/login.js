document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/query/login");
    const data = await response.json();

    if (response.ok && data.status === 'success') {
      const loginBtn = document.getElementById("loginBtn");
      loginBtn.textContent = "Dashboard";
      loginBtn.setAttribute("data-bs-target", "");
      loginBtn.innerHTML = "<a style='text-decoration: none; color: black;' href='/dashboard'>Dashboard</a>";
    }
  } catch (error) {
    console.error("Error fetching login status:", error);
  }


  document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorBox = document.getElementById("login-error-msg-box");

    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        window.location.href = "/dashboard";
      } else {
        console.warn("Login failed:", data.error);
        errorBox.textContent = "Incorrect username or password. Please try again.";
        errorBox.style.padding = "1em";
      }
    } catch (error) {
      console.error("Login request error:", error);
      errorBox.textContent = "An error occurred. Please try again later.";
      errorBox.style.padding = "1em";
    }
  });
});
