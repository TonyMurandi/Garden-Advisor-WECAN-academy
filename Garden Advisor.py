import google.genai as genai
import json
import os
import datetime
from dotenv import load_dotenv
# load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-3.5-flash"
# make output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
# stage 1 prompt - diagnosis of the garden problem
crop = input("enter crop: ")
county = input("enter county: ")
problem = input("describe the problem: ")
stage1_prompt = f"""
Role: You're an agricultural expert for small scale farmers in Kenya.
Task: Analyze the farmer's problem and list 3 likely causes and come up with possible solutions to the suggested causes
Context: Crop: {crop}, County: {county}, Problem: {problem}. Assume limited budget and local Kenyan context
Constraints: Only list agricultural related causes. Do not respond to anything that is not related to the topic of agriculture, instead respond with "I can only provide agricultural advice, would you like me to continue with that?"
Output: Return only valid json, with this exact format: {{"likely_causes": ["cause1", "cause2", "cause3"]}} and {{"possible_solutions": ["solution1", "solution2", "solution3"]}}. Do not include any other text or explanation, and provide the answers in point form. If you cannot provide 3 causes or solutions, please provide as many as you can, but do not make up any causes or solutions.
"""
