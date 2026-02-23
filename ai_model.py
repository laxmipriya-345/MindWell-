import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

MODEL_PATH = "mood_model.pkl"

class MoodPredictor:

    def train(self, moods):

        if len(moods) < 2:
            return None

        X = np.arange(len(moods)).reshape(-1,1)
        y = np.array(moods)

        model = LinearRegression()
        model.fit(X, y)

        joblib.dump(model, MODEL_PATH)

        return model


    def predict_next(self):

        if not os.path.exists(MODEL_PATH):
            return None

        model = joblib.load(MODEL_PATH)

        next_day = np.array([[30]])
        prediction = model.predict(next_day)

        prediction = max(1, min(5, prediction[0]))

        return round(prediction, 2)
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def mental_health_chat(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive mental health assistant."},
                {"role": "user", "content": message}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "API error. Check your key."     