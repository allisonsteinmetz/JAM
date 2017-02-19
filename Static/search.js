$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

$(function(){
	$('#searchButton').click(function(){
		$.ajax({
			url: '/search',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				table = document.getElementById("searchResults");
				table.innerHTML = "";
				response = JSON.parse(response);
				for(i = 0; i < response.length; i++){
					row = table.insertRow(i);
					data = row.insertCell(0);
					data.innerHTML = response[i];
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
