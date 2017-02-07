// $(function(){
// 	$('searchButton').click(function(){
// 		$.ajax({
// 			url: '/',
// 			data: $('search').serialize(),
// 			type: 'POST',
// 			success: function(response){
// 				console.log(response);
// 			},
// 			error: function(error){
// 				console.log(error);
// 			}
// 		});
// 	});
// });

function updateResults(results)
{
  var table = document.getElementById("searchResults")
  var results = document.results
  console.log(results);
  for(i = 0; i < results.length; i++)
  {
    console.log(results[i])
  }
}
