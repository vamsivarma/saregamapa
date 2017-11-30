
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

      _this = this;  

      register_saregamapa_search_events();
    }

    function register_saregamapa_search_events() {
      moduleHolderElem.find('#saregamapa_search').on('keypress',function(e) {
        
        if(e.which == 13) {
          e.preventDefault();
          e.stopPropagation();
          search_sites();
        }

        
      });
      
      moduleHolderElem.find('#saregamapa_search_btn').off('click').on('click', function(e) {
          search_sites();
      });
    }


    function clear_previous_results() {   
      //Clear previous search results...
      moduleHolderElem.find('#results-container').html('');

      //Disable the text input until all the search results are fetched...
      document.getElementById('saregamapa_search').disabled = true;
      document.getElementById('saregamapa_search_btn').disabled = true;
      document.getElementById('saregamapa_wc_btn').disabled = true;

    }

    function search_sites() {
      var search_text = moduleHolderElem.find("#saregamapa_search").val();
    
      //Validate the search query...
      if(!search_text){
        alert("Please enter value in search box!");
        return;
      } else if(search_text.length < 4) {
          alert("Search query should be minimum 4 character. Please try again!");
          return;
      } else {
        //Prepare search  query for effficient searching...
        //search_text = addOperatorsToQuery(search_text);
      }
       

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
      
    function display_results(response) {

       var results =  response.search_results;
       var resultsLen = results.length;

       if(resultsLen) {

          //This should get executed only once
          if(overlayElem.is(':visible')) {
            overlayElem.hide();
            loadingMessageElem.show();    
          }

         var searchResults = '';  

         for(var i=0; i < resultsLen; i++) {

           var cur_result = results[i]; 
           var song_name = cur_result[2]; 
           var song_url = cur_result[3];
              
           searchResults += '<li>';
           searchResults +='<h3 class="ss-post-title"><a target="_blank" href="' + song_url + '">' + song_name + '</a></h3>';
           searchResults += '</li>';
         }

         //Add all the results for a site at once to the DOM
         resultsHolderElem.append(searchResults);
       } 

       handle_search_asyn_counter(resultsLen);
    }

    //Handle failure calls based on timeout
    function handle_search_failure(xhr, textStatus, errorThrown) {
      handle_search_asyn_counter(0);
    }

    function handle_search_asyn_counter(resultsLen) {
      
      //search is finished...
      //Hide the status message
      document.getElementById('saregamapa_search').disabled = false;
      document.getElementById('saregamapa_search_btn').disabled = false;
      document.getElementById('saregamapa_wc_btn').disabled = false;

      loadingMessageElem.hide();

      //If no results are found
      overlayElem.hide(); 
     
      if( !resultsLen ) {
          //Show no results found message
          resultsHolderElem.html('<div class="ss-noresults-common">No posts found, please try again...</div>'); 
      }

    }

    return {
      'initSearchModule': initSearchModule
    }

  })();


  