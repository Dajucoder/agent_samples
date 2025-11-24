import os
import random
import google.generativeai as genai

def get_weather(location: str):
    """Get the current weather for a location.
    
    Args:
        location: The city or region to get the weather for.
    """
    # Mock weather data
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Snowy"]
    temps = range(-5, 35)
    return f"The weather in {location} is {random.choice(conditions)} with a temperature of {random.choice(temps)}°C."

class WeatherAgent:
    def __init__(self):
        self.name = "WeatherBot"
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        
        # Create the model with tools
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[get_weather]
        )
        
        # Start a chat session with automatic function calling enabled
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def run(self, input_text: str) -> str:
        try:
            response = self.chat.send_message(input_text)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
