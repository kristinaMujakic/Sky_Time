const currentDate = new Date();
const defaultDate = currentDate.toISOString().split('T')[0];

$(function () {
    $('#date').val(defaultDate);

    $('#select-all').change(function () {
        const isChecked = $(this).prop('checked');

        $('.toggle input[type="checkbox"]').not(this).prop({
            disabled: isChecked,
            checked: isChecked ? true : false
        });

        $('#fav-toggle').not(this).prop({
            disabled: isChecked,
            checked: isChecked ? true : false
        });
    });

    $("#get-sky-time-btn").on("click", processForm);

    $(".toggle").on("change", function () {
        const selectedCheckboxes = $(".toggle:checked");
        const selectedData = [];

        selectedCheckboxes.each(function () {
            const city = $(this).data("city");
            const country = $(this).data("country");
            selectedData.push({ city, country });
        });

        processSelectedData(selectedData);
    });

    $("#get-btn-fav").on("click", async function (evt) {
        evt.preventDefault();

        const selectedData = [];

        // Loop through selected checkboxes and prepare the selected data
        $(".list-toggle:checked").each(function () {
            const city = $(this).data("city");
            const country = $(this).data("country");

            selectedData.push({
                city: city,
                country: country
            });
        });

        // Call the function to process selected data
        await processSelectedData(selectedData);
    });
});

async function processForm(evt) {
    evt.preventDefault();

    const city = $('#city').val();
    const country = $('#country').val();
    const selectedCheckboxes = $(".toggle input[type='checkbox']:checked");

    if (city.trim() === '' || country.trim() === '') {
        flashErrorMessage("Please enter a city and a country.");
        return;
    } else {
        hideErrorMessage();
    }

    if (selectedCheckboxes.length === 0) {
        flashErrorMessage("Please select at least one option.");
    } else {
        hideErrorMessage();

        const formData = {
            city: city,
            country: country,
            date: $('#date').val(),
            selectAll: $('#select-all').prop('checked'),
        };

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

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
            console.log(error);
        }
    }
}

async function processSelectedData(selectedData) {
    try {
        const response = await fetch('/get_selected_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(selectedData)
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        const contentType = response.headers.get('content-type');

        if (contentType && contentType.indexOf('application/json') !== -1) {
            const data = await response.json();
            handleSelectedData(data);
        } else {
            throw new Error('Response is not valid JSON');
        }

    } catch (error) {
        console.log(error);
    }
}

function handleResponse(resp) {
    const fields = [
        { id: 'sunrise', infoId: 'sunrise-info', label: 'Sunrise' },
        { id: 'sunset', infoId: 'sunset-info', label: 'Sunset' },
        { id: 'day_length', infoId: 'day-length-info', label: 'Day Length' },
        { id: 'moonrise', infoId: 'moonrise-info', label: 'Moonrise' },
        { id: 'moonset', infoId: 'moonset-info', label: 'Moonset' },
    ];

    for (const field of fields) {
        const value = resp[field.id];
        const isChecked = $(`#${field.id}`).is(':checked') || $('#select-all').is(':checked');
        const displayValue = value === '-:-' ? 'Unavailable' : value;

        if (isChecked) {
            $(`#${field.infoId}`).text(`${field.label}: ${displayValue}`);
        } else {
            $(`#${field.infoId}`).empty();
        }
    }
}

function handleSelectedData(data) {

    $('#selected-data').empty();

    const fields = [
        { id: 'sunrise', infoId: 'sunrise-info', label: 'Sunrise' },
        { id: 'sunset', infoId: 'sunset-info', label: 'Sunset' },
        { id: 'day_length', infoId: 'day-length-info', label: 'Day Length' },
        { id: 'moonrise', infoId: 'moonrise-info', label: 'Moonrise' },
        { id: 'moonset', infoId: 'moonset-info', label: 'Moonset' },
    ];

    for (const locationData of data) {
        const city = locationData.location['city'];

        const locationElement = $('<div>').addClass('locationData');

        const headerElement = $('<p>').addClass('city').text(city);
        locationElement.append(headerElement);

        $('#selectedData').append(locationElement);

        for (const field of fields) {
            const value = locationData[field.id];
            const displayValue = value === '-:-' ? 'Unavailable' : value;

            const infoElement = $('<p>').text(`${field.label}: ${displayValue}`);
            locationElement.append(infoElement);
        }

        $('#selected-data').append(locationElement);
    }
}

function flashErrorMessage(message) {
    hideErrorMessage();
    const errorMessageElement = $('<p>').text(message).addClass('error');
    $('.getBtn').prepend(errorMessageElement);
}

function hideErrorMessage() {
    $('.error').remove();
}
