import json
import configparser
from aliyunsdkvod.request.v20170321 import GetVideoPlayAuthRequest
from aliyunsdkcore import client
from flask import *

from aliyunsdkcore.auth.composer import rpc_signature_composer

import http.client


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/', static_folder='./html/')

config = configparser.ConfigParser()
config.read('configure.pri')
ukid = config['UserKey']['accesskeyid']
ukas = config['UserKey']['accesskeysecret']
clt = client.AcsClient(ukid, ukas, 'cn-shanghai')


def get_video_playauth(clt, video_id):
        request = GetVideoPlayAuthRequest.GetVideoPlayAuthRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(video_id)
        response = json.loads(clt.do_action_with_exception(request))
        return response


def get_all_category():
    param = {'Action': 'GetCategories', 'CateId': -1, 'Version': '2017-03-21'}
    path = rpc_signature_composer.get_signed_url(param, ukid, ukas, 'JSON', 'GET', [])
    domain = 'vod.cn-shanghai.aliyuncs.com'
    connection = http.client.HTTPConnection(domain)
    connection.request('GET', path)
    response = connection.getresponse()
    ret = (response.read().decode())
    return ret


def get_video_list(cateId):
    param = {'Action': 'GetVideoList', 'CateId': cateId, 'Version': '2017-03-21'}
    path = rpc_signature_composer.get_signed_url(param, ukid, ukas, 'JSON', 'GET', [])
    domain = 'vod.cn-shanghai.aliyuncs.com'
    connection = http.client.HTTPConnection(domain)
    connection.request('GET', path)
    response = connection.getresponse()
    ret = (response.read().decode())
    return ret


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


@app.route('/cate', methods=['GET'])
def getCate():
    return get_all_category()


@app.route('/list', methods=['GET'])
def getList():
    cateId = request.args.get('id')
    return get_video_list(cateId)


if __name__ == "__main__":
    app.run()
