let autocomplete;

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('address'),
        {
            componentRestrictions: {'country': ['IE']},
            location: {lat: 53.350140, lng: -6.266155},
            radius: 31053.48,
            name: 'Dublin',
        }
    )
    autocomplete.addListener('place_changed', OnPlaceChanged);
}

function OnPlaceChanged () {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
        document.getElementById('address').placeholder = 'Enter a place';
    } else {
        document.getElementById('address').innerHTML = place.name;
    }
}