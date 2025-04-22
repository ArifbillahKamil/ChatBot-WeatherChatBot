from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

bot = ChatBot("ChatBot", read_only=False, 
              logic_adapters=[
                {
                    "import_path": "chatterbot.logic.BestMatch",
                    "default_response": "I'm sorry, I don't understand.",
                    "maximum_similarity_threshold": 0.90,
                }
              ])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('userMessage')
    
    # Coba dulu weather API
    try:
        weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid=731e687c61d2ca0d9766b52889231025&units=metric"
        response = requests.get(weather_api_url)
        
        if response.status_code == 200:
            weather_data = response.json()
            return jsonify({
                "type": "weather",
                "data": {
                    "city": weather_data['name'],
                    "temp": weather_data['main']['temp'],
                    "description": weather_data['weather'][0]['description']
                }
            })
    except:
        pass
    
    # Jika weather API gagal, gunakan chatbot
    bot_response = str(bot.get_response(user_input))
    return jsonify({
        "type": "chat",
        "data": bot_response
    })

if __name__ == "__main__":
    app.run(debug=True)