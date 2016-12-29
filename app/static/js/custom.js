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
    if ( $('#'+toggle_div_id).is(":visible")){
      $('#'+toggle_div_id).hide();
      $("#hide-twitter-content").hide();
      $('html, body').animate({
        scrollTop: $('#tweet-sources').offset().top - 50
      }, 500);
    } else {
      $('#'+button_id).toggleClass('active');
      $(".twitter-content").hide();
      $('#'+toggle_div_id).show();
      $("#hide-twitter-content").show();
      $('html, body').animate({
        scrollTop: $('.chart-notes').offset().top - 50
      }, 500);
    }
  });
});

// Hide button
$(function() {
  $('#hide-twitter-content').on("click",function(e) {
    $(".twitter-content").hide();
    $(this).hide();
    $(".btn.active").each(function(i, obj) {
      $(this).toggleClass('active');
    });
    $('html, body').animate({
      scrollTop: $('#tweet-sources').offset().top - 50
    }, 500);
  })
})

// Perform AJAX request on the server
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

//   $(function() {
//     $('a#filterString').bind('click', function() {
//        $.ajax({
//           type: "GET",
//           url: "/_string_filter",
//           contentType: "application/json; charset=utf-8",
//           data: { string: $('input[name="string"]').val() },
//           dataType: "string",
//           success: function(data) {
//               $('#echoResult').text(data.value);
//           }
//       });
//   });
// });
