from datetime import date

def user_language(request):
    request['user-language'] = 'RU'

def current_date(request):
    request['date'] = date.today()