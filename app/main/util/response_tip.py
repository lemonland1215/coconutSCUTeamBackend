# src/api/utils/responses.py
from flask import make_response, jsonify

INVALID_FIELD_NAME_SENT_422 = {
    "http_status": 422,
    "status": "invalidField",
    "message": "Invalid fields found"
    }

INVALID_INPUT_422 = {
    "http_status": 422,
    "status": "invalidInput",
    "message": "Please make sure your input valid."
    }

BAD_REQUEST_400 = {
    "http_status": 400,
    "status": "badRequest",
    "message": "Bad request"
    }

ITEM_LOCKED_400 = {
    "http_status": 400,
    "status": "itemLocked",
    "message": "Unlock the item if you want want to modify it."
    }
ITEM_NOT_EXISTS = {
    "http_status": 400,
    "status": "itemNotExists",
    "message": "No such item."
}


ITEM_FREEZED_400 = {
    "http_status": 400,
    "status": "itemFreezed",
    "message": "Unfreeze the item if you want want to make it function."
    }

SERVER_ERROR_500 = {
    "http_status": 500,
    "status": "serverError",
    "message": "Server error"
    }

SERVER_ERROR_404 = {
    "http_status": 404,
    "status": "notFound",
    "message": "Resource not found"
    }

UNAUTHORIZED_403 = {
    "http_status": 403,
    "status": "notAuthorized",
    "message": "You are not authorized"
    }

SUCCESS_200 = {
    'http_status': 200,
    'status': 'success',
    }

SUCCESS_201 = {
    'http_status': 201,
    'status': 'success',
    }
SUCCESS_204 = {
    'http_status': 204,
    'status': 'success'
    }


def response_with(response, value=None, message=None,
        error=None, headers={}, pagination=None):
    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'status': response['status']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_status'], headers)