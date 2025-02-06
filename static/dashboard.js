document.addEventListener('DOMContentLoaded', async () => {
    loadSection('propertyNav');
    loadSection('viewPropertyNav');
    fetchProperties('income_property_id');
    fetchProperties('expense_property_id');
    fetchTables();
    countProperties();
});

function loadSection(domain) {
    let navOption = document.getElementById(domain);
    let navOptionLabel = document.getElementById(domain + "Label");
    navOptions = ['propertyNav', 'incomeNav', 'expensesNav', 'viewPropertyNav', 'viewIncomeNav', 'viewExpensesNav']

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

    fetchTables();
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

async function fetchIncomesTable() {
    try {
        const response = await fetch('/api/income');
        const incomes = await response.json();
        const tableBody = document.querySelector('#incomesTable tbody');
        tableBody.innerHTML = '';

        incomes.forEach(income => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${income.name}</td>
                <td>${income.amount}</td>
                <td>${income.date}</td>
                <td>${income.extra}</td>
                <td><button class="btn btn-danger" onclick="deleteitem(${income.id},'income')">Delete</button></td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching incomes:", error);
    }
}

async function fetchPropertiesTable() {
    try {
        const response = await fetch('/api/properties');
        const properties = await response.json();
        const tableBody = document.querySelector('#propertiesTable tbody');
        tableBody.innerHTML = '';

        properties.forEach(property => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${property.name}</td>
                <td>${property.value}</td>
                <td>${property.unit}</td>
                <td><button class="btn btn-danger" onclick="deleteitem(${property.id},'properties')">Delete</button></td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching properties:", error);
    }
}

async function fetchExpensesTable() {
    try {
        const response = await fetch('/api/expenses');
        const expenses = await response.json();
        const tableBody = document.querySelector('#expensesTable tbody');
        tableBody.innerHTML = '';

        expenses.forEach(expense => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${expense.name}</td>
                <td>${expense.amount}</td>
                <td>${expense.extra}</td>
                <td><button class="btn btn-danger" onclick="deleteitem(${expense.id},'expenses')">Delete</button></td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching properties:", error);
    }
}

async function deleteitem(id, api) {
    if (!confirm("Are you sure you want to delete this item?")) return;

    try {
        const response = await fetch(`/api/${api}/delete/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        alert(result.message);

        if (response.ok) {
            fetchExpensesTable()
            fetchIncomesTable()
            fetchPropertiesTable()
        }
    } catch (error) {
        console.error("Error deleting item:", error);
        alert("Could not delete item.");
    }
}

function fetchTables() {
    fetchExpensesTable();
    fetchIncomesTable();
    fetchPropertiesTable();
}

async function countProperties() {
    let response = await fetch("/api/properties");  // Fetch properties from backend
    let properties = await response.json();
    let propertyCount = 0;
    let output = document.getElementById('propertiesCount');
    let no_data = document.getElementById('propertiesCount_no-data');

    output.innerHTML = 'No Properties';

    properties.forEach(property => {
        propertyCount = propertyCount + 1
    });

    no_data.style.display = 'none';
    output.innerHTML = '<b>' + propertyCount + '</b>'
}