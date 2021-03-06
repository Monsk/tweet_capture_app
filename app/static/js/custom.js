// @TODO:
// * styling of the submitted search term
// * Binding UI behaviour to server

// -----------------------
// Chart plotting and showing
// -----------------------

// $('.card').each(function(i, obj){
//   // Add a listener to a chart area being shown
//   $(this).on('shown.bs.collapse', function (e) {
//     const targetChart = $(e.target).find('.chart')[0].id;
//
//     // if the chart doesn't exist, draw it!
//     if ($('#' + targetChart).children().length === 0) {
//       switch(targetChart){
//         case 'sourceBarChart':
//         plotSourceChart(sourceData);
//         break;
//         case 'timeLangChart':
//         plotTimeLangChart(timeLangData);
//         break;
//         case 'sentimentChart':
//         plotSentimentChart(sentimentData);
//         break;
//         default:
//         break;
//       };
//     };
//
//     // scroll to the top of the chart
//     $('html, body').animate({
//       scrollTop: $('#' + targetChart).parent().parent().offset().top - 50
//     }, 500);
//   })
// })

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
    arr.push($(this).val().toLowerCase());
  });
  $.getJSON('/_string_filter', { str_arr: JSON.stringify(arr) })
  .done(function(data){
    var stringMatchData = data;
    $('#timeStringMatchChart').empty();
    plotStringMatchChart(stringMatchData);
    // if( $('.add-text-input').length === 0){
    //   $('.text-input').after("<div id='add-text-input' class='pull-right'><a>Add series</a></div>");
    //   $.fn.textInputClickBind();
    // }
    $('html, body').animate({
      scrollTop: $('#stringMatch').offset().top - 50
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
    // $('.add-text-input').before("<input class='text-area' id='text-area-" + n + "' type=text size=10 name='string'>")
    $('#StringMatchBtnGroup').before("<input class='text-area form-control mb-2 mr-sm-2 mb-sm-0' id='text-area-" + n + "' type=text size=10 name='string'>")

    if (n > 2){
      $('.add-text-input').remove();
    }
    return false;
  });
}


// -----------------------
// Twitter content buttons
// -----------------------
var toggleTwitterContent = function(d){
  var button_id = $(this).attr('id');
  var toggle_div_id = 'timeline_' + button_id;
  console.log(button_id);

  // d.preventDefault();

  if ($('#' + toggle_div_id).is(':visible')){
    console.log('hiding');
    $('#' + toggle_div_id).hide();
    $("#hide-twitter-content").hide();
    $('html, body').animate({
      scrollTop: $("#sources").offset().top - 50
    }, 500);
  } else {
    $twitterLoading.show();
    // $("#hide-twitter-content").hide();
    // Hide all visible elements
    $('.timeline').each(function(i, obj) {
      $(this).hide();
    })
    // If the element exists, show it
    if ($('#' + toggle_div_id).length){
      console.log('showing content');
      $twitterLoading.hide();
      $('#' + toggle_div_id).show()
      // $("#hide-twitter-content").show();
    } else {
      // If the element doesn't exist, create it
      console.log('creating content');
      $("#hide-twitter-content").before( "<div id=" + toggle_div_id + " class='timeline'><a class='twitter-timeline' data-lang='en' data-height='500' data-theme='light' data-link-color='#2B7BB9' href='https://twitter.com/" + button_id + "'></a><script async src='//platform.twitter.com/widgets.js' charset='utf-8'></script></div>" );
      $('#' + toggle_div_id).show();
      if ($('.twitter-timeline').length) {
        //Timeline exists is it rendered ?
        interval_timeline = false;
        interval_timeline = setInterval(function(){
          if ($('.twitter-timeline').hasClass('twitter-timeline-rendered')) {
            if ($('#' + toggle_div_id).height() > 100) {
              //Callback
              clearInterval(interval_timeline);
              $twitterLoading.hide();
            }
          }
        },200);
      };
    };
  };
};



var $twitterLoading = $('#loadingDiv').hide();

// Hide button
$(function() {
  $('#hide-twitter-content').on("click",function(e) {
    $(".timeline").hide();
    $(this).hide();
    $(".btn.active").each(function(i, obj) {
      $(this).toggleClass('active');
    });
    $('html, body').animate({
      scrollTop: $("#sources").offset().top - 50
    }, 500);
  })
})

// ---------------------
// General functions
// ---------------------

// Number counter
$(document)
$('.count').each(function () {
  $(this).prop('Counter',0).animate({
    Counter: $(this).text()
  }, {
    duration: 4000,
    easing: 'swing',
    step: function (now) {
      $(this).text(Math.ceil(now));
    }
  });
});

// Adds a class when target is in view
function onViewport(el, elClass, offset, callback) {
  /*** Based on http://ejohn.org/blog/learning-from-twitter/ ***/
  var didScroll = false;
  var this_top;
  var height;
  var top;

  if (!offset) { var offset = 600 };

  $(window).scroll(function() {
      didScroll = true;
  });

  setInterval(function() {
    if (didScroll) {
      didScroll = false;
      dist_from_top = $(this).scrollTop();

      $(el).each(function(i){
        this_top = $(this).offset().top - offset;
        height   = $(this).height();

        // Scrolled within current section
        if (dist_from_top >= this_top && !$(this).hasClass(elClass)) {
          $(this).addClass(elClass);

          if (typeof callback == "function") callback($(this));
        }
      });
    }
  }, 100);
}
