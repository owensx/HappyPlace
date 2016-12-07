function initMap(mapCenter) {
	var map = new google.maps.Map(document.getElementById('map'), {
			zoom: 15
			, center: {lat: mapCenter[0], lng: mapCenter[1]} 
		}
	);
	
	var marker = new google.maps.Marker({
		map: map
		, position: {lat: mapCenter[0], lng: mapCenter[1]} 
		, animation: google.maps.Animation.DROP
	});
}
