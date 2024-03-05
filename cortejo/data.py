#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortejo - Create Cypress tests based on a human language definition (using AI)
@copyright: Copyright © 2024 Iwan van der Kleijn
@license: MIT
"""


from dataclasses import dataclass


@dataclass
class TestData:
    #def __init__(self, use_case, description, type, input_elements, action, expected_result):
    use_case: str
    description: str
    type: str
    input_elements: str
    action: str
    expected_result: str
