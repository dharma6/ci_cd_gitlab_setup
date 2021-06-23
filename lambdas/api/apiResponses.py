import json

# class to handle return types and data


class API:
    def __init__(self):
        pass

    def response(self, statusCode = 502, data = {}):
            return {
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Origin': '*',
                },
                "statusCode": statusCode,
                "body": json.dumps(data),
            }

    def _200(self, data = {}):
        return self.response(200, data)

    def _400(self, data = {}):
        return self.response(400, data)

    def _404(self, data = {}):
        return self.response(404, data)

    def _500(self, data = {}):
        return self.response(500, data)
