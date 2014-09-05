from datetime import datetime

def parse(s):
    formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']
    d = None
    for format in formats:
        try:
            d = datetime.strptime(s, format)
            break
        except ValueError:
            pass
    return d