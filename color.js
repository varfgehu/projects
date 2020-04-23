function selectBackground(){
    var e = document.getElementById("color");
    var BackgroundValue = e.options[e.selectedIndex].value;
    document.body.style.backgroundColor=BackgroundValue;
}