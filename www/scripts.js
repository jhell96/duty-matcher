$(document).ready(function() {
    var site_base_url = 'http://localhost:5000';
    
    $('#loader').hide();

    // button handler for help queue
    $("#run-button").on('click', function () {
        var freshq = $("#freshman-q").prop('value');
        var sophq = $("#sophomore-q").prop('value');
        var junq = $("#junior-q").prop('value');
        var senq = $("#senior-q").prop('value');
        $('#assignments-table').empty()
        $('#loader').show();

        $.ajax({
            type: "GET",
            url: site_base_url + "/run",
            data: 'freshman-q='+freshq+'&sophomore-q='+sophq+'&junior-q='+junq+'&senior-q='+senq
        }).then(function(data) {
            $('#loader').hide();
            $('#assignments-table').empty()
            for (key in data.results) {
                var key_render = key.split('_').slice(0, -1).join(' ')
                $('#assignments-table').append(
                    $('<tr>').append(
                        $('<td>').text(key_render),
                        $('<td>').text(data.results[key])
                    )
                );
            }
        });
    });
});