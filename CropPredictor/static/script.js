// FORM SUBMISSION LOGIC
document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get input values
    const nitrogen = document.getElementById('nitrogen').value;
    const phosphorus = document.getElementById('phosphorus').value;
    const potassium = document.getElementById('potassium').value;
    const temperature = document.getElementById('temperature').value;
    const humidity = document.getElementById('humidity').value;
    const ph = document.getElementById('ph').value;
    const rainfall = document.getElementById('rainfall').value;

    // Send to backend
    fetch('/predict-farming', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            N: nitrogen,
            P: phosphorus,
            K: potassium,
            temperature: temperature,
            humidity: humidity,
            ph: ph,
            rainfall: rainfall
        }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.predicted_crop) {
            resultDiv.innerHTML = `🌱 <strong>Predicted Crop:</strong> ${data.predicted_crop}`;
        } else {
            resultDiv.innerHTML = `⚠️ Error retrieving prediction`;
        }

        // Save to localStorage (history)
        const history = JSON.parse(localStorage.getItem('history')) || [];
        history.push({
            date: new Date().toLocaleString(),
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall,
            predicted_crop: data.predicted_crop || 'Unknown'
        });
        localStorage.setItem('history', JSON.stringify(history));
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = '⚠️ Network error or server not responding.';
    });
});


// LOAD HISTORY ON history.html
if (document.getElementById('history-table')) {
    const history = JSON.parse(localStorage.getItem('history')) || [];
    const tbody = document.getElementById('history-table').getElementsByTagName('tbody')[0];

    history.forEach(record => {
        const row = tbody.insertRow();
        row.insertCell(0).innerText = record.date;
        row.insertCell(1).innerText = record.nitrogen;
        row.insertCell(2).innerText = record.phosphorus;
        row.insertCell(3).innerText = record.potassium;
        row.insertCell(4).innerText = record.temperature;
        row.insertCell(5).innerText = record.humidity;
        row.insertCell(6).innerText = record.ph;
        row.insertCell(7).innerText = record.rainfall;
        row.insertCell(8).innerText = record.predicted_crop;
    });
}
