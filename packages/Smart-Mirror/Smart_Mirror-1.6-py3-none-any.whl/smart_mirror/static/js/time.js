function doDate()
{
    Date.prototype.monthNames = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ];
    Date.prototype.dayNames = [
        "Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Saturday"
    ];


    Date.prototype.getMonthName = function() {
        return this.monthNames[this.getMonth()];
    };
    Date.prototype.getShortMonthName = function () {
        return this.getMonthName().substr(0, 3);
    };
    Date.prototype.getDayName = function() {
        return this.dayNames[this.getDay()];
    };
    Date.prototype.getShortDayName = function() {
        return this.getDayName().substr(0, 3);
    };

    var now = new Date();
    
    // date = now.toDateString();
    day = now.getShortDayName();
    date = now.getDate();
    month = now.getShortMonthName();
    year = now.getFullYear();

    var hr = now.getHours();
    var min = now.getMinutes();
    if (min < 10) {
        min = "0" + min;
    }
    var ampm = "AM";
    
    if(hr == 12) {          // 12:00 --> 12:00 PM
        ampm = "PM";
    }
    else if(hr == 0) {      // 00:00 --> 12:00 AM
        hr += 12;
    }
    else if( hr > 12 ) {    // 13:00 --> 01:00 PM
        hr -= 12;
        ampm = "PM";
    }


    // time = now.toLocaleTimeString();
    document.getElementById("day").innerHTML = day;
    document.getElementById("date").innerHTML = date;
    document.getElementById("month").innerHTML = month;
    document.getElementById("year").innerHTML = year;
    // document.getElementById("todaysDate").innerHTML = day + ", " + date + " " + month + " " + year;
    document.getElementById("hr").innerHTML = hr;
    document.getElementById("min").innerHTML = min;
    document.getElementById("ampm").innerHTML = ampm;
}

setInterval(doDate, 60000);