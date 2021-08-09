'''
Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

'''
import json
import base64
import asyncio
import ssl
import websockets
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'secret_key_here'

# Global variables
count = 0
ws = ''

# System Info to be synced with web page:
system_info = {}


async def start():
    global ws
    global system_info
    print('Starting Websocket connection to device: ' + session['ip_address'])
    ws = await connect()
    try:
        print('-'*25 + ' Connected ' + '-'*25)
        system_info['is_muted'] = await get_mic_status(ws)
        system_info['connected_cameras'] = await get_cameras_list(ws)
        system_info['volume'] = await get_volume(ws)
    finally:
        await ws.close()


''' Handling Flask web application's routes '''


@app.route('/')
# Default route
def default():
    return redirect('/login')


@app.route('/login')
# Login route
def login():
    return render_template('login.html')


@app.route('/verify_login', methods=['POST'])
# Verify login route
def verify_login():
    session['ip_address'] = request.form.get('ip_address')
    session['username'] = request.form.get('username')
    session['password'] = request.form.get('password')
    print('Device: ' + session['ip_address'])
    session['count'] = 0

    print('New login - IP: ' + str(session['ip_address']))

    return redirect('/index')


@app.route('/logout')
# Logout route
def logout():
    print('Logout - device:' + str(session['ip_address']))
    session.pop('ip_address')
    session.pop('username')
    session.pop('password')
    return redirect('/login')

@app.route('/index')
# Default route
def index():
    asyncio.run(start())
    return render_template('index.html', device_ip_address=session['ip_address'], system_info=system_info)


@app.route('/mute_device', methods=['POST'])
# Mute Device route
def mute_device():
    print('Muting device: ' + session['ip_address'])
    asyncio.run(mute_mic())
    return str(system_info['is_muted'])


@app.route('/trigger_usb_mode', methods=['POST'])
def trigger_usb_mode():
    print('Triggering USB mode on device: ' + session['ip_address'])
    asyncio.run(trigger_usb_mode())
    return ''


@app.route('/enable_usb_mode', methods=['POST'])
def enable_usb_mode():
    print('Enabling USB mode on device: ' + session['ip_address'])
    asyncio.run(enable_usb_mode())
    return 'Enabled'


@app.route('/disable_usb_mode', methods=['POST'])
def disable_usb_mode():
    print('Disabling USB mode on device: ' + session['ip_address'])
    asyncio.run(disable_usb_mode())
    return 'Disabled'


@app.route('/move_camera', methods=['POST'])
def move_camera():
    camera_id = request.form.get('camera_id')
    direction = request.form.get('direction')
    new_location = asyncio.run(move_camera(camera_id, direction))
    return new_location


@app.route('/change_volume_level', methods=['POST'])
def change_volume_level():
    v_level = request.form.get('volume_level')
    response = asyncio.run(change_volume_level(v_level))
    return response


@app.route('/dial', methods=['POST'])
def dial():
    number_to_dial = request.form.get('number_to_dial')
    response = asyncio.run(dial(number_to_dial))
    return response

''' Websocket functions '''


async def connect():
    return await websockets.connect('wss://{}/ws/'.format(session['ip_address']), ssl=ssl._create_unverified_context(), extra_headers={
        'Authorization': 'Basic {}'.format(base64.b64encode('{}:{}'.format(session['username'], session['password']).encode()).decode('utf-8'))})


def construct(method):
    global count
    count += 1
    return {'jsonrpc': '2.0', 'id': str(count), 'method': method}


def query(params):
    print('* Method: xQuery ' + params)
    payload = construct('xQuery')
    payload['params'] = {'Query': params.split()}
    return payload


def get(params):
    print('* Method: xGet ' + params)
    payload = construct('xGet')
    params = [i if not i.isnumeric() else int(i) for i in params.split()]
    payload['params'] = {'Path': params}
    return payload


def status(params):
    print('* Method: xStatus ' + params)
    payload = construct('xStatus')
    params = [i if not i.isnumeric() else int(i) for i in params.split()]
    payload['params'] = {'Path': params}
    return payload

def command(path, params=None):
    print('* Method: xCommand ' + path)
    payload = construct('{}{}'.format('xCommand/', '/'.join(path.split(' '))))

    # Params are for multiline commands and other command parameters {'ConfigId':'example', 'body':'<Extensions><Version>1.0</Version>...</Extensions>'}
    if params != None:
        payload['params'] = params

    return payload


def config(path, value):
    print('* Method: xSet ' + path)
    payload = construct('xSet')
    payload['params'] = {
        "Path": ['Configuration'] + path.split(' '),
        "Value": value
    }
    return payload


def feedbackSubscribe(path=None, notify=False):
    payload = construct('xFeedback/Subscribe')
    payload['params'] = {
        "Query": path.split(' '),
        "NotifyCurrentValue": notify
    }
    return payload


async def send(ws, message):
    await ws.send(json.dumps(message))
    print('-'*5 + ' Sending: ' + '-'*5)
    print(message)


async def receive(ws):
    result = await ws.recv()
    print('-'*5 + ' Received: ' + '-'*5)
    print(result)
    return (json.loads(result))


''' Custom functions '''


async def get_mic_status(ws):
    # Getting Status: Audio Microphones Mute
    params = 'Status Audio Microphones Mute'
    await send(ws, get(params))
    result = await receive(ws)
    is_muted = (result['result'] == 'On')
    print('is_muted: ' + str(is_muted))
    return is_muted


async def get_cameras_list(ws):
    # Getting Status: Cameras Camera[n] Connected
    i = 0
    connected_cameras = []
    while i < 7:
        i += 1
        params = 'Status Cameras Camera ' + str(i) + ' Connected'
        await send(ws, get(params))
        result = await receive(ws)
        try:
            is_connected = (result['result'] == 'True')
            if(is_connected):
                print('is_connected: ' + str(i))
                connected_cameras.append(str(i))
        except:
            break
    return connected_cameras


async def get_volume(ws):
    # Getting Status: Audio Microphones Mute
    params = 'Status Audio Volume'
    await send(ws, get(params))
    result = await receive(ws)
    volume = result['result']
    print('volume: ' + str(volume))
    return volume


async def mute_mic():
    global system_info
    ws = await connect()
    try:
        # Checking Mic state, to trigger
        system_info['is_muted'] = await get_mic_status(ws)

        # Changing Microphone Mute state (Off/On)
        if(system_info['is_muted']):
            params = 'Audio Microphones Unmute'
        else:
            params = 'Audio Microphones Mute'
        await send(ws, command(params))
        await receive(ws)

        # Getting Mic state, to update web page
        system_info['is_muted'] = await get_mic_status(ws)
    finally:
        await ws.close()


async def enable_usb_mode():
    ws = await connect()
    try:
        print('Enabling USB mode...')
        thecmd = 'UserInterface Extensions Panel Clicked'
        vars = {'PanelId': 'proUSB_Inactive_1-0-0'}
        await send(ws, command(thecmd, vars))
        await receive(ws)

    finally:
        await ws.close()


async def disable_usb_mode():
    ws = await connect()
    try:
        print('Disabling USB mode...')
        thecmd = 'UserInterface Extensions Panel Clicked'
        vars = {'PanelId': 'proUSB_Active_1-0-0'}
        await send(ws, command(thecmd, vars))
        await receive(ws)

    finally:
        await ws.close()


async def trigger_usb_mode():
    ws = await connect()
    try:
        print('Triggering USB mode...')

        # TODO: Get current state of USB-Mode, to know which one to trigger

    finally:
        await ws.close()


async def subscribe_to_audio():
    print('Subscribing to audio')
    ws = await connect()
    await send(ws, feedbackSubscribe('Status Audio Volume', True))
    while True:
        await receive(ws)


async def move_camera(camera_id, direction):
    ws = await connect()
    try:
        print('Moving camera id-' + camera_id + ' direction: ' +
              direction + ' on device: ' + session['ip_address'])
        change_value = 1000
        new_value = ''
        
        # Pan, if right or left
        if (direction == 'right' or direction == 'left'):
            # Getting Status: Cameras Camera [n] Position Pan
            params = 'Status Cameras Camera ' + str(camera_id) + ' Position Pan'
            await send(ws, get(params))
            result = await receive(ws)
            current_pan = result['result']
            print('current_pan: ' + str(current_pan))
            
            # Changing value, depends on direction
            if(direction =='right'): new_value = current_pan-change_value
            else: new_value = current_pan+change_value

            # xCommand Camera PositionSet CameraId:x Pan:y
            params = 'Camera PositionSet'
            vars={'CameraId':str(camera_id), 'Pan': str(new_value)}
            await send(ws, command(params,vars))
            result = await receive(ws)
        
        # Tile, if up or down
        elif (direction == 'up' or direction == 'down'):
            # Getting Status: Cameras Camera [n] Position Tilt
            params = 'Status Cameras Camera ' + \
                str(camera_id) + ' Position Tilt'
            await send(ws, get(params))
            result = await receive(ws)
            current_tilt = result['result']
            print('current_tilt: ' + str(current_tilt))

            # Changing value, depends on direction
            if(direction == 'up'):
                new_value = current_tilt+change_value
            else:
                new_value = current_tilt-change_value

            # xCommand Camera PositionSet CameraId:x Tilt:y
            params = 'Camera PositionSet'
            vars = {'CameraId': str(camera_id), 'Tilt': str(new_value)}
            await send(ws, command(params, vars))
            result = await receive(ws)
            
    finally:
        await ws.close()
        return str(new_value)


async def change_volume_level(level):
    ws = await connect()
    try:
        print('Changing audio level to: ' + level)
        # xCommand Audio Volume Set Level:xx
        params = 'Audio Volume Set'
        vars = {'Level': str(level)}
        await send(ws, command(params, vars))
        result = await receive(ws)

    finally:
        await ws.close()
        return (result['result']['status'])


async def dial(number):
    ws = await connect()
    try:
        print('Dialing to: ' + number)
        # xCommand Dial Number: [number]
        params = 'Dial'
        vars = {'Number': str(number)}
        await send(ws, command(params, vars))
        result = await receive(ws)

    finally:
        await ws.close()
        return (result['result']['status'])


# ''' Starting Flask web application '''
if __name__ == "__main__":
    print('Starting flask web application..')
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
