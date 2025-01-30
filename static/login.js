document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault(); 

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      window.location.href = "/dashboard"; // Redirect on success
    } else {
      console.log("Login failed:", data.error);
      document.getElementById("login-error-msg-box").textContent = "Incorrect username or password. Please try again.";
      document.getElementById("login-error-msg-box").style.padding = "1em";
    }
  });
});