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

function applySearch() {
	var sQuery = document.getElementById("searchQuery").value;
	alert(sQuery)
	sendRequest("http://localhost:8080/search/" + sQuery, printSearchResults)
}

function wordCloud() {
	var sQuery = document.getElementById("searchQuery").value;
	alert(sQuery)
	sendRequest("http://localhost:8080/wordcloud/" + sQuery, printSearchResults)	
}

window.onload = function() {
	alert("On Page load")		
}