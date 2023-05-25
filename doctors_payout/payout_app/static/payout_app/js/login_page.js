


function styleInputLabe() {
    const hexColors = [
        "#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#dfe6e9",
        "#b2bec3", "#6c5ce7", "#0984e3", "#00cec9", "#00b894",
        "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8", "#636e72",
        "#2d3436", "#e84393", "#d63031", "#e17055", "#fdcb6e",
        "#f6e58d", "#ffbe76", "#ff7979", "#badc58", "#dff9fb",
        "#c7ecee", "#6ab04c", "#eb4d4b", "#f0932b", "#f9ca24",
        "#7ed6df", "#e056fd", "#686de0", "#30336b", "#95afc0",
        "#535c68", "#130f40", "#4834d4", "#be2edd", "#22a6b3",
        "#00a8ff", "#9c88ff", "#fbc531", "#4cd137", "#487eb0",
        "#40739e", "#44bd32", "#e1b12c", "#8c7ae6"
    ];
    const label = document.querySelectorAll('label')
    const randomIndex = Math.floor(Math.random() * hexColors.length);
    label.forEach((el) => {

        const randomColor = hexColors[randomIndex];
        el.style.color = randomColor;
    })

    const inputs = document.querySelectorAll('input');
    const errors = document.querySelectorAll('.error');
    const combinedArray = [...inputs, ...errors];
    const randomIndex1 = Math.floor(Math.random() * hexColors.length)
    combinedArray.forEach((el) => {
        const randomColor = hexColors[randomIndex1];
        el.style.color = randomColor;
        el.style.boxShadow = `3px 3px 10px ${randomColor}, -1px -1px 6px ${randomColor}`
    })

}




function typeText() {
    const errorElement = document.querySelector(".error");
    if (!errorElement) return;

    const text = errorElement.innerHTML;
    let currentIndex = 0;

    const intervalId = setInterval(() => {
        if (currentIndex >= text.length) {
            clearInterval(intervalId);
            setTimeout(() => removeText(errorElement, text), 5000);// Delay of 5 seconds (5000 milliseconds)
            return;
        }

        const partialText = text.slice(0, currentIndex + 1);
        errorElement.innerHTML = partialText;
        currentIndex++;
    }, 50); // Adjust the interval time (in milliseconds) to control the typing speed
}

function removeText(errorElement, text) {
    let currentIndex = text.length;

    const intervalId = setInterval(() => {
        if (currentIndex <= 0) {
            clearInterval(intervalId);
            errorElement.remove()
            return;
        }

        const partialText = text.slice(0, currentIndex - 1);
        errorElement.innerHTML = partialText;
        currentIndex--;
    }, 10); // Adjust the interval time (in milliseconds) to control the typing speed
}



styleInputLabe()
setInterval(styleInputLabe, 5000);

typeText();