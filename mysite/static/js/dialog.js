$(document).ready(function() {
    $('#dialog').dialog({
        autoOpen: false
    });
    $('#open-dialog').on("click", function() {
        $("#dialog").dialog("open");
    });
    $('#submit').on("click", function(e) {
        var form = $('#dialog').find('form');
        var data = {};
        form.serializeArray().map(function(x){data[x.name] = x.value;});
        var json = JSON.stringify(data);
        var url = form.attr('action');
        var method = form.attr('method');
        var csrf = data['csrfmiddlewaretoken'];
        $.ajax({
            method: method,
            url: url,
            data: json,
            contentType: "application/json",
            dataType: "application/json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            },
            success: function(response) {
                console.log(response);
                location.reload();
            },
        });
        e.preventDefault();
    })
});