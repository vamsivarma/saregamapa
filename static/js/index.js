function sendRequest(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.responseType = "JSON";

  xhr.onload = function(e) {
  	callback(JSON.parse(xhr.response));
	}
		
	xhr.send(); 
}

function printSearchResults(result) {
  alert(result)
}  	

function printWordCloud(result) {
	alert(result)
}

window.onload = function() {
	alert("On Page load")
	sendRequest("http://localhost:8080/wordcloud", printWordCloud)

	sendRequest("http://localhost:8080/search", printSearchResults)	
}