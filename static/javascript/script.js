"use strict";

/*Function which changes gallery main image while updating opacity of thumbnails.*/
function imgUpdate(thumbnailIndex) {
    var thumbnail = document.getElementsByClassName('thumbnail');
    var i;
    /*Sets all thumbnails to semi-transparant.*/
    for (i = 0; i < thumbnail.length; i++) {
        thumbnail[i].style.opacity = 0.5;
    }
    /*Changes gallery image.*/
    switch (thumbnailIndex) {
    case 0:
        document.getElementById('currentImage').src = "../../static/images/details-page/living-room.jpg";
        break;
    case 1:
        document.getElementById('currentImage').src = "../../static/images/details-page/bathroom.jpg";
        break;
    case 2:
        document.getElementById('currentImage').src = "../../static/images/details-page/bedroom.jpg";
        break;
    case 3:
        document.getElementById('currentImage').src = "../../static/images/details-page/kitchen.jpg";
        break;
    }
    /*Sets chosen thumbnail to fully opacity to give the illusion it is active.*/
    thumbnail[thumbnailIndex].style.opacity = 1;
}

/*Function which loads a Google Map API*/
function loadMap() {
    var kapalua = {
        lat: 21.003528
        , lng: -156.660055
    };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 18
        , center: kapalua
    });
    var marker = new google.maps.Marker({
        position: kapalua
        , map: map
    });
}

/*Function which displays tab content.*/
function openTab(event, page) {
    var tabContent = document.getElementsByClassName('tabContent');
    var tablinks = document.getElementsByClassName('tablinks');
    var i;
    /*Resets all tab content to hidden*/
    for (i = 0; i < tablinks.length; i++) {
        tabContent[i].style.display = "none";
    }
    /*Resets all tab links to non-active*/
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    /*Displays chosen tab*/
    document.getElementById(page).style.display = "block";
    event.currentTarget.className += " active";
}

/*Function is an extension of openTab above; automatically sets dining as default tab.*/
window.onload = function() {
    document.getElementById("defaultTab").click();
}

/*Gets current date and returns it in formatted style.*/
function getCurrentDate() {
    var currentDate = new Date();
    var day = currentDate.getUTCDate();
    var month = currentDate.getUTCMonth() + 1;
    var year = currentDate.getUTCFullYear();
    var monthNames = ["January", "February", "March", "April", "May", "June"
            , "July", "August", "September", "October", "November", "December"];
    var formattedDate = (monthNames[month] + ' ' + day + ' ' + year);
    return formattedDate;
}

/*Prevents user from entering nothing in review section.*/
$(document).ready(function () {
    $('#review').keyup(function () {
        if ($.trim($('#review').val()) === '') {
            document.getElementById('postButton').disabled = true;
        }
        else {
            document.getElementById('postButton').disabled = false;
        }
    });
});

/*Functions below open and close form (depending on where the user clicks for close) */
function openForm() {
    var form = document.getElementById('form');
    form.style.display = "block";
}

function closeForm() {
    var form = document.getElementById('form');
    form.style.display = "none";
}

function externalClick() {
    var form = document.getElementById('form');
    if (event.target == form) {
        form.style.display = "none";
    }
} 

/*Allows user to close confirmation after their booking*/
function closeConfirmation() {
    var form = document.getElementById('confirmationBox');
    confirmationBox.style.display = "none";
}

/*Function which finds the difference between two dates*/
function dateDifference() {
    var oneDay = 86400000; /* Milliseconds in a day */
    var firstDate = new Date(document.getElementById('startDate').value);
    var secondDate = new Date(document.getElementById('endDate').value);
    
    var difference = (secondDate.getTime() - firstDate.getTime())/(oneDay);
    
    return difference;
}

/*Function which updates price when user changes dates*/
$(document).ready(function () {
    setMaxMinDates();
    $('#startDate, #endDate').change(function () {
        var diff = dateDifference();
        var price = (diff * 100);
        setMaxMinDates();
        bookingOverlap();
        
        /* Prevents anything but a positive number (or 0) being outputted as the price. */
        if (isNaN(diff)) {
            price = 0;
            diff = 0;
        }  else if (diff < 0) {
            price = 0;
            diff = 0;
        }
        
        price += 150;
        
        /* Prints out price onto form while displaying it with thousands seperators */
        document.getElementById('nights').innerHTML = diff;
        document.getElementById('changingPrice').innerHTML = price.toLocaleString();
    });
});

/*Function which takes rental list from HTML template and stores it into the global
variable for use in other functions.*/
var allStartDate;
var allEndDate;
function sendList(start, end) {
    allStartDate = start;
    allEndDate = end;
}

/*Function which checks if users date range is already booked*/
function bookingOverlap() {
    var startDate = new Date(document.getElementById('startDate').value);
    var endDate = new Date(document.getElementById('endDate').value);
    var fileStartDate;
    var fileEndDate;
    var overlap = false;
    
    /*Tests whether two date ranges overlap*/
    for (var i = 0; i < allStartDate.length; i++) { 
        fileStartDate = new Date(allStartDate[i]);
        fileEndDate = new Date(allEndDate[i]);
        
        if ((startDate <= fileEndDate) && (fileStartDate <= endDate)) {
            overlap = true;
            break;
        }
    }
    
    /*Displays message if dates overlap*/
    if (overlap) {
        document.getElementById('overlap').style.visibility = "visible";
        document.getElementById('overlap').style.opacity = 1;
        document.getElementById('bookButton').disabled = true;
    } else {
        document.getElementById('overlap').style.visibility = "hidden";
        document.getElementById('bookButton').disabled = false;
    }
}



/*Function which returns current date in format accepted by HTML*/
function getHTMLDate(aDate) {
    var dd = aDate.getDate();
    var mm = aDate.getMonth() + 1;
    var yyyy = aDate.getFullYear();
    
    /*Ensures dates and months are in correct format*/
    if (dd < 10) {
        dd = '0' + dd;
    } 
    
    if (mm < 10) {
        mm = '0' + mm;
    } 
    
    return yyyy + '-' + mm + '-' + dd;
}

/*Fucntion which prevent user from creating illogical bookings by constantly changing the minimum possible date*/
function setMaxMinDates() {
    var startDate = document.getElementById("startDate");
    var endDate = document.getElementById("endDate");
    
    /*Sets start date minimum date to today*/
    var dateChanger = getHTMLDate(new Date());
    startDate.setAttribute("min", dateChanger);
    
    /*Prevents user from selecting start date which is after end date*/
    if (dateDifference() < 0) {
        dateChanger = getHTMLDate(new Date(startDate.value));
        endDate.value = dateChanger;
    }
    
    /*Sets check out date minimum value to chosen start date, else sets it to today if none has been chosen*/
    if (startDate && startDate.value) {
        dateChanger = getHTMLDate(new Date(startDate.value));
        endDate.setAttribute("min", dateChanger);
    } else {
        var dateChanger = getHTMLDate(new Date());
        endDate.setAttribute("min", dateChanger);
    }
}