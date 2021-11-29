
const size = 3;
const q = 12;
const op = ['A', 'B', 'C', 'D'];
var mood = "";

// make int and address
function toAdress(address){
    var Saddress = address.toString();
    return "0".repeat(size-Saddress.length) + Saddress;
}

// return int of random question
function selectQ(){
    var temp = Math.random()*100;
    return (temp - temp%1)%q;
}

function chargeMood(){
    mood = "/spotifySearch/result?mood=";
    for(var i = 0; i < q; i++){
        var qDiv = document.getElementById(toAdress(i));
        //console.log(qDiv);
        if(qDiv){
            var selected = document.getElementById(toAdress(i)).getElementsByClassName("selected")[0];
            //console.log(selected);
            if(selected){
                mood = mood.concat(document.getElementById(toAdress(i)).getElementsByClassName("selected")[0].id);
            }else{
                mood = mood.concat("n");
            }
        }else{
            mood = mood.concat("n");
        }
    }
    console.log(mood);
    document.getElementById("load").href = mood;
}

function selectIMG(e){
    parentDiv = e.target.parentElement.getElementsByTagName("img");
    for(i in parentDiv) parentDiv[i].className = "";
    e.target.classList.add("selected");
    chargeMood();
}

function setUp(){
    chargeMood();
    const main = document.getElementById("questions");
    var n = 7;

    // create set of questions
    var qSet = new Set([]);
    while(n){
        const p = toAdress(selectQ());
        if(!qSet.has(p)){
            qSet.add(p);
            n--;
        }
    }
    qSet.forEach(key => {
        var qDiv = document.createElement("div");
        qDiv.id = key;

        //Assign title
        var title = document.createElement("h1");
        // Get text from question
        fetch("../static/questions/q"+key+"/question.txt")
        .then(response => response.text())
        .then(data => {
            title.innerHTML = key + " " + data;
        });
        qDiv.appendChild(title);

        // Get images
        for( d in op){
            var image = document.createElement("img");
            image.id = op[d];
            image.setAttribute("onclick", "selectIMG(event)");
            image.src = "../static/questions/q"+key+"/img/"+op[d]+".png";
            qDiv.appendChild(image);
        }

        main.appendChild(qDiv);
    })
}









