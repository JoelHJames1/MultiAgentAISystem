"""
JAFS - Jarvis Agent Framework System
Main entry point for the JAFS AI agent framework
"""

import argparse
import sys
from jafs.core.orchestrator import AgentOrchestrator
from jafs.ui.cli import CLI

def main():
    """Main entry point for the JAFS AI agent"""
    parser = argparse.ArgumentParser(description="JAFS AI - Jarvis Agent Framework System")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to configuration file")
    parser.add_argument("--mode", type=str, default="single", choices=["single", "multi"], help="Agent mode")
    parser.add_argument("--task", type=str, help="Task description")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Initialize the CLI
    cli = CLI(verbose=args.verbose)
    
    # Display welcome message
    cli.display_welcome()
    
    # Initialize the agent orchestrator
    orchestrator = AgentOrchestrator(config_path=args.config)
    
    # If task is provided as argument, execute it
    if args.task:
        result = orchestrator.execute_task(args.task, mode=args.mode)
        cli.display_result(result)
        return
    
    # Otherwise, start interactive mode
    cli.start_interactive_mode(orchestrator)

if __name__ == "__main__":
    main()
