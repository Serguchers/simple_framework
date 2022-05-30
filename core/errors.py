class PageNotFound404(Exception):
    def __call__(self, request):
        return '404 ERROR', '404 PAGE NOT FOUND'