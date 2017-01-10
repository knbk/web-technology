$(document).ready(function() {
    $('#dialog').dialog({
        autoOpen: false
    });
    $('#open-dialog').on("click", function() {
        $("#dialog").dialog("open");
    });
    $('#submit').on("click", function(e) {
        var form = $('#dialog').find('form');
        var data = form.serialize();
        var url = form.attr('action');
        var method = form.attr('method');
        var csrf = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            method: method,
            url: url,
            data: data,
            dataType: "json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            },
            success: function(response) {
                console.log(response);
                location.reload();
            }
        });
        e.preventDefault();
    })
});