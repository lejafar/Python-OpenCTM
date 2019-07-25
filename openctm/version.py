from datetime import datetime, date

today = date.today()
now = datetime.now()
__version__ = f'1.0.10a{today.year}{today.month}{today.day}{now.hour}{now.minute}'
