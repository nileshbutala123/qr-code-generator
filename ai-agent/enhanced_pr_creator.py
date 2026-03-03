#!/usr/bin/env python3
"""
Enhanced PR Creator
Creates pull requests with human-in-the-loop approval
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class EnhancedPRCreator:
    def __init__(self, repo_path: str = "."):
        """
        Initialize PR creator
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = Path(repo_path)
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_owner = None
        self.repo_name = None
        self._detect_repo_info()
    
    def create_pr_with_approval(self, branch_name: str, title: str, description: str, 
                                files_changed: list, changes_summary: str) -> Dict[str, Any]:
        """
        Create a PR with human approval step
        
        Args:
            branch_name: Name of the feature branch
            title: PR title
            description: PR description
            files_changed: List of changed files
            changes_summary: Summary of all changes
            
        Returns:
            dict: PR creation result with approval status
        """
        print("\n" + "="*60)
        print("🔍 HUMAN APPROVAL REQUIRED - Code Review")
        print("="*60)
        
        # Show summary
        self._show_pr_summary(branch_name, title, description, files_changed, changes_summary)
        
        # Get human approval
        approved = self._get_approval()
        
        if not approved:
            return {
                'success': False,
                'approved': False,
                'message': 'PR creation cancelled by user'
            }
        
        # Stage and commit
        try:
            result = self._commit_changes(branch_name, title)
            if not result['success']:
                return result
            
            # Create PR on GitHub
            pr_result = self._create_github_pr(branch_name, title, description)
            
            return {
                'success': True,
                'approved': True,
                'branch': branch_name,
                'pr_url': pr_result.get('pr_url'),
                'pr_number': pr_result.get('pr_number'),
                'message': f"✅ PR created and ready for review!"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error creating PR: {str(e)}'
            }
    
    def _show_pr_summary(self, branch: str, title: str, description: str, 
                         files: list, changes: str) -> None:
        """Show PR information for review"""
        
        print(f"\n📝 PR DETAILS:")
        print(f"   Branch: {branch}")
        print(f"   Title: {title}")
        print(f"   Description: {description}")
        print(f"\n📁 Files Changed ({len(files)}):")
        for f in files[:10]:
            print(f"   - {f}")
        if len(files) > 10:
            print(f"   ... and {len(files) - 10} more")
        
        print(f"\n📊 CHANGES SUMMARY:")
        print(changes[:500] + ("..." if len(changes) > 500 else ""))
    
    def _get_approval(self) -> bool:
        """Get human approval via CLI"""
        print("\n" + "-"*60)
        response = input("🤔 Proceed with creating PR? (yes/no): ").strip().lower()
        
        if response in ['y', 'yes', 'true', '1']:
            return True
        else:
            print("❌ PR creation cancelled")
            return False
    
    def _commit_changes(self, branch_name: str, commit_message: str) -> Dict[str, Any]:
        """Commit changes to git"""
        try:
            # Create or checkout branch
            result = subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0 and 'already exists' not in result.stderr:
                # Try to checkout existing branch
                subprocess.run(['git', 'checkout', branch_name], cwd=self.repo_path, capture_output=True)
            
            print(f"✓ Branch: {branch_name}")
            
            # Stage all changes
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, capture_output=True)
            print(f"✓ Staged changes")
            
            # Commit
            commit_result = subprocess.run(
                ['git', 'commit', '-m', f"🤖 {commit_message}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if commit_result.returncode == 0:
                print(f"✓ Committed")
            else:
                if 'nothing to commit' in commit_result.stderr:
                    print(f"ℹ️  No changes to commit")
                else:
                    print(f"⚠️  Commit message: {commit_result.stderr}")
            
            # Push to remote
            push_result = subprocess.run(
                ['git', 'push', '-u', 'origin', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if push_result.returncode == 0:
                print(f"✓ Pushed to origin/{branch_name}")
            else:
                print(f"⚠️  Push result: {push_result.stderr}")
            
            return {
                'success': True,
                'branch': branch_name,
                'committed': commit_result.returncode == 0
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_github_pr(self, branch_name: str, title: str, description: str) -> Dict[str, Any]:
        """Create PR on GitHub using API"""
        
        if not self.github_token:
            print("\n⚠️  GITHUB_TOKEN not set. Cannot create PR automatically.")
            print("    To enable auto PR creation:")
            print("    1. Get token from: https://github.com/settings/tokens")
            print("    2. Set: export GITHUB_TOKEN='your_token_here'")
            print("    3. Grant: repo (full control) and workflow scopes")
            return {
                'success': False,
                'message': 'GitHub token not configured',
                'manual_instructions': f"""
Manual PR Creation:
1. Push branch: git push origin {branch_name}
2. Go to: {self._get_github_repo_url()}/pull/new/{branch_name}
3. Title: {title}
4. Description: {description}
5. Create Pull Request
                """
            }
        
        try:
            from github import Github
        except ImportError:
            print("⚠️  PyGithub not installed. Install with: pip install PyGithub")
            return {'success': False, 'error': 'PyGithub not installed'}
        
        try:
            g = Github(self.github_token)
            
            if not self.repo_owner or not self.repo_name:
                print("⚠️  Could not detect repository details")
                return {'success': False, 'error': 'Repo not detected'}
            
            repo = g.get_user(self.repo_owner).get_repo(self.repo_name)
            
            # Create PR
            pr = repo.create_pull(
                title=title,
                body=description,
                head=branch_name,
                base='main'
            )
            
            print(f"✓ Created PR: {pr.html_url}")
            
            return {
                'success': True,
                'pr_url': pr.html_url,
                'pr_number': pr.number
            }
        
        except Exception as e:
            print(f"⚠️  Error creating GitHub PR: {e}")
            return {
                'success': False,
                'error': str(e),
                'manual_url': f"{self._get_github_repo_url()}/pull/new/{branch_name}"
            }
    
    def _detect_repo_info(self) -> None:
        """Detect GitHub owner/repo from .git/config"""
        try:
            git_config = self.repo_path / '.git' / 'config'
            if git_config.exists():
                with open(git_config, 'r') as f:
                    content = f.read()
                    # Look for remote origin URL
                    for line in content.split('\n'):
                        if 'url =' in line:
                            url = line.split('url =')[-1].strip()
                            # Parse github.com/owner/repo.git
                            if 'github.com' in url:
                                parts = url.split('/')[-2:]
                                self.repo_owner = parts[0]
                                self.repo_name = parts[1].replace('.git', '')
                                break
        except:
            pass
    
    def _get_github_repo_url(self) -> str:
        """Get GitHub repository URL"""
        if self.repo_owner and self.repo_name:
            return f"https://github.com/{self.repo_owner}/{self.repo_name}"
        return "https://github.com/your-repo"
    
    def show_pr_instructions(self, branch_name: str, title: str) -> str:
        """Show manual PR creation instructions"""
        return f"""
╔══════════════════════════════════════════════════════╗
║          Manual Pull Request Creation               ║
╚══════════════════════════════════════════════════════╝

Branch Created: origin/{branch_name}

To create PR manually:

1. Copy this link:
   {self._get_github_repo_url()}/compare/main...{branch_name}

2. OR follow these steps:
   a) Go to your repository on GitHub
   b) Click "Pull requests"
   c) Click "New pull request"
   d) Select: main <- {branch_name}
   e) Title: {title}
   f) Click "Create pull request"

Your code changes are now on the {branch_name} branch
and ready for review on GitHub!
"""
