let gameStartTime = Date.now() / 1000;

async function loadStory() {
    const response = await fetch('/api/next-story');
    const story = await response.json();
    
    document.getElementById('mainImage').src = story.image;
    document.getElementById('news1').querySelector('.summary').textContent = story.trueSummary;
    document.getElementById('news2').querySelector('.summary').textContent = story.fakeSummary;
}

async function checkAnswer(selectedPosition) {
    const response = await fetch('/api/submit-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            selectedPosition: selectedPosition,
            startTime: gameStartTime
        })
    });
    
    const result = await response.json();
    showFeedback(result);
    gameStartTime = Date.now() / 1000;  // Reset timer for next question
}

function speakText() {
            let text = document.getElementById("text").innerText;
            let speech = new SpeechSynthesisUtterance(text);
            speech.lang = "en-US"; // Set language
            speech.rate = 1; // Adjust speed (1 is normal)
            speech.pitch = 1; // Adjust pitch
            window.speechSynthesis.speak(speech);
        }

function speakText() {
    let text = document.getElementById("text").innerText;
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US"; // Set language
    speech.rate = 1; // Adjust speed (1 is normal)
    speech.pitch = 1; // Adjust pitch
    window.speechSynthesis.speak(speech);
}