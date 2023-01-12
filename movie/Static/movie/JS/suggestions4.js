var $input = document.getElementById('searchBox4');
var baseUrl = "http://sg.media-imdb.com/suggests/";
var $result = document.getElementById('result4');
var body = document.getElementsByTagName('body');

document.getElementById('searchBox4').addEventListener('keyup', function(){

	//clearing blank spaces from input
	var cleanInput = document.getElementById('searchBox4').value.replace(/\s/g, "");
	document.getElementById('result4').innerHTML = "";
	
	//clearing result div if the input box in empty
	if(cleanInput.length === 0) {
		document.getElementById('result4').innerHTML = "";
	}
	
	if(cleanInput.length > 0) {
		
		var queryUrl = baseUrl + cleanInput[0].toLowerCase() + "/" 
					  + cleanInput.toLowerCase()
					  + ".json";	
		$.ajax({
		    
		    url: queryUrl,
		    dataType: 'jsonp',
		    cache: true,
		    jsonp: false,
		    jsonpCallback: "imdb$" + cleanInput.toLowerCase()
		
		}).done(function (result) {
	    	
	    	//clearing result div if there is a valid response
	    	if(result.d.length > 0) {
	    		$result.innerHTML = "";
	    	}
		    
		    for(var i = 0; i < result.d.length; i++) {
		    	
		    	var category = result.d[i].id.slice(0,2);
		    	

		    		if(category === "tt" && result.d[i].y) {
						var resultRow = document.createElement('button');
		    			var destinationUrl;

						destinationUrl = result.d[i].l;
						resultRow.setAttribute('value', destinationUrl);
						resultRow.setAttribute("onclick","fill4(this.value)")
						
						resultRow.setAttribute('target', '_blank');
		    			resultRow.innerHTML = result.d[i].l + " (" + result.d[i].y + ")";
		    		}

		    		$("#result4").append(resultRow);

		    	}
		    }
		
		);
	}
});

function fill4(destinationUrl){
	document.getElementById('searchBox4').value = destinationUrl;
	document.getElementById('result4').innerHTML = "";
}