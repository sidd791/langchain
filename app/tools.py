from datetime import datetime

def greet_tool():
    return "Hello! How can I assist you today?"

def time_tool():
    return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
