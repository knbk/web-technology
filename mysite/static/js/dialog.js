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
        $.post({
            url: url,
            data: data,
            dataType: "json",
            success: function(response) {
                console.log(response);
            }
        });
        e.preventDefault();
    })
});