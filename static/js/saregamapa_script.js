
$(document).ready(function($) {

  var holderElem = $('#saregamapa-search-holder');
  
  if(holderElem.length) {
    advancedSearchModule.initSearchModule(holderElem);
  }



 });  
  

  var advancedSearchModule = (function() {
    
    var searchResultsCount = 0;
  
    //DOM for Search page...
    var moduleHolderElem = '';
    var searchResultsCountElem = '';
    var resultsHolderElem = '';
    var scrollButtonElem = '';
    var overlayElem = '';
    var loadingMessageElem = '';
    var clusterCountElem = '';

    var _this = '';
    var baseURL = "http://localhost:8080/";

    function initSearchModule(holderElem) {
      
      //Initializing DOM of Advanced Search module
      moduleHolderElem = holderElem;
      resultsHolderElem = moduleHolderElem.find('#results-container');
      overlayElem = moduleHolderElem.find('#ss-overlay');
      loadingMessageElem = moduleHolderElem.find('#ss-loading-message');
      searchResultsCountElem = moduleHolderElem.find('#ss-results-count-message');
      scrollButtonElem = moduleHolderElem.find('#ss-scrollToTop');
      clusterCountElem = moduleHolderElem.find('#saregamapa_cc');
      
      _this = this;  

      register_saregamapa_search_events();
    }

    function register_saregamapa_search_events() {
      moduleHolderElem.find('#saregamapa_search').on('keypress',function(e) {
        
        if(e.which == 13) {
          e.preventDefault();
          e.stopPropagation();
          search_songs();
        }

        
      });
      
      moduleHolderElem.find('#saregamapa_search_btn').off('click').on('click', function(e) {
          search_songs();
      });

      moduleHolderElem.find('#saregamapa_wc_btn').off('click').on('click', function(e) {
          cluster_songs();
      });
    }


    function clear_previous_results() {   
      //Clear previous search results...
      moduleHolderElem.find('#results-container').html('');

      //Disable the text input until all the search results are fetched...
      //document.getElementById('saregamapa_search').disabled = true;
      //document.getElementById('saregamapa_search_btn').disabled = true;
      //document.getElementById('saregamapa_wc_btn').disabled = true;

    }

    function is_query_valid(query) {
      var validFlag = true;

      //Validate the search query...
      if(!query){
        alert("Please enter value in search box!");
        validFlag = false;
      } else if(query.length < 4) {
          alert("Search query should be minimum 4 character. Please try again!");
          validFlag = false;
      }

      return validFlag;
    }

    function search_songs() {
      var search_text = moduleHolderElem.find("#saregamapa_search").val();
    
      if(is_query_valid(search_text)) {
        clear_previous_results();

        //Show loader
        overlayElem.show();     

        $.ajax({
          type: 'GET',
          url: baseURL + "search?qs=" + search_text,
          timeout: 1000000,
          dataType: 'json',
          success: display_results.bind(this),
          error: handle_search_failure.bind(this)
        });
      }
    }

    function cluster_songs() {
      var search_text = moduleHolderElem.find("#saregamapa_search").val();
    
      if(is_query_valid(search_text)) {
        clear_previous_results();

        var cc = clusterCountElem.val()

        //Show loader
        overlayElem.show();     

        var apiPath = "wordcloud?qs=" + search_text + "&cc=" + cc; 

        $.ajax({
          type: 'GET',
          url: baseURL + apiPath,
          //timeout: 1000000,
          //dataType: 'json',
          success: display_cluster_results.bind(this),
          error: handle_search_failure.bind(this)
        });
      }

    }

    function format_song_url(url) {
      var fixed_part = 'https://www.azlyrics.com/lyrics/';

      url = url.split("+").join("");
      var urlArray = url.split("/");
      var urlArrayLen = urlArray.length;
      var lastPart = urlArray[urlArrayLen-1];
      var lastPartAry = lastPart.split("_");

      var variablePart = urlArray[2] + "/" + lastPartAry[0] + ".html";

      return fixed_part + variablePart; 
    }
      
    function display_results(response) {

       var results =  response.search_results;
       var resultsLen = results.length;

       if(resultsLen) {
         render_songs(resultsHolderElem, results); 
       } 

       handle_search_asyn_counter(resultsLen);
    }

    function display_cluster_results(response) {
      var clusterResults =  response.cluster_results;
      var clusterResultsLen = clusterResults.length;

       if(clusterResultsLen) {

         var searchResults = '';  

         for(var i=0; i < clusterResultsLen; i++) {

          var cur_cluster_data = clusterResults[i]
           resultsHolderElem.append("<li><h3 class='cluster-title-cls'>Cluster Data " + i + " and Word Cloud:</h3></li>"); 
           resultsHolderElem.append("<ul id='cluster_" + i + "' ></ul>");

           var curClusterElem = resultsHolderElem.find("#cluster_" + i); 

           curClusterElem.append("<li><img width='800px' height='500px' src='static/wordcloud/cluster_" + i + ".png' /></li>");

           render_songs(curClusterElem, cur_cluster_data);   
         }
       } 

        handle_search_asyn_counter(clusterResultsLen);
    }

    function render_songs(renderElem, songsAry) {

      var songsHTML = '';  
      var songsAryLen = songsAry.length;

      for(var i=0; i < songsAryLen; i++) {

       var cur_song = songsAry[i]; 
       var song_name = cur_song[2]; 
       var song_url = format_song_url(cur_song[3]);
          
       songsHTML += '<li>';
       songsHTML +='<h3 class="ss-post-title"><a target="_blank" href="' + song_url + '">' + song_name + '</a></h3>';
       songsHTML += '</li>';
      }

      //Add all the results for a site at once to the DOM
      renderElem.append(songsHTML);

    }

    //Handle failure calls based on timeout
    function handle_search_failure(xhr, textStatus, errorThrown) {
      handle_search_asyn_counter(0);
    }

    function handle_search_asyn_counter(resultsLen) {
      
      //search is finished...
      //Hide the status message
      //document.getElementById('saregamapa_search').disabled = false;
      //document.getElementById('saregamapa_search_btn').disabled = false;
      //document.getElementById('saregamapa_wc_btn').disabled = false;

      loadingMessageElem.hide();

      //If no results are found
      overlayElem.hide(); 
     
      if( !resultsLen ) {
          //Show no results found message
          resultsHolderElem.html('<div class="ss-noresults-common">No songs/clusters found, please try again...</div>'); 
      }

    }

    return {
      'initSearchModule': initSearchModule
    }

  })();


  