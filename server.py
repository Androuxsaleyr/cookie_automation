# Import Flask module to work with
from flask import Flask, request , jsonify
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Loading the enviromental var
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))


# making app that can use flask which in turn takes the __name__ constructor
app = Flask(__name__)
CORS(app, origins=["https://orteil.dashnet.org"])


# Will get the current state of the game from the script that is running and save it to a json file which we can then take actions on
@app.route('/save-game-state', methods=['POST'])
def save_game_state():
    data = request.get_json()

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "game_state.json")

    # Save the file in the same folder as this script
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Game state saved to {file_path}")
    return jsonify({"status": "saved"}), 200

# This function is a prompt to be sent to get the recommendation which we later use in the /recommend
def get_ai_recommendation(game_state):
    unlocked_upgrades = [
        upg for upg in game_state["upgrades"]
        if upg["unlocked"] and not upg["bought"]
    ]

    unlocked_buildings = [
        bld for bld in game_state["buildings"]
        if bld["price"] <= game_state["cookies"]
    ]
    prompt = f"""
        You are an expert Cookie Clicker strategist.

        Your task is to return a list of recommended purchases in this exact format:
        upgrade:<id>
        building:<id>,<amount>

        Strategy:
        - Only recommend purchases that are affordable given the current cookie count.
        - Only recommend upgrades that are both unlocked and not yet purchased.
        - Only recommend buildings that are unlocked and available for purchase.
        - Favor buildings that are currently unowned or minimally owned, especially when newly unlocked.
        - Spend as many cookies as possible each turn, focusing on purchases that offer strong CPS gains per cost.
        - You may recommend buying multiple units of a building if it improves efficiency.
        - When recommending multiple purchases, calculate the total cost and ensure it does not exceed the available cookie count.
        - Do not assume infinite resources — all recommendations must fit within the current cookie budget.

        Available cookies: {game_state["cookies"]}

        Unlocked upgrades:
        {json.dumps(unlocked_upgrades, indent=2)}

        Unlocked buildings:
        {json.dumps(unlocked_buildings, indent=2)}

        Formatting:
        - Do NOT explain your reasoning.
        - Do NOT include any extra text, commentary, or formatting.
        - Only return the list of recommended purchases, one per line.
        """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


# this is where the brains lie
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    print("📥 /recommend endpoint triggered")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "game_state.json")

    if not os.path.exists(file_path):
        return jsonify({"error": "game_state.json not found"}), 404

    with open(file_path, "r") as f:
        game_state = json.load(f)

    recommendation = get_ai_recommendation(game_state)
    print("🤖 AI Recommendation:\n", recommendation)  
    return jsonify({"recommendation": recommendation})


# For the main running function
if __name__ == '__main__':
    app.run(debug=True)

