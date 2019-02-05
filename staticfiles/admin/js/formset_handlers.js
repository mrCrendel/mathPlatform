(function($) {
    alert('asdas');
    $("#select2-id_assignmenttopic_set-0-subject-container").change(function () {
        alert("eheh");
        var subject = $(this).val();  // get the selected country ID from the HTML input
        alert(subject);
        $.ajax({                       // initialize an AJAX request
            url: '/ajax/load_topics/',                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
            data: {
              'subject': subject       // add the country id to the GET parameters
            },
            dataType: 'json',
            cache: false,
            success: function (data) {   // `data` is the return of the `load_cities` view function
              $("#select2-id_assignmenttopic_set-0-topic-container").html(data);  // replace the contents of the city input with the data that came from the server
            }
        });
    });
})(django.jQuery);