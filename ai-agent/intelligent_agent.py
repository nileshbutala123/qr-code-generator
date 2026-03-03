#!/usr/bin/env python3
"""
Intelligent AI Agent
Main orchestrator that coordinates all components for intelligent code generation
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from requirements_reader import RequirementsReader
from codebase_analyzer import CodebaseAnalyzer
from claude_codegen import ClaudeCodeGen
from enhanced_pr_creator import EnhancedPRCreator


class IntelligentAgent:
    def __init__(self, requirements_file: str = "requirements/features.txt", repo_path: str = "."):
        """
        Initialize the intelligent AI agent
        
        Args:
            requirements_file: Path to requirements file (xlsx/txt/md/json)
            repo_path: Path to the Git repository
        """
        self.requirements_file = Path(requirements_file)
        self.repo_path = Path(repo_path)
        
        # Initialize components
        self.reader = RequirementsReader()
        self.analyzer = CodebaseAnalyzer(str(repo_path))
        self.claude = ClaudeCodeGen(str(repo_path))
        self.pr_creator = EnhancedPRCreator(str(repo_path))
        
        # State
        self.requirements = []
        self.codebase_context = ""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.plan = {
            'session_id': self.session_id,
            'requirements': [],
            'changes': [],
            'summary': ""
        }
    
    def run(self, interactive: bool = True) -> Dict[str, Any]:
        """
        Run the intelligent agent workflow
        
        Args:
            interactive: Whether to enable human approval steps
            
        Returns:
            dict: Final results with PR information
        """
        print("\n" + "="*70)
        print("🤖 INTELLIGENT AI AGENT - QR Code Generator Feature Development")
        print("="*70)
        
        # Step 1: Read requirements
        print("\n📖 Step 1: Reading requirements...")
        self.requirements = self._read_requirements()
        if not self.requirements:
            return {'success': False, 'error': 'No requirements found'}
        
        print(f"✓ Loaded {len(self.requirements)} requirements")
        
        # Step 2: Analyze codebase
        print("\n📊 Step 2: Analyzing codebase...")
        analysis = self.analyzer.analyze()
        self.codebase_context = self.analyzer.get_context_for_claude()
        print(f"✓ Found {len(analysis['endpoints'])} endpoints and {len(analysis['models'])} models")
        
        # Step 3: Process each requirement with Claude
        print("\n🧠 Step 3: Processing requirements with Claude AI...")
        all_changes = []
        for i, req in enumerate(self.requirements, 1):
            print(f"\n   [{i}/{len(self.requirements)}] {req.get('feature', 'Unknown')}")
            change = self._process_requirement(req, i)
            if change:
                all_changes.append(change)
        
        if not all_changes:
            return {'success': False, 'error': 'No changes generated'}
        
        # Step 4: Summarize changes
        print("\n📝 Step 4: Summarizing all changes...")
        changes_summary = self._summarize_changes(all_changes)
        
        # Step 5: Create PR with human approval
        print("\n🔄 Step 5: Creating pull request...")
        if interactive:
            pr_result = self._create_pr_interactive(all_changes, changes_summary)
        else:
            pr_result = self._create_pr_auto(all_changes, changes_summary)
        
        # Final summary
        print("\n" + "="*70)
        print("✅ INTELLIGENT AGENT WORKFLOW COMPLETE")
        print("="*70)
        
        return {
            'success': True,
            'session_id': self.session_id,
            'requirements_processed': len(self.requirements),
            'changes_generated': len(all_changes),
            'pr_result': pr_result,
            'plan': self.plan,
            'timestamp': datetime.now().isoformat()
        }
    
    def _read_requirements(self) -> List[Dict[str, str]]:
        """Read requirements from file"""
        try:
            reqs = self.reader.read(str(self.requirements_file))
            print(f"   Loaded from: {self.requirements_file}")
            return reqs
        except Exception as e:
            print(f"❌ Error reading requirements: {e}")
            return []
    
    def _process_requirement(self, requirement: Dict[str, str], index: int) -> Dict[str, Any]:
        """Process a single requirement with Claude"""
        
        # Generate implementation plan
        result = self.claude.generate_implementation(requirement, self.codebase_context)
        
        if not result.get('success'):
            print(f"      ⚠️  Failed: {result.get('error')}")
            return None
        
        print(f"      ✓ Analysis complete (tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out)")
        
        change = {
            'requirement': requirement,
            'analysis': result['analysis'],
            'index': index,
            'status': 'analyzed'
        }
        
        self.plan['requirements'].append({
            'id': requirement.get('id', f'REQ-{index}'),
            'feature': requirement.get('feature', 'Unknown'),
            'priority': requirement.get('priority', 'medium'),
            'analysis_tokens': result['usage']['input_tokens'] + result['usage']['output_tokens']
        })
        
        return change
    
    def _summarize_changes(self, all_changes: List[Dict]) -> str:
        """Create a summary of all changes"""
        summary = f"""# AI-Generated Implementation Plan
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session ID: {self.session_id}

## Summary
Processed {len(all_changes)} requirements using Claude API.
Total features to implement: {len(self.requirements)}

## Requirements Analyzed
"""
        for i, req in enumerate(self.requirements, 1):
            priority_emoji = "🔴" if req.get('priority') == 'high' else "🟡" if req.get('priority') == 'medium' else "🟢"
            summary += f"\n{priority_emoji} [{i}] {req.get('feature', 'Unknown')}"
            summary += f"\n    Description: {req.get('description', 'No description')}"
            summary += f"\n    Priority: {req.get('priority', 'medium').upper()}\n"
        
        summary += f"\n## Next Steps\n"
        summary += f"1. Review each requirement's implementation plan\n"
        summary += f"2. Approve the generated code changes\n"
        summary += f"3. Run tests to verify: `pytest tests/`\n"
        summary += f"4. Merge PR after code review\n"
        
        self.plan['summary'] = summary
        return summary
    
    def _create_pr_interactive(self, all_changes: List[Dict], summary: str) -> Dict[str, Any]:
        """Create PR with human-in-the-loop approval"""
        
        branch_name = f"ai-feature/{self.session_id}"
        title = f"🤖 AI-Generated: {len(self.requirements)} new features"
        
        files = [req.get('feature', 'unknown').lower().replace(' ', '_') + '.py' 
                for req in self.requirements]
        
        description = f"""## Automated Code Generation

This PR contains AI-generated implementations for {len(self.requirements)} features.

### Features Included
{chr(10).join([f"- {r.get('feature', 'Unknown')}" for r in self.requirements])}

### Analysis
- Generated using Claude 3.5 Sonnet
- Analyzed existing codebase ({len(self.analyzer.endpoints)} endpoints)
- Respects FastAPI patterns and conventions

### Testing Required
- [ ] Run: `pytest tests/`
- [ ] Manual testing of new endpoints
- [ ] Check integration with existing code

### Files Modified
{chr(10).join([f"- `{f}`" for f in files[:10]])}

---
*Generated by Intelligent AI Agent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
        """
        
        result = self.pr_creator.create_pr_with_approval(
            branch_name=branch_name,
            title=title,
            description=description,
            files_changed=files,
            changes_summary=summary
        )
        
        if result['success']:
            if result.get('pr_url'):
                print(f"\n✅ PR Created: {result['pr_url']}")
            else:
                print(self.pr_creator.show_pr_instructions(branch_name, title))
        
        return result
    
    def _create_pr_auto(self, all_changes: List[Dict], summary: str) -> Dict[str, Any]:
        """Create PR automatically without approval"""
        branch_name = f"ai-feature/{self.session_id}"
        title = f"🤖 AI-Generated: {len(self.requirements)} features"
        
        files = [f"{req.get('feature', 'unknown').lower().replace(' ', '_')}.py" 
                for req in self.requirements]
        
        return self.pr_creator.create_pr_with_approval(
            branch_name=branch_name,
            title=title,
            description="Automated feature generation",
            files_changed=files,
            changes_summary=summary
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            'session_id': self.session_id,
            'requirements_loaded': len(self.requirements),
            'codebase_analyzed': bool(self.codebase_context),
            'plan': self.plan,
            'status': 'ready'
        }


def main():
    """CLI entry point"""
    import sys
    
    # Parse arguments
    requirements_file = "requirements/features.txt"
    interactive = True
    
    if len(sys.argv) > 1:
        if '--file' in sys.argv:
            idx = sys.argv.index('--file')
            if idx + 1 < len(sys.argv):
                requirements_file = sys.argv[idx + 1]
    
    if '--no-interactive' in sys.argv:
        interactive = False
    
    if '--help' in sys.argv:
        print("""
Intelligent AI Agent - QR Code Generator

Usage:
    python -m ai_agent.intelligent_agent [OPTIONS]

Options:
    --file PATH              Path to requirements file (default: requirements/features.txt)
    --no-interactive         Skip human approval steps
    --help                   Show this help message

Examples:
    # Use default requirements file with approval
    python -m ai_agent.intelligent_agent
    
    # Use custom requirements file
    python -m ai_agent.intelligent_agent --file requirements/my_features.xlsx
    
    # Automatic mode without approval
    python -m ai_agent.intelligent_agent --no-interactive

Requirements:
    - ANTHROPIC_API_KEY environment variable set
    - GITHUB_TOKEN environment variable set (for auto PR)
    - Git repository initialized
        """)
        return
    
    # Check environment
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY not set")
        print("   Get your API key from: https://console.anthropic.com/api_keys")
        print("   Then run: export ANTHROPIC_API_KEY='your-key'")
        sys.exit(1)
    
    # Run agent
    agent = IntelligentAgent(requirements_file=requirements_file)
    result = agent.run(interactive=interactive)
    
    # Print results
    if result['success']:
        print(f"\n✅ Success!")
        print(f"   Session: {result['session_id']}")
        print(f"   Requirements processed: {result['requirements_processed']}")
        print(f"   Changes generated: {result['changes_generated']}")
    else:
        print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
