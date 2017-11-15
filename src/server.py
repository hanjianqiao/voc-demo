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


def get_sub_category(cate_id = None):
    if cate_id == None:
        cate_id = -1
    param = {'Action': 'GetCategories', 'CateId': cate_id, 'Version': '2017-03-21'}
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


def get_all_video_list():
    param = {'Action': 'GetVideoList', 'Version': '2017-03-21'}
    path = rpc_signature_composer.get_signed_url(param, ukid, ukas, 'JSON', 'GET', [])
    domain = 'vod.cn-shanghai.aliyuncs.com'
    connection = http.client.HTTPConnection(domain)
    connection.request('GET', path)
    response = connection.getresponse()
    ret = (response.read().decode())
    return ret


def get_up_auth(title, filename, cateid):
    if cateid == None:
        cateid = 755789223
    param = {'Action': 'CreateUploadVideo', 'Title': title, 'FileName': filename, 'CateId': cateid,'Version': '2017-03-21'}
    path = rpc_signature_composer.get_signed_url(param, ukid, ukas, 'JSON', 'GET', [])
    domain = 'vod.cn-shanghai.aliyuncs.com'
    connection = http.client.HTTPConnection(domain)
    connection.request('GET', path)
    response = connection.getresponse()
    ret = (response.read().decode())
    return ret


def get_video_path(video_id):
    param = {'Action': 'GetPlayInfo', 'VideoId': video_id, 'Version': '2017-03-21'}
    path = rpc_signature_composer.get_signed_url(param, ukid, ukas, 'JSON', 'GET', [])
    domain = 'vod.cn-shanghai.aliyuncs.com'
    connection = http.client.HTTPConnection(domain)
    connection.request('GET', path)
    response = connection.getresponse()
    ret = (response.read().decode())
    return ret
# print(get_video_playauth(clt)['PlayAuth'])


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



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
    cate_id = request.args.get('cate_id')
    return get_sub_category(cate_id)


@app.route('/list', methods=['GET'])
def getList():
    cateId = request.args.get('id')
    return get_video_list(cateId)


@app.route('/playpath', methods=['GET'])
def getVideoPath():
    video_id = request.args.get('video_id')
    return get_video_path(video_id)


@app.route('/all', methods=['GET'])
def getAllList():
    return get_all_video_list()

@app.route('/upauth', methods=['GET'])
def getUpAuth():
    return get_up_auth(request.args.get('title'), request.args.get('filename'), request.args.get('cateid'))

@app.route('/')
def hello():
    return redirect("/category.html", code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
