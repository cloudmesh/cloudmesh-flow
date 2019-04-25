/*
 * This file is used in the home.html to call the rest api that visualizes the selected workflow.
 *
 */


let ns = {};


ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'list',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
     };


}());


ns.view = (function() {
    'use strict';



    // return the API
    return {

        build_table: function(flows) {
            let rows = ''


            $('.flows table > tbody').empty();


            if (flows) {
                var t = $('#flows').DataTable();
                for (let i=0, l=flows.length; i < l; i++) {
                  var name = `<a href="/flow/monitor/${flows[i].name}">${flows[i].name}</a>`;
                  t.row.add([name, flows[i].modified]).draw(false);

                }

            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body');



    setTimeout(function() {
        model.read();
    }, 100)






    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);

    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));

