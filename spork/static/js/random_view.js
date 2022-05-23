$(document).ready(function() {




    $('#new-random-button').click(function(e) {
        $.ajax({
                url: '/random',
                type: 'GET',
            })
            .done(function(data) {
                $('#random-card').empty().append("<img src=\""+ data['image_link'] + "\" width=\"100% \" height=\"225 \" class=\"card-img-top \" text=\"Thumbnail \"><div class=\"card-body \"><h4 class=\"my-0 font-weight-normal \">" + data['recipe']['title'] + "</h4><p class=\"card-text \">" + data['recipe']['description'] + "</p><div class=\"d-flex justify-content-between align-items-center \"><div class=\"btn-group \"><a href=\"/recipe/view/" + data['recipe']['recipeID'] + " \"><button type=\"button \" class=\"btn btn-sm btn-outline-secondary \">View</button></a><button type=\"button \" class=\"btn btn-sm btn-outline-secondary \">Rate</button></div><small class=\"text-muted \">Serves: " + data['recipe']['serving'] + "</small></div></div></div>")
            });


        e.preventDefault();

    })
})
