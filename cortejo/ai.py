#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

from typing import Dict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from cortejo.data import BoundedContexts, TestData
import os
import re
from cortejo.templates import expand_prompt_template

try:
    # set the key from file "openai_key.txt" in the same directory as this file or set
    # the environment variable OPENAI_API_KEY
    load_dotenv("openai_api_key.env")
    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])  # type: ignore
except Exception as e:
    print(e)
    exit(1)

def extract_code_block(prompt_response: str):
    # Pattern to extract text between ```javascript and ```
    pattern = r"```javascript(.*?)```"
    match = re.search(pattern, prompt_response, re.DOTALL)

    if match:
        # Return the extracted code block, stripping any leading or trailing whitespace
        return match.group(1).strip()
    else:
        # Return the entire input text if no code block is found
        return prompt_response


def generate_test(bounded_context: str, use_case: str, test_data: List[TestData]) -> str:

    prompt = expand_prompt_template(bounded_context, use_case, test_data)
    if prompt is None:
        raise ValueError("No template given (Template environment not initialized)")    

    response = llm.invoke(prompt)
    return extract_code_block(response.content) # type: ignore