$(document).ready(function () {




    $('#new-random-button').click(function (e) {
        $.ajax({
            url: '/random',
            type: 'GET',
        })
            .done(function (data) {
                $('#random-card').empty().append("<a href=\"/recipe/view/" + data['recipe']['recipeID'] + "\"><div class=\"card mb-4 box-shadow\"><div class=\"card-header\"><h4 class=\"my-0 font-weight-normal\">" + data['recipe']['title'] + "</h4></div><div class=\"card-body\"><img src=\"" + data['image_link'] +
                    "\" alt=\"image\" width=\"100\" class=\"img-thumbnail\"><ul class=\"list-unstyled mt-3 mb-4\"><li> # of servings " + data['recipe']['serving'] + " </li></ul><span id=\"number-of-ingredients\"> </span></div></div></a>")
            });
        e.preventDefault();

    })
})

// "<a href=\"/recipe/view/"+data['recipeID']+ "><div class=\"card mb-4 box-shadow\"><div class=\"card-header\"><h4 class=\"my-0 font-weight-normal\">" + data['title'] + "</h4></div><div class=\"card-body\"><img src=\"{{url_for('static', filename='images/'+ " + data['image'] +
//  ")}}\" alt=\"image\" width=\"100\" class=\"img-thumbnail\"><ul class=\"list-unstyled mt-3 mb-4\"><li> # of servings " + data['serving'] + " </li></ul><span id=\"number-of-ingredients\"> </span></div></div></a>"