let instructionsShown = false;

function showInstructions(){
    console.log(instructionsShown)
    const section = document.getElementById('instructions');
    if (instructionsShown == false) {
        section.style.display = 'block';
        instructionsShown = true;
    }
    else {
        section.style.display = 'none';
        instructionsShown = false;
    }
}
