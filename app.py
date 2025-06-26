from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Updated path: assume ps-eval is in the same directory as app.py
PS_EVAL_PATH = os.path.join(os.path.dirname(__file__), "ps-eval")

@app.route("/")
def index():
    return "Poker Equity Evaluator API is running."

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()

    hero = data.get("hero")
    villain = data.get("villain")
    board = data.get("board")

    if not hero or not villain or not board:
        return jsonify({"error": "Missing hero, villain, or board cards"}), 400

    try:
        hero_str = ",".join(hero)
        villain_str = ",".join(villain)
        board_str = ",".join(board)

        command = [
            PS_EVAL_PATH,
            "-g", "h",
            "-b", board_str,
            "-h", hero_str,
            "-h", villain_str
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": "ps-eval failed", "details": result.stderr}), 500

        output_lines = result.stdout.strip().splitlines()
        equity_data = {}

        for line in output_lines:
            parts = line.split()
            if len(parts) >= 2:
                hand = parts[0]
                equity = float(parts[1])
                if hand == hero_str:
                    equity_data["heroEquity"] = equity
                elif hand == villain_str:
                    equity_data["villainEquity"] = equity

        return jsonify(equity_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
