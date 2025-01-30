document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript Loaded!"); // Debugging

  document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Stop normal form submission
    console.log("Login Form Submitted!"); // Debugging

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    console.log("Username:", username); // Debugging
    console.log("Password:", password); // Debugging

    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      console.log("Login successful! Redirecting...");
      window.location.href = "/dashboard"; // Redirect on success
    } else {
      console.log("Login failed:", data.error);
      alert(data.error); // Show error message
    }
  });
});
