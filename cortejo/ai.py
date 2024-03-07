#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create Cypress tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

from typing import Dict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from cortejo.data import BoundedContexts, TestData
import os
import re


try:
    # set the key from file "openai_key.txt" in the same directory as this file or set
    # the environment variable OPENAI_API_KEY
    load_dotenv("openai_api_key.env")
    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])  # type: ignore
except Exception as e:
    print(e)
    exit(1)



def generate_test_prompt(url: str, use_case: str, test_data: list[TestData]) -> str:
    templates = [f"""For the Use Case "{use_case}", create a series of Cypress tests. Do not include
the cy.visit call to each tests. But rather, include it in the beforeEach block with the url: {{url}}. 
For the tests use the following data representing each test case:
    """]
    
    for data in test_data:
        if data.skip_generation:
            continue
        
        templates.append(f"""Description :- {data.description}	
Type :- {data.type}	
Input Elements :- {data.input_elements}
Action :- {data.action}	
Expected Result :- {data.expected_result}
""")
        
    return "\n".join(templates)


def extract_code_block(markdown_text):
    # Pattern to extract text between ```javascript and ```
    pattern = r"```javascript(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)

    if match:
        # Return the extracted code block, stripping any leading or trailing whitespace
        return match.group(1).strip()
    else:
        # Return None or an empty string if no code block is found
       raise ValueError("No code block found in the text returned from the AI model")


def generate_cypress_test(url: str, bounded_context: str, use_case: str, test_data: List[TestData]) -> str:

    prompt = generate_test_prompt(url, use_case, test_data)
    response = llm.invoke(prompt)
    return extract_code_block(response.content) # type: ignore