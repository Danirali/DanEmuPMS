document.addEventListener('DOMContentLoaded', async() => {
    loadSection('propertyNav')
    document.getElementById("formMessage").textContent = '';
})

function loadSection(domain) {
    navOption = document.getElementById(domain)
    navOptionLabel = document.getElementById(domain + "Label")

    navOptions = ['propertyNav','incomeNav','expensesNav']

    navOptions.forEach(option => {
        document.getElementById(option).style.display = 'none';
        document.getElementById(option + "Label").classList.remove('active');
    });

    document.getElementById(domain).style.display = 'block';
    document.getElementById(domain + "Label").classList.add('active');
}

document.getElementById("propertyForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let name = document.getElementById("name").value;
    let value = document.getElementById("value").value;
    let unit = document.getElementById("unit").value;

    let response = await fetch("/api/add_property", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, value, unit })
    });

    let result = await response.json();
    document.getElementById("formMessage").textContent = result.message;

    if (response.ok) {
        document.getElementById("propertyForm").reset();
    }
});