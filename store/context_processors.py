from .store import Store

def store(request):
    # return the cart default data
    return {'store':Store(request)}
