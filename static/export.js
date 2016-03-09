function switchStage(stage, details) {
    $('.stage').hide().filter('#stage-' + stage).show().find('#details').text(details || '');
}

function checkPath() {
    var path = $('#path').val();
    $.getJSON('/export/check_path', {path: path}, function(data) {
        switchStage(data.ok ? 'confirm' : 'bad-path', path);
    });
}

$(function(){
    $('a[href^=#stage-]').click(function(e){
        e.preventDefault();
        switchStage($(this).attr('href').replace(/#stage\-/, ''));
    })
    $('#path').keydown(function(e){
        switchStage('nothing');
    });
    $('#check-path').click(checkPath);
    $('a[href=#stage-export]').click(function(){
        $.getJSON('/export/do_export', {path: $('#path').val()}, function(data){
            if (data.ok)
                switchStage('success');
            else
                switchStage('failed', data.error);
        });
    });
});
