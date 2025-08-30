
import os
import base64
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

def generate_story_and_character_and_background(user_prompt: str) -> dict:
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.9)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a world-class story-writing and character-development AI. Your task is to craft a compelling short story and a detailed character description and background location of character based on a user's request."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    tools = []
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    story_generation_prompt = f"""
    Given the following user prompt, perform three tasks:
    1. Write a short story that is exactly 200 words.
    2. Create a detailed character description for the main protagonist of the story that is exactly 100 words. The description should include:
       - Name
       - Age
       - Appearance
       - Personality (with quirks and flaws)
       - Background/History
       - Motivations
       - A unique skill or ability
       - A central conflict they face.
    3. Create a detailed description of the story's setting/background that is exactly 100 words.
    User Prompt: {user_prompt}
    Ensure the story and descriptions are coherent and well-integrated. Structure your response with the following headers to make parsing easy:
    --- STORY ---
    --- CHARACTER DESCRIPTION ---
    --- BACKGROUND DESCRIPTION ---
    """
    try:
        response = agent_executor.invoke({"input": story_generation_prompt})
        generated_text = response.get('output', "Failed to generate content.")
        if "--- STORY ---" in generated_text and "--- CHARACTER DESCRIPTION ---" in generated_text and "--- BACKGROUND DESCRIPTION ---" in generated_text:
            start_story = generated_text.find("--- STORY ---") + len("--- STORY ---")
            end_story = generated_text.find("--- CHARACTER DESCRIPTION ---")
            story = generated_text[start_story:end_story].strip()
            start_char = end_story + len("--- CHARACTER DESCRIPTION ---")
            end_char = generated_text.find("--- BACKGROUND DESCRIPTION ---")
            char_description = generated_text[start_char:end_char].strip()
            start_bg = end_char + len("--- BACKGROUND DESCRIPTION ---")
            bg_img_desc = generated_text[start_bg:].strip()
        else:
            story = "Generated content is not in the expected format."
            char_description = ""
            bg_img_desc = ""
        return {
            "story": story,
            "char_description": char_description,
            "bg_img_desc": bg_img_desc
        }
    except Exception as e:
        return {
            "story": f"An error occurred: {e}",
            "char_description": f"An error occurred: {e}",
            "bg_img_desc": f"An error occurred: {e}"
        }
