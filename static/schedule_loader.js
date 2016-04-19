$(function(){
    $('a#fetch').click(function(){
        $.getJSON('/schedule_loader/load', {source: $('#source').val(), filename: $('#filename').val()}, function(data){
            $('#result').text(data.res);
            $('#result').removeClass('alert-success alert-warning hidden').addClass(data.success ? 'alert-success' : 'alert-warning')
        });
    });
    $('a#select-file').click(function(){
        $.getJSON('/schedule_loader/select', {}, function(data){
            $('#source').val(data.file);
        });
    });
});