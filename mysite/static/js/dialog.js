$(document).ready(function() {
    $('#dialog').dialog({
        autoOpen: false
    });
    $('#open-dialog').on("click", function() {
        $("#dialog").dialog("open");
    });
    $('#submit').on("click", function(e) {
        var data = {};
        $("#dialog").find('form').serializeArray().map(function(x){data[x.name] = x.value;});
        var json = JSON.stringify(data);
        console.log(json);
    })
});