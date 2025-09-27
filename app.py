import requests
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
import base64



load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Content Generation API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["Content-Type"],
    allow_methods=["POST", "OPTIONS"],
)

# Environment variables
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
AGENT_ID = os.getenv('AGENT_ID')
DUST_API_KEY = os.getenv('DUST_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Dust API configuration
dust_url = f"https://dust.tt/api/v1/w/{WORKSPACE_ID}/assistant/conversations"
dust_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {DUST_API_KEY}"
}

# OpenAI configuration (only initialize if API key is available)
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

# Pydantic models
class GenerateContentRequest(BaseModel):
    topics_of_interest: List[str] = ["AI & Technology", "Startups"]
    ai_voice: str = "professional"
    about_context: str = "I want to promote my startup that creates an AI agent to help HR people to recruit"
    post_preference: str = "make impactful post"

class GenerateImageRequest(BaseModel):
    prompt: str = "A beautiful landscape with mountains and a lake"
    
# Response will be the parsed JSON content directly, no wrapper model needed

def load_prompt_template() -> str:
    """Load the prompt template from prompt.txt file"""
    try:
        with open("prompt.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Prompt template not found"
    except Exception as e:
        print(f"Error loading prompt template: {e}")
        return "Error loading prompt template"

def format_user_information(topics_of_interest: List[str], ai_voice: str, about_context: str, post_preference: str) -> str:
    """Format user parameters into a readable string for the prompt"""
    # Format the user parameters according to the prompt template inputs
    formatted_info = f"""
<user_profile>
topics_of_interest: {topics_of_interest}
ai_voice: {ai_voice}
about_context: {about_context}
post_preference: {post_preference}
</user_profile>
"""
    return formatted_info

def generate_content_with_dust(topics_of_interest: List[str], ai_voice: str, about_context: str, post_preference: str) -> tuple[bool, Optional[Dict], Optional[str]]:
    """
    Shared function to generate content using Dust API
    Returns: (success, parsed_content, error_message)
    """
    try:
        # Load prompt template and format user information
        prompt_template = load_prompt_template()
        user_information = format_user_information(topics_of_interest, ai_voice, about_context, post_preference)
        
        # Combine prompt template with user information
        combined_content = f"{prompt_template}\n\n{user_information}"
        print(f"Combined prompt content:\n{combined_content}")
        
        # Prepare parameters for Dust API
        parameters = {
            "message": {
                "content": combined_content,
                "mentions": [
                    {
                        "configurationId": AGENT_ID
                    }
                ],
                "context": {
                    "username": "slava",
                    "timezone": "Europe/Paris"
                }
            },
            "blocking": True,
            "title": "Content generation",
            "skipToolsValidation": True
        }
        
        # Call Dust API
        import time
        start_time = time.time()
        response = requests.post(dust_url, headers=dust_headers, json=parameters)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

        if response.status_code != 200:
            return False, None, f"Dust API call failed with status {response.status_code}"
        
        dust_data = response.json()
        
        # Extract the generated content from the Dust API response
        generated_content = None
        try:
            # The content is located at conversation.content[1][0].content
            if (dust_data.get("conversation") and 
                dust_data["conversation"].get("content") and 
                len(dust_data["conversation"]["content"]) > 1 and
                len(dust_data["conversation"]["content"][1]) > 0):
                generated_content = dust_data["conversation"]["content"][1][0].get("content")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Generated content: {generated_content}. Error extracting content from Dust response: {e}")
            generated_content = f"Error extracting generated content: {generated_content}"
        
        # Parse the generated content as JSON
        parsed_content = None
        try:
            if generated_content:
                parsed_content = json.loads(generated_content)
        except json.JSONDecodeError as e:
            print(f"Generated content: {generated_content}.Error parsing generated content as JSON: {e}")
            parsed_content = {"error": f"Failed to parse generated content as JSON: {generated_content}"}
        
        return True, parsed_content, None
        
    except Exception as e:
        return False, None, f"Internal server error: {str(e)}"

@app.post("/generate-content")
async def generate_content(request: GenerateContentRequest):
    """
    Generate social media content using Dust API with direct parameters
    Returns the parsed JSON content directly
    """
    success, parsed_content, error_message = generate_content_with_dust(
        request.topics_of_interest,
        request.ai_voice,
        request.about_context,
        request.post_preference
    )
    
    if success:
        return parsed_content
    else:
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


def create_image_with_openai(post: str):
    """Create image using OpenAI DALL-E API"""
    try:
        if not client:
            return False, None, "OpenAI API key not configured"
            
        prompt = f"Create a social media post image for: {post}"
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        return True, image_url, None
            
    except Exception as e:
        return False, None, f"OpenAI API error: {str(e)}"

@app.post("/image-generation")
async def image_generation(request: GenerateImageRequest):
    """Generate image using OpenAI API"""
    success, image_url, error_message = create_image_with_openai(request.prompt)
    
    if success:
        return {"image_url": image_url}
    else:
        raise HTTPException(status_code=500, detail=error_message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
