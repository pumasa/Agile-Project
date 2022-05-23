$(document).ready(function() {
    $(".moreBox").slice(0, 6).show();
    if ($(".moreBox:hidden").length == 0) {
        $("#view-more-button").hide();
    }
    $("#view-more-button").on('click', function(e) {
        e.preventDefault();
        $(".moreBox:hidden").slice(0, 3).slideDown();
        if ($(".moreBox:hidden").length == 0) {
            $("#view-more-button").fadeOut('slow');
        }
    });
});

// $( document ).ready(function () {
//     $(".moreBox").slice(0, 2).show();
//       if ($(".blogBox:hidden").length != 0) {
//         $("#loadMore").show();
//       }   
//       $("#loadMore").on('click', function (e) {
//         e.preventDefault();
//         $(".moreBox:hidden").slice(0, 1).slideDown();
//         if ($(".moreBox:hidden").length == 0) {
//           $("#loadMore").fadeOut('slow');
//         }
//       });
//     });