var $input = document.getElementById('searchBox');
var baseUrl = "http://sg.media-imdb.com/suggests/";
var $result = document.getElementById('result');
var body = document.getElementsByTagName('body');

$input.addEventListener('keyup', function(){

	//clearing blank spaces from input
	var cleanInput = $input.value.replace(/\s/g, "");
	
	//clearing result div if the input box in empty
	if(cleanInput.length === 0) {
		$result.innerHTML = "";
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
					var destinationUrl = result.d[i].l;
					resultRow.innerHTML = result.d[i].l + " (" + result.d[i].y + ")";

					resultRow.setAttribute("type","submit")
					resultRow.setAttribute('name','q')
					resultRow.setAttribute('value', destinationUrl);
					resultRow.setAttribute('target', '_blank');

					$("#result").append(resultRow);
				}
		    	/*
		    	if(category === "tt") {		    		
		    		//row for risplaying one result
					
		    		var resultRow = document.createElement('button');
		    		var destinationUrl = result.d[i].l;
					
		    		if(category === "tt") {
		    			destinationUrl = result.d[i].l;
		    		} else {
		    			destinationUrl = result.d[i].l;
		    		}
		    		
		    		resultRow.setAttribute("type","submit")
					resultRow.setAttribute('name','q')
					resultRow.setAttribute('value', destinationUrl);
		    		resultRow.setAttribute('target', '_blank');
					
		    		//creating and setting description

		    		if(category === "tt" && result.d[i].y) {
						var resultRow = document.createElement('button');
		    			var destinationUrl = result.d[i].l;
		    			resultRow.innerHTML = result.d[i].l + " (" + result.d[i].y + ")";

						resultRow.setAttribute("type","submit")
						resultRow.setAttribute('name','q')
						resultRow.setAttribute('value', destinationUrl);
						resultRow.setAttribute('target', '_blank');
		    		}
					
		    		$("#result").append(resultRow);
					
		    	}*/
		    }
		
		});
	}
});