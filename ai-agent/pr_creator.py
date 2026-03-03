#!/usr/bin/env python3
"""
PR Creator
Creates pull requests on GitHub
"""

import subprocess
from datetime import datetime
from pathlib import Path


class PRCreator:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
    
    def create_pr(self, plan: dict, code: dict, requirements: list) -> dict:
        """
        Create pull request
        
        Args:
            plan (dict): Implementation plan
            code (dict): Generated code
            requirements (list): Requirements list
            
        Returns:
            dict: PR creation result
        """
        try:
            # Check if git is available
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            
            # Create branch
            branch_name = f"ai-feature/{plan['plan_id'].lower()}"
            self._create_branch(branch_name)
            
            # Stage and commit
            self._stage_files()
            commit_message = self._create_commit_message(plan, code, requirements)
            self._commit(commit_message)
            
            # Push branch
            self._push_branch(branch_name)
            
            return {
                'success': True,
                'branch': branch_name,
                'commit_message': commit_message,
                'files_changed': len(code['files']),
                'timestamp': datetime.now().isoformat(),
                'message': 'Branch created and pushed. Create PR manually on GitHub.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Git operations skipped: {str(e)}'
            }
    
    def _create_branch(self, branch_name: str) -> None:
        """Create git branch"""
        try:
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            print(f"  ✓ Branch created: {branch_name}")
        except subprocess.CalledProcessError:
            # Branch might exist
            subprocess.run(['git', 'checkout', branch_name], cwd=self.repo_path)
    
    def _stage_files(self) -> None:
        """Stage all changes"""
        subprocess.run(['git', 'add', '.'], cwd=self.repo_path, capture_output=True)
        print("  ✓ Files staged")
    
    def _commit(self, message: str) -> None:
        """Commit changes"""
        subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=self.repo_path,
            capture_output=True
        )
        print("  ✓ Changes committed")
    
    def _push_branch(self, branch_name: str) -> None:
        """Push branch to remote"""
        subprocess.run(
            ['git', 'push', '-u', 'origin', branch_name],
            cwd=self.repo_path,
            capture_output=True
        )
        print(f"  ✓ Pushed to: origin/{branch_name}")
    
    def _create_commit_message(self, plan: dict, code: dict, requirements: list) -> str:
        """Create detailed commit message"""
        req_list = '\n'.join([f'- {req["feature"]}' for req in requirements[:5]])
        
        return f"""🤖 AI Generated: {plan['total_requirements']} requirements

Generated {code['total_files']} files with {code['total_lines_of_code']} LOC

Plan ID: {plan['plan_id']}

Requirements:
{req_list}

Tasks: {plan['total_tasks']} ({len(plan['priority_order'])} prioritized)
"""
