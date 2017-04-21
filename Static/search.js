function search() {
    event.preventDefault();
    $.ajax({
        url: '/search',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            table = document.getElementById("searchResults");
            table.innerHTML = "";
            response = JSON.parse(response);
            for (i = 0; i < response.length; i++) {
                row = table.insertRow(i);
                data = row.insertCell(0);
                data.innerHTML = response[i];
                row.setAttribute('onclick', 'getData(this)');
                row.setAttribute('id', response[i])
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function getData(row) {
    var modal = document.getElementById("analyzing");
    cell = row.cells;
    console.log(cell[0].innerHTML);
    name = cell[0].innerHTML;
    searchType = $('#typeSelector').val();
    $.ajax({
        url: '/select',
        data: {
            'name': name,
            'searchType': searchType
        },
        type: 'POST',
        beforeSend: function() {
            modal.style.display = "block";
        },
        success: function(response) {
            window.location = "/users";
        },
        error: function(error) {
            console.log(error);
        }
    });
}
