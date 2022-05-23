$(document).ready(function() {




    $('#new-random-button').click(function(e) {
        $.ajax({
                url: '/random',
                type: 'GET',
            })
            .done(function(data) {
                $('#random-card').empty().append("<a href=\"/recipe/view/" + data['recipe']['recipeID'] + "\"><div class=\"col-md-10\" style=\"margin-left: auto;margin-right: auto;\"><img src=\"" + data['image_link'] + "\" width=\"100% \" height=\"225 \" class=\"card-img-top \" text=\"Thumbnail \"><div class=\"card-body \"><h4 class=\"my-0 font-weight-normal \">" + data['recipe']['title'] + "</h4><p class=\"card-text \">" + data['recipe']['description'] + "</p><div class=\"d-flex justify-content-between align-items-center \"><div class=\"btn-group \"><small class=\"text-muted \">By: " + data['recipe']['author'] + "</small> </div><small class=\"text-muted \">Serves: " + data['recipe']['serving'] + "</small></div></div></div></a></div>")
            });


        e.preventDefault();

    })
})