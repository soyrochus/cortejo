#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create Cypress tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

import argparse
import os
from pathlib import Path
from typing import Dict, List
import pandas as pd
import tomllib
from cortejo.ai import generate_cypress_test
from cortejo.data import TestData


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

def get_run_params():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='Process runtime parameters.')

    # Adding arguments
    parser.add_argument('-c', '--config', type=str, help='Path to the config TOML file', default=None)
    parser.add_argument('test_def_path', type=str, help='Path to the test definition Excel file')
    parser.add_argument('tests_output_path', type=str, nargs='?', default=',', help='Path for the tests output')

    # Parse the arguments
    args = parser.parse_args()

    # Convert string paths to Path instances
    config_path = Path(args.config) if args.config else None
    test_def_path = Path(args.test_def_path)
    tests_output_path = Path(args.tests_output_path)

    return config_path, test_def_path, tests_output_path

def get_config(config_path: Path | None = None) -> Dict[str, Dict[str, str]]:
    if config_path is None:
        # Check in the current directory
        current_dir_path = Path('cortejo.toml')
        home_dir_path = Path.home() / '.cortejo.toml'
        
        if current_dir_path.exists():
            config_path = current_dir_path
        elif home_dir_path.exists():
            config_path = home_dir_path
        else:
             return {"cypress": {"tests-path": "cypress/integration"}}
    else:
        config_path = Path(config_path)
    
    # Check if the specified config path exists
    if not config_path.exists():
       raise Exception(f"Config file {config_path} does not exist")

    # Read the TOML file and return the content
    with open(config_path, 'rb') as file:
        try:
            data = tomllib.load(file)
        except Exception as e:
            raise Exception(f"Error reading config file {config_path}: {e}")
    
    return data

if __name__ == '__main__':
    try:
        config_path, test_def_path, tests_output_path = get_run_params()
        config_data = get_config(config_path)
        test_data = read_tests(test_def_path)
        use_cases = split_tests_in_use_cases(test_data) 
        print(generate_cypress_test('Login', use_cases))
    except Exception as e:
        print(e)
        exit(1)
    #test_data = read_tests('data/test-data.xlsx')
    #test_data = read_tests('data/devonfw.xlsx')
    #use_cases = split_tests_in_use_cases(test_data) 
    #print(generate_cypress_test('Login', use_cases))