$(document).ready(function() {
    $('#dialog').dialog({
        autoOpen: false
    });
    $('#open-dialog').on("click", function() {
        $("#dialog").dialog("open");
    });
    $('#submit').on("click", function(e) {
        var data = {};
        var form = $('#dialog').find('form');
        form.serializeArray().map(function(x){data[x.name] = x.value;});
        var json = JSON.stringify(data);
        var url = form.attr('action');
        $.post({
            url: url,
            data: json,
            dataType: "json",
            success: function(response) {
                console.log(response);
            }
        });
        e.preventDefault();
    })
});