// 

async function processForm(evt) {
    evt.preventDefault();

    const formData = {
        city: $('#city').val(),
        state: $('#state').val(),
        country: $('#country').val(),
        date: $('#date').val()
    };

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        const data = await response.json();
        handleResponse(data);
    } catch (error) {
        console.error(error);
    }
}

function handleResponse(resp) {
    const location = resp.location;
    const date = resp.date;
    const sunrise = resp.sunrise;
    const sunset = resp.sunset;
    const dayLength = resp.day_length;
    const moonrise = resp.moonrise;
    const moonset = resp.moonset;

    $('#location').text(`Location: ${location.city}, ${location.state}, ${location.country}`);
    $('#date').text(`Date: ${date}`);
    $('#sunrise').text(`Sunrise: ${sunrise}`);
    $('#sunset').text(`Sunset: ${sunset}`);
    $('#day-length').text(`Day Length: ${dayLength}`);
    $('#moonrise').text(`Moonrise: ${moonrise}`);
    $('#moonset').text(`Moonset: ${moonset}`);
}

$("#search-form").on("submit", processForm);
