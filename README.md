# Pac-Man Pathfinding Game

## 🎮 Project Overview
This project is a **Pac-Man-inspired game** that integrates **pathfinding algorithms** to control ghost AI. The goal is to demonstrate and compare different search algorithms—**Breadth-First Search (BFS), Depth-First Search (DFS), and A* (A-Star)**—to determine the most efficient way for ghosts to chase Pac-Man in a maze.

## 🚀 Features
- **Pac-Man Movement**: Player-controlled Pac-Man using arrow keys.
- **Ghost AI**: Ghosts use BFS, DFS, or A* to chase Pac-Man.
- **Maze Representation**: A 2D grid where `0` represents open paths and `1` represents walls.
- **Performance Metrics**:
  - Number of steps taken by each algorithm.
  - Execution time for path calculation.
  - Visual representation of visited nodes.
- **Power-Ups**: Power pellets allow Pac-Man to eat ghosts.
- **Random Fruits**: Occasionally appear for bonus points.

## 📂 Project Structure
```
PacMazeGame/
│── assets/               # Images, sounds, fonts (if used)
│── algorithms/           # Pathfinding algorithms
│   │── bfs.py            # BFS implementation
│   │── dfs.py            # DFS implementation
│   │── astar.py          # A* implementation
│── game/                 # Game mechanics
│   │── pacman.py         # Pac-Man movement
│   │── ghosts.py         # Ghost AI
│   │── maze.py           # Maze rendering
│── utils/                # Helper functions
│   │── timer.py          # Performance measurement
│   │── settings.py       # Game settings (grid size, speed, colors)
│── main.py               # Entry point of the game
│── requirements.txt      # Dependencies list
│── README.md             # Documentation
```

## 🛠 Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/PacMazeGame.git
cd PacMazeGame
```

### **2️⃣ Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Game**
```bash
python main.py
```

## 🎯 How to Play
- Use **arrow keys** to move Pac-Man.
- Avoid ghosts unless you eat a **power pellet**.
- Collect **pellets and fruits** to increase your score.
- Ghosts chase Pac-Man using **BFS, DFS, or A* algorithms**.
- The game ends when Pac-Man is caught or all pellets are eaten.

## 📊 Algorithm Comparison
| Algorithm | Shortest Path Guarantee | Speed | Exploration Efficiency |
|-----------|------------------------|-------|------------------------|
| **BFS**  | ✅ Yes                  | ⏳ Slow  | 🟡 Explores all paths equally |
| **DFS**  | ❌ No                   | ⚡ Fast  | 🔴 May take longer paths |
| **A***   | ✅ Yes                  | 🚀 Fastest  | 🟢 Uses heuristics to prioritize best paths |

## 📜 License
This project is licensed under the **MIT License**.

## 🙌 Contributors
- **Your Name** – [GitHub Profile](https://github.com/yourusername)

Feel free to contribute by submitting **pull requests** or opening **issues**! 😊

---

### 🎮 Enjoy the game and happy coding! 🚀

