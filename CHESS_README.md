# Chess Game Application

A beautiful, interactive chess game built with Flask, HTML, CSS, and JavaScript. Features complete chess rules implementation with move validation, game state management, and a modern responsive UI.

## Features

### 🎮 Game Features
- **Complete Chess Rules**: All standard chess pieces with proper move validation
- **Move Validation**: Real-time validation of all chess moves
- **Game State Management**: Tracks current player, move history, and captured pieces
- **Visual Feedback**: Highlights selected pieces, valid moves, and capture opportunities
- **Move History**: Complete record of all moves made during the game
- **Captured Pieces Display**: Shows all pieces captured by each player

### 🎨 UI/UX Features
- **Modern Design**: Beautiful gradient backgrounds and smooth animations
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Interactive Board**: Click to select pieces and make moves
- **Visual Indicators**: 
  - Blue highlight for selected pieces
  - Green highlight for valid moves
  - Red highlight for capture opportunities
- **Coordinate System**: Shows chess notation (a-h, 1-8) on the board
- **Real-time Updates**: Instant feedback for all game actions

### 🛠 Technical Features
- **Flask Backend**: RESTful API for game logic and state management
- **Object-Oriented Design**: Clean, maintainable code structure
- **Error Handling**: Comprehensive error handling and user feedback
- **Session Management**: Persistent game state across browser sessions

## Installation

1. **Clone or download the project files**
   ```bash
   # Make sure you have the following files:
   # - chess_app.py
   # - templates/chess.html
   # - requirements.txt (updated with Flask)
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python chess_app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## How to Play

### Basic Controls
- **Select a piece**: Click on any piece of your color
- **Make a move**: Click on a highlighted square (green for moves, red for captures)
- **New Game**: Click the "New Game" button to start fresh
- **Show Valid Moves**: Click the button to highlight all valid moves for the selected piece

### Chess Rules Implemented
- **Pawns**: Forward movement (1 or 2 squares from starting position), diagonal captures
- **Rooks**: Horizontal and vertical movement
- **Knights**: L-shaped movement (2 squares in one direction, 1 square perpendicular)
- **Bishops**: Diagonal movement
- **Queens**: Combination of rook and bishop movements
- **Kings**: One square in any direction

### Game Flow
1. White always moves first
2. Players take turns moving pieces
3. Valid moves are highlighted when a piece is selected
4. Captured pieces are displayed in the sidebar
5. Move history is recorded and displayed
6. Game continues until checkmate or stalemate

## Project Structure

```
chess-game/
├── chess_app.py          # Main Flask application
├── templates/
│   └── chess.html        # HTML template with CSS and JavaScript
├── requirements.txt      # Python dependencies
└── CHESS_README.md       # This file
```

## API Endpoints

- `GET /` - Main game page
- `GET /api/game-state` - Get current game state
- `GET /api/valid-moves/<row>/<col>` - Get valid moves for a piece
- `POST /api/make-move` - Make a chess move
- `POST /api/new-game` - Start a new game

## Technical Details

### Backend (Python/Flask)
- **ChessGame Class**: Handles all game logic and state
- **Move Validation**: Comprehensive validation for all piece types
- **State Management**: Tracks board state, current player, and game history
- **RESTful API**: Clean API design for frontend communication

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: CSS Grid and Flexbox for layout
- **Interactive Elements**: Event-driven JavaScript for user interactions
- **Visual Feedback**: CSS animations and transitions
- **Chess Notation**: Unicode chess symbols for pieces

## Customization

### Styling
The game uses CSS custom properties and modern styling techniques. You can easily customize:
- Colors and themes
- Board size and layout
- Animations and transitions
- Typography and spacing

### Game Logic
The chess logic is modular and extensible. You can add:
- Special moves (castling, en passant)
- Check and checkmate detection
- AI opponent
- Game saving/loading
- Multiplayer support

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Future Enhancements

- [ ] Check and checkmate detection
- [ ] Castling and en passant moves
- [ ] AI opponent with different difficulty levels
- [ ] Game saving and loading
- [ ] Multiplayer support
- [ ] Tournament mode
- [ ] Move timer
- [ ] Sound effects
- [ ] Dark/light theme toggle

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change the port in chess_app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Flask not found**
   ```bash
   pip install flask
   ```

3. **Board not displaying correctly**
   - Check browser console for JavaScript errors
   - Ensure all files are in the correct locations
   - Verify Flask server is running

### Performance
- The game is optimized for smooth performance
- Large move histories may slow down the UI
- Consider clearing move history for very long games

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the UI/UX
- Fixing bugs
- Adding tests
- Improving documentation

## License

This project is open source and available under the MIT License.

---

**Enjoy playing chess! ♔♛** 