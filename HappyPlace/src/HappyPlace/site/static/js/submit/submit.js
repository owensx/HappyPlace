var googlePlaces;
var googlePlacesIterator;

function init(){
	windowHeight = document.documentElement.clientHeight;
	
	$('.halfScreen').each(function(){
		$(this).height((windowHeight / 2) - getMarginHeight());
	});
	
	$("#cityForm select#id_city").change(function(){
		if ($(this).prop("selectedIndex") == 0){
			$("#cityForm input#id_name").show();
			$("#cityForm label[for='id_name']").show();
		} else {
			$("#cityForm input#id_name").hide();
			$("#cityForm label[for='id_name']").hide();
		}
	});
	
	$("input#fromOpen").change(function(){
   	 	if($(this).prop('checked')){       	 		
   	 		$("input#id_start").attr('disabled', true);
   	 	} else {
   	 		$("input#id_start").val("");
   	 		
   	 		$("input#id_start").attr('disabled', false);
	 		}
   	 });
   	 
   	 $("input#toClose").change(function(){
   	 	if($(this).prop('checked')){       	 		
   	 		$("input#id_end").attr('disabled', true);
   	 	} else {
   	 		$("input#id_end").val("");
   	 		
   	 		$("input#id_end").attr('disabled', false);
   	 	}
   	 });
}

function getMarginHeight(){
	return parseInt($('#form').css("margin-top"));
}

function scrollHalf(){
	$('body,html').scrollTop(windowHeight / 2);
}

function scrollFull(){
	$('body,html').scrollTop(windowHeight);
}

function onStateFormSumbit(){
	
}

function onCityFormSumbit(){
	
}

function onHappyPlaceFormSumbit(){
	
}

function hideHappyPlaceFormInputFields(){	
	$('#happyPlaceForm input').hide();
	$("#happyPlaceForm label").hide();

	$('#happyPlaceForm #id_city').hide();
	$("#happyPlaceForm select#id_happyPlace").hide();
	
	$('#happyPlaceForm input#id_name').show();
	$("#happyPlaceForm label[for='id_name']").show();
	
	$('#happyPlaceForm input#id_neighborhood').show();
	$("#happyPlaceForm label[for='id_neighborhood']").show();
	
	$('#happyPlaceForm input#id_neighborhoodName').show();
	$("#happyPlaceForm label[for='id_neighborhoodName']").show();

	
	$("#happyPlaceForm button").not('#searchButton').hide();
}

function setHappyHourDays(buttonName){
	clearHappyHourDays();
	  
	switch (buttonName){
		case 'daily':
			$("#happyHourForm #id_days_0").prop('checked', true);
			$("#happyHourForm #id_days_1").prop('checked', true);
			$("#happyHourForm #id_days_2").prop('checked', true);
			$("#happyHourForm #id_days_3").prop('checked', true);
			$("#happyHourForm #id_days_4").prop('checked', true);
			$("#happyHourForm #id_days_5").prop('checked', true);
			$("#happyHourForm #id_days_6").prop('checked', true);
			break;
		
		case 'weekdays':
			$("#happyHourForm #id_days_1").prop('checked', true);
			$("#happyHourForm #id_days_2").prop('checked', true);
			$("#happyHourForm #id_days_3").prop('checked', true);
			$("#happyHourForm #id_days_4").prop('checked', true);
			$("#happyHourForm #id_days_5").prop('checked', true);
			break;
			
		case 'weekends':
			$("#happyHourForm #id_days_0").prop('checked', true);
			$("#happyHourForm #id_days_6").prop('checked', true);
	    	break;
	}
}	
	 
function clearHappyHourDays(){
	$("#happyHourForm #id_days_0").prop('checked', false);
	$("#happyHourForm #id_days_1").prop('checked', false);
	$("#happyHourForm #id_days_2").prop('checked', false);
	$("#happyHourForm #id_days_3").prop('checked', false);
	$("#happyHourForm #id_days_4").prop('checked', false);
	$("#happyHourForm #id_days_5").prop('checked', false);
	$("#happyHourForm #id_days_6").prop('checked', false);
}

function onHappyHourSubmit(){
	$("input#id_start").attr('disabled', false);
	$("input#id_end").attr('disabled', false);  

	if($("input#fromOpen").prop('checked')){
		$("input#id_start").val("00:00:01");
	}
	
	if($("input#toClose").prop('checked')){
		$("input#id_end").val("02:01:00");
	}
}

function onSearchButtonClick(){
	queryString = $("#happyPlaceForm input#id_name").val() + ' ' + $("#happyPlaceForm input#cityName") + ' ' + $("#happyPlaceForm input#id_address").val();

	$.getJSON("/getPlaceId/" + queryString, function(data) {
		googlePlaces = data;
		googlePlacesIterator = -1;
		
		loadNextGooglePlace();
		
		$('#map').show();
		$('#happyPlaceForm #submitButton').show();	
		$('#happyPlaceForm #nextButton').show();	
		
		if (googlePlacesIterator == googlePlaces.length - 1){
			$('#happyPlaceForm #nextButton').hide();
		}
		
		$('.errorlist').hide();
		$('#happyPlaceForm #prevButton').hide();
	});

	
}

function loadNextGooglePlace() {
	$('#happyPlaceForm #prevButton').show();

	if (++googlePlacesIterator == googlePlaces.length - 1) {
		$('#happyPlaceForm #nextButton').hide();
	}

	$("#happyPlaceForm input#id_name").val(googlePlaces[googlePlacesIterator].name);
	$("#happyPlaceForm input#id_address").val(googlePlaces[googlePlacesIterator].address);
	$("#happyPlaceForm input#id_latitude").val(googlePlaces[googlePlacesIterator].latitude);
	$("#happyPlaceForm input#id_longitude").val(googlePlaces[googlePlacesIterator].longitude);
	$("#happyPlaceForm input#id_site").val(googlePlaces[googlePlacesIterator].site);
	$("#happyPlaceForm input#id_phone").val(googlePlaces[googlePlacesIterator].phone);
	$("#happyPlaceForm input#id_place_id").val(googlePlaces[googlePlacesIterator].placeId);
	
	mapCenter=[googlePlaces[googlePlacesIterator].latitude, googlePlaces[googlePlacesIterator].longitude];
	initMap(mapCenter);	
}

function loadPrevGooglePlace() {
	$('#happyPlaceForm #nextButton').show();
	
	if (--googlePlacesIterator == 0) {
		$('#happyPlaceForm #prevButton').hide();
	}
	
	$("#happyPlaceForm input#id_name").val(googlePlaces[googlePlacesIterator].name);
	$("#happyPlaceForm input#id_address").val(googlePlaces[googlePlacesIterator].address);
	$("#happyPlaceForm input#id_latitude").val(googlePlaces[googlePlacesIterator].latitude);
	$("#happyPlaceForm input#id_longitude").val(googlePlaces[googlePlacesIterator].longitude);
	$("#happyPlaceForm input#id_site").val(googlePlaces[googlePlacesIterator].site);
	$("#happyPlaceForm input#id_phone").val(googlePlaces[googlePlacesIterator].phone);
	$("#happyPlaceForm input#id_place_id").val(googlePlaces[googlePlacesIterator].placeId);
	
	mapCenter=[googlePlaces[googlePlacesIterator].latitude, googlePlaces[googlePlacesIterator].longitude];
	initMap(mapCenter);	
}

function clearForm(formId){
	$(formId).find("input[type=text], textarea").val("");
}