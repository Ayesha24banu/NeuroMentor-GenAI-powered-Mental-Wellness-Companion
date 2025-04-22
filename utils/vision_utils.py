#utils/ vision_utils.py
import google.generativeai as genai
from PIL import Image
from config.settings import settings

def analyze_image(image_path):
    """
    Analyzes an image using a supported Gemini model and returns only the emotional context.
    """
    try:
        # Ensure correct API key is set
        genai.configure(api_key=settings.GOOGLE_API_KEY)

        # List available models to confirm the right one is being used
        available_models = list(genai.list_models())  # Convert generator to list for inspection
        print("Available models:", available_models)

        # Find the correct model name for image analysis
        model_name = "gemini-1.5-flash"  # Switch to the supported model

        # Use the identified model for image analysis
        model = genai.GenerativeModel(model_name)
        
        # Open and process the image
        image = Image.open(image_path)
        image = image.convert("RGB")  # Ensure the image is in RGB format
        
        # Perform image analysis with the emotional context prompt
        response = model.generate_content([
            "Analyze this image purely based on its emotional context. "
            "Focus only on the emotions it conveys. Do not suggest improvements, feedback, or modifications. "
            "Just describe the emotional atmosphere you perceive.",
            image
        ])
        
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Failed to retrieve a valid response."

    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Unable to analyze the image due to an error: {e}"

