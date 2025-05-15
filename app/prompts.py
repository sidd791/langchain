intents = {
    "greet": {
        "examples": ["hello", "hi", "hey", "good morning"],
        "description": "Greet the user",
        "tools": ["greet_tool"]
    },
    "time": {
        "examples": ["what time is it", "tell me the current time", "time now"],
        "description": "Tell the current time",
        "tools": ["time_tool"]
    }
}
