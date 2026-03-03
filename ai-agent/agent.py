#!/usr/bin/env python3
"""
Main AI Agent Orchestrator
Coordinates the entire workflow: Requirements → Plan → Code → PR
"""

import os
from pathlib import Path
from .requirements_reader import RequirementsReader
from .planner import Planner
from .coder import Coder
from .pr_creator import PRCreator


class AIAgent:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.requirements_reader = RequirementsReader()
        self.planner = Planner()
        self.coder = Coder(repo_path)
        self.pr_creator = PRCreator(repo_path)
        
    def run(self, requirements_file: str):
        """
        Execute the full AI Agent workflow
        
        Args:
            requirements_file (str): Path to requirements file (xlsx, txt, md)
            
        Returns:
            dict: Workflow results
        """
        print("🤖 AI Agent Started...\n")
        
        try:
            # Step 1: Read Requirements
            print("📖 Step 1: Reading Requirements...")
            requirements = self.requirements_reader.read(requirements_file)
            print(f"✅ Found {len(requirements)} requirements\n")
            
            # Step 2: Plan Implementation
            print("📋 Step 2: Planning Implementation...")
            plan = self.planner.create_plan(requirements)
            print(f"✅ Created plan with {len(plan['tasks'])} tasks\n")
            
            # Step 3: Generate Code
            print("💻 Step 3: Generating Code...")
            code_results = self.coder.generate(plan, requirements)
            print(f"✅ Generated {len(code_results['files'])} files\n")
            
            # Step 4: Create PR (optional - requires GitHub CLI)
            print("🔄 Step 4: Creating Pull Request (optional)...")
            try:
                pr_result = self.pr_creator.create_pr(
                    plan=plan,
                    code=code_results,
                    requirements=requirements
                )
                print(f"✅ PR Created: {pr_result.get('branch', 'N/A')}\n")
            except Exception as e:
                print(f"⚠️  PR creation skipped: {str(e)}\n")
                pr_result = {'success': False, 'message': 'PR creation skipped'}
            
            return {
                'success': True,
                'requirements_count': len(requirements),
                'requirements': requirements,
                'plan': plan,
                'code': code_results,
                'pr': pr_result,
                'message': 'AI Agent workflow completed successfully!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'AI Agent workflow failed: {str(e)}'
            }


def main():
    """Main entry point"""
    agent = AIAgent(repo_path=".")
    
    # Check if requirements file exists
    requirements_file = "requirements/features.xlsx"
    
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file not found: {requirements_file}")
        print("📝 Please create requirements/features.xlsx first")
        return
    
    # Run the agent
    result = agent.run(requirements_file)
    
    # Print results
    print("\n" + "="*50)
    if result['success']:
        print("✅ SUCCESS! AI Agent completed all tasks")
        print(f"Requirements: {result['requirements_count']}")
        print(f"Files Generated: {result['code']['total_files']}")
        print(f"Lines of Code: {result['code']['total_lines_of_code']}")
    else:
        print(f"❌ FAILED: {result['error']}")
    print("="*50)


if __name__ == "__main__":
    main()
