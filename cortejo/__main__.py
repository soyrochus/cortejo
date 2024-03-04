#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create Cypress tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

from dataclasses import dataclass
import os
from typing import Dict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pandas as pd


try:
    # set the key from file "openai_key.txt" in the same directory as this file or set
    # the environment variable OPENAI_API_KEY
    load_dotenv("openai_api_key.env")
    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])  # type: ignore
except Exception as e:
    print(e)
    exit(1)


@dataclass
class TestData:
    #def __init__(self, use_case, description, type, input_elements, action, expected_result):
    use_case: str
    description: str
    type: str
    input_elements: str
    action: str
    expected_result: str


def read_tests(filename):
    # Read the first sheet of the Excel file
    df = pd.read_excel(filename, sheet_name=0)

    # Select only the required columns
    columns = ['Use Case', 'Description', 'Type', 'Input Elements', 'Action', 'Expected Result']
    df = df[columns]

    # Convert the DataFrame rows to TestData objects
    test_data_list = [TestData(row['Use Case'], row['Description'], row['Type'], row['Input Elements'], row['Action'], 
                               row['Expected Result']) for index, row in df.iterrows()]

    return test_data_list


def split_tests_in_use_cases(test_data) -> Dict[str, List[TestData]]:

    use_cases: Dict[str, List[TestData]] = {}
    for test in test_data:
        if test.use_case not in use_cases: 
            use_cases[test.use_case] = []
        use_cases[test.use_case].append(test)
    return use_cases


def generate_test_prompt(use_case: str, test_data: list[TestData]) -> str:
    templates = [f"""For the Use Case "{use_case}", create a series of Cypress tests. Do not include
the cy.visit call to each tests. But rather, include it in the beforeEach block. 
For the tests use the following data representing each test case:
    """]
    
    for data in test_data:
        templates.append(f"""Description :- {data.description}	
Type :- {data.type}	
Input Elements :- {data.input_elements}
Action :- {data.action}	
Expected Result :- {data.expected_result}
""")
        
    return "\n".join(templates)
    
def generate_cypress_test(use_case: str, test_data: list[TestData]) -> str:
    prompt = generate_test_prompt(use_case, test_data)
    response = llm.invoke(prompt)
    return response.content # type: ignore


if __name__ == '__main__':
    test_data = read_tests('data/test-data.xlsx')
    use_cases = split_tests_in_use_cases(test_data) 
    print(generate_cypress_test('Login', use_cases['Login']))