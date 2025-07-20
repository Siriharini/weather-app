document.addEventListener('DOMContentLoaded', () => {
    const cityInput = document.getElementById('cityInput');
    const searchBtn = document.getElementById('searchBtn');
    const messageDisplay = document.getElementById('message');
    const weatherCard = document.getElementById('weatherCard');
    const locationElement = document.getElementById('location');
    const temperatureElement = document.getElementById('temperature');
    const descriptionElement = document.getElementById('description');
    const weatherIconElement = document.getElementById('weatherIcon');
    const humidityElement = document.getElementById('humidity');
    const windSpeedElement = document.getElementById('windSpeed');

    const BACKEND_URL = 'http://127.0.0.1:5000/weather';

    function displayMessage(msg, isError = false) {
        messageDisplay.textContent = msg;
        messageDisplay.style.color = isError ? '#ffdddd' : 'rgba(255, 255, 255, 0.8)';
        weatherCard.classList.add('hidden');
    }

    function displayWeatherData(data) {
        locationElement.textContent = `${data.city}, ${data.country}`;
        temperatureElement.textContent = `${Math.round(data.temperature)}°C`;
        descriptionElement.textContent = data.description;
        weatherIconElement.src = `http://openweathermap.org/img/wn/${data.icon}@2x.png`;
        weatherIconElement.alt = data.description;
        humidityElement.textContent = `${data.humidity}%`;
        windSpeedElement.textContent = `${data.wind_speed} m/s`;

        messageDisplay.textContent = '';
        weatherCard.classList.remove('hidden');
    }

    async function fetchWeather() {
        const city = cityInput.value.trim();
        if (!city) {
            displayMessage("Please enter a city name.");
            return;
        }

        displayMessage("Fetching weather data...", false);

        try {
            const response = await fetch(`${BACKEND_URL}?city=${encodeURIComponent(city)}`);
            const data = await response.json();

            if (!response.ok) {
                displayMessage(`Error: ${data.error || 'Something went wrong.'}`, true);
                console.error('Backend Error:', data);
                return;
            }

            displayWeatherData(data);

        } catch (error) {
            displayMessage("Could not connect to the weather service. Please ensure the Python backend is running.", true);
            console.error('Fetch error:', error);
        }
    }

    searchBtn.addEventListener('click', fetchWeather);

    cityInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            fetchWeather();
        }
    });
});