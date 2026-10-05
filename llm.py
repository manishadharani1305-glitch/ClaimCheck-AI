import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from the .env file")

client = Groq(api_key=api_key)


def verify_claims(claim_text, reference_text):

    prompt = f"""
You are ClaimCheck AI, an intelligent document claim verification system.

Your task is to compare the CLAIM DOCUMENT with the REFERENCE DOCUMENT.

CLAIM DOCUMENT:
{claim_text}

REFERENCE DOCUMENT:
{reference_text}

Analyze the information carefully.

For each important claim, classify it as:

SUPPORTED
The reference document provides evidence supporting the claim.

CONTRADICTED
The reference document contains information that conflicts with the claim.

UNVERIFIED
The reference document does not contain enough information to verify the claim.

For every result provide:

1. Claim
2. Status
3. Evidence from the reference
4. Explanation

Do not invent information that is not present in the documents.

Give the final answer in this exact format:

CLAIM 1
Claim: <claim>
Status: SUPPORTED / CONTRADICTED / UNVERIFIED
Evidence: <evidence from reference document>
Explanation: <short explanation>

CLAIM 2
Claim: <claim>
Status: SUPPORTED / CONTRADICTED / UNVERIFIED
Evidence: <evidence from reference document>
Explanation: <short explanation>

Continue for all important claims.

At the end provide:

SUMMARY
Supported: <number>
Contradicted: <number>
Unverified: <number>

IMPORTANT:
- Only use information present in the documents.
- Never invent evidence.
- If evidence is missing, mark the claim UNVERIFIED.
- Keep explanations short and clear.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a precise document verification assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content