function generateValidationRules(form) {
    var rules = {};
    form.find('input[type=number]').each(function(_, e) {
        rules[$(e).attr('name')] = {
            min: 0,
            required: true,
        };
    });
    return rules;
}

$(function() {
	//This allows the Match ID field to be automatically filled
	//based on the previous value entered + 1
    if (!$('#match_id').val())
        $('#match_id').val(Number(localStorage.getItem('last_match_id')) + 1);
    $('#scouting-form').on('submit', function() {
        localStorage.setItem('last_match_id',$('#match_id').val());
    }).validate({
        rules: generateValidationRules($('#scouting-form')),
        highlight: function(element) {
            $(element).closest('.form-field').addClass('has-error');
        },
        unhighlight: function(element) {
            $(element).closest('.form-field').removeClass('has-error');
        },
        errorElement: 'span',
        errorClass: 'help-block',
        errorPlacement: function(error, element) {
            // disable messages
            return true;
        }
    });

    //Add +/- buttons next to input fields so it is easy on touchscreen
    function mkbutton() {
        return $('<a>').attr('href', '#').addClass('btn btn-default input-group-addon').click(function(e){e.preventDefault();});
    }
    $('input[type=number]').each(function(i, e) {
        if ($(e).hasClass('no-buttons'))
            return;
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
