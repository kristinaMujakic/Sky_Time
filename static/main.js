const currentDate = new Date();
const defaultDate = currentDate.toISOString().split('T')[0];

$(function () {
    $('#date').val(defaultDate);

    // select all options
    $('#select-all').change(function () {
        const isChecked = $(this).prop('checked');

        // toggle based on the "Select All" checkbox
        $('.toggle input[type="checkbox"]').not(this).prop({
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


$("#search-form").on("submit", processForm);