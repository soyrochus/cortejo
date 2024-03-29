#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

import argparse
import os
from pathlib import Path
import tomllib
from typing import Dict
from cortejo.ai import generate_test
from cortejo.data import BoundedContexts, ConfigData, TestData, get_bounded_contexts, read_tests
from cortejo.templates import init_template_env

def get_run_params():
    # Initialize the parser
    parser = argparse.ArgumentParser(prog='cortejo', description='Create tests based on a human language definition (using AI)')

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

def get_config(config_path: Path | None = None) -> ConfigData:
    if config_path is None:
        # Check in the current directory
        current_dir_path = Path('cortejo.toml')
        
        if current_dir_path.exists():
            config_path = current_dir_path
        else:
            raise Exception(f"Config file {current_dir_path} does not exist")
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
                first_test = bounded_contexts[context][use_case][0]
                file_content = generate_test(context, use_case, bounded_contexts[context][use_case])
                test_file.write(file_content)

if __name__ == '__main__':
    try:
        config_path, test_def_path, project_path = get_run_params()
        config_data = get_config(config_path)
        init_template_env(config_data)
        output_path = Path.joinpath(project_path.resolve(), Path(config_data['tests']['tests-path']))
        if not output_path.exists():
            raise Exception(f"Tests path {output_path} does not exist")
        
        test_data = read_tests(test_def_path, config_data)
        bounded_contexts = get_bounded_contexts(test_data) 
        write_tests(output_path, bounded_contexts)
       
        print(f"Tests written to {output_path}")
        
    except Exception as e:
        print(e)
        exit(1)
