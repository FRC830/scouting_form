$(function(){
    $('a#fetch').click(function(){
        $.getJSON('/schedule_loader/load', {source: $('#source').val(), name: $('#filename').val()}, function(data){
            alert(data);
        });
    });
});