import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to sys.path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.weather_agent import WeatherAgent

def main():
    print("Initializing Weather Agent...")
    agent = WeatherAgent()
    
    print(f"Agent {agent.name} is ready.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        response = agent.run(user_input)
        print(f"{agent.name}: {response}")

if __name__ == '__main__':
    main()
