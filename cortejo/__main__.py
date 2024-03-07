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
import tomllib
from typing import Dict
from cortejo.ai import generate_cypress_test
from cortejo.data import BoundedContexts, TestData, get_bounded_contexts, read_tests

def get_run_params():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='Process runtime parameters.')

    # Adding arguments
    parser.add_argument('-c', '--config', type=str, help='Path to the config TOML file', default=None)
    parser.add_argument('test_def_path', type=str, help='Path to the test definition Excel file')
    parser.add_argument('project_path', type=str, nargs='?', default='.', help='Project Path (default: current directory)')

    # Parse the arguments
    args = parser.parse_args()

    # Convert string paths to Path instances
    config_path = Path(args.config) if args.config else None
    test_def_path = Path(args.test_def_path)
    project_path = Path(args.project_path).resolve()
    if not project_path.exists():
        raise Exception(f"Project path {project_path} does not exist")

    return config_path, test_def_path, project_path

def get_config(config_path: Path | None = None) -> Dict[str, Dict[str, str]]:
    if config_path is None:
        # Check in the current directory
        current_dir_path = Path('cortejo.toml')
        #home_dir_path = Path.home() / '.cortejo.toml'
        
        if current_dir_path.exists():
            config_path = current_dir_path
        #elif home_dir_path.exists():
        #    config_path = home_dir_path
        else:
             return {"cypress": {"tests-path": "cypress/e2e"}}
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

def write_tests(tests_output_path: Path, bounded_contexts:BoundedContexts):
    for context in bounded_contexts:
        dir_path = os.path.join(tests_output_path, context)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        for use_case in bounded_contexts[context]:
            test_file_path = os.path.join(dir_path, f"{use_case}.spec.js")
            with open(test_file_path, 'w') as test_file:
                tests = generate_cypress_test(context, use_case, bounded_contexts)
                test_file.write(tests)

if __name__ == '__main__':
    try:
        config_path, test_def_path, project_path = get_run_params()
        config_data = get_config(config_path)
        test_data = read_tests(test_def_path)
        bounded_contexts = get_bounded_contexts(test_data) 
        output_path = Path.joinpath(project_path.resolve(), Path(config_data['cypress']['tests-path']))
        if not output_path.exists():
            raise Exception(f"Tests path {output_path} does not exist")
        write_tests(output_path, bounded_contexts)
        #print(generate_cypress_test('Auth', 'Login', bounded_contexts))
        print(f"Tests written to {output_path}")
        
    except Exception as e:
        print(e)
        exit(1)
