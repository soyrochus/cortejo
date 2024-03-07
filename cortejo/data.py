#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create Cypress tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""
from dataclasses import dataclass
from typing import Dict, List
import pandas as pd

@dataclass
class TestData:
    bounded_context: str
    url: str
    use_case: str
    description: str
    type: str
    skip_generation: bool
    input_elements: str
    action: str
    expected_result: str

UseCases = Dict[str, List[TestData]]
BoundedContexts = Dict[str, UseCases]
ConfigData = Dict[str, Dict[str, str]]

def read_tests(filename:str, config_data: ConfigData) -> List[TestData]:
    # Read the first sheet of the Excel file
    df = pd.read_excel(filename, sheet_name=0)

    # Select only the required columns
    columns = ['Bounded Context', 'Use Case', 'Description', 'Type', 'Skip Generation', 'Input Elements', 'Action', 'Expected Result']
    df = df[columns]

    # Convert the DataFrame rows to TestData objects
    test_data_list = [TestData(row['Bounded Context'], "", row['Use Case'], row['Description'], row['Type'], 'yes' ==  row['Skip Generation'],
                               row['Input Elements'], row['Action'], row['Expected Result']) for index, row in df.iterrows()] 
    
    default_url = config_data['cypress'].get('default-url', None)
    for test in test_data_list:
        url = config_data['urls'].get(test.bounded_context, None)
        if url is None:
            if default_url is None:
                raise Exception(f"No URL found for bounded context {test.bounded_context}")
            else:
                test.url = default_url
        else:
            test.url = url
            
    return test_data_list


def get_bounded_contexts(test_data: List[TestData]) -> BoundedContexts:
    """ Split the test data into bounded contexts and use cases """

    context_dict: BoundedContexts = {}
    for data in test_data:
        if data.bounded_context not in context_dict:
            context_dict[data.bounded_context] = {}
        
        if data.use_case not in context_dict[data.bounded_context]:
            context_dict[data.bounded_context][data.use_case] = []
        
        context_dict[data.bounded_context][data.use_case].append(data)
    
    return context_dict