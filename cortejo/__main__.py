#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create Cypress tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

import os
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


class TestData:
    def __init__(self, use_case, description, type, input_elements, action, expected_result):
        self.use_case = use_case
        self.description = description
        self.type = type
        self.input_elements = input_elements
        self.action = action
        self.expected_result = expected_result


def read_tests(filename):
    # Read the first sheet of the Excel file
    df = pd.read_excel(filename, sheet_name=0)

    # Select only the required columns
    columns = ['Use Case', 'Description', 'Type', 'Input Elements', 'Action', 'Expected Result']
    df = df[columns]

    # Convert the DataFrame rows to TestData objects
    test_data_list = [TestData(row['Use Case'], row['Description'], row['Type'], row['Input Elements'], row['Action'], row['Expected Result']) for index, row in df.iterrows()]

    return test_data_list


if __name__ == '__main__':
    test_data = read_tests('data/test-data.xlsx')
    for test in test_data:
        print(test.use_case, test.description)
