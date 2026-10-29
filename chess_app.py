#!/usr/bin/env python3
"""
Chess Game Application
A complete chess game with move validation and game state management
"""

import uuid
from collections import OrderedDict
from datetime import datetime

from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "chess_game_secret_key_2024"


class ChessGame:
    """Chess game logic and state management"""

    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = "white"
        self.game_over = False
        self.game_result = None  # 'checkmate', 'stalemate', or None
        self.move_history = []
        self.captured_pieces = {"white": [], "black": []}
        self.en_passant_target = None
        self.winner = None
        # Track piece movements for castling
        self.piece_moved = {
            "white_king": False,
            "white_rook_queenside": False,
            "white_rook_kingside": False,
            "black_king": False,
            "black_rook_queenside": False,
            "black_rook_kingside": False,
        }

    def initialize_board(self):
        """Initialize the chess board with pieces in starting positions"""
        board = [["" for _ in range(8)] for _ in range(8)]

        # Set up pawns
        for col in range(8):
            board[1][col] = "black_pawn"
            board[6][col] = "white_pawn"

        # Set up other pieces
        pieces = [
            "rook",
            "knight",
            "bishop",
            "queen",
            "king",
            "bishop",
            "knight",
            "rook",
        ]
        for col, piece in enumerate(pieces):
            board[0][col] = f"black_{piece}"
            board[7][col] = f"white_{piece}"

        return board

    def get_piece_color(self, piece):
        """Get the color of a piece"""
        if not piece:
            return None
        return piece.split("_")[0]

    def get_piece_type(self, piece):
        """Get the type of a piece"""
        if not piece:
            return None
        return piece.split("_")[1]

    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8

    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        if not self.is_valid_position(row, col):
            return []

        piece = self.board[row][col]
        if not piece:
            return []

        piece_color = self.get_piece_color(piece)
        piece_type = self.get_piece_type(piece)

        if piece_color != self.current_player:
            return []

        moves = []

        if piece_type == "pawn":
            moves = self.get_pawn_moves(row, col, piece_color)
        elif piece_type == "rook":
            moves = self.get_rook_moves(row, col, piece_color)
        elif piece_type == "knight":
            moves = self.get_knight_moves(row, col, piece_color)
        elif piece_type == "bishop":
            moves = self.get_bishop_moves(row, col, piece_color)
        elif piece_type == "queen":
            moves = self.get_queen_moves(row, col, piece_color)
        elif piece_type == "king":
            moves = self.get_king_moves(row, col, piece_color)

        return moves

    def get_pawn_moves(self, row, col, color):
        """Get valid moves for a pawn"""
        moves = []
        direction = -1 if color == "white" else 1
        start_row = 6 if color == "white" else 1

        # Forward move
        new_row = row + direction
        if self.is_valid_position(new_row, col) and not self.board[new_row][col]:
            moves.append((new_row, col))

            # Double move from starting position
            if row == start_row:
                new_row2 = row + 2 * direction
                if (
                    self.is_valid_position(new_row2, col)
                    and not self.board[new_row2][col]
                ):
                    moves.append((new_row2, col))

        # Diagonal captures
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            new_row = row + direction
            if (
                self.is_valid_position(new_row, new_col)
                and self.board[new_row][new_col]
                and self.get_piece_color(self.board[new_row][new_col]) != color
            ):
                moves.append((new_row, new_col))

        if self.en_passant_target:
            ep_row, ep_col = self.en_passant_target
            if ep_row == row + direction and abs(ep_col - col) == 1:
                moves.append((ep_row, ep_col))

        return moves

    def get_pawn_attacks(self, row, col, color):
        """Squares a pawn attacks, used for check detection"""
        direction = -1 if color == "white" else 1
        attacks = []
        for col_offset in (-1, 1):
            new_row, new_col = row + direction, col + col_offset
            if self.is_valid_position(new_row, new_col):
                attacks.append((new_row, new_col))
        return attacks

    def get_king_attacks(self, row, col):
        """One-square king attacks, without castling"""
        attacks = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col):
                    attacks.append((new_row, new_col))
        return attacks

    def get_rook_moves(self, row, col, color):
        """Get valid moves for a rook"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self.is_valid_position(new_row, new_col):
                    break

                target_piece = self.board[new_row][new_col]
                if not target_piece:
                    moves.append((new_row, new_col))
                elif self.get_piece_color(target_piece) != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def get_knight_moves(self, row, col, color):
        """Get valid moves for a knight"""
        moves = []
        knight_moves = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target_piece = self.board[new_row][new_col]
                if not target_piece or self.get_piece_color(target_piece) != color:
                    moves.append((new_row, new_col))

        return moves

    def get_bishop_moves(self, row, col, color):
        """Get valid moves for a bishop"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self.is_valid_position(new_row, new_col):
                    break

                target_piece = self.board[new_row][new_col]
                if not target_piece:
                    moves.append((new_row, new_col))
                elif self.get_piece_color(target_piece) != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def get_queen_moves(self, row, col, color):
        """Get valid moves for a queen (combination of rook and bishop)"""
        return self.get_rook_moves(row, col, color) + self.get_bishop_moves(
            row, col, color
        )

    def get_king_moves(self, row, col, color):
        """Get valid moves for a king"""
        moves = []
        king_moves = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target_piece = self.board[new_row][new_col]
                if not target_piece or self.get_piece_color(target_piece) != color:
                    moves.append((new_row, new_col))

        # Add castling moves if available
        castling_moves = self.get_castling_moves(row, col, color)
        moves.extend(castling_moves)

        return moves

    def can_castle(self, color, side):
        """Check if castling is possible for given color and side"""
        king_key = f"{color}_king"
        rook_key = f"{color}_rook_{side}"

        # Check if king or rook have moved
        if self.piece_moved[king_key] or self.piece_moved[rook_key]:
            return False

        # Determine positions
        king_row = 7 if color == "white" else 0
        if side == "kingside":
            king_col, rook_col = 4, 7
            between_cols = [5, 6]
        else:  # queenside
            king_col, rook_col = 4, 0
            between_cols = [1, 2, 3]

        # Check if pieces are in correct positions
        if (
            self.board[king_row][king_col] != f"{color}_king"
            or self.board[king_row][rook_col] != f"{color}_rook"
        ):
            return False

        # Check if squares between king and rook are empty
        for col in between_cols:
            if self.board[king_row][col]:
                return False

        # Check if king is in check
        if self.is_king_in_check(color):
            return False

        # Check if king would pass through or land in check
        king_path = [4, 5, 6] if side == "kingside" else [4, 3, 2]
        for col in king_path:
            # Temporarily move king to check for check
            original = self.board[king_row][col]
            self.board[king_row][col] = f"{color}_king"
            self.board[king_row][4] = ""

            in_check = self.is_king_in_check(color)

            # Restore board
            self.board[king_row][4] = f"{color}_king"
            self.board[king_row][col] = original

            if in_check:
                return False

        return True

    def get_castling_moves(self, row, col, color):
        """Get available castling moves for the king"""
        moves = []

        # Only kings on their starting square can castle
        expected_row = 7 if color == "white" else 0
        if row != expected_row or col != 4:
            return moves

        # Check kingside castling
        if self.can_castle(color, "kingside"):
            moves.append((expected_row, 6))

        # Check queenside castling
        if self.can_castle(color, "queenside"):
            moves.append((expected_row, 2))

        return moves

    def _save_position(self):
        return {
            "board": [row[:] for row in self.board],
            "en_passant_target": self.en_passant_target,
            "piece_moved": dict(self.piece_moved),
            "captured_pieces": {
                color: list(pieces) for color, pieces in self.captured_pieces.items()
            },
        }

    def _restore_position(self, saved):
        self.board = saved["board"]
        self.en_passant_target = saved["en_passant_target"]
        self.piece_moved = saved["piece_moved"]
        self.captured_pieces = saved["captured_pieces"]

    def _place_move(self, from_pos, to_pos, promotion=None):
        """Apply a move, including castling, en passant, and promotion."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        color = self.get_piece_color(piece)
        piece_type = self.get_piece_type(piece)
        direction = -1 if color == "white" else 1

        if piece_type == "king" and abs(to_col - from_col) == 2:
            if to_col > from_col:
                rook_from_col, rook_to_col = 7, 5
            else:
                rook_from_col, rook_to_col = 0, 3
            rook = self.board[from_row][rook_from_col]
            self.board[from_row][rook_to_col] = rook
            self.board[from_row][rook_from_col] = ""

        captured_piece = self.board[to_row][to_col]
        if (
            piece_type == "pawn"
            and self.en_passant_target == (to_row, to_col)
            and not captured_piece
        ):
            captured_row = to_row - direction
            captured_piece = self.board[captured_row][to_col]
            self.board[captured_row][to_col] = ""

        if captured_piece:
            self.captured_pieces[color].append(captured_piece)

        moved_piece = piece
        if piece_type == "pawn" and to_row in (0, 7):
            choice = promotion if promotion in ("queen", "rook", "bishop", "knight") else "queen"
            moved_piece = f"{color}_{choice}"

        self.board[to_row][to_col] = moved_piece
        self.board[from_row][from_col] = ""
        self.update_piece_moved_status(piece, from_row, from_col)

        if piece_type == "pawn" and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        else:
            self.en_passant_target = None

        return moved_piece, captured_piece

    def make_move(self, from_pos, to_pos, promotion=None):
        """Make a move on the board"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if self.game_over:
            return False, "Game is over"

        if not self.is_valid_position(from_row, from_col) or not self.is_valid_position(
            to_row, to_col
        ):
            return False, "Invalid position"

        piece = self.board[from_row][from_col]
        if not piece:
            return False, "No piece at source position"

        if self.get_piece_color(piece) != self.current_player:
            return False, "Not your piece"

        valid_moves = self.get_legal_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False, "Invalid move"

        if (
            self.get_piece_type(piece) == "pawn"
            and to_row in (0, 7)
            and promotion not in ("queen", "rook", "bishop", "knight")
        ):
            return False, "Choose a piece to promote to"

        mover = self.current_player
        moved_piece, captured_piece = self._place_move(from_pos, to_pos, promotion)

        self.move_history.append(
            {
                "from": from_pos,
                "to": to_pos,
                "piece": moved_piece,
                "captured": captured_piece,
                "player": mover,
                "timestamp": datetime.now().isoformat(),
            }
        )

        self.current_player = "black" if mover == "white" else "white"

        result = self.is_checkmate_or_stalemate()
        if result == "checkmate":
            self.winner = mover
            return True, f"Checkmate! {mover.capitalize()} wins!"
        if result == "stalemate":
            return True, "Stalemate! Game is a draw!"

        return True, "Move successful"

    def update_piece_moved_status(self, piece, from_row, from_col):
        """Update the piece moved tracking for castling"""
        color = self.get_piece_color(piece)
        piece_type = piece.split("_")[1]

        if piece_type == "king":
            self.piece_moved[f"{color}_king"] = True
        elif piece_type == "rook":
            # Determine which rook based on starting position
            if color == "white" and from_row == 7:
                if from_col == 0:
                    self.piece_moved["white_rook_queenside"] = True
                elif from_col == 7:
                    self.piece_moved["white_rook_kingside"] = True
            elif color == "black" and from_row == 0:
                if from_col == 0:
                    self.piece_moved["black_rook_queenside"] = True
                elif from_col == 7:
                    self.piece_moved["black_rook_kingside"] = True

    def find_king(self, color):
        """Find the position of the king of the specified color"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == f"{color}_king":
                    return (row, col)
        return None

    def is_king_in_check(self, color):
        """Check if the king of the specified color is in check"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False

        king_row, king_col = king_pos
        opponent_color = "black" if color == "white" else "white"

        # Check if any opponent piece can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.get_piece_color(piece) == opponent_color:
                    # Get all possible moves for this piece
                    piece_type = self.get_piece_type(piece)
                    moves = []

                    if piece_type == "pawn":
                        moves = self.get_pawn_attacks(row, col, opponent_color)
                    elif piece_type == "rook":
                        moves = self.get_rook_moves(row, col, opponent_color)
                    elif piece_type == "knight":
                        moves = self.get_knight_moves(row, col, opponent_color)
                    elif piece_type == "bishop":
                        moves = self.get_bishop_moves(row, col, opponent_color)
                    elif piece_type == "queen":
                        moves = self.get_queen_moves(row, col, opponent_color)
                    elif piece_type == "king":
                        moves = self.get_king_attacks(row, col)

                    # Check if any move can capture the king
                    if king_pos in moves:
                        return True

        return False

    def is_move_legal(self, from_pos, to_pos):
        """Check if a move is legal (doesn't leave own king in check)"""
        saved = self._save_position()
        color = self.current_player
        try:
            self._place_move(from_pos, to_pos, promotion="queen")
            return not self.is_king_in_check(color)
        finally:
            self._restore_position(saved)

    def get_legal_moves(self, row, col):
        """Get all legal moves for a piece (excluding moves that leave king in check)"""
        basic_moves = self.get_valid_moves(row, col)
        legal_moves = []

        for move in basic_moves:
            if self.is_move_legal((row, col), move):
                legal_moves.append(move)

        return legal_moves

    def is_checkmate_or_stalemate(self):
        """Check if the current position is checkmate or stalemate"""
        # Check if current player has any legal moves
        has_legal_moves = False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.get_piece_color(piece) == self.current_player:
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        has_legal_moves = True
                        break
            if has_legal_moves:
                break

        if not has_legal_moves:
            if self.is_king_in_check(self.current_player):
                self.game_result = "checkmate"
                self.game_over = True
                return "checkmate"
            else:
                self.game_result = "stalemate"
                self.game_over = True
                return "stalemate"

        return None

    def get_game_state(self):
        """Get current game state for API"""
        return {
            "board": self.board,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "game_result": self.game_result,
            "move_history": self.move_history,
            "captured_pieces": self.captured_pieces,
            "in_check": self.is_king_in_check(self.current_player),
            "winner": self.winner,
        }


MAX_GAMES = 200
games = OrderedDict()


def get_game():
    """Return the game for this browser, creating one if needed."""
    game_id = session.get("game_id")
    if game_id not in games:
        game_id = str(uuid.uuid4())
        session["game_id"] = game_id
        session.permanent = True
        games[game_id] = ChessGame()
        while len(games) > MAX_GAMES:
            games.popitem(last=False)
    else:
        games.move_to_end(game_id)
    return games[game_id]


@app.route("/")
def index():
    """Main chess game page"""
    return render_template("chess.html")


@app.route("/api/game-state")
def get_game_state():
    """Get current game state"""
    game = get_game()
    return jsonify(game.get_game_state())


@app.route("/api/valid-moves/<int:row>/<int:col>")
def get_valid_moves(row, col):
    """Get legal moves for a piece at given position"""
    game = get_game()
    moves = game.get_legal_moves(row, col)
    captures = [
        [move_row, move_col]
        for move_row, move_col in moves
        if game.board[move_row][move_col] or game.en_passant_target == (move_row, move_col)
    ]
    return jsonify({"moves": moves, "captures": captures})


@app.route("/api/make-move", methods=["POST"])
def make_move():
    """Make a move"""
    game = get_game()
    data = request.get_json(silent=True) or {}
    from_pos = tuple(data["from"])
    to_pos = tuple(data["to"])
    promotion = data.get("promotion")

    success, message = game.make_move(from_pos, to_pos, promotion)
    return jsonify(
        {
            "success": success,
            "message": message,
            "needs_promotion": (not success) and message == "Choose a piece to promote to",
            "game_state": game.get_game_state(),
        }
    )


@app.route("/api/new-game", methods=["POST"])
def new_game():
    """Start a new game for this browser"""
    game_id = session.get("game_id") or str(uuid.uuid4())
    session["game_id"] = game_id
    games[game_id] = ChessGame()
    games.move_to_end(game_id)
    return jsonify(
        {
            "success": True,
            "message": "New game started",
            "game_state": games[game_id].get_game_state(),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
