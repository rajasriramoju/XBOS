$(document).ready(function() {
    $("input").change(function(){
        if($(this).is(":checked")){
            console.log("Is checked");
            document.getElementById("intelligence-control-on-off").innerText = "Intelligent Control On"
            document.getElementById("intelligent-control").style.backgroundColor = "green"
        }
        else{
            console.log("Is Not Checked");
            document.getElementById("intelligence-control-on-off").innerText = "Intelligent Control Off"
            document.getElementById("intelligent-control").style.backgroundColor = "red"
        }
    })
})