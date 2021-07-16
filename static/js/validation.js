

function validate(){
    var temperature = parseFloat(document.getElementById("formId").elements[0].value);
    var humidity = parseFloat(document.getElementById("formId").elements[1].value);
    var ph = parseFloat(document.getElementById("formId").elements[2].value);
    var rainfall = parseFloat(document.getElementById("formId").elements[3].value);
    var flags = [];
    flags[0] = validateElement(temperature,5,45,"tempV");
    flags[1] = validateElement(humidity,10,100,"humV");
    flags[2] = validateElement(ph,3,10,"phV");
    flags[3] = validateElement(rainfall,15,300,"rainV");
    if(flags.reduce((a,b)=>{return a+b;})==0){
        document.getElementById("Button").disabled=false;
    }
}

function validateElement(element, lower, upper, Id){
    if(element<lower || element>upper){
        document.getElementById(Id).innerHTML="Values between "+lower+" and "+upper+" allowed!";
        document.getElementById("Button").disabled=true;
        return 1;
    }
    else{
        document.getElementById(Id).innerHTML="";
        return 0;
    }
}