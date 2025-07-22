from flask import jsonify

class CustomResponseModel:
    def __init__(self, message, data, success: bool = True):
        self.message = message
        self.data = data
        self.success = success
    def Unauthorized(self):
        return jsonify({
            'success': False,
            'message': self.message,
            'code': 401
        })
    def InternalServerError(self, code = 500):
        return jsonify({
            'success': False,
            'message': self.message,
            'code': code
        })
    def BadRequest(self, code = 400):
        return jsonify({
            'success': False,
            'message': self.message,
            'code': code
        })
    def Ok(self):
        return jsonify({
            'success': self.success,
            'message': self.message,
            'code': 200,
            'data': self.data
        })