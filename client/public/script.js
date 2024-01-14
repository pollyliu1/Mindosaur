// Function to change the text
function changeText() {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = 'The text has been changed!';
}

// Event listener for the button
document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('changeTextBtn');
    button.addEventListener('click', changeText);
});
