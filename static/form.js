$(function() {
	//This allows the Match ID field to be automatically filled
	//based on the previous value entered + 1
    $('#match_id').val(Number(localStorage.getItem('last_match_id')) + 1);
    $('#scouting-form').on('submit', function() {
        localStorage.setItem('last_match_id',$('#match_id').val());
    });
});
