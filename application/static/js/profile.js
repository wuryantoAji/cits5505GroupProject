//Get user's name and display
document.addEventListener("DOMContentLoaded", function () {
  fetch("/get_username")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("username").textContent = data.username;
    });
});

//Get and display solved puzzles
function fetchAndDisplaySolvedPuzzles() {
  fetch("/get_solved_puzzles")
    .then((response) => response.json())
    .then((data) => {
      const solvedList = document.getElementById("solved");
      solvedList.innerHTML = ""; // Clear existing items
      data.puzzles.forEach((puzzle) => {
        let item = document.createElement("li");
        item.textContent = puzzle.name;
        solvedList.appendChild(item);
      });
    });
}

//Get and display created puzzles
function fetchAndDisplayCreatedPuzzles() {
  fetch("/get_created_puzzles")
    .then((response) => response.json())
    .then((data) => {
      const createdList = document.getElementById("create-puzzle");
      createdList.innerHTML = ""; // Clear existing items
      data.puzzles.forEach((puzzle) => {
        let item = document.createElement("li");
        item.textContent = puzzle.name;
        createdList.appendChild(item);
      });
    });
}

//listening events
document.addEventListener("DOMContentLoaded", () => {
  fetchAndDisplaySolvedPuzzles();
  fetchAndDisplayCreatedPuzzles();
});

// Get and display scores
function fetchAndDisplayScores() {
  fetch("/get_scores")
    .then((response) => response.json())
    .then((data) => {
      const scoreSection = document.getElementById("score");
      scoreSection.innerHTML = `<h2>Overall Score: ${data.overall}</h2>`; // Display overall score
      const list = document.createElement("ul");
      data.scores.forEach((score) => {
        let item = document.createElement("li");
        item.textContent = `Game: ${score.game}, Score: ${score.score}`;
        list.appendChild(item);
      });
      scoreSection.appendChild(list); // Display individual game scores
    });
}
document.addEventListener("DOMContentLoaded", fetchAndDisplayScores);
