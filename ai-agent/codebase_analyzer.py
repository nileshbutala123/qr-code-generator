#!/usr/bin/env python3
"""
Codebase Analyzer
Analyzes the existing FastAPI QR code repository structure and code
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any


class CodebaseAnalyzer:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.structure = {}
        self.key_files = {}
        self.endpoints = []
        self.models = []
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the FastAPI repository structure
        
        Returns:
            dict: Analysis of codebase including endpoints, models, dependencies
        """
        print("🔍 Analyzing FastAPI QR Code repository...")
        
        self._scan_directory_structure()
        self._extract_fastapi_endpoints()
        self._extract_models()
        self._analyze_dependencies()
        
        return {
            'structure': self.structure,
            'endpoints': self.endpoints,
            'models': self.models,
            'key_files': self.key_files,
            'dependencies': self._get_dependencies(),
            'summary': self._create_summary()
        }
    
    def _scan_directory_structure(self) -> None:
        """Scan directory structure"""
        for root, dirs, files in os.walk(self.repo_path):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'venv', '.env', 'QR code']]
            
            level = root.replace(str(self.repo_path), '').count(os.sep)
            indent = ' ' * 2 * level
            rel_path = os.path.relpath(root, self.repo_path)
            
            self.structure[rel_path] = []
            
            for file in files:
                if not file.startswith('.'):
                    file_path = os.path.join(rel_path, file)
                    self.structure[rel_path].append(file)
                    
                    # Track key files
                    if file in ['main.py', 'qr_code_generator.py', 'requirements.txt', '.github/workflows/deploy.yml']:
                        self.key_files[file] = file_path
    
    def _extract_fastapi_endpoints(self) -> None:
        """Extract FastAPI endpoints from main.py"""
        main_file = self.repo_path / 'main.py'
        
        if not main_file.exists():
            return
        
        try:
            with open(main_file, 'r') as f:
                content = f.read()
                
            # Find endpoints
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '@app.' in line:
                    method = line.split('@app.')[1].split('(')[0]
                    # Get the next line to see function name
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if 'async def' in next_line or 'def' in next_line:
                            func_name = next_line.split('def ')[-1].split('(')[0]
                            # Try to extract path
                            if '"' in line or "'" in line:
                                path = line.split("'")[1] if "'" in line else line.split('"')[1]
                                self.endpoints.append({
                                    'method': method.upper(),
                                    'path': path,
                                    'function': func_name
                                })
        except Exception as e:
            print(f"⚠️  Error analyzing endpoints: {e}")
    
    def _extract_models(self) -> None:
        """Extract Pydantic models from main.py"""
        main_file = self.repo_path / 'main.py'
        
        if not main_file.exists():
            return
        
        try:
            with open(main_file, 'r') as f:
                content = f.read()
            
            # Find Pydantic models
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('class ') and 'BaseModel' in line:
                    model_name = line.split('class ')[1].split('(')[0]
                    self.models.append(model_name)
        except Exception as e:
            print(f"⚠️  Error analyzing models: {e}")
    
    def _analyze_dependencies(self) -> None:
        """Analyze project dependencies"""
        pass
    
    def _get_dependencies(self) -> List[str]:
        """Get project dependencies from requirements.txt"""
        try:
            with open(self.repo_path / 'requirements.txt', 'r') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            return deps
        except:
            return []
    
    def _create_summary(self) -> str:
        """Create human-readable summary of codebase"""
        summary = f"""
        FastAPI QR Code Generator Repository Analysis
        ===============================================
        
        Total Endpoints: {len(self.endpoints)}
        - {', '.join([f"{e['method']} {e['path']}" for e in self.endpoints[:5]])}
        
        Pydantic Models: {', '.join(self.models[:5])}
        
        Key Files:
        - main.py (FastAPI application)
        - qr_code_generator.py (Core logic)
        - requirements.txt (Dependencies)
        
        Tech Stack:
        - FastAPI
        - Uvicorn
        - Qrcode library
        - Pydantic
        
        The codebase generates QR codes via REST API with cleanup, 
        retrieval, and metadata endpoints.
        """
        return summary.strip()
    
    def get_file_content(self, file_path: str) -> str:
        """Get content of a specific file"""
        full_path = self.repo_path / file_path
        try:
            with open(full_path, 'r') as f:
                return f.read()
        except:
            return ""
    
    def get_context_for_claude(self) -> str:
        """Get formatted context for Claude API calls"""
        context = f"""
# FastAPI QR Code Generator Repository Context

## Project Overview
This is a production FastAPI application that generates QR codes and manages them.

## Endpoints ({len(self.endpoints)} total)
```
{json.dumps(self.endpoints, indent=2)}
```

## Pydantic Models
- {', '.join(self.models)}

## File Structure
```
{json.dumps(self.structure, indent=2)}
```

## Key Files Content

### main.py (FastAPI Application)
```python
{self._get_file_snippet('main.py', 50)}
```

### qr_code_generator.py (Core Logic)
```python
{self._get_file_snippet('qr_code_generator.py', 50)}
```

## Dependencies
- {', '.join(self._get_dependencies())}

## Important Notes
- The API uses CORS middleware with allow_origins=["*"]
- QR codes are stored in "QR code/" folder with metadata
- All endpoints return JSON responses
- Error handling uses HTTPException from FastAPI
"""
        return context.strip()
    
    def _get_file_snippet(self, filename: str, lines: int = 50) -> str:
        """Get first N lines of a file"""
        file_path = self.repo_path / filename
        try:
            with open(file_path, 'r') as f:
                content = f.readlines()[:lines]
            return ''.join(content)
        except:
            return f"# {filename} not found"
