import json
import configparser
from aliyunsdkvod.request.v20170321 import GetVideoPlayAuthRequest
from aliyunsdkcore import client
from flask import *

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/', static_folder='./html/')

config = configparser.ConfigParser()
config.read('configure.pri')
clt = client.AcsClient(config['UserKey']['accesskeyid'], config['UserKey']['accesskeysecret'], 'cn-shanghai')

def get_video_playauth(clt, video_id):
        request = GetVideoPlayAuthRequest.GetVideoPlayAuthRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(video_id)
        response = json.loads(clt.do_action_with_exception(request))
        return response


# print(get_video_playauth(clt)['PlayAuth'])

@app.route('/<path:filename>')
def send_js(filename):
    print(filename)
    
    return send_from_directory('./html/', filename)

@app.route('/query', methods=['GET'])
def query():
    video_id = request.args.get('video_id')
    auth = get_video_playauth(clt, video_id)
    
    return auth['PlayAuth']


if __name__ == "__main__":
    app.run()

