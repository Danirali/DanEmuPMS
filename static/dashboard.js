document.addEventListener('DOMContentLoaded', async () => {
    loadSection('propertyNav');
    fetchProperties('income_property_id');
    fetchProperties('expense_property_id');

    try {
        const response = await fetch("/api/income/net"); // Replace with your API endpoint
        const data = await response.json();

        const netIncome = data.net_income;
        const expenses = data.expenses;  // Assuming your API returns expenses too

        const ctx = document.getElementById("netIncome_donut").getContext("2d");

        new Chart(ctx, {
            type: "doughnut", // Ring chart (donut) type
            data: {
                labels: ["Net Income", "Expenses"],
                datasets: [
                    {
                        data: [netIncome, expenses],
                        backgroundColor: ["#4CAF50", "#FF5252"],
                        hoverBackgroundColor: ["#66BB6A", "#FF1744"],
                    },
                ],
            },
            options: {
                responsive: true,
                cutout: "60%", // Creates the ring effect
                plugins: {
                    legend: { position: "bottom" },
                },
            },
        });
    } catch (error) {
        console.error("Error fetching net income data:", error);
    }
})

function loadSection(domain) {
    let navOption = document.getElementById(domain);
    let navOptionLabel = document.getElementById(domain + "Label");
    navOptions = ['propertyNav', 'incomeNav', 'expensesNav']

    navOptions.forEach(option => {
        document.getElementById(option).style.display = 'none';
        document.getElementById(option + "Label").classList.remove('active');
    });

    navOptionLabel.classList.add('active');
    navOption.style.display = 'block';

    document.getElementById('formMessage').innerHTML = '';

    Array.from(document.getElementsByClassName('btn')).forEach(button => {
        button.classList.remove('bg-success');
        button.classList.remove('bg-danger');
    });
}

async function fetchProperties(element_id) {
    let response = await fetch("/api/properties");  // Fetch properties from backend
    let properties = await response.json();
    let propertyDropdown = document.getElementById(element_id);

    // Clear existing options
    propertyDropdown.innerHTML = '<option value="">Select a Property</option>';

    // Populate dropdown with property names but store their IDs
    properties.forEach(property => {
        let option = document.createElement("option");
        option.value = property.id;  // Set the property ID as the value
        option.textContent = property.name;  // Show the property name
        propertyDropdown.appendChild(option);
    });


}

document.getElementById("incomeForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    let name = document.getElementById("incomeName").value;
    let amount = document.getElementById("incomeAmount").value;
    let date = document.getElementById("income_date").value;
    let property_id = document.getElementById("income_property_id").value;
    let extra = document.getElementById("income_extra").value;

    let response = await fetch("/api/income/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, amount, date, property_id, extra })
    });

    let result = await response.json();

    if (response.ok) {
        document.getElementById("incomeSubmitBtn").classList.add('bg-success');
        document.getElementById("incomeForm").reset();
    } else {
        document.getElementById("incomeSubmitBtn").classList.add('bg-danger');
    }
});

document.getElementById("propertyForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    let name = document.getElementById("name").value;
    let value = document.getElementById("value").value;
    let unit = document.getElementById("unit").value;

    let response = await fetch("/api/properties/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, value, unit })
    });

    let result = await response.json();

    if (response.ok) {
        document.getElementById("propertySubmitBtn").classList.add('bg-success');
        document.getElementById("propertyForm").reset();
    } else {
        document.getElementById("incomeSubmitBtn").classList.add('bg-danger');
    }
});



document.getElementById("expenseForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    let name = document.getElementById("expenseName").value;
    let amount = document.getElementById("expenseAmount").value;
    let category = document.getElementById("category").value;
    let property_id = document.getElementById("expense_property_id").value;
    let extra = document.getElementById("expense_extra").value;


    try {
        let response = await fetch("/api/expenses/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, amount, category, property_id, extra })
        });

        let result = await response.json();

        if (response.ok) {
            document.getElementById("expenseSubmitBtn").classList.add('bg-success');
            document.getElementById("expenseForm").reset();
        } else {
            document.getElementById("incomeSubmitBtn").classList.add('bg-danger');
        }
    } catch (error) {
        document.getElementById("formMessage").textContent = "Error: Could not add expense.";
    }
});