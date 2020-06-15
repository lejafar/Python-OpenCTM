from datetime import datetime, date

today = date.today()
now = datetime.now()
__version__ = f'1.1.0a{today.year}{today.month}{today.day}'
