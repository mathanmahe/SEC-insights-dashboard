function loadData() {
    var ticker = document.getElementById('ticker').value;
    var year = document.getElementById('year').value;
    console.log('Loading data for:', ticker, year);
    fetch('loadData/', {
        method: 'POST',
        body: JSON.stringify({
            ticker: ticker,
            year: year
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data loaded:', data)
        displayInsights(data.insights);
        displayImages(data.images);
    })
    .catch(error => console.error('Error loading data:', error));
}

function displayInsights(insights) {
    const insightsContainer = document.getElementById('insights');
    insightsContainer.innerHTML = insights;
}

function displayImages(images) {
    const visualizationsContainer = document.getElementById('visualizations');
    visualizationsContainer.innerHTML = ''; // Clear previous images
    images.forEach(imageBase64 => {
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${imageBase64}`;
        visualizationsContainer.appendChild(img);
    });
}