$(function () {
    $("#event-container").find(":button").click(function() {
        console.log("button clicked");
        var evt_title = $(this).val();
        console.log(evt_title);

        var formdata = new FormData();
        formdata.append('evt_title', evt_title);
        formdata.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        $.ajax({
           type : 'POST',
           url  : '/matchings/join_event/',
           data : formdata,
           success: function(data) {
              alert(data);
              location.reload(true);
           },
           processData : false,
           contentType : false,
        });
    });
})