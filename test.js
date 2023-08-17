Object.defineProperty(String.prototype, 'capitalize', {
    value: function() {
      return this.charAt(0).toUpperCase() + this.slice(1);
    },
    enumerable: false
  });

async function setBubbleText(text) {
    const originalText = text;

    if (text.startsWith(', ')) {
        text = text.substring(2)
    }

    text = text.capitalize()

    console.log("Fixed: " + text)

    const bubbleTextElement = document.getElementById('bubble-text');

    bubbleTextElement.innerHTML = "";

    for (let i = 0; i < text.length; i++) {
        const character = text[i];

        await new Promise(resolve => setTimeout(resolve, 60));

        if (window.bubbleText != originalText) {
            return;
        }

        if (character == '.' || character == ',' || character == '!' || character == '?') {
            await new Promise(resolve => setTimeout(resolve, 400));
        }

        bubbleTextElement.innerHTML += character;
    }
}

window.bubbleText = '';
window.thinking = true;

setInterval(() => {
    fetch('http://localhost:3000/get_bubble_text').then(async response => {
        const bubbleText = await response.text()

        console.log("Bubble: " + bubbleText)

        if (bubbleText == '') {
            console.log("thinking true")
            window.thinking = true;
            return;
        }

        

        window.thinking = false;

        if (bubbleText != window.bubbleText) {
            document.getElementById('bubble-text').innerHTML = '';
            setBubbleText(bubbleText);
            window.bubbleText = bubbleText;
        }
    })
}, 500)

window.bubbleI = 1

setInterval(() => {
    const bubbleTextElement = document.getElementById('bubble-text');
    const thinkingBubbleElement = document.getElementById('thinking-bubble');

    if (!window.thinking) {
        bubbleTextElement.style.display = 'block';
        thinkingBubbleElement.style.display = 'none';
    } else {
        bubbleTextElement.style.display = 'none';
        thinkingBubbleElement.style.display = 'block';
    }

    thinkingBubbleElement.innerHTML = '&#x2022;'.repeat(window.bubbleI + 1)

    if (window.bubbleI < 2) {
        window.bubbleI += 1;
    } else {
        window.bubbleI = 1;
    }
}, 700)