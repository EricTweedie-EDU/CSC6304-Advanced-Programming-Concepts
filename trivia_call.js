// Javascript functions to call the trivia API

const startButton = document.getElementById('start-button');
const nextButton = document.getElementById('next-button');
const questionContainer = document.getElementById('question-container');
const questionElement = document.getElementById('question');
const answerButtonsElement = document.getElementById('answer-buttons');
const scoreContainer = document.getElementById('score-container');
const scoreElement = document.getElementById('score');
const errorMessage = document.getElementById('error-message');
const loadingMessage = document.getElementById('loading-message');
const noQuestionsMessage = document.getElementById('no-questions-message');
const restartButton = document.getElementById('restart-button');

let currentQuestionIndex = 0;
let score = 0;
let questions = [];

// Fetch trivia questions from the API
async function fetchQuestions() {
    try {
        loadingMessage.classList.remove('hide');
        const response = await fetch('https://opentdb.com/api.php?amount=10&type=multiple');
        const data = await response.json();
        questions = data.results;
        loadingMessage.classList.add('hide');
        if (questions.length === 0) {
            noQuestionsMessage.classList.remove('hide');
        } else {
            startGame();
        }
    } catch (error) {
        loadingMessage.classList.add('hide');
        errorMessage.textContent = 'Failed to load questions. Please try again later.';
        errorMessage.classList.remove('hide');
    }
}

// Start the game
function startGame() {
    startButton.classList.add('hide');
    questionContainer.classList.remove('hide');
    currentQuestionIndex = 0;
    score = 0;
    showQuestion();
}

// Show the current question
function showQuestion() {
    resetState();
    const question = questions[currentQuestionIndex];
    questionElement.textContent = question.question;
    question.incorrect_answers.concat(question.correct_answer).forEach(answer => {
        const button = document.createElement('button');
        button.textContent = answer;
        button.classList.add('btn');
        if (answer === question.correct_answer) {
            button.dataset.correct = true;
        }
        button.addEventListener('click', selectAnswer);
        answerButtonsElement.appendChild(button);
    });
}

// Reset the state for the next question
function resetState() {
    nextButton.classList.add('hide');
    while (answerButtonsElement.firstChild) {
        answerButtonsElement.removeChild(answerButtonsElement.firstChild);
    }
}

// Handle answer selection
function selectAnswer(e) {
    const selectedButton = e.target;
    const correct = selectedButton.dataset.correct === 'true';
    if (correct) {
        score++;
    }
    Array.from(answerButtonsElement.children).forEach(button => {
        setStatusClass(button, button.dataset.correct === 'true');
    });
    if (currentQuestionIndex < questions.length - 1) {
        nextButton.classList.remove('hide');
    } else {
        showScore();
    }
}

// Set the status class for buttons
function setStatusClass(element, correct) {
    element.classList.remove('correct', 'wrong');
    if (correct) {
        element.classList.add('correct');
    } else {
        element.classList.add('wrong');
    }
}

// Show the final score
function showScore() {
    questionContainer.classList.add('hide');
    scoreContainer.classList.remove('hide');
    scoreElement.textContent = score;
}

// Event listeners
startButton.addEventListener('click', fetchQuestions);
nextButton.addEventListener('click', () => {
    currentQuestionIndex++;
    showQuestion();
});

// Restart the game
restartButton.addEventListener('click', () => {
    scoreContainer.classList.add('hide');
    startButton.classList.remove('hide');
    noQuestionsMessage.classList.add('hide');
    errorMessage.classList.add('hide');
});


