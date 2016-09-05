function init(lastSelectedCity, lastSelectedNeighborhood, photosPath) {
	//get mobileFlag
	document.getElementById('mobileFlag').value = jQuery.browser.mobile;
    
	slideshow(lastSelectedCity, lastSelectedNeighborhood, photosPath);
    
    $('select#city').val(lastSelectedCity).attr('selected', true);

	//deconstruct spaces for URL
	var url = "/getNeighborhoods/" + $("select#city").val().replace(/\s/g,'_');
	$.getJSON(url, function(data) {
		var options = '<option value="all"> All Neighborhoods </option>';
		for (var i = 0; i < data.length; i++) {
			options += '<option value="' + data[i] + '">' + data[i] + '</option>';
		}

		$("select#neighborhood").html(options);
		$('select#neighborhood').val(lastSelectedNeighborhood).attr('selected', true);
	});
	
    $("select#city").change(function() { 
    	$('select#neighborhood').val('all').attr('selected', true);
    	
    	var slowdown = 3000*36856/4.6784568*89+40/660/3;
    	
		document.getElementById('selectForm').submit();       	
	});

    $("select#neighborhood").change(function() {        			
		document.getElementById('selectForm').submit();       	
	});
    
    $("input#currentTimeOnly").change(function() {        			
		document.getElementById('selectForm').submit();       	
	});
}

function slideshow(lastSelectedCity, lastSelectedNeighborhood, photosPath) {  
	lastSelectedCity = lastSelectedCity.replace(/\s/g,'_');
	lastSelectedNeighborhood = lastSelectedNeighborhood.replace(/\s/g,'_');

	$.getJSON("/getPhotos/" + lastSelectedCity + "/" + lastSelectedNeighborhood, function(data) {
        	
       		if (lastSelectedNeighborhood == 'all') {
       			lastSelectedNeighborhood = '';
       		}
       		
       		var pics = [];
			for (var x = 1; x <= data; x++) {
		       	pics[x-1] =	photosPath + lastSelectedCity + "/" + lastSelectedNeighborhood + "/" + x + ".jpg";
    	    }  
    	    
        	shuffle(pics);
        	
        	$.backstretch(pics,{duration:6000, fade:1000});
	});
}

function initMap(mapCenter, markersInfo) {
	var geocoder = new google.maps.Geocoder();	
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 15,
		center: {lat: mapCenter[0], lng: mapCenter[1]}
	});
	
	var sumLat = 0;
	var sumLng = 0;
	var service = new google.maps.places.PlacesService(map);

	markersInfo.forEach(function(markerInfo){
		addMarkerToMap(geocoder, map, markerInfo);
	});
	
}


function addMarkerToMap(geocoder, map, happyPlaceInfo){
	happyPlaceName = happyPlaceInfo[0]
	latLng = happyPlaceInfo[1]
	specials = happyPlaceInfo[2]
	
	var marker = new google.maps.Marker({
		map: map,
		position: latLng,
		animation: google.maps.Animation.DROP,
		infoWindowOpen: false
	});
	
	var infoWindow = new google.maps.InfoWindow({
	    content: getInfoWindowHtml(happyPlaceName, specials)
	});
	
	marker.addListener('click', function() {
		if (marker.infoWindowOpen){
			infoWindow.close();
			marker.infoWindowOpen = false;
		} else {
			infoWindow.open(map, marker);
			marker.infoWindowOpen = true;
		}
	});
}

function getInfoWindowHtml(happyPlaceName, specials){
	var infoHtml = '';
	var displayNotes = '';
	
	if (specials == ''){
		infoHtml = '<br style = "clear: left;">' + '<p>' + 'No Specials Today!' + '</p>';
	} else {
		specials.forEach(function(specialDetails){
			var start = specialDetails[0];
			var end = specialDetails[1];
			var displayNotes = specialDetails[2];
			var icons = specialDetails[3];
			
			infoHtml += '<p style = "margin-top: 28px; margin-bottom: 0px;">' + start + '-' + end + ':' + '</p>';
			icons.forEach(function(icon){
				infoHtml += getIconHtml(icon);
			});
			
			if (displayNotes != ''){
				infoHtml += '<br style = "clear: left;"> <p style = "margin-top: 2px;">' + displayNotes + '</p>';
			}
		});		
	}
	
	return  '<u style = "font-size: 22px; margin: 0px";>' + happyPlaceName + '</u>' + infoHtml;
}

function getIconHtml(special){
	specialName = special[0];
	specialValue = special[1];
	
	if (specialValue != ''){
		iconHtml = '<img style="font-size: 15px; float: left; padding-left:5px;" height="20px" src="static/icons/' + specialValue + specialName + '.png"/>';
		return iconHtml;
	} else return '';
}

function shuffle(o) {
	for(var j, x, i = o.length; i; j = parseInt(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
	return o;
}

/*! Backstretch - v2.0.4 - 2013-06-19
* http://srobbin.com/jquery-plugins/backstretch/
* Copyright (c) 2013 Scott Robbin; Licensed MIT */
(function(a,d,p){a.fn.backstretch=function(c,b){(c===p||0===c.length)&&a.error("No images were supplied for Backstretch");0===a(d).scrollTop()&&d.scrollTo(0,0);return this.each(function(){var d=a(this),g=d.data("backstretch");if(g){if("string"==typeof c&&"function"==typeof g[c]){g[c](b);return}b=a.extend(g.options,b);g.destroy(!0)}g=new q(this,c,b);d.data("backstretch",g)})};a.backstretch=function(c,b){return a("body").backstretch(c,b).data("backstretch")};a.expr[":"].backstretch=function(c){return a(c).data("backstretch")!==p};a.fn.backstretch.defaults={centeredX:!0,centeredY:!0,duration:5E3,fade:0};var r={left:0,top:0,overflow:"hidden",margin:0,padding:0,height:"100%",width:"100%",zIndex:-999999},s={position:"absolute",display:"none",margin:0,padding:0,border:"none",width:"auto",height:"auto",maxHeight:"none",maxWidth:"none",zIndex:-999999},q=function(c,b,e){this.options=a.extend({},a.fn.backstretch.defaults,e||{});this.images=a.isArray(b)?b:[b];a.each(this.images,function(){a("<img />")[0].src=this});this.isBody=c===document.body;this.$container=a(c);this.$root=this.isBody?l?a(d):a(document):this.$container;c=this.$container.children(".backstretch").first();this.$wrap=c.length?c:a('<div class="backstretch"></div>').css(r).appendTo(this.$container);this.isBody||(c=this.$container.css("position"),b=this.$container.css("zIndex"),this.$container.css({position:"static"===c?"relative":c,zIndex:"auto"===b?0:b,background:"none"}),this.$wrap.css({zIndex:-999998}));this.$wrap.css({position:this.isBody&&l?"fixed":"absolute"});this.index=0;this.show(this.index);a(d).on("resize.backstretch",a.proxy(this.resize,this)).on("orientationchange.backstretch",a.proxy(function(){this.isBody&&0===d.pageYOffset&&(d.scrollTo(0,1),this.resize())},this))};q.prototype={resize:function(){try{var a={left:0,top:0},b=this.isBody?this.$root.width():this.$root.innerWidth(),e=b,g=this.isBody?d.innerHeight?d.innerHeight:this.$root.height():this.$root.innerHeight(),j=e/this.$img.data("ratio"),f;j>=g?(f=(j-g)/2,this.options.centeredY&&(a.top="-"+f+"px")):(j=g,e=j*this.$img.data("ratio"),f=(e-b)/2,this.options.centeredX&&(a.left="-"+f+"px"));this.$wrap.css({width:b,height:g}).find("img:not(.deleteable)").css({width:e,height:j}).css(a)}catch(h){}return this},show:function(c){if(!(Math.abs(c)>this.images.length-1)){var b=this,e=b.$wrap.find("img").addClass("deleteable"),d={relatedTarget:b.$container[0]};b.$container.trigger(a.Event("backstretch.before",d),[b,c]);this.index=c;clearInterval(b.interval);b.$img=a("<img />").css(s).bind("load",function(f){var h=this.width||a(f.target).width();f=this.height||a(f.target).height();a(this).data("ratio",h/f);a(this).fadeIn(b.options.speed||b.options.fade,function(){e.remove();b.paused||b.cycle();a(["after","show"]).each(function(){b.$container.trigger(a.Event("backstretch."+this,d),[b,c])})});b.resize()}).appendTo(b.$wrap);b.$img.attr("src",b.images[c]);return b}},next:function(){return this.show(this.index<this.images.length-1?this.index+1:0)},prev:function(){return this.show(0===this.index?this.images.length-1:this.index-1)},pause:function(){this.paused=!0;return this},resume:function(){this.paused=!1;this.next();return this},cycle:function(){1<this.images.length&&(clearInterval(this.interval),this.interval=setInterval(a.proxy(function(){this.paused||this.next()},this),this.options.duration));return this},destroy:function(c){a(d).off("resize.backstretch orientationchange.backstretch");clearInterval(this.interval);c||this.$wrap.remove();this.$container.removeData("backstretch")}};var l,f=navigator.userAgent,m=navigator.platform,e=f.match(/AppleWebKit\/([0-9]+)/),e=!!e&&e[1],h=f.match(/Fennec\/([0-9]+)/),h=!!h&&h[1],n=f.match(/Opera Mobi\/([0-9]+)/),t=!!n&&n[1],k=f.match(/MSIE ([0-9]+)/),k=!!k&&k[1];l=!((-1<m.indexOf("iPhone")||-1<m.indexOf("iPad")||-1<m.indexOf("iPod"))&&e&&534>e||d.operamini&&"[object OperaMini]"==={}.toString.call(d.operamini)||n&&7458>t||-1<f.indexOf("Android")&&e&&533>e||h&&6>h||"palmGetResource"in d&&e&&534>e||-1<f.indexOf("MeeGo")&&-1<f.indexOf("NokiaBrowser/8.5.0")||k&&6>=k)})(jQuery,window);