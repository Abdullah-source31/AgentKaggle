import os
import sys
import requests
from dotenv import load_dotenv

# --- CONCEPT 1: SECURITY FEATURES (Secure Environment Loading) ---
# This pulls the secret key from the hidden .env file so it never leaks on screen.
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "AIzaSyYourActualKeyHere":
    print("[ERROR]: Security Violation. Valid API Key missing from environment context.")
    sys.exit(1)

from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

# --- CONCEPT 2: AGENT SKILLS (Dual-Scale Weather Analytics) ---
def get_current_weather(location: str) -> str:
    """Fetches real-time weather globally and normalizes both Celsius and Fahrenheit scales."""
    try:
        # Fetching raw data from the free public service
        url = f"https://wttr.in/{location}?format=%t+%C"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            raw_output = response.text.strip() # Example: "+77°F Clear" or "+25°C Rain"
            
            # Extract numbers safely
            digits = "".join([c for c in raw_output.split("°")[0] if c.isdigit() or c == '-'])
            temp_value = int(digits)
            condition = raw_output.split("°")[-1][1:].strip() # Extracts condition after the unit
            
            # Dynamically check if the source data is Fahrenheit or Celsius
            if "F" in raw_output:
                fahrenheit = temp_value
                celsius = int((fahrenheit - 32) * 5/9)
            else:
                celsius = temp_value
                fahrenheit = int((celsius * 9/5) + 32)
                
            return f"Weather in {location}: {celsius}°C ({fahrenheit}°F) | Condition: {condition}"
        return f"Could not retrieve live data for {location}."
    except Exception as e:
        return f"Weather tool error: {str(e)}"

print("--- Multi-Agent Dual-Scale System Initialized Safely ---")
user_query = "I am traveling to Lahore right now. What should I wear?"
print(f"User Request: {user_query}\n")

# =====================================================================
# --- CONCEPT 3: MULTI-AGENT SYSTEM (ADK Pipeline) ---
# =====================================================================

# AGENT 1: The Weather Specialist Agent (Executes Tool Skill)
print("[System] Routing request to Agent 1 (Weather Specialist)...")
agent_weather_response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=f"Find the weather for this request: {user_query}",
    config=types.GenerateContentConfig(
        system_instruction="You are a data extraction agent. Use get_current_weather to extract raw dual-scale metrics.",
        tools=[get_current_weather],
    ),
)
raw_weather_report = agent_weather_response.text
print(f"[Agent 1 Output]: Cached data -> {raw_weather_report}\n")

# AGENT 2: The Concierge Fashion Agent (Consumes Context for reasoning)
print("[System] Handing off context to Agent 2 (Concierge Fashion Expert)...")
final_response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=f"Provide packing list based on this dual-scale data: {raw_weather_report}. Intent: {user_query}",
    config=types.GenerateContentConfig(
        system_instruction="You are an expert travel stylist. Turn raw dual-scale metrics into clear outfit advice.",
    ),
)

print(f"[Agent 2 Final Response]:\n{final_response.text}")