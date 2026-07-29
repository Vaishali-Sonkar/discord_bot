import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from langchain.tools import tool
from tavily import TavilyClient
import os
import io
from PIL import Image
from langchain_core.tools import tool
from google import genai
from google.genai import types



model=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")




tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def generate_image(prompt: str) -> str:
    """Use this tool to generate an image based on a text prompt."""
    try:
        # Initialize client (it will automatically find GEMINI_API_KEY in your .env)
        client = genai.Client()
        
        # Use the modern generate_content method with the new image model
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=prompt,
            config=types.GenerateContentConfig(
                # Tell Gemini we explicitly want an IMAGE back
                response_modalities=["IMAGE"], 
                # Optional: Force a square aspect ratio
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                ),
            ),
        )
        
        filename = f"image_{uuid.uuid4().hex[:8]}.png"
        
        # The new SDK syntax requires us to parse the 'parts' of the response
        for part in response.parts:
            # Check if the part contains image data
            if part.inline_data:
                # The SDK has a handy as_image() helper now!
                generated_image = part.as_image()
                generated_image.save(filename)
                
                return f"Success! Image saved as {filename}. You MUST include the exact text '{filename}' in your final response."
                
        return "Failed to generate image: No image data returned."
        
    except Exception as e:
        print(f"\n--- TOOL ERROR DEBUG ---: {str(e)}\n")
        return f"Error generating image: {str(e)}"
@tool
def SurfInternet(query: str) -> str:
    """Use this tool Search the internet for latest information in lessest words possible"""
    result = tavily_client.search(query)
    return str(result)

agent = create_agent(
    model=model,
    tools=[SurfInternet,generate_image]
)
