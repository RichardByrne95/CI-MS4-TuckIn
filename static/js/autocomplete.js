let autocomplete;
let service;

// Initialise autocomplete
function initAutocomplete () {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('address'),
        {
            componentRestrictions: {'country': ['IE']},
            location: {lat: 53.350140, lng: -6.266155},
            radius: 31053.48,
            name: 'Dublin',
        }
    );
    autocomplete.addListener('place_changed', OnPlaceChanged);
}

function OnPlaceChanged () {
    // Handle selecting address from autocomplete
    let place = autocomplete.getPlace();
    if (!place.geometry) {
        document.getElementById('address').placeholder = 'Enter a place';
    } else {
        document.getElementById('address').innerHTML = place.name;
        
        // Handle address verification
        const addressVerification = (address) => {
            service = new google.maps.places.PlacesService(address);
            let request = {
                query: place.name,
                fields: ['formatted_address'],
            };
            service.findPlaceFromQuery(request, function (results, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    let hasDublin = results[0].formatted_address.indexOf('Dublin');
                    let hasCountyDublin = results[0].formatted_address.indexOf('County Dublin');
                    let hasBaile = results[0].formatted_address.indexOf('Baile Átha Cliath');
                    let hasContae = results[0].formatted_address.indexOf('Contae Bhaile Átha Cliath');
                    if (hasDublin != -1 || hasCountyDublin != -1 || hasBaile != -1 || hasContae != -1) {
                        $(".find-button").attr('disabled', false);
                        $(".error-message").html('');
                    } else {
                        $(".find-button").attr('disabled', true);
                        $(".error-message").html('Your address must be inside Dublin');
                    }
                }
            });
        };
        addressVerification(document.getElementById('address'));
    }
}