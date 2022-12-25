from fastapi import APIRouter, Depends, HTTPException, Response, status
import json


class ErrorJSONType(type):
    def __getattr__(self, item):
        error_code = getattr(ErrorCode, item)
        return {
            'code': error_code[0],
            'message': error_code[1]
        }


class ErrorCode:
    SAMPLE_ERROR = (9940410001, 'sample error')

    class dict(metaclass=ErrorJSONType):
        pass


def count(obj):
    if isinstance(obj, list):
        return len(obj)
    elif isinstance(obj, str) or isinstance(obj, dict) or isinstance(obj, int) or isinstance(obj, bool):
        return 1
    elif obj is None:
        return 0
    else:
        raise ValueError("Can not count items of %s" % type(obj))


def ok(data=None, result_number=None, reason=None):
    if reason:
        return Response(json.dumps(dict(message=data or reason[1], error=True, number=reason[0])))
    if not result_number:
        result_number = count(data)
    return Response(json.dumps(dict(message=data, number=result_number, error=False)), status_code=status.HTTP_200_OK)


def bad_request(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_400_BAD_REQUEST)


def created(data=None, result_number=None, reason=None):
    if reason:
        return Response(json.dumps(dict(message=data or reason[1], error=True, number=reason[0])),
                        status_code=status.HTTP_201_CREATED)
    if not result_number:
        result_number = count(data)
    return Response(json.dumps(dict(message=data, error=False, number=result_number)),
                    status_code=status.HTTP_201_CREATED)


def accepted(data=None, result_number=None, reason=None):
    if reason:
        return Response(json.dumps(dict(message=data or reason[1], error=True, number=reason[0])),
                        status_code=status.HTTP_202_ACCEPTED)
    if not result_number:
        result_number = count(data)
    return Response(json.dumps(dict(message=data, error=False, number=result_number)),
                    status_code=status.HTTP_202_ACCEPTED)


def unauthorized(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_401_UNAUTHORIZED)


def forbidden(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_403_FORBIDDEN)


def not_found(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_404_NOT_FOUND)


def not_acceptable(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_406_NOT_ACCEPTABLE)


def conflict(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_409_CONFLICT)


def internal_server_error(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def bad_gateway(reason, message=None):
    return Response(json.dumps(dict(message=message or reason[1], error=True, number=reason[0])),
                    status_code=status.HTTP_502_BAD_GATEWAY)
