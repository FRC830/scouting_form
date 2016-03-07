$(function() {
	//This allows the Match ID field to be automatically filled
	//based on the previous value entered + 1
    $('#match_id').val(Number(localStorage.getItem('last_match_id')) + 1);
    $('#scouting-form').on('submit', function() {
        localStorage.setItem('last_match_id',$('#match_id').val());
    });

    //Add +/- buttons next to input fields so it is easy on touchscreen
    function mkbutton() {
        return $('<a>').attr('href', '#').addClass('btn btn-default input-group-addon').click(function(e){e.preventDefault();});
    }
    $('input[type=number]').each(function(i, e) {
        var increment = function(n) {
            return function() {
                $(e).val(Number($(e).val()) + n);
                $(e).trigger('keyup');
            }
        }
        var button_inc = mkbutton().text('+').insertAfter($(e)).click(increment(1));
        var button_dec = mkbutton().text('-').insertBefore($(e)).click(increment(-1));
    });
    $('.checkbox-button-field input[type=checkbox]').change(function() {
        var label = $(this).parent('label');
        label.removeClass('btn-default btn-success').addClass(
            $(this).prop('checked') ? 'btn-success' : 'btn-default'
        );
    });
});
