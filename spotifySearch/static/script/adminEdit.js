
const size = 3;
const q = 12;
const op = ['A', 'B', 'C', 'D'];
const moodForm = document.getElementById('mood');

function validateMood(mood){
    if(mood.length != q) return false;
    for(var i = 0; i < q; i++){
        if(!(mood[i] == 'n' || mood[i] == 'A' || mood[i] == 'B' || mood[i] == 'C' || mood[i] == 'D')){
            return false;
        }
    }
    return true;
}

moodForm.addEventListener('input', ()=>{
    if(validateMood(moodForm.value)){
        document.getElementById('error').innerHTML = "Valid Mood";
        document.getElementById('submit').style.display = 'block';

        var qsDiv = document.getElementById('questions');
        for(var i = 0; i < q; i++){
            var qDiv = qsDiv.childNodes[i].getElementsByTagName('img');
            for(var j = 0; j < 4; j++){
                if(moodForm.value[i] == qDiv[j].id) qDiv[j].className = "selected";
                else qDiv[j].className = "";
            }
        }

    }else{
        document.getElementById('error').innerHTML = "Not A Valid Mood";
        document.getElementById('submit').style.display = 'none';
    }
});

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

function selectIMG(e){
    parentDiv = e.target.parentElement.getElementsByTagName("img");
    for(i in parentDiv) parentDiv[i].className = "";
    e.target.classList.add("selected");

    var tempMood = "";
    var qsDiv = document.getElementById('questions');
    for(var i = 0; i < q; i++){
        var qDiv = qsDiv.childNodes[i].getElementsByTagName('img');
        for(var j = 0; j < 5; j++){
            if(j == 4){
                tempMood = tempMood.concat('n');
                break;
            }
            if(qDiv[j].className == "selected"){ 
                tempMood =  tempMood.concat(qDiv[j].id);
                break;
            }
        }
    }

    console.log(tempMood)
    moodForm.value = tempMood;

    document.getElementById('error').innerHTML = "Valid Mood";
    document.getElementById('submit').style.display = 'block';
}

function setUp(){
    const main = document.getElementById("questions");
    const moodForm = document.getElementById('mood');

    // create set of questions
    var qSet = new Set([]);
    for(var i = 0; i < q; i++){
        qSet.add(toAdress(i));
    }

    qSet.forEach(key => {
        var qDiv = document.createElement("div");
        qDiv.id = key;

        //Assign title
        var title = document.createElement("h1");
        // Get text from question
        fetch("../../spotifySearch/static/data/questions/q"+key+"/question.txt")
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
            image.src = "../../spotifySearch/static/data/questions/q"+key+"/img/"+op[d]+".png";
            if(moodForm.value[parseInt(key)] == op[d]) image.className = "selected";
            qDiv.appendChild(image);
        }

        main.appendChild(qDiv);
    })
}