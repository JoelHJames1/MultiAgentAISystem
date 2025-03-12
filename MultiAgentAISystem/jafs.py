#!/usr/bin/env python
"""
JAFS - Jarvis Agent Framework System
User-friendly command-line interface

Author   Joel Hernandez James
Current Date  3/12/2025
Class
"""

import sys
import os
import argparse
import re
import subprocess

def detect_task_type(task):
    """
    Automatically detect the type of task and set the appropriate mode.
    
    Args:
        task: The task description
        
    Returns:
        The appropriate mode for the task
    """
    # Default to auto mode
    mode = "auto"
    
    # Research-related keywords
    research_keywords = [
        "research", "find", "search", "look up", "investigate", 
        "analyze", "study", "explore", "learn about"
    ]
    
    # Calculation-related keywords
    calc_keywords = [
        "calculate", "compute", "solve", "evaluate", "what is", 
        "how much", "add", "subtract", "multiply", "divide"
    ]
    
    # Creative-related keywords
    creative_keywords = [
        "create", "generate", "write", "compose", "design", 
        "develop", "make", "build", "draft"
    ]
    
    # Check for research-related tasks
    for keyword in research_keywords:
        if re.search(r'\b' + keyword + r'\b', task.lower()):
            mode = "multi"
            break
            
    # Check for calculation-related tasks
    for keyword in calc_keywords:
        if re.search(r'\b' + keyword + r'\b', task.lower()):
            mode = "single"
            break
            
    # Check for creative-related tasks
    for keyword in creative_keywords:
        if re.search(r'\b' + keyword + r'\b', task.lower()):
            mode = "multi"
            break
    
    return mode

def main():
    """
    Main entry point for the JAFS user-friendly interface.
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="JAFS - Jarvis Agent Framework System",
        epilog="Just tell JAFS what you want, and it will figure out the rest!"
    )
    
    # Add arguments
    parser.add_argument(
        "task", 
        nargs="*", 
        help="What you want JAFS to do (e.g., 'research quantum computing', 'calculate 2 + 2')"
    )
    parser.add_argument(
        "--mode", 
        choices=["single", "multi", "auto"],
        help="Force a specific mode (optional)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Show detailed output"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no task is provided, show help
    if not args.task:
        parser.print_help()
        return
    
    # Join the task arguments into a single string
    task = " ".join(args.task)
    
    # Detect the task type if mode is not specified
    mode = args.mode if args.mode else detect_task_type(task)
    
    # Get the parent directory (where jafs and anus directories are)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Build the command
    cmd = [
        "python", 
        "-m", 
        "jafs.main"
    ]
    
    # Add mode if specified
    if mode:
        cmd.extend(["--mode", mode])
    
    # Add verbose flag if specified
    if args.verbose:
        cmd.append("--verbose")
    
    # Add task
    cmd.extend(["--task", task])
    
    # Set PYTHONPATH to the parent directory
    env = os.environ.copy()
    env["PYTHONPATH"] = parent_dir
    
    # Print the command if verbose
    if args.verbose:
        print(f"Executing: {' '.join(cmd)}")
        print(f"PYTHONPATH: {parent_dir}")
    
    # Execute the command
    subprocess.run(cmd, env=env, cwd=parent_dir)

if __name__ == "__main__":
    main()
