document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startButton');
    const closeButton = document.getElementById('closeButton');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const gameCanvas = document.getElementById('gameCanvas');
    const difficultySelect = document.getElementById('difficultySelect'); // Added

    // herni okno
    const canvas = gameCanvas;
    const ctx = canvas.getContext('2d');

    // promenne
    let player1, player2;
    let gameStarted = false;
    let gameOver = false;

    // promenne pohyb palky
    const keys = {};

    // start button
    startButton.addEventListener('click', () => {
        player1 = document.getElementById('player1Name').value || 'Player 1';
        player2 = document.getElementById('player2Name').value || 'Player 2';
        
        if (player1 && player2) {
            welcomeScreen.classList.add('hidden');
            canvas.classList.remove('hidden');
            gameStarted = true;
            gameOver = false;
            setupGame();
        } else {
            alert('Please enter names for both players.');
        }
    });

    // co se deje po zmacknuti klaves
    closeButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to close the game?')) {
            window.close();
        }
    });

    document.addEventListener('keydown', (event) => {
        keys[event.code] = true;
    });

    document.addEventListener('keyup', (event) => {
        keys[event.code] = false;
    });

    function setupGame() {
        // precte velikost obrazovky
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;

        // vyska herniho okna(80% vysky obrazovky;  4:3 pomer stran)
        canvas.height = screenHeight * 0.8;
        canvas.width = canvas.height * (4 / 3);

        // horizontalni zarovnani okna
        canvas.style.position = 'absolute';
        canvas.style.top = `${(screenHeight - canvas.height) / 2}px`;
        canvas.style.left = `${(screenWidth - canvas.width) / 2}px`;

        // vyber obtiznosti
        const difficulty = difficultySelect.value;
        let paddleSpeed, ballSpeedX, ballSpeedY;

        switch (difficulty) {
            case 'beginner':
                paddleSpeed = 4;
                ballSpeedX = 3;
                ballSpeedY = 2;
                break;
            case 'guru':
                paddleSpeed = 6;
                ballSpeedX = 5;
                ballSpeedY = 3;
                break;
            case 'djokovic':
                paddleSpeed = 8;
                ballSpeedX = 7;
                ballSpeedY = 5;
                break;
        }

        // herni objekty v %ech velikosti okna (0.02 =2%)
        const paddleWidth = canvas.width * 0.02; 
        const paddleHeight = canvas.height * 0.2; 
        const ballSize = canvas.width * 0.025; 

        let leftPaddle = { x: canvas.width * 0.05, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight };
        let rightPaddle = { x: canvas.width - canvas.width * 0.05 - paddleWidth, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight };
        let ball = { x: canvas.width / 2 - ballSize / 2, y: canvas.height / 2 - ballSize / 2, size: ballSize, speedX: ballSpeedX, speedY: ballSpeedY };

        let player1Score = 0;
        let player2Score = 0;

        function gameLoop() {
            if (!gameStarted || gameOver) return;

            // Handle input
            if (keys['KeyW'] && leftPaddle.y > 0) {
                leftPaddle.y -= paddleSpeed;
            }
            if (keys['KeyS'] && leftPaddle.y < canvas.height - leftPaddle.height) {
                leftPaddle.y += paddleSpeed;
            }
            if (keys['ArrowUp'] && rightPaddle.y > 0) {
                rightPaddle.y -= paddleSpeed;
            }
            if (keys['ArrowDown'] && rightPaddle.y < canvas.height - rightPaddle.height) {
                rightPaddle.y += paddleSpeed;
            }

            // Move ball
            ball.x += ball.speedX;
            ball.y += ball.speedY;

            // Ball collision with top and bottom
            if (ball.y <= 0 || ball.y + ball.size >= canvas.height) {
                ball.speedY *= -1;
            }

            // Ball collision with paddles
            if (ball.x <= leftPaddle.x + leftPaddle.width &&
                ball.y + ball.size >= leftPaddle.y &&
                ball.y <= leftPaddle.y + leftPaddle.height) {
                ball.speedX *= -1;
                ball.x = leftPaddle.x + leftPaddle.width;
            }
            if (ball.x + ball.size >= rightPaddle.x &&
                ball.y + ball.size >= rightPaddle.y &&
                ball.y <= rightPaddle.y + rightPaddle.height) {
                ball.speedX *= -1;
                ball.x = rightPaddle.x - ball.size;
            }

            // Ball out of bounds
            if (ball.x <= 0) {
                player2Score++;
                if (player2Score >= 10) {
                    endGame(player2);
                    return;
                }
                resetBall();
            }
            if (ball.x + ball.size >= canvas.width) {
                player1Score++;
                if (player1Score >= 10) {
                    endGame(player1);
                    return;
                }
                resetBall();
            }

            // kresleni
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // kresli palky
            ctx.fillStyle = 'white';
            ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
            ctx.fillRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);

            // kresli mic
            ctx.beginPath();
            ctx.arc(ball.x + ball.size / 2, ball.y + ball.size / 2, ball.size / 2, 0, Math.PI * 2);
            ctx.fill();

            // kresli skore
            ctx.font = '24px Arial';
            ctx.fillText(`${player1} ${player1Score} - ${player2Score} ${player2}`, canvas.width / 2, 30);

            requestAnimationFrame(gameLoop);
        }

        function resetBall() {
            ball.x = canvas.width / 2 - ball.size / 2;
            ball.y = canvas.height / 2 - ball.size / 2;
            ball.speedX *= -1;
        }

        function endGame(winnerName) {
            gameOver = true;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'white';
            ctx.font = '36px Arial';
            ctx.fillText(`${winnerName} Wins!`, canvas.width / 2 - ctx.measureText(`${winnerName} Wins!`).width / 2, canvas.height / 2);
        }

        gameLoop();
    }

    // prizpusobeni velikosti okna
    window.addEventListener('resize', () => {
        if (gameStarted && !gameOver) {
            setupGame();
        }
    });
});
