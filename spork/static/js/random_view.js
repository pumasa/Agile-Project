$(document).ready(function() {




    $('#new-random-button').click(function(e) {
        $.ajax({
                url: '/random',
                type: 'GET',
            })
            .done(function(data) {
                $('#random-card').empty().append("<img src=\"{{url_for('static',filename='images/'+" + data['image'] + ")}} \" width=\"100% \" height=\"225 \" class=\"card-img-top \" text=\"Thumbnail \"><div class=\"card-body \"><h4 class=\"my-0 font-weight-normal \">{{" + data['title'] + "}}</h4><p class=\"card-text \">{{" + data['description'] + "}}</p><div class=\"d-flex justify-content-between align-items-center \"><div class=\"btn-group \"><a href=\"/recipe/view/{{" + data['recipeID'] + "}} \"><button type=\"button \" class=\"btn btn-sm btn-outline-secondary \">View</button></a><button type=\"button \" class=\"btn btn-sm btn-outline-secondary \">Rate</button></div><small class=\"text-muted \">Serves: {{" + data['serving'] + "}}</small></div></div></div>")
            });


        e.preventDefault();

    })
})

// "<a href=\"/recipe/view/"+data['recipeID']+ "><div class=\"card mb-4 box-shadow\"><div class=\"card-header\"><h4 class=\"my-0 font-weight-normal\">" + data['title'] + "</h4></div><div class=\"card-body\"><img src=\"{{url_for('static', filename='images/'+ " + data['image'] +
//  ")}}\" alt=\"image\" width=\"100\" class=\"img-thumbnail\"><ul class=\"list-unstyled mt-3 mb-4\"><li> # of servings " + data['serving'] + " </li></ul><span id=\"number-of-ingredients\"> </span></div></div></a>"