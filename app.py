from flask import Flask, g, request
import json

app = Flask(__name__)

# toがない場合2, 10, 16すべてを返す
# jsonで返す
def convert(fr, value, prefix):
    if prefix:
        if fr == 2:
            data = {'2': '0b' + str(int(value)), '10': str(int(value, 2)), '16': hex(int(value, 2))}
        elif fr == 10:
            data = {'2': bin(int(value)), '10': str(int(value)), '16': hex(int(value))}
        elif fr == 16:
            data = {'2': bin(int(value, 16)), '10': str(int(value, 16)), '16': '0x' + str(int(value))}
    else:
        if fr == 2:
            data = {'2': str(int(value)), '10': str(int(value, 2)), '16': hex(int(value, 2))[2:]}
        elif fr == 10:
            data = {'2': bin(int(value))[2:], '10': str(int(value)), '16': hex(int(value))[2:]}
        elif fr == 16:
            data = {'2': bin(int(value, 16))[2:], '10': str(int(value, 16)), '16': str(int(value))}
    return json.dumps(data)

def error_handler_400(message, hint = None,):
    return {
        "status": False,
        "message": {
            "message" : message,
            "hint": hint
            },
        "data": {}
    }, 400

# get
@app.route('/api', methods=['GET'])
def get():
    # get request arguments
    fr = request.args.get('from', None)
    if fr is None:
        fr = 10  # default value
    else:
        try:
            fr = int(fr)
            # from 2, 10, 16 check
            if fr not in [2, 10, 16]:
                return error_handler_400('invalid arguments', 'from parameter should be 2, 10, 16')
        except ValueError:
            fr = 10
            
    to = request.args.get('to')
    if to is not None:
        try:
            to = int(to)
            if to not in [2, 10, 16]:
                return error_handler_400('invalid arguments', 'to parameter should be 2, 10, 16')
        except ValueError:
            to = None

    # 'value' パラメータは文字列のまま扱う
    value = request.args.get('value')
    # valueにprefixがある場合切り取り、fromを変更
    if value is not None and value[:2] == '0b':
        fr = 2
        value = value[2:]
    elif value is not None and value[:2] == '0x':
        fr = 16
        value = value[2:]
    
    if value is None:
        return error_handler_400('missing arguments', 'value parameter is required')
    # if fr == 2 value should be 0 or 1
    elif fr == 2 and not all(c in '01' for c in value):
        return error_handler_400('invalid arguments', 'value parameter should be 0 or 1')
    # if fr == 16 value should be 0-9 or a-f
    elif fr == 16 and not all(c in '0123456789abcdef' for c in value):
        return error_handler_400('invalid arguments', 'value parameter should be 0-9 or a-f')
    # if fr == 10 value should be 0-9
    elif fr == 10 and not value.isdigit():
        return error_handler_400('invalid arguments', 'value parameter should be 0-9')
    prefix = request.args.get('prefix')
    if prefix is not None:
        if prefix not in ['true', 'false']:
            return error_handler_400('invalid arguments', 'prefix parameter should be true or false')
        else:
            prefix = True if prefix == 'true' else False
    else:
        prefix = False
    
    data = convert(fr, value, prefix)
    if to is None:
        return {
            "status": True,
            "data": json.loads(data),
            "message": "success"
            }, 200
    else:
        return {
            "status": True,
            "data":{str(to): json.loads(data)[str(to)]},
            "message": "success"
            }, 200
        
    
if __name__ == '__main__':
    app.run()
