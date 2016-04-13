$(function(){
    $('a[href=#load]').click(function(){
        $.getJSON('/schedule_loader/load', {source: $('#source').val(), name: $('#filename')}, function(data){
            alert(data);
        });
    });
});