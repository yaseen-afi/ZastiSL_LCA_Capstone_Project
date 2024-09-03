document.addEventListener('DOMContentLoaded', function() {
    const resultsTab = document.getElementById('results-tab');
    const scenariosTab = document.getElementById('scenarios-tab');
    const loader = document.querySelector('.loader');

    // Set current date in the Created Date input field
    const newCreatedDateField = document.getElementById('newCreatedDate');
    if (newCreatedDateField) {
        newCreatedDateField.value = new Date().toLocaleDateString();
    }

    // Get the current page's filename
    const currentPage = window.location.pathname.split('/').pop();

    // Redirect index.html to results.html
    if (currentPage === 'index.html' || currentPage === '') {
        window.location.href = 'results.html';
        return; // Stop further script execution
    }

    // Set the active tab based on the current page
    if (currentPage === 'results.html' && resultsTab) {
        resultsTab.classList.add('active');
        scenariosTab.classList.remove('active');
    } else if (currentPage === 'scenarios.html' && scenariosTab) {
        scenariosTab.classList.add('active');
        resultsTab.classList.remove('active');
    }

    // Show loader on page load
    if (loader) {
        loader.style.display = 'none';
        window.addEventListener('load', function () {
            loader.style.display = 'none';
        });
    }

    // Handle page navigation with loader
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            if (loader) loader.style.display = 'block';
            setTimeout(() => {
                window.location.href = this.href;
            }, 500); // Delay to simulate loading
        });
    });

    // Tab navigation function
    window.navigateToNewTab = function(tabId) {
        const tabTrigger = new bootstrap.Tab(document.querySelector(`a[href="#${tabId}"]`));
        tabTrigger.show();
    };

    window.saveAndGenerateNewScenario = function() {
        console.log("Save and Generate button clicked");
    
        // Show the loader
        const loader = document.querySelector('.loader');
        if (loader) {
            loader.style.display = 'block';
            console.log("Loader displayed");
        }
    
        // Delay to allow the loader to appear before redirection
        setTimeout(() => {
            console.log("Redirecting to results page");
            window.location.href = 'results.html';
        }, 500);
    };


    //Emmission factors mongodb RESTAPIs
    document.addEventListener('DOMContentLoaded', function() {
        const endpoint = 'http://127.0.0.1:8000/v1/emissions';
    
        // Fetch data from the FastAPI endpoint and populate the table
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('emissionFactorsTableBody');
                data.forEach((item, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${item.name}</td>
                        <td><input type="number" class="form-control" name="value" value="${item.value}" data-id="${item.id}" data-index="${index}"></td>
                        <td>${item.unit}</td>
                        <td>${item.source}</td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching emission factors:', error));
    });
    
    function cancelEdit() {
        window.location.reload(); // Reload the page to cancel changes
    }
    
    function saveEmissionFactors() {
        const tableBody = document.getElementById('emissionFactorsTableBody');
        const rows = tableBody.querySelectorAll('tr');
        const updatedData = [];
    
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            updatedData.push({
                id: cells[1].querySelector('input').getAttribute('data-id'),
                name: cells[0].innerText,
                value: parseFloat(cells[1].querySelector('input').value),
                unit: cells[2].innerText,
                source: cells[3].innerText
            });
        });
    
        // Send updated data to the FastAPI endpoint
        fetch('http://127.0.0.1:8000/v1/emissions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Emission factors updated successfully');
            // Optionally, reload the data from the server to reflect changes
            window.location.reload();
        })
        .catch(error => console.error('Error saving emission factors:', error));
    }
    
    function getLandAreaInHectares() {
        const landArea = parseFloat(document.getElementById('newFarmLandArea').value);
        const areaUnit = document.getElementById('newAreaUnit').value;
        return areaUnit === 'acres' ? landArea / 1000 : landArea;
    }
    
    function buildPayload() {
        const landAreaHectares = getLandAreaInHectares();
    
        const rawMaterialsInputs = [
            { name: "Seed Production", amount: parseFloat(document.querySelector('#raw-material-stage .amount-column input[data-id="seed-production"]').value) },
            { name: "Fertilizer Production Urea-N", amount: parseFloat(document.querySelector('#raw-material-stage .amount-column input[data-id="fertilizer-production-urea"]').value) },
            // Add other raw materials...
        ];
    
        const manufacturingInputs = [
            { name: "Electricity", amount: parseFloat(document.querySelector('#manufacturing-stage .amount-column input[data-id="electricity"]').value) },
            // Add other manufacturing inputs...
        ];
    
        const transportationInputs = [
            { name: "Transportation, light commercial vehicle", amount: parseFloat(document.querySelector('#transportation-stage .amount-column input[data-id="transport-light-commercial"]').value) },
            // Add other transportation inputs...
        ];
    
        return {
            land_area_hectares: landAreaHectares,
            inputs: [
                { stage: "Raw Materials", inputs: rawMaterialsInputs },
                { stage: "Manufacturing", inputs: manufacturingInputs },
                { stage: "Transportation", inputs: transportationInputs },
            ]
        };
    }
    
    function buildPayload() {
        const landAreaHectares = getLandAreaInHectares();
    
        const rawMaterialsInputs = [
            { name: "Seed Production", amount: parseFloat(document.querySelector('#raw-material-stage .amount-column input[data-id="seed-production"]').value) },
            { name: "Fertilizer Production Urea-N", amount: parseFloat(document.querySelector('#raw-material-stage .amount-column input[data-id="fertilizer-production-urea"]').value) },
            // Add other raw materials...
        ];
    
        const manufacturingInputs = [
            { name: "Electricity", amount: parseFloat(document.querySelector('#manufacturing-stage .amount-column input[data-id="electricity"]').value) },
            // Add other manufacturing inputs...
        ];
    
        const transportationInputs = [
            { name: "Transportation, light commercial vehicle", amount: parseFloat(document.querySelector('#transportation-stage .amount-column input[data-id="transport-light-commercial"]').value) },
            // Add other transportation inputs...
        ];
    
        return {
            land_area_hectares: landAreaHectares,
            inputs: [
                { stage: "Raw Materials", inputs: rawMaterialsInputs },
                { stage: "Manufacturing", inputs: manufacturingInputs },
                { stage: "Transportation", inputs: transportationInputs },
            ]
        };
    }
    


});
