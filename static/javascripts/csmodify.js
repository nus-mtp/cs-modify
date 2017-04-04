/****************************************************************/
/* =============== CS-MODIFY JAVASCRIPT FILE ================== */
/* This file serves as the central javascript source for all the*/
/* custom-defined animations or interactions on the page.       */
/****************************************************************/

/*
 * FUNCTIONS FOR SIDEBAR ANIMATIONS
 */

/* Set the width of the side navigation to 400px */
function openSidebar() {
    document.getElementById("sidebar").style.width = "400px";
}

/* Set the width of the side navigation to 0 */
function closeSidebar() {
    document.getElementById("sidebar").style.width = "0";
}

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
  $('#sidebar-button').click(function(e) {
    e.stopPropagation();
    openSidebar();
  });
  $('body').click(function(e) {
    if (e.target.id != 'sidebar') {
        closeSidebar();
    }
  });
})

/*
 * FUNCTIONS FOR SCROLLING TO TOP OF PAGE
 */

// Collapses the navbar on scroll
$(window).scroll(function() {
    try{
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
        }
    }catch(err){
        console.log(err.message, err.name);
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

/*
 *   FUNCTION FOR SHOWING PROMPT WHEN USER CLICKS ON LOGOUT BUTTON
 */
 function confirmLogout() {
    toLogout = window.confirm("Are you sure you want to logout?");
    if (toLogout) {
        $.ajax({
            type: "POST",
            url: "/logout"
        }).done(function() {
            window.location = "/login";
        })
    }
 }

/*
 * FUNCTIONS FOR CUSTOM VALIDATION MESSAGES FOR LOGIN
 * AND REGISTRATION FORMS
 */
function check(input) {
    if (input.validity.patternMismatch) {
        input.setCustomValidity("User ID should be alphanumeric and within 9 characters.");
    } else if (input.validity.valueMissing) {
        input.setCustomValidity("Please fill in your User ID.");
    }
}


/* ========== DOCUMENT-READY FUNCTIONS ========== */
$(document).ready(function() {
    /*
     * READY FUNCTION:FUNCTIONS FOR ENABLING SORTING FOR CERTAIN TABLES
     */

    /*
     * order: [column #, asc/desc],
     * where column # uses 0-based indexing
     * from left to right
    */
    var table = $('#module-listing-table').DataTable( {
        "aaSorting": [],
    } );

    // Apply the search
    table.columns().every( function () {
        var col = this;
 
        $('input', this.header()).on('keyup change', function () {
            if (col.search() !== this.value) {
                col
                    .search(this.value)
                    .draw();
            }
        } );

        $('#toggleButton').on('click', function () {
            if (col.search() !== this.value) {
                col
                    .search(this.value)
                    .draw();
            }
        } );
    } );

    $('#delete-module-table').DataTable( {
        "aaSorting": []
    } );

    $('#fixed-mounting-table').DataTable( {
        "aaSorting": [],
        "columnDefs": [
            { type: 'num-html', width: "12%", targets: 3 },
            { type: 'num-html', width: "12%", targets: 4 },
            { type: 'num-html', width: "12%", targets: 6 },
            { type: 'num-html', width: "12%", targets: 7 }
        ],
        "initComplete": function(settings, json) {
            $('#fixed-mounting-table').show();
            $('.toggle-columns-display').show();
            $('.loading-div').hide();
            $('#fixed-mounting-table').DataTable().columns.adjust().draw();
            setTimeout(function() {
                $('.dataTable').width("100%");
            }, 200);
        }
    } );

    $('#tentative-mounting-table').DataTable( {
        "aaSorting": [],
        "columnDefs": [
            { type: 'num-html', width: "12%", targets: 3 },
            { type: 'num-html', width: "12%", targets: 4 },
            { type: 'num-html', width: "12%", targets: 6 },
            { type: 'num-html', width: "12%", targets: 7 }
        ],
        "initComplete": function(settings, json) {
            $('#tentative-mounting-table').show();
            $('.toggle-columns-display').show();
            $('.loading-div').hide();
            $('#tentative-mounting-table').DataTable().columns.adjust().draw();
            setTimeout(function() {
                $('.dataTable').width("100%");
            }, 200);
        }
    } );

    $('#student-year-table').DataTable( {
        "aaSorting": [],
        "bPaginate": false,
        "searching": false
    } );

    $('#modified-modules-summary-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" }
        ]
    } );

    $('#modified-modules-mounting-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" }
        ]
    } );

    $('#modified-modules-quota-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" },
            { "targets": [2, 3, 4], "width": "13%", type: 'num-html' }
        ]
    } );

    $('#modified-modules-details-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" },
        ]
    } );

    $('#specific-modified-module').DataTable( {
        "autoWidth": false,
        "columnDefs": [
            { "targets": [0, 1], "width": "25%" }
        ]
    } );

    $('#student-focus-area-table').DataTable( {
        "aaSorting": [],
        "pageLength": 25,
        "bPaginate": false,
        "searching": false
    } );

    $('#oversubscribed-modules-table').DataTable( {
        "order": [[ 4, "desc" ]],
        "columnDefs": [
            { "targets": 0, "width": "8%" },
            { "targets": 3, "type": 'num-html', "width": "12%" },
            { "targets": 4, "width": "12%" },
            { "targets": 5, "width": "12%" }
        ],
        "initComplete": function(settings, json) {
            $('#oversubscribed-modules-table').show();
            $('.loading-div').hide();
            $('#oversubscribed-modules-table').DataTable().columns.adjust().draw();
            setTimeout(function() {
                $('.dataTable').width("100%");
            }, 200);
        }
    } );

    $('#modules-taken-prior-table').DataTable( {
        "order": [[ 6, "desc" ], [ 0, "asc" ], [ 3, "asc" ]],
        "columnDefs": [
            { "targets": [0, 3], "width": "8%" },
            { "targets": [1, 4], "width": "20%" },
            { "targets": 6, "width": "20%" }
        ],
        "initComplete": function(settings, json) {
            $('#modules-taken-prior-table').show();
            $('.loading-div').hide();
            $('#modules-taken-prior-table').DataTable().columns.adjust().draw();
            setTimeout(function() {
                $('.dataTable').width("100%");
            }, 200);
        }
    } );

    $('#modules-taken-prior-intern-table').DataTable( {
        "order": [[ 2, "desc" ]],
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "60%" },
        ]
    } );
     
    $('#common-module-table').DataTable( {
        "aaSorting": [],
        "initComplete": function(settings, json) {
            $('#common-module-table').show();
            $('.loading-div').hide();
            $('#common-module-table').DataTable().columns.adjust().draw();
            setTimeout(function() {
                $('.dataTable').width("100%");
            }, 200);
        }
    } );

    $('#non-overlap-table').DataTable( {
        "aaSorting": [],
        "deferRender": true,
        "initComplete": function(settings, json) {
            $('#non-overlap-table').show();
            $('.loading-div').hide();
            $('#non-overlap-table').DataTable().columns.adjust().draw();
            setTimeout(function() {
                $('.dataTable').width("100%");
            }, 200);
        }
    } );
     
    $('#students-taking-module-table').DataTable({
       aaSorting: [],
        "deferRender": true
    });

    $('#mod-specific-size-table').DataTable( {
        "order": [[ 2, "asc"]]
    } );
} );

window.onresize = function() {
    $('.dataTable').width("100%");
}
