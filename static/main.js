const currentDate = new Date();
const defaultDate = currentDate.toISOString().split('T')[0];

$(function () {
    $('#date').val(defaultDate);

    // Select all options when "Select All" checkbox is checked
    $('#select-all').change(function () {
        const isChecked = $(this).prop('checked');

        $('.toggle input[type="checkbox"]').not(this).prop({
            disabled: isChecked,
            checked: isChecked ? true : false
        });
    });

    // Handle form submission
    $("#search-form").on("submit", processForm);

    // Handle form submission for the favourites page
    $("#favourites-form").on("submit", processSelectedData);
});

async function processForm(evt) {
    evt.preventDefault();

    const formData = {
        city: $('#city').val(),
        country: $('#country').val(),
        date: $('#date').val(),
        selectAll: $('#select-all').prop('checked'),
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

async function processSelectedData(evt) {
    evt.preventDefault();


    const selectedCheckboxes = $(".toggle:checked");
    const selectedData = [];


    selectedCheckboxes.each(function () {
        const city = $(this).data("city");
        const country = $(this).data("country");
        selectedData.push({ city, country });
    });


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
        const locationElement = $('<div>').addClass('location-data');

        for (const field of fields) {
            const value = locationData[field.id];
            const displayValue = value === '-:-' ? 'Unavailable' : value;

            const infoElement = $('<p>').text(`${field.label}: ${displayValue}`);
            locationElement.append(infoElement);
        }

        $('#selected-data').append(locationElement);
    }
}
