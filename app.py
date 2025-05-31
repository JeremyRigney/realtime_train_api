from flask import Flask, jsonify
import requests
import xmltodict
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_trains():
    try:
        # Fetch XML from Irish Rail
        url = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML"
        response = requests.get(url)
        data = xmltodict.parse(response.content, item_depth=1)

        # Convert to DataFrame and then to JSON
        df = pd.DataFrame.from_dict(data['ArrayOfObjTrainPositions']['objTrainPositions'])
        df['TrainLatitude'] = df['TrainLatitude'].astype(float)
        df['TrainLongitude'] = df['TrainLongitude'].astype(float)
        trains_json = df.to_dict(orient='records')

        return jsonify(trains_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT not set
    app.run(host="0.0.0.0", port=port)