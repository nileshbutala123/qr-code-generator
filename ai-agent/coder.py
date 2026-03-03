#!/usr/bin/env python3
"""
Coder
Generates code based on plan and requirements
"""

from pathlib import Path
from datetime import datetime


class Coder:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
    
    def generate(self, plan: dict, requirements: list) -> dict:
        """
        Generate code files
        
        Args:
            plan (dict): Implementation plan
            requirements (list): List of requirements
            
        Returns:
            dict: Generated code files
        """
        generated_files = []
        
        # Create generated folder
        generated_folder = self.repo_path / "generated"
        generated_folder.mkdir(exist_ok=True)
        
        # Generate implementation files
        for task in plan['tasks']:
            file_content = self._generate_file_content(task, requirements)
            file_path = self._get_file_path(task)
            
            # Save file
            self._save_file(file_path, file_content)
            
            generated_files.append({
                'path': str(file_path.relative_to(self.repo_path)),
                'task_id': task['task_id'],
                'status': 'generated',
                'lines_of_code': len(file_content.split('\n'))
            })
        
        return {
            'generation_id': f"GEN-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'files': generated_files,
            'total_files': len(generated_files),
            'total_lines_of_code': sum(f['lines_of_code'] for f in generated_files)
        }
    
    def _generate_file_content(self, task: dict, requirements: list) -> str:
        """Generate file content based on task"""
        feature_name = task['feature'].replace(' ', '_').lower()
        template = f"""#!/usr/bin/env python3
\"\"\"
{task['feature']}

{task['description']}

Task ID: {task['task_id']}
Priority: {task['priority'].upper()}
Created: {datetime.now().isoformat()}
\"\"\"


def implement_{feature_name}():
    \"\"\"
    Implement: {task['feature']}
    
    Description:
        {task['description']}
    
    Requirements:
        {chr(10).join([f'- {{req["feature"]}}' for req in requirements[:3]])}
    
    Returns:
        dict: Implementation result
    \"\"\"
    return {{
        'status': 'pending',
        'feature': '{task['feature']}',
        'task_id': '{task['task_id']}'
    }}


if __name__ == "__main__":
    result = implement_{feature_name}()
    print(f"✅ Implemented: {{result['feature']}}")
"""
        return template
    
    def _get_file_path(self, task: dict) -> Path:
        """Get file path for task"""
        task_id = task['task_id'].lower().replace('-', '_')
        file_name = f"{task_id}.py"
        return self.repo_path / "generated" / file_name
    
    def _save_file(self, file_path: Path, content: str) -> None:
        """Save file to disk"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"  ✓ Generated: {file_path.relative_to(self.repo_path)}")
