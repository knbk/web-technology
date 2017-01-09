$(document).ready(function() {
    $('#dialog').dialog({
        autoOpen: false
    });
    $('#open-dialog').on("click", function() {
        $("#dialog").dialog("open");
    });
    $('#submit').on("click", function(e) {
        var data = $('#dialog').find('form').serialize();
        var json = JSON.stringify(data);
        console.log(json);
    })
});