document.addEventListener('DOMContentLoaded', function() {

    let select_all_trucks = document.querySelector("#all_trucks");
    let select_all_speds = document.querySelector("#all_sped");
        select_all_trucks.onchange = function () {
        if (select_all_trucks.checked == true) {
            truck_boxes.forEach(function(box) {
            box.checked = true;
        });
        }
        else {
            truck_boxes.forEach(function(box) {
            box.checked = false;
        });
        }};


        let truck_boxes = document.querySelectorAll("#truck_box");
        let sped_boxes = document.querySelectorAll("#sped_box");
        select_all_speds.onchange = function () {
        if (select_all_speds.checked == true) {
            sped_boxes.forEach(function(box) {
            box.checked = true;
        });
        }
        else {
            sped_boxes.forEach(function(box) {
            box.checked = false;
        });
        };

    
}});