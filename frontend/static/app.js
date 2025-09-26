// Frontend JavaScript functions
const API_BASE_URL = 'http://localhost:5646';

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        displayOutput(`<h3>Health Response:</h3><p>${data.message}</p>`);
    } catch (error) {
        displayOutput(`<h3>Error:</h3><p>Failed to fetch hello message: ${error.message}</p>`);
    }
}

async function fetchData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/data`);
        const result = await response.json();
        
        let html = '<h3>Data from Backend:</h3>';
        result.data.forEach(item => {
            html += `<div class="data-item">ID: ${item.id}, Name: ${item.name}</div>`;
        });
        
        displayOutput(html);
    } catch (error) {
        displayOutput(`<h3>Error:</h3><p>Failed to fetch data: ${error.message}</p>`);
    }
}

function displayOutput(content) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = content;
}

function clearOutput() {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '';
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask Web App loaded successfully!');
});