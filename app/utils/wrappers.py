
from flask import jsonify, request

from functools import update_wrapper

from app.utils import session, reference, logger

logger = logger.Logger(__name__)

def ready_for_output(result):
    if result['status'] != 'ok':
        logger.error(result['message'])

    return jsonify(result)

def tokenize():
    def decorator(f):
        def wrapped(*args, **kwargs):
            reference.Reference().create()

            try:
                token = request.json['token']
            except Exception:
                reference.Reference().clean()

                return ready_for_output({
                    'status': 'error',
                    'message': 'API token is required'
                })

            try:
                success = session.State().authorize(token)
                if not success:
                    return ready_for_output({
                        'status': 'error',
                        'message': 'Invalid API token'
                    })

                result = f(*args, **kwargs)
            except Exception as e:
                logger.error(str(e))

                result = ready_for_output({
                    'status': 'error',
                    'message': 'Unknown API error'
                })

                session.State().clean()
                reference.Reference().clean()

                return result

            result = ready_for_output(result)

            session.State().clean()
            reference.Reference().clean()

            return result

        return update_wrapper(wrapped, f)

    return decorator

def nullable():
    """
    Some API endponts dont have session state and does not need authorization.
    But it is very usefull to define decorator for those requests as well to
    be able to catch exceptions and transform them to json
    """
    def decorator(f):
        def wrapped(*args, **kwargs):
            reference.Reference().create()

            try:
                result = f(*args, **kwargs)
            except Exception as e:
                logger.error(str(e))

                result = ready_for_output({
                    'status': 'error',
                    'message': 'Unknown API error'
                })

                reference.Reference().clean()

                return result

            result = ready_for_output(result)

            reference.Reference().clean()

            return result

        return update_wrapper(wrapped, f)

    return decorator
