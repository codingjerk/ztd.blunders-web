from datetime import datetime

def cached(expireDelta):
    def decorator(func):
        memo = {}
        expires = {}

        def result(*args):
            if args in memo and datetime.now() <= expires[args]:
                pass # Do nothing, all cached
            else:
                memo[args] = func(*args)
                expires[args] = datetime.now() + expireDelta

            return memo[args]

        return result

    return decorator

