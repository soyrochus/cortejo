#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""

from typing import List, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from cortejo.data import ConfigData, TestData

template_env : Optional[Environment]= None

def init_template_env(config_data: ConfigData):
    global template_env
    
    template_path_config = config_data['tests'].get('templates-path', None)
    template_path = Path(template_path_config) if template_path_config else None
    if template_path is not None and template_path.exists():
        template_env = Environment(loader=FileSystemLoader(template_path))
    
def expand_prompt_template(bounded_context: str, use_case: str, test_data: List[TestData]) -> Optional[str]:
    # Create a Jinja2 environment that loads templates from the filesystem
    global template_env
    if template_env is None:
        return None #raise ValueError("No template given (Template environment not initialized)")
    
    #filter test-data to remove skipped tests
    filtered_test_data = [data for data in test_data if not data.skip_generation]

    try:
        # Check if the template exists
        if f"{bounded_context.lower()}-{use_case.lower()}.j2" in template_env.list_templates():
            # Load the template
            template = template_env.get_template(f"{bounded_context.lower()}-{use_case.lower()}.j2")
        else:
            # Load a default template
            template = template_env.get_template("__default__.j2")
        
        # Render the template with the test data
        result = template.render(bounded_context = bounded_context,use_case=use_case, list=filtered_test_data)
    except Exception as e:
        raise ValueError(f"Error rendering template: {e}")
       
    return result