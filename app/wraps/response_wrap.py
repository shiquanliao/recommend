from flask import jsonify


def error(codeType):
    result = {'code': codeType}
    return jsonify(result)


def success(data):
    data['code'] = 0
    return jsonify(data)
