document.addEventListener("DOMContentLoaded", function() {

    // Highlight the active nav link based on the current page URL
    var navLinks = document.getElementsByTagName("a");
    var currentPage = window.location.pathname;

    for (var i = 0; i < navLinks.length; i++) {
        if (navLinks[i].getAttribute("href") === currentPage) {
            navLinks[i].className = "active";
        }
    }

    // Disable nav links based on login status
    var nav = document.getElementsByTagName("nav")[0];
    var loggedIn = nav.getAttribute("data-logged-in");

    if (loggedIn === "true") {
        // User is logged in — grey out Login and Register
        document.getElementById("nav-login").classList.add("disabled-link");
        document.getElementById("nav-register").classList.add("disabled-link");
    } else {
        // User is not logged in — grey out Home, Timer, and Logout
        document.getElementById("nav-home").classList.add("disabled-link");
        document.getElementById("nav-timer").classList.add("disabled-link");
        document.getElementById("nav-logout").classList.add("disabled-link");
    }

    // Highlight overdue due dates in the assignments table
    var dateCells = document.getElementsByClassName("due-date");
    var today = new Date();
    today.setHours(0, 0, 0, 0);

    for (var j = 0; j < dateCells.length; j++) {
        var dueDate = new Date(dateCells[j].getAttribute("data-date"));
        if (dueDate < today) {
        }
    }

});

