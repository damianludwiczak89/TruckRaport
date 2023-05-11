document.addEventListener('DOMContentLoaded', function() {

    // Show button to confirm delete truck
    document.querySelector("#delete_truck").onclick = function () {
        if (document.querySelector("#confirmation").style.display == "none") {
            document.querySelector("#confirmation").style.display = "block";
        }
        else {
            document.querySelector("#confirmation").style.display = "none"
        }
    };

    // Hide edit tour form
    document.querySelector("#edit_tour_form").style.display = "none";

    // Button to hide edit tour form
    document.querySelector('#cancel').onclick = function () {
        document.querySelector("#add_tour_form").style.display = "block";
        document.querySelector("#edit_tour_form").style.display = "none";
    }
    // Get user's default rate and display it on the form
    fetch('/default_rate')
    .then(response => response.json())
    .then(default_rate => {
        let rate = parseFloat(default_rate.default_rate);
        document.querySelector("#id_Rate").value = rate;
        document.querySelector("#id_Default_rate").value = rate;
    });

    // Function to change the default rate in database
    document.querySelector('#change_rate').onclick = function () {
        fetch('/default_rate', {
            method: 'PUT',
            body: JSON.stringify({
                default_rate: document.querySelector("#id_Default_rate").value
            })
          })
          .then(() => {
            document.querySelector("#id_Rate").value = document.querySelector("#id_Default_rate").value;
         });
        };
        
    // Calculate freight when km is input
    document.querySelector('#id_Km').onchange = function () {
        km = document.querySelector('#id_Km').value;
        rate = document.querySelector("#id_Rate").value;
        document.querySelector("#id_Freight").value = km * rate;
    };

    // Change the rate if input freight manullay is gives rate other than default
    document.querySelector('#id_Freight').onchange = function () {
        km = document.querySelector('#id_Km').value;
        rate = document.querySelector("#id_Rate").value;
        freight = document.querySelector("#id_Freight").value;
        document.querySelector("#id_Rate").value = freight/km;
    };

    // Same functons as above but for edit form fields
    km = document.querySelectorAll('#id_Km');
    km[1].onchange = function () {
        km = document.querySelectorAll('#id_Km');
        km = km[1].value;
        rate = document.querySelectorAll("#id_Rate");
        rate = rate[1].value;
        freight = document.querySelectorAll("#id_Freight");
        freight[1].value = km * rate;

    };
    freight = document.querySelectorAll('#id_Freight');
    freight[1].onchange = function () {
        km = document.querySelectorAll('#id_Km');
        km = km[1].value;
        rate = document.querySelectorAll("#id_Rate");
        
        freight = document.querySelectorAll("#id_Freight");
        freight = freight[1].value;
        rate[1].value = freight / km;

    }


    // Hide buttons to confirm delete
    document.querySelectorAll('#confirm_delete').forEach(function(button) {
        button.style.display = "none";
        });
    
        document.querySelectorAll('#delete').forEach(function(button) {
            button.onclick = function () {
            selector_list = document.querySelectorAll(`[data-id=${CSS.escape(button.dataset.id)}]`);
            // Selector list 2 is a div that contains the button
            if (selector_list[3].style.display == "block"){
                selector_list[3].style.display = "none";
            }
            else {
            selector_list[3].style.display = "block";
            }

            }});
    
    // Edit button - hide add form, display edit form
    document.querySelectorAll('#edit').forEach(function(button) {
        button.onclick = function () {

            document.querySelector("#add_tour_form").style.display = "none";
            document.querySelector("#edit_tour_form").style.display = "block";

            fetch('/get_tour/'+button.dataset.id+'')
            .then(response => response.json())
            .then(tour => {
                date = document.querySelectorAll('#id_Date');
                km = document.querySelectorAll('#id_Km');
                freight = document.querySelectorAll('#id_Freight');
                rate = document.querySelectorAll('#id_Rate');
                spedition = document.querySelector('#spedition');
                id = document.querySelector("#id_Id");
                console.log(tour);
                spedition.value = tour.spedition;              
                date[1].value = tour.date;
                km[1].value = tour.km;
                freight[1].value = tour.freight;
                rate[1].value = tour.rate;
                id.value = tour.id;

                // Fetch for the name of the spe

        })
    };
    });

    let button = document.querySelector('#change_truck');
    button.onclick = function () {
        fetch('/edit_truck/'+button.dataset.id+'', {
            method: 'PUT',
            body: JSON.stringify({
                truck_name: document.querySelector("#id_New_name").value
            })
          })
          .then(() => {
            document.querySelector("#truck_name").innerHTML = document.querySelector("#id_New_name").value;
         });
        };
});