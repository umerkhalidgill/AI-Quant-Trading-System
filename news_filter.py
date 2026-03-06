from datetime import datetime

def news_filter():

    hour = datetime.now().hour

    # Example high impact news time
    if hour in [13,14]:
        return False

    return True