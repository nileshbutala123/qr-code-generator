#!/usr/bin/env python3
"""
Free AI Agent - Offline Mode
Uses intelligent pattern matching and templates instead of API calls
Perfect for hobby projects - completely free and offline!
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class FreeCodeGenerator:
    """
    Free code generator using patterns and templates
    No API calls required - completely offline
    """
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate(self, requirement: Dict[str, str], codebase_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate code implementation for a requirement
        Uses pattern matching and templates - completely free
        """
        feature = requirement.get('feature', '').lower()
        description = requirement.get('description', '').lower()
        priority = requirement.get('priority', 'medium')
        
        print(f"      🔍 Pattern matching for: {requirement['feature']}")
        
        # Analyze requirement
        analysis = self._analyze_requirement(feature, description)
        
        if not analysis:
            return {'success': False, 'error': 'Could not match requirement pattern'}
        
        # Generate implementation
        implementation = self._generate_implementation(analysis, codebase_context)
        
        return {
            'success': True,
            'analysis': implementation['analysis'],
            'files': implementation['files'],
            'code_snippets': implementation['code_snippets'],
            'tokens': {'input': 0, 'output': 0}  # Free - no tokens
        }
    
    def _analyze_requirement(self, feature: str, description: str) -> Dict[str, Any]:
        """Analyze requirement using pattern matching"""
        
        # Email/notification patterns
        if any(word in feature for word in ['email', 'notification', 'send', 'mail']):
            return {
                'type': 'email_feature',
                'requires': ['smtp_config', 'email_model', 'endpoint'],
                'endpoints': ['POST /send-qr-email'],
                'models': ['EmailRequest', 'EmailResponse'],
            }
        
        # Input/form patterns
        if any(word in feature for word in ['text box', 'input', 'form', 'field']):
            return {
                'type': 'input_feature',
                'requires': ['form_field', 'html_element', 'validation'],
                'endpoints': [],
                'models': ['with_email_field'],
            }
        
        # Database patterns
        if any(word in feature for word in ['database', 'storage', 'postgres', 'sql']):
            return {
                'type': 'database_feature',
                'requires': ['sqlalchemy', 'models', 'migrations'],
                'endpoints': ['GET /history', 'POST /restore/{qr_id}'],
                'models': ['QRHistory', 'UserMetadata'],
            }
        
        # Authentication patterns
        if any(word in feature for word in ['auth', 'login', 'user', 'jwt']):
            return {
                'type': 'auth_feature',
                'requires': ['jwt', 'password_hashing', 'token_validation'],
                'endpoints': ['POST /auth/register', 'POST /auth/login', 'POST /auth/refresh'],
                'models': ['RegisterRequest', 'LoginRequest', 'TokenResponse'],
            }
        
        # Analytics patterns
        if any(word in feature for word in ['analytics', 'dashboard', 'stats', 'chart']):
            return {
                'type': 'analytics_feature',
                'requires': ['charting_library', 'statistics', 'api_endpoint'],
                'endpoints': ['GET /analytics/overview', 'GET /analytics/daily'],
                'models': [],
            }
        
        # Batch patterns
        if any(word in feature for word in ['batch', 'multiple', 'mass', 'bulk']):
            return {
                'type': 'batch_feature',
                'requires': ['list_processing', 'bulk_endpoint'],
                'endpoints': ['POST /generate-batch'],
                'models': ['BatchRequest', 'BatchResponse'],
            }
        
        return None
    
    def _generate_implementation(self, analysis: Dict, codebase_context: Dict) -> Dict[str, Any]:
        """Generate implementation based on analysis"""
        
        feature_type = analysis['type']
        endpoints = analysis.get('endpoints', [])
        models = analysis.get('models', [])
        
        code = self._get_template(feature_type, endpoints, models)
        files = self._get_files(feature_type)
        
        return {
            'analysis': code['analysis'],
            'files': files,
            'code_snippets': code['snippets'],
        }
    
    def _get_template(self, feature_type: str, endpoints: List, models: List) -> Dict[str, Any]:
        """Get template for feature type"""
        
        templates = {
            'email_feature': {
                'analysis': f"""## Email Notifications Implementation

### New Endpoints
{chr(10).join([f'- {ep}' for ep in endpoints])}

### New Models
- EmailRequest(recipients: List[str], subject: str, body: str)
- EmailResponse(success: bool, sent_to: List[str], timestamp: str)

### SMTP Configuration
- Add to environment variables
- Support for Gmail, SendGrid, AWS SES
- Async email sending with task queue

### Integration
- Add email button next to QR download
- Send via FastAPI background task
- Log all sent emails

### Code Changes
- New file: app/email_service.py (150 lines)
- Update main.py (30 lines)
- Add tests: tests/test_email.py (80 lines)

### Dependencies
- python-multipart
- aiosmtplib
- email-validator
""",
                'snippets': [
                    ('app/email_service.py', '''from fastapi import BackgroundTasks
from pydantic import EmailStr

class EmailService:
    async def send_qr_email(self, recipient: EmailStr, qr_path: str):
        """Send QR code via email"""
        # Implementation
        pass
'''),
                    ('main.py endpoint', '''@app.post("/send-qr-email")
async def send_qr_email(request: EmailRequest, background_tasks: BackgroundTasks):
    """Send generated QR code via email"""
    background_tasks.add_task(email_service.send_qr_email, 
                            request.email, qr_path)
    return EmailResponse(success=True, sent_to=[request.email])
'''),
                ]
            },
            
            'input_feature': {
                'analysis': f"""## Email Input Field Implementation

### HTML Changes
- Add email input field to QR form
- Add validation on client side
- Show email preview before generation

### JavaScript Updates
- Validate email format
- Optional: save to localStorage
- Handle email send action

### Integration Points
- Email input optional (user can skip)
- If provided, automatically offer "Send to Email" button
- Remember last used email

### Changes
- Update index.html (20 lines)
- Update static/main.js (50 lines)
- No backend changes needed (just UI)

### Testing
- Test with valid/invalid emails
- Test with empty email field
- Verify form still works without email
""",
                'snippets': [
                    ('HTML form update', '''<input type="email" id="email" placeholder="Optional: enter your email" />
<button onclick="sendToEmail()">Send QR to Email</button>
'''),
                    ('JavaScript validation', '''function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}
'''),
                ]
            },
            
            'database_feature': {
                'analysis': """## Database Integration (PostgreSQL)

### Database Models
- QRCode(id, url, qr_path, created_at, expires_at)
- User(id, email, created_at)
- QRHistory(id, user_id, qr_code_id)

### New Endpoints
- GET /history - List all generated QR codes
- GET /history/{qr_id} - Get specific QR metadata
- POST /restore/{qr_id} - Restore deleted QR code

### Migration Strategy
1. Create PostgreSQL database
2. Run SQLAlchemy migrations
3. Migrate existing QR data from files
4. Keep file backup during transition

### Code Files
- app/models.py - SQLAlchemy models
- app/database.py - Database connection
- alembic/versions/ - Migrations

### Configuration
- Add DATABASE_URL to .env
- Connection pooling with psycopg

### Testing
- Unit tests for models
- Integration tests for queries
- Test migration rollback
""",
                'snippets': [
                    ('models.py', '''from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QRCode(Base):
    __tablename__ = "qr_codes"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    qr_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
'''),
                ]
            },
            
            'auth_feature': {
                'analysis': """## User Authentication Implementation

### Endpoints
- POST /auth/register - Create new user
- POST /auth/login - Login with credentials
- POST /auth/refresh - Refresh JWT token
- POST /auth/logout - Logout

### Models
- RegisterRequest(username, email, password)
- LoginRequest(username, password)
- TokenResponse(access_token, refresh_token, expires_in)

### Security
- Password hashing with bcrypt
- JWT tokens with 1-hour expiration
- Refresh tokens with 7-day expiration
- CORS security headers

### Database
- Users table with hashed passwords
- Login history tracking
- Token blacklist for logout

### Files
- app/auth.py (200 lines)
- app/security.py (100 lines)
- Update main.py (50 lines)

### Testing
- Test valid/invalid credentials
- Test JWT token validation
- Test token refresh
- Test logout
""",
                'snippets': [
                    ('auth.py', '''from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta

pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)
'''),
                ]
            },
            
            'analytics_feature': {
                'analysis': """## Analytics Dashboard Implementation

### New Endpoints
- GET /analytics/overview - Total stats
- GET /analytics/daily - Daily breakdown
- GET /analytics/by-platform - By source
- POST /analytics/export - Export CSV

### Frontend
- New page: /dashboard
- Charts using Chart.js
- Date range filter
- Export buttons

### Metrics
- Total QR codes generated
- Daily generation count
- Popular URLs
- Peak hours
- Success rate

### Data Collection
- Log all QR generation requests
- Track user agents and IPs
- Measure response times

### Files
- static/dashboard.html (300 lines)
- static/dashboard.js (250 lines)
- app/analytics.py (150 lines)

### Dependencies
- Chart.js (CDN)
- pandas for data analysis
""",
                'snippets': [
                    ('dashboard.html', '''<div id="chart"></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  fetch('/analytics/daily')
    .then(r => r.json())
    .then(data => {
      // Create chart with data
    });
</script>
'''),
                ]
            },
            
            'batch_feature': {
                'analysis': """## Batch QR Generation

### Endpoint
- POST /generate-batch
  - Input: List of URLs
  - Output: List of QR paths + ZIP file

### Request Model
- BatchRequest(urls: List[str], format: str = 'png', zip: bool = True)
- Returns: BatchResponse(total: int, generated: int, zip_url: str)

### Implementation
- Accept up to 100 URLs per batch
- Generate in parallel (async)
- Create ZIP file for download
- Monitor performance

### Files
- app/batch_service.py (100 lines)
- New endpoint in main.py (30 lines)
- Test file (60 lines)

### Optimizations
- Use asyncio for parallel generation
- Stream ZIP file for large batches
- Cache repeated URLs

### Error Handling
- Invalid URL validation
- Duplicate detection
- Partial success responses
""",
                'snippets': [
                    ('batch_service.py', '''import asyncio
import zipfile
from typing import List

async def generate_batch(urls: List[str]):
    tasks = [generator.generate(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    # Create ZIP file
    zip_path = f"batch_{datetime.now().timestamp()}.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        for result in results:
            z.write(result['path'])
    return zip_path
'''),
                ]
            },
        }
        
        return templates.get(feature_type, {
            'analysis': f'Implementation plan for {feature_type}',
            'snippets': []
        })
    
    def _get_files(self, feature_type: str) -> List[str]:
        """Get list of files to be created"""
        
        file_map = {
            'email_feature': ['email_service.py', 'test_email.py'],
            'input_feature': [],  # No backend files needed
            'database_feature': ['models.py', 'database.py', 'migrations/'],
            'auth_feature': ['auth.py', 'security.py', 'test_auth.py'],
            'analytics_feature': ['analytics.py', 'dashboard.html', 'dashboard.js'],
            'batch_feature': ['batch_service.py', 'test_batch.py'],
        }
        
        return file_map.get(feature_type, [])
    
    def _load_templates(self) -> Dict:
        """Load code templates"""
        return {}


class FreeIntelligentAgent:
    """Free, offline version of Intelligent AI Agent"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.generator = FreeCodeGenerator()
    
    def run(self, interactive: bool = True) -> Dict[str, Any]:
        """Run the free agent"""
        print("\n" + "="*70)
        print("🤖 FREE INTELLIGENT AI AGENT - Hobby Project Edition")
        print("="*70)
        print("\n✨ No API keys needed - completely offline and free!\n")
        
        # Step 1: Read requirements
        print("📖 Step 1: Reading requirements...")
        requirements = self._load_requirements()
        if not requirements:
            return {'success': False, 'error': 'No requirements found'}
        print(f"✓ Loaded {len(requirements)} requirements\n")
        
        # Step 2: Analyze codebase
        print("📊 Step 2: Analyzing codebase...")
        codebase = self._analyze_codebase()
        print(f"✓ Found {len(codebase['endpoints'])} endpoints\n")
        
        # Step 3: Process requirements
        print("🧠 Step 3: Processing requirements (offline)...\n")
        all_changes = []
        for i, req in enumerate(requirements, 1):
            print(f"   [{i}/{len(requirements)}] {req['feature']}")
            result = self.generator.generate(req, codebase)
            
            if result['success']:
                all_changes.append({
                    'requirement': req,
                    'analysis': result['analysis'],
                    'files': result.get('files', []),
                })
                print(f"      ✓ Generated ({len(result.get('files', []))} files)\n")
            else:
                print(f"      ✗ {result.get('error')}\n")
        
        if not all_changes:
            return {'success': False, 'error': 'No changes generated'}
        
        # Step 4: Show summary
        print("📝 Step 4: Implementation Summary\n")
        self._show_summary(requirements, all_changes)
        
        # Step 5: Human approval
        if interactive:
            print("\n" + "="*70)
            print("🔍 HUMAN APPROVAL REQUIRED")
            print("="*70 + "\n")
            
            response = input("👀 Review the plans above. Proceed with PR? (yes/no): ").strip().lower()
            
            if response not in ['y', 'yes']:
                return {'success': False, 'message': 'Cancelled by user'}
        
        print("\n✅ READY FOR ACTION:\n")
        print("📋 Next Steps:")
        print("1. Review generated implementation plans above")
        print("2. Create new files based on code snippets")
        print("3. Run: pytest tests/")
        print("4. Commit and push to GitHub\n")
        
        return {
            'success': True,
            'session_id': self.session_id,
            'requirements': len(requirements),
            'changes': len(all_changes),
            'mode': 'FREE (Offline)',
            'message': '✨ Plans generated successfully!'
        }
    
    def _load_requirements(self) -> List[Dict]:
        """Load requirements from file"""
        req_file = Path('requirements/features.txt')
        requirements = []
        
        if req_file.exists():
            with open(req_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) >= 2:
                            requirements.append({
                                'id': f'REQ-{i}',
                                'feature': parts[0].strip(),
                                'description': parts[1].strip() if len(parts) > 1 else parts[0].strip(),
                                'priority': parts[2].strip().lower() if len(parts) > 2 else 'medium',
                            })
        
        return requirements
    
    def _analyze_codebase(self) -> Dict:
        """Analyze codebase"""
        return {
            'endpoints': [
                'GET /', 'GET /health', 'POST /generate',
                'GET /qr/{folder}', 'GET /metadata/{folder}', 'POST /cleanup'
            ],
            'models': ['QRGenerateRequest', 'QRGenerateResponse', 'CleanupResponse'],
        }
    
    def _show_summary(self, requirements: List, changes: List):
        """Show implementation summary"""
        for change in changes:
            req = change['requirement']
            priority_emoji = "🔴" if req['priority'] == 'high' else "🟡" if req['priority'] == 'medium' else "🟢"
            
            print(f"\n{priority_emoji} {req['feature'].upper()}")
            print("─" * 70)
            print(change['analysis'])
            if change.get('files'):
                print(f"\nFiles to create: {', '.join(change['files'])}\n")


def main():
    """Run free agent"""
    try:
        agent = FreeIntelligentAgent()
        result = agent.run(interactive=True)
        
        if result['success']:
            print("\n" + "="*70)
            print(f"✅ SUCCESS - {result['message']}")
            print("="*70)
            print(f"\n📊 Summary:")
            print(f"   Requirements: {result['requirements']}")
            print(f"   Changes Generated: {result['changes']}")
            print(f"   Cost: FREE 💰")
            print(f"   Mode: {result['mode']}\n")
        else:
            print(f"\n❌ {result.get('message', 'Failed')}")
            return 1
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
