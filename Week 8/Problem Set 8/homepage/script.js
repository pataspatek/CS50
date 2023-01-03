function darkMode() {
    if (document.body.style.backgroundColor == "black") {
        document.body.style.backgroundColor = "white";
        document.getElementById('btn').src = "assets/moon.jpg";
        document.getElementById('header').style.color = "black";
        document.getElementById('options').style.color = "blue";
        document.getElementById('bottom-bar').style.backgroundColor = "white";
    } else {
        document.body.style.backgroundColor = "black";
        document.getElementById('btn').src = "assets/sun.jpg";
        document.getElementById('header').style.color = "white";
        document.getElementById('options').style.color = "white";
        document.getElementById('bottom-bar').style.backgroundColor = "black";
    }
}


