document.addEventListener('DOMContentLoaded', async() => {
    loadSection('propertiesNav')
})

let propertyForm = document.getElementById('propertyForm');

function loadSection(domain) {
    let navOption = document.getElementById(domain);
    let propertyNav = document.getElementById('propertyNavLabel');
    let incomeNav = document.getElementById('incomeNavLabel');
    let expensesNav = document.getElementById('expensesNavLabel');

    propertyNav.setAttribute('class','flex-sm-fill text-sm-center nav-link')
    incomeNav.setAttribute('class','flex-sm-fill text-sm-center nav-link')
    expensesNav.setAttribute('class','flex-sm-fill text-sm-center nav-link')

    navOption.setAttribute('class','flex-sm-fill text-sm-center nav-link active')
    navOption.style.display = 'block';
}