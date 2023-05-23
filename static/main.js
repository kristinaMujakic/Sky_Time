const currentDate = new Date();
const defaultDate = currentDate.toISOString().split('T')[0];

$(function () {
    $('#date').val(defaultDate);

    // select all options
    $('#select-all').change(function () {
        const isChecked = $(this).prop('checked');

        // toggle based on the "Select All" checkbox
        $('.options input[type="checkbox"]').not(this).prop({
            disabled: isChecked,
            checked: isChecked ? true : false
        });
    });
});

async function processForm(evt) {
    evt.preventDefault();

    const formData = {
        city: $('#city').val(),
        country: $('#country').val(),
        date: $('#date').val(),
        selectAll: $('#select-all').val(),
        // saveSearch: $('#save-search').prop('checked')
    };

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        // if (formData.saveSearch) {
        //     saveSearchToFavorites(formData);
        // }

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf('application/json') !== -1) {
            const data = await response.json();
            handleResponse(data);
        } else {
            throw new Error('Response is not valid JSON');
        }
    } catch (error) {
        console.error(error);
    }
}

function handleResponse(resp) {
    const sunrise = resp.sunrise;
    const sunset = resp.sunset;
    const dayLength = resp.day_length;
    const moonrise = resp.moonrise;
    const moonset = resp.moonset;

    if ($('#sunrise').is(':checked') || $('#select-all').is(':checked')) {
        $('#sunrise-info').text(`Sunrise: ${sunrise}`);
    } else {
        $('#sunrise-info').empty();
    }

    if ($('#sunset').is(':checked') || $('#select-all').is(':checked')) {
        $('#sunset-info').text(`Sunset: ${sunset}`);
    } else {
        $('#sunset-info').empty();
    }

    if ($('#day-length').is(':checked') || $('#select-all').is(':checked')) {
        $('#day-length-info').text(`Day Length: ${dayLength}`);
    } else {
        $('#day-length-info').empty();
    }

    if ($('#moonrise').is(':checked') || $('#select-all').is(':checked')) {
        $('#moonrise-info').text(`Moonrise: ${moonrise}`);
    } else {
        $('#moonrise-info').empty();
    }

    if ($('#moonset').is(':checked') || $('#select-all').is(':checked')) {
        $('#moonset-info').text(`Moonset: ${moonset}`);
    } else {
        $('#moonset-info').empty();
    }
}

$("#search-form").on("submit", processForm);
