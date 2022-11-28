let instructionsShown = false;

function showInstructions(){
    console.log(instructionsShown)
    const section = document.getElementById('instructions');
    if (instructionsShown == false) {
        section.style.display = 'flex';
        instructionsShown = true;
    }
    else {
        section.style.display = 'none';
        instructionsShown = false;
    }
}
