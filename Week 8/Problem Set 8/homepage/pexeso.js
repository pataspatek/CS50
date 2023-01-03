const cardId = ["card-1", "card-2", "card-3", "card-4", "card-5", "card-6", "card-7", "card-8", "card-9", "card-10", "card-11", "card-12"];
const data = ["data-1", "data-2", "data-3", "data-4", "data-5", "data-6", "data-7", "data-8", "data-9", "data-10", "data-11", "data-12"];


function start() {
    document.getElementById('pexeso-table').removeAttribute('hidden');
    document.getElementById('start-pexeso').innerHTML = "Restart";

    var pictures = ["pexeso/python.png", "pexeso/python.png", "pexeso/r.png", "pexeso/r.png", "pexeso/php.jpg", "pexeso/php.jpg", "pexeso/JS.png", "pexeso/JS.png", "pexeso/java.png", "pexeso/java.png", "pexeso/c_plus.png", "pexeso/c_plus.png"];

    for (let i = 0; i < 12; i++) {
        let randomImg = pictures[Math.floor(Math.random()*pictures.length)];
        document.getElementById(cardId[i]).src = randomImg;
        pictures.splice(pictures.indexOf(randomImg), 1);

        document.getElementById(cardId[i]).style.visibility = "hidden";
        document.getElementById(data[i]).style.border = "3px solid blue";
    }
}


var flippedId = [];
var flippedPictureSource = [];

function flipCard(id) {
    var picture = document.getElementById(cardId[id]);
    var surface = document.getElementById(data[id]);

    if (flippedId.length < 2 && picture.style.visibility == "hidden") {

        picture.style.visibility = "visible";

        if (flippedId[0] != cardId.indexOf(cardId[id])) {
            flippedId.push(cardId.indexOf(cardId[id]));
            flippedPictureSource.push(picture.src);
        }

        if (flippedId.length == 2) {
            var first = document.getElementById(cardId[flippedId[0]]);
            var second = document.getElementById(cardId[flippedId[1]]);

            if (flippedPictureSource[0] == flippedPictureSource[1]) {
                document.getElementById(data[flippedId[0]]).style.border = "3px solid green";
                document.getElementById(data[flippedId[1]]).style.border = "3px solid green";
                flippedId = [];
                flippedPictureSource = [];
            } else {
                setTimeout(() => {
                    first.style.visibility = "hidden";
                    second.style.visibility = "hidden";
                }, 2000);
                setTimeout(() => {
                    flippedId = [];
                    flippedPictureSource = [];
                }, 2000);
            }
        }
    }
}


