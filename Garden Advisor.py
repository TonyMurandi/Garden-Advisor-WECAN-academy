import google.genai as genai
import google.genai.types as types
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

# call the Gemini API for stage 1
response = client.models.generate_content(
    model=model,
    contents=stage1_prompt
)
print("/n== stage 1: diagnosis ===/n")
print(response.text)

stage1_result = response.text

# stage 2 - prompt - solution of diagnosis
stage2_prompt = f"""
Role: You're an agricultural expert for small scale farmers in Kenya
Task: Based on the diagnosis provided, suggest a detailed solution for each of the likely causes identified in stage 1. Provide practical steps that the farmer can take to address each cause, considering limited budget and local Kenyan context.
Context: Crop: {crop}, County: {county}, Problem: {problem}. Diagnosis: {stage1_result}
Constraints: Only provide agricultural related solutions. Do not respond to anything that is not related to the
output: Return only valid json, with this exact format: {{"detailed_solutions": {{"cause1": ["step1", "step2"], "cause2": ["step1", "step2"], "cause3": ["step1", "step2"]}}}}. Do not include any other text or explanation, and provide the answers in point form. If you cannot provide detailed solutions for all causes, please provide as many as you can, but do not make up any solutions.
"""

# call the Gemini API for stage 2
response2 = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=stage2_prompt
)
print("/n== stage 2: solution ===/n")
print(response2.text)

stage2_result = response2.text

# save the results to a json file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"output/garden_advice_{timestamp}.json", "w") as f:
    data = {
        "stage1": stage1_result,
        "stage2": stage2_result
    }
    f.write(f"Crop: {crop}\nCounty: {county}\nProblem: {problem}\n")
    f.write(f"Generated at: {timestamp}\n")
    f.write("=" * 50 + "/n/n")
    f.write("Stage 1: Diagnosis\n")
    f.write("=" * 50 + "/n")
    f.write(stage1_result + "/n/n")
    f.write("=" * 50 + "/n/n")
    f.write("Stage 2: Detailed Solutions of Diagnosis\n")
    f.write("=" * 50 + "/n")
    f.write(stage2_result + "/n/n")

print(f"/nResults saved to output/garden_advice_{timestamp}.json and .txt")
