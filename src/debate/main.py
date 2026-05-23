#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from debate.crew import Debate

def run():
    """
    Run the crew.
    """
    inputs = {
        'motion': 'Suppliment vitamins are best for the human body',
    }
    
    try:
        result = Debate().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
