from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Assuming you have a saved tokenizer file
with open('padder.pkl', 'rb') as f:
    pad_sequences = pickle.load(f)
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('hate_speech_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text')

    if text is not None:
        # Convert text to padding sequence using the loaded tokenizer
        seq = tokenizer.texts_to_sequences([text])
        padded_pred = pad_sequences(seq, maxlen=50, padding='post', truncating='post')

        # Make prediction
        pred_model = model.predict(padded_pred)
        avg = (pred_model[0][0] + pred_model[0][1] + pred_model[0][2]) / 3
        final_prediction_index = 0
        for i in pred_model:
            max=0
            for j in list(i):
                if j-avg>max:
                    max=j-avg
                    final_prediction_index=list(i).index(j)

        return jsonify({'prediction': int(final_prediction_index)})
    else:
        return jsonify({'error': 'Input text not provided.'})

if __name__ == '__main__':
    app.run(debug=True)
