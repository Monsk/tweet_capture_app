// -----------------------
// Twitter content buttons
// -----------------------

// Buttons
$(function() {
  // 1. Toggle the active states of the twitter-button
  // 2. Show the relevant content
  // 3. Scroll to the top of the open content
  $(".twitter-button").on("click",function(e) {
    var button_id = $(this).attr('id');
    var toggle_div_id = 'timeline_' + button_id;
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

// Perform AJAX request on the server, plot timeStringMatchChart
$(function() {
  $('a#filterString').bind('click', function() {
    var result = null;
    $.getJSON('/_string_filter', {
      string: $('input[name="string"]').val(),
    })
    .done(function(data){
      var stringMatchData = data;
      $('#timeStringMatchChart').empty();
      plotStringMatchChart(stringMatchData);
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
  });
});
