#!/usr/bin/env python3
"""
Requirements Reader
Reads requirements from Excel, TXT, or MD files
"""

import json
from pathlib import Path


class RequirementsReader:
    def read(self, file_path: str) -> list:
        """
        Read requirements from different formats
        
        Args:
            file_path (str): Path to requirements file
            
        Returns:
            list: List of requirements
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.xlsx':
            return self._read_excel(file_path)
        elif file_ext == '.txt':
            return self._read_text(file_path)
        elif file_ext == '.md':
            return self._read_markdown(file_path)
        elif file_ext == '.json':
            return self._read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def _read_excel(self, file_path: str) -> list:
        """Read from Excel file"""
        try:
            import openpyxl
        except ImportError:
            print("⚠️  openpyxl not installed. Install with: pip install openpyxl")
            return self._read_text(file_path)
        
        requirements = []
        try:
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
            
            for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
                if row[0]:  # If first column is not empty
                    requirements.append({
                        'id': row[0],
                        'feature': row[1] if len(row) > 1 else 'Feature',
                        'description': row[2] if len(row) > 2 else row[1],
                        'priority': row[3].lower() if len(row) > 3 and row[3] else 'medium',
                        'status': 'pending'
                    })
        except Exception as e:
            print(f"⚠️  Error reading Excel: {str(e)}")
        
        return requirements
    
    def _read_text(self, file_path: str) -> list:
        """Read from text file"""
        requirements = []
        try:
            with open(file_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(':')
                        requirements.append({
                            'id': f'REQ-{i}',
                            'feature': parts[0].strip(),
                            'description': parts[1].strip() if len(parts) > 1 else parts[0].strip(),
                            'priority': 'medium',
                            'status': 'pending'
                        })
        except Exception as e:
            print(f"⚠️  Error reading text file: {str(e)}")
        
        return requirements
    
    def _read_markdown(self, file_path: str) -> list:
        """Read from markdown file"""
        requirements = []
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line.startswith('- '):
                        requirements.append({
                            'id': f'REQ-{i}',
                            'feature': line.replace('- ', '').strip(),
                            'description': line.replace('- ', '').strip(),
                            'priority': 'medium',
                            'status': 'pending'
                        })
        except Exception as e:
            print(f"⚠️  Error reading markdown file: {str(e)}")
        
        return requirements
    
    def _read_json(self, file_path: str) -> list:
        """Read from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading JSON file: {str(e)}")
            return []
