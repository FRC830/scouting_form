$(function(){
    $('a#fetch').click(function(){
        $.getJSON('/schedule_loader/load', {source: $('#source').val(), filename: $('#filename').val()}, function(data){
            $('#result').text(data.res);
            $('#result').removeClass('alert-success alert-warning').addClass(data.success ? 'alert-success' : 'alert-warning')
        });
    });
});