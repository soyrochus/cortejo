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
    use_case: str
    description: str
    type: str
    input_elements: str
    action: str
    expected_result: str

UseCases = Dict[str, List[TestData]]
BoundedContexts = Dict[str, UseCases]

def read_tests(filename)-> List[TestData]:
    # Read the first sheet of the Excel file
    df = pd.read_excel(filename, sheet_name=0)

    # Select only the required columns
    columns = ['Bounded Context', 'Use Case', 'Description', 'Type', 'Input Elements', 'Action', 'Expected Result']
    df = df[columns]

    # Convert the DataFrame rows to TestData objects
    test_data_list = [TestData(row['Bounded Context'], row['Use Case'], row['Description'], row['Type'], row['Input Elements'], row['Action'], 
                               row['Expected Result']) for index, row in df.iterrows()]

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