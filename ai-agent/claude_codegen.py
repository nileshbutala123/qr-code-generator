#!/usr/bin/env python3
"""
Claude AI Integration
Integrates Claude API for intelligent code analysis and generation
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ClaudeCodeGen:
    def __init__(self, repo_path: str = "."):
        """
        Initialize Claude integration
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = Path(repo_path)
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = "claude-3-5-sonnet-20241022"
        
        if not self.api_key:
            print("⚠️  ANTHROPIC_API_KEY environment variable not set")
            print("   Get your key from: https://console.anthropic.com/")
            print("   Then run: export ANTHROPIC_API_KEY='your-key-here'")
    
    def generate_implementation(self, requirement: Dict[str, str], codebase_context: str) -> Dict[str, Any]:
        """
        Use Claude to generate implementation for a requirement
        
        Args:
            requirement: The requirement to implement
            codebase_context: Context about the existing codebase
            
        Returns:
            dict: Generated implementation plan and code
        """
        # If configured to use a mock backend, return a deterministic mock response
        backend = os.getenv('AGENT_LLM_BACKEND', '').lower()
        if backend == 'mock':
            feature = requirement.get('feature', 'Feature')
            # Simple mock analyses per known features (fallback to generic summary)
            mock_map = {
                'User Authentication': 'Mock: Add auth endpoints (login/register), JWT tokens, user model, tests.',
                'Database Integration': 'Mock: Add SQLAlchemy models, DB session, migrations, QR history endpoints.',
                'Analytics Dashboard': 'Mock: Add analytics endpoints, Chart.js frontend, daily stats.',
                'Email Notifications': 'Mock: Add SMTP/email sender, POST /email-qr endpoint, tests.'
            }
            analysis = mock_map.get(feature, f"Mock: Implementation plan for {feature} - create module and tests.")
            return {
                'success': True,
                'analysis': analysis,
                'requirement': requirement,
                'model': 'mock-backend',
                'usage': {'input_tokens': 0, 'output_tokens': 0}
            }

        # Default: use Anthropic Claude as before
        if not self.api_key:
            return {
                'success': False,
                'error': 'ANTHROPIC_API_KEY not configured'
            }

        try:
            import anthropic
        except ImportError:
            return {
                'success': False,
                'error': 'anthropic package not installed. Install with: pip install anthropic'
            }

        client = anthropic.Anthropic(api_key=self.api_key)
        prompt = self._create_prompt(requirement, codebase_context)
        print(f"🤖 Claude analyzing: {requirement.get('feature', 'Unknown')}")
        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = message.content[0].text
            return {
                'success': True,
                'analysis': response_text,
                'requirement': requirement,
                'model': self.model,
                'usage': {
                    'input_tokens': message.usage.input_tokens,
                    'output_tokens': message.usage.output_tokens
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'requirement': requirement}
    
    def review_code_change(self, current_code: str, proposed_change: str, context: str) -> Dict[str, Any]:
        """
        Use Claude to review a proposed code change
        
        Args:
            current_code: The existing code
            proposed_change: The proposed change
            context: Context about the change
            
        Returns:
            dict: Review results with risks and suggestions
        """
        if not self.api_key:
            return {'success': False, 'error': 'API key not configured'}
        
        try:
            import anthropic
        except ImportError:
            return {'success': False, 'error': 'anthropic not installed'}
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        prompt = f"""Review this code change for a FastAPI QR Code Generator.

Context: {context}

Current Code:
```python
{current_code}
```

Proposed Change:
```python
{proposed_change}
```

Please analyze:
1. Does the change follow the existing code patterns?
2. Are there any potential bugs or issues?
3. Does it maintain backward compatibility?
4. Any security concerns?
5. Would it pass the existing test suite?

Return as JSON with keys: risks, suggestions, compat_score (0-100), security_concerns"""
        
        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response = message.content[0].text
            
            # Try to parse JSON response
            try:
                review_data = json.loads(response)
            except:
                review_data = {'raw_review': response}
            
            return {
                'success': True,
                'review': review_data,
                'usage': {
                    'input_tokens': message.usage.input_tokens,
                    'output_tokens': message.usage.output_tokens
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_tests(self, feature_code: str, feature_name: str) -> Dict[str, Any]:
        """
        Generate unit tests for a feature
        
        Args:
            feature_code: The feature implementation code
            feature_name: Name of the feature
            
        Returns:
            dict: Generated test code
        """
        if not self.api_key:
            return {'success': False, 'error': 'API key not configured'}
        
        try:
            import anthropic
        except ImportError:
            return {'success': False, 'error': 'anthropic not installed'}
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        prompt = f"""Generate pytest unit tests for this FastAPI feature.

Feature Name: {feature_name}

Feature Code:
```python
{feature_code}
```

Generate comprehensive tests covering:
1. Happy path
2. Edge cases
3. Error handling
4. Input validation

Return only valid Python pytest code starting with imports."""
        
        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            test_code = message.content[0].text
            
            return {
                'success': True,
                'test_code': test_code,
                'usage': {
                    'input_tokens': message.usage.input_tokens,
                    'output_tokens': message.usage.output_tokens
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_prompt(self, requirement: Dict[str, str], codebase_context: str) -> str:
        """Create a detailed prompt for Claude"""
        
        return f"""You are an expert Python/FastAPI developer analyzing requirements for a production API.

# Requirement
**Feature**: {requirement.get('feature', 'Unknown')}
**Description**: {requirement.get('description', 'No description')}
**Priority**: {requirement.get('priority', 'medium')}

# Existing Codebase Context
{codebase_context}

# Task
Analyze this requirement and provide:

1. **Implementation Strategy**
   - What endpoints need to be added/modified?
   - What database/storage changes needed?
   - What dependencies might be required?

2. **Proposed Changes**
   - List specific files that need changes
   - For each file, show the exact code changes (use code diffs)
   - Include any new files needed

3. **Modified Main.py Endpoints**
   ```
   Show exact @app.get(), @app.post() decorators with paths
   Include complete function signatures
   ```

4. **New Dependencies**
   - Any new packages to add to requirements.txt?

5. **Testing Strategy**
   - What test cases should be added?
   - Any new pytest fixtures needed?

6. **Migration Steps** (if any)
   - How to migrate existing data if needed?

7. **Risks & Considerations**
   - Any backwards compatibility concerns?
   - Performance implications?
   - Security considerations?

Format your response as a structured JSON or clear sections for parsing."""
