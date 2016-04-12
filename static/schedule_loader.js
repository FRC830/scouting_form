$(function(){
    $('a[href=#load]').click(function(){
        $.getJSON('/export/do_export', {source: $('#source').val(), name: $('#filename')}, function(data){
            alert(data);
        });
    });
});