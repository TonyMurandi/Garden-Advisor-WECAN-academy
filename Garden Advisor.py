import google.generativeai as genai
import json
import os
import datetime
from dotenv import load_dotenv
# load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# pick the AI model
model = genai.GenerativeModel("gemini-1.5-flash")
# make output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
# stage 1 prompt - diagnosis of the garden problem
stage1_prompt = """ 
Role: You're an agricultural expert for small scale farmers
Task: Analyze the farmer's problem and list 3 likely causes
Context: Crop: {Crop}, County: {county}, Problem: {Problem}. Assume limited budget and local Kenyan context
Constraints: Only list agricultural causes. Do not give anything that is not related to the topic of agriculture
Output: Return only valid json, with this exact format
"""
