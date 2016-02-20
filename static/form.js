$(function() {
	//This allows the Match ID field to be automatically filled
	//based on the previous value entered + 1
    $('#match_id').val(Number(localStorage.getItem('last_match_id')) + 1);
    $('#scouting-form').on('submit', function() {
        localStorage.setItem('last_match_id',$('#match_id').val());
    });
    //Allows input boxes to be changed with arrow keys
    $("input[type='text']").keydown(function(e){
    	if(e.keyCode == 38){
    		this.value = parseInt(this.value)+1;
    	} else if (e.keyCode == 40){
    		this.value = parseInt(this.value)-1;
    	}
    });

    //Add +/- buttons next to input fields so it is easy on touchscreen
    function mkbutton() {
        return $('<a>').attr('href', '#').addClass('btn btn-default').click(function(e){e.preventDefault();});
    }
    $('input[type=text]').each(function(i, e) {
        var increment = function(n) {
            return function() {
                $(e).val(Number($(e).val()) + n);
                $(e).trigger('keyup');
            }
        }
        var button_inc = mkbutton().text('+').insertAfter($(e)).click(increment(1));
        var button_dec = mkbutton().text('-').insertBefore($(e)).click(increment(-1));
        var width = 8;
        var height = 15;
        button_inc.width(width).height(height);
        button_dec.width(width).height(height);
    });
});
