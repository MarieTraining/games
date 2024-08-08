const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const screenWidth = canvas.width;
const screenHeight = canvas.height;

const paddleWidth = 15;
const paddleHeight = 100;
const paddleSpeed = 7;
const ballSize = 20;

let player1Score = 0;
let player2Score = 0;
let ballSpeedX;
let ballSpeedY;

let leftPaddle = { x: 50, y: screenHeight / 2 - paddleHeight / 2 };
let rightPaddle = { x: screenWidth - 50 - paddleWidth, y: screenHeight / 2 - paddleHeight / 2 };
let ball = { x: screenWidth / 2 - ballSize / 2, y: screenHeight / 2 - ballSize / 2, speedX: 0, speedY: 0 };

const welcomeScreen = document.getElementById('welcomeScreen');
const startButton = document.getElementById('startButton');
const player1NameInput = document.getElementById('player1Name');
const player2NameInput = document.getElementById('player2Name');

function showWelcomeScreen() {
    welcomeScreen.classList.remove('hidden');
}

function startGame() {
    welcomeScreen.classList.add('hidden');
    ballSpeedX = selectDifficulty();
    ballSpeedY = ballSpeedX;
    countdown();
    gameLoop();
}

function selectDifficulty() {
    // Choose difficulty (replace with your preferred way to choose difficulty)
    return 5; // Default difficulty
}

function countdown() {
    let count = 3;
    const interval = setInterval(() => {
        ctx.clearRect(0, 0, screenWidth, screenHeight);
        ctx.font = '74px Arial';
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.fillText(count, screenWidth / 2, screenHeight / 2);
        count -= 1;
        if (count < 0) {
            clearInterval(interval);
        }
    }, 1000);
}

function gameLoop() {
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    
    function update() {
        // Pohyb palek
        if (keys['w'] && leftPaddle.y > 0) leftPaddle.y -= paddleSpeed;
        if (keys['s'] && leftPaddle.y < screenHeight - paddleHeight) leftPaddle.y += paddleSpeed;
        if (keys['ArrowUp'] && rightPaddle.y > 0) rightPaddle.y -= paddleSpeed;
        if (keys['ArrowDown'] && rightPaddle.y < screenHeight - paddleHeight) rightPaddle.y += paddleSpeed;

        // Pohyb mice
        ball.x += ballSpeedX;
        ball.y += ballSpeedY;

        // Kolize mice nahore a dole
        if (ball.y <= 0 || ball.y >= screenHeight - ballSize) ballSpeedY *= -1;

        // Kolize mice s palkami
        if (ball.x <= leftPaddle.x + paddleWidth && ball.y + ballSize > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight) {
            ballSpeedX *= -1;
            ball.x = leftPaddle.x + paddleWidth;
        } else if (ball.x >= rightPaddle.x - ballSize && ball.y + ballSize > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight) {
            ballSpeedX *= -1;
            ball.x = rightPaddle.x - ballSize;
        }

        // Mic mimo limity (reset)
        if (ball.x <= 0) {
            player2Score += 1;
            resetBall();
        } else if (ball.x >= screenWidth - ballSize) {
            player1Score += 1;
            resetBall();
        }

        // Check jestli nekdo z hracu dosahl 10 bodu=vyhral
        if (player1Score >= 10) {
            displayWinner(player1NameInput.value);
            return;
        }
        if (player2Score >= 10) {
            displayWinner(player2NameInput.value);
            return;
        }

        // Kresleni
        ctx.clearRect(0, 0, screenWidth, screenHeight);
        ctx.fillStyle = 'white';
        ctx.fillRect(leftPaddle.x, leftPaddle.y, paddleWidth, paddleHeight);
        ctx.fillRect(rightPaddle.x, rightPaddle.y, paddleWidth, paddleHeight);
        ctx.beginPath();
        ctx.arc(ball.x + ballSize / 2, ball.y + ballSize / 2, ballSize / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.moveTo(screenWidth / 2, 0);
        ctx.lineTo(screenWidth / 2, screenHeight);
        ctx.stroke();

        // Zobrazení jmen hráčů s pozadím
        ctx.fillStyle = 'black';
        ctx.fillRect(screenWidth / 2 - 150, 10, 300, 50);
        ctx.fillStyle = 'white';
        ctx.font = '48px Arial';
        ctx.fillText(`${player1NameInput.value} : ${player2NameInput.value}`, screenWidth / 2, 50);

        // Zobrazení skóre s pozadím
        ctx.fillStyle = 'black';
        ctx.fillRect(screenWidth / 2 - 150, 80, 300, 50);
        ctx.fillStyle = 'white';
        ctx.font = '74px Arial';
        ctx.fillText(`${player1Score}:${player2Score}`, screenWidth / 2, 120);
    }

    function resetBall() {
        ball.x = screenWidth / 2 - ballSize / 2;
        ball.y = screenHeight / 2 - ballSize / 2;
        ballSpeedX *= -1;
    }

    function handleKeyDown(event) {
        keys[event.key] = true;
    }

    function handleKeyUp(event) {
        keys[event.key] = false;
    }

    const keys = {};

    setInterval(update, 1000 / 60);
}

function displayWinner(winnerName) {
    ctx.clearRect(0, 0, screenWidth, screenHeight);
    ctx.font = '74px Arial';
    ctx.fillStyle = 'white';
    ctx.textAlign = 'center';
    ctx.fillText(`${winnerName} Wins!`, screenWidth / 2, screenHeight / 2);
    setTimeout(() => {
        window.location.reload();
    }, 3000);
}

startButton.addEventListener('click', startGame);

showWelcomeScreen();
