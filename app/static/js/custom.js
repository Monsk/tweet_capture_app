// @TODO:
// * styling of the submitted search term
// * Binding UI behaviour to server
// * Implement addition and removal of chart series

// -----------------------
// String input field behaviour
// -----------------------

// Show the loading icon during ajax request
var $loading = $('#stringMatchLoadingDiv').hide();
$(document)
.ajaxStart(function () {
  $('.text-input').hide();
  $loading.show();
})
.ajaxStop(function () {
  $loading.hide();
  $('.text-input').show();
});

// Perform AJAX request on the server, plot timeStringMatchChart
$.fn.ajaxStringRequest = function(){
  var result = null;
  var arr = [];
  $('input[name="string"]').each(function(i, obj){
    arr.push($(this).val());
  });
  console.log(arr);
  $.getJSON('/_string_filter', JSON.stringify(arr))
  .done(function(data){
    var stringMatchData = data;
    $('#timeStringMatchChart').empty();
    plotStringMatchChart(stringMatchData);
    // if( $('.add-text-input').length === 0){
    //   $('.text-input').after("<div id='add-text-input' class='pull-right'><a>Add series</a></div>");
    //   $.fn.textInputClickBind();
    // }
    $('html, body').animate({
      scrollTop: $('#timeStringMatchChart').offset().top - 50
    }, 500);
  })
  .fail(function(){
    console.log('request failed');
  })
  .always(function(){
    console.log('complete');
  })
  // Prevents the AJAX request shooting you to the top of the page
  return false;
};

// Bind requests to a hit of the return key
$.fn.returnKeyBind = function(){
  $('.text-area').keyup(function(event) {
    if (event.keyCode == 13) {
      $.fn.ajaxStringRequest();
      // $(this).siblings('.filterString').replaceWith("<a href=# class='remove-filter'> X</a>");
      $(this).siblings('.remove-filter').xclickBind();
      // $(this).replaceWith($('input[name="string"]').val());
      return false;
    }
  })
};

// Bind requests to GO clicks
$.fn.goClickBind = function(){
  $('.filterString').bind('click', function(){
    $.fn.ajaxStringRequest();
    var parent = $(this).parent();
    // $(this).siblings('.text-area').replaceWith($('input[name="string"]').val());
    // $(this).replaceWith("<a href=# class='remove-filter'> X</a>");
    parent.children('.remove-filter').xclickBind();
    return false;
  })
};

// Bind element removal to the X button
$.fn.xclickBind = function(){
  $(this).bind('click', function(){
    $(this).parent().empty();
    return false;
  })
}

// Initial key bindings
$(document).ready(function() {
  $.fn.goClickBind();
  $.fn.returnKeyBind();
  $.fn.textInputClickBind();
});

// Click 'Add series' and show a new text input and remove the 'Add series'
$.fn.textInputClickBind = function(){
  $('.add-text-input').bind('click', function(){
    var n = $('.text-area').length + 1;
    $('.add-text-input').before("<input class='text-area' id='text-area-" + n + "' type=text size=10 name=string>")
    if (n > 2){
      $('.add-text-input').remove();
    }
    return false;
  });
}


// -----------------------
// Twitter content buttons
// -----------------------

var $twitterLoading = $('#loadingDiv').hide();
// Buttons
$(function() {
  // 1. Toggle the active states of the twitter-button
  // 2. Show the relevant content
  // 3. Scroll to the top of the open content
  $(".twitter-button").on("click",function(e) {
    var button_id = $(this).attr('id');
    var toggle_div_id = 'timeline_' + button_id;
    $twitterLoading.show();
    e.preventDefault();

    $(".btn.active").each(function(i, obj) {
      $(this).toggleClass('active');
    });
    if ($('#' + toggle_div_id).is(':visible')){
      console.log('hiding');
      $('#' + toggle_div_id).hide();
      $("#hide-twitter-content").hide();
      $('html, body').animate({
        scrollTop: $('#tweet-sources').offset().top - 50
      }, 500);
    } else {
      $("#hide-twitter-content").hide();
      // Hide all visible elements
      $('.timeline').each(function(i, obj) {
        $(this).hide();
      })
      // If the element exists, show it
      if ($('#' + toggle_div_id).length){
        $twitterLoading.hide();
        $('#' + toggle_div_id).show()
        $("#hide-twitter-content").show();
        $('html, body').animate({
          scrollTop: $('#tweet-sources').height()
        }, 500);
      } else {
        // If the element doesn't exist, create it
        $("#hide-twitter-content").before( "<div id=" + toggle_div_id + " class='timeline'><a class='twitter-timeline' data-lang='en' data-height='500' data-theme='light' data-link-color='#2B7BB9' href='https://twitter.com/" + button_id + "'></a><script async src='//platform.twitter.com/widgets.js' charset='utf-8'></script></div>" );
        $('#' + toggle_div_id).show();
        if ($('.twitter-timeline').length) {
          //Timeline exists is it rendered ?
          interval_timeline = false;
          interval_timeline = setInterval(function(){
            if ($('.twitter-timeline').hasClass('twitter-timeline-rendered')) {
              if ($('.twitter-timeline').height() > 100) {
                //Callback
                clearInterval(interval_timeline);
                $twitterLoading.hide();
                $('html, body').animate({
                  scrollTop: $('#tweet-sources').height()
                }, 500);
                $("#hide-twitter-content").show();
              }
            }
          },200);
        };
      };
    };
  });
});

// Hide button
$(function() {
  $('#hide-twitter-content').on("click",function(e) {
    $(".timeline").hide();
    $(this).hide();
    $(".btn.active").each(function(i, obj) {
      $(this).toggleClass('active');
    });
    $('html, body').animate({
      scrollTop: $('#tweet-sources').offset().top - 50
    }, 500);
  })
})
