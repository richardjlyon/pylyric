from flask import Flask, jsonify
from pylyric.lyric import Lyric
import pylyric.config as cfg

app = Flask(__name__)

lcc = LyricClientCredentials(
        client_id=cfg.CLIENT_ID,
        client_secret=cfg.CLIENT_SECRET,
        api_key=cfg.API_KEY,
        access_token=cfg.ACCESS_TOKEN,
        refresh_token=cfg.REFRESH_TOKEN,
        redirect_url=cfg.REDIRECT_URL
)

lyric = Lyric(client_credentials_manager=lcc)
locationID = lyric.locations()[0]['locationID']
deviceID = lyric.locations()[0]['devices'][0]['deviceID']

device = lyric.device(locationID, deviceID)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/lyric/api/v1.0/indoortemperature', methods=['GET'])
def get_indoortemperature():
    return jsonify({'indoorTemperature': d.indoorTemperature})


if __name__ == '__main__':
    app.run(debug=True)
