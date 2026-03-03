#!/usr/bin/env python3
"""
Planner
Creates implementation plan from requirements
"""

from datetime import datetime


class Planner:
    def create_plan(self, requirements: list) -> dict:
        """
        Create implementation plan
        
        Args:
            requirements (list): List of requirements
            
        Returns:
            dict: Implementation plan with tasks and timeline
        """
        tasks = self._generate_tasks(requirements)
        timeline = self._create_timeline(tasks)
        
        return {
            'plan_id': f"PLAN-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'total_requirements': len(requirements),
            'total_tasks': len(tasks),
            'tasks': tasks,
            'timeline': timeline,
            'priority_order': self._prioritize_tasks(tasks)
        }
    
    def _generate_tasks(self, requirements: list) -> list:
        """Generate implementation tasks from requirements"""
        tasks = []
        for req in requirements:
            priority = req.get('priority', 'medium').lower()
            
            # Create subtasks based on priority
            subtasks = self._create_subtasks(req)
            
            tasks.append({
                'task_id': f"TASK-{req['id']}",
                'requirement_id': req['id'],
                'feature': req['feature'],
                'description': req['description'],
                'priority': priority,
                'subtasks': subtasks,
                'status': 'planned',
                'estimated_hours': len(subtasks) * 2
            })
        
        return tasks
    
    def _create_subtasks(self, requirement: dict) -> list:
        """Create subtasks for each requirement"""
        subtasks = [
            {'name': 'Design', 'status': 'pending'},
            {'name': 'Implement', 'status': 'pending'},
            {'name': 'Test', 'status': 'pending'},
            {'name': 'Document', 'status': 'pending'}
        ]
        return subtasks
    
    def _create_timeline(self, tasks: list) -> dict:
        """Create timeline for tasks"""
        high_priority = len([t for t in tasks if t['priority'] == 'high'])
        medium_priority = len([t for t in tasks if t['priority'] == 'medium'])
        low_priority = len([t for t in tasks if t['priority'] == 'low'])
        
        return {
            'phase_1_high_priority': high_priority,
            'phase_2_medium_priority': medium_priority,
            'phase_3_low_priority': low_priority,
            'total_estimated_hours': sum(t['estimated_hours'] for t in tasks),
            'estimated_completion_days': (sum(t['estimated_hours'] for t in tasks) + 7) // 8
        }
    
    def _prioritize_tasks(self, tasks: list) -> list:
        """Prioritize tasks by importance"""
        priority_map = {'high': 1, 'medium': 2, 'low': 3}
        return sorted(tasks, key=lambda t: priority_map.get(t['priority'], 2))
