from django.http import HttpResponseBadRequest

def ajax_required(fn):
    def wrap_fn(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()  ## 400 error

    wrap_fn.__doc__ = fn.__doc__
    wrap_fn.__name__ = fn.__name__
    return wrap_fn
