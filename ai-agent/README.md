# AI Agent Setup Guide

The QR Code Generator now includes an **AI Agent** for automated code generation from requirements files. This guide explains how to set it up and use it.

## 📋 Components

The AI Agent consists of 5 integrated modules:

1. **requirements_reader.py** - Reads requirements from files (xlsx, txt, md, json)
2. **planner.py** - Creates implementation plans with prioritized tasks
3. **coder.py** - Generates Python code from plans
4. **pr_creator.py** - Creates GitHub pull requests with generated code
5. **agent.py** - Main orchestrator coordinating the entire workflow

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages for AI Agent:
- `openpyxl>=3.10.0` - Read Excel files
- `gitpython>=3.1.27` - Git operations
- `PyGithub>=1.55` - GitHub API (optional for PR creation)

### 2. Prepare Requirements File

Place your requirements in one of these formats in the `requirements/` folder:

**Option A: Text file** (`requirements/features.txt`)
```
Feature Name | Description | Priority (High/Medium/Low)
User Auth | Implement login system | High
Database | Add persistence layer | High
```

**Option B: Excel file** (`requirements/features.xlsx`)
Create columns: ID, Feature, Description, Priority

**Option C: Markdown** (`requirements/features.md`)
```markdown
# Requirements

## High Priority
- Feature 1: Description
- Feature 2: Description
```

**Option D: JSON** (`requirements/features.json`)
```json
{
  "requirements": [
    {"feature": "Feature 1", "description": "...", "priority": "High"}
  ]
}
```

### 3. Run the AI Agent

**Option A: Via CLI**
```bash
python -m ai_agent.agent
```

**Option B: Via FastAPI Endpoint**
```bash
curl -X POST http://localhost:8000/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirements_file": "requirements/features.txt",
    "auto_commit": false,
    "description": "AI Generated Features"
  }'
```

**Option C: Via Python**
```python
from ai_agent.agent import AIAgent

agent = AIAgent(requirements_file="requirements/features.txt")
result = agent.run(auto_commit=False)
print(result)
```

## 📊 Workflow

```
Requirements File
       ↓
[RequirementsReader] → Parse file (auto-detects format)
       ↓
[Planner] → Create implementation plan
       ↓
    - Prioritize requirements
    - Generate tasks (Design, Implement, Test, Document)
    - Estimate timeline
       ↓
[Coder] → Generate Python files
       ↓
    - Creates main implementation
    - Adds test files
    - Generates documentation
       ↓
[PRCreator] → Create GitHub PR (optional)
       ↓
    - Create feature branch
    - Commit changes
    - Push to repository
       ↓
Generated Code Output
```

## 📁 Folder Structure

```
qr-code-generator/
├── ai-agent/
│   ├── __init__.py
│   ├── agent.py           # Main orchestrator
│   ├── requirements_reader.py  # Reads requirements
│   ├── planner.py              # Creates plans
│   ├── coder.py                # Generates code
│   └── pr_creator.py           # Creates PRs
│
├── requirements/
│   ├── features.txt       # Sample requirements
│   └── create_sample_xlsx.py  # Generate sample Excel
│
├── generated/
│   └── [auto-generated code files]
│
└── main.py  # Updated with /ai/generate and /ai/status endpoints
```

## 🔌 API Endpoints

### Check AI Agent Status
```
GET /ai/status

Response:
{
  "available": true,
  "version": "1.0.0",
  "message": "AI Agent modules loaded"
}
```

### Generate Code from Requirements
```
POST /ai/generate

Request:
{
  "requirements_file": "requirements/features.txt",
  "auto_commit": false,
  "description": "AI Generated Feature Implementation"
}

Response:
{
  "success": true,
  "plan_id": "plan_20250212_153022",
  "total_tasks": 12,
  "files_generated": 4,
  "branch": "ai-feature/plan_20250212_153022",
  "message": "Code generation completed successfully"
}
```

## 📝 Example Usage

### Sample Input (requirements/features.txt)
```
User Authentication | JWT-based login system with refresh tokens | High
Database Integration | PostgreSQL with SQLAlchemy ORM | High
API Rate Limiting | Rate limiting per user and IP | Medium
Analytics Dashboard | Charts and statistics for QR usage | Medium
```

### Generated Output
```
generated/
├── authentication.py       # Login and JWT implementation
├── database.py             # Database models and queries
├── rate_limiting.py        # Rate limiting middleware
├── analytics.py            # Analytics logic
├── test_authentication.py   # Tests for auth
└── IMPLEMENTATION_PLAN.md   # Detailed plan
```

## ⚙️ Configuration

### Default Settings
- **Requirements file**: `requirements/features.txt`
- **Output folder**: `generated/`
- **Auto-commit**: `False` (manual review before commit)

### Environment Variables (Optional)
```bash
AI_AGENT_REQUIREMENTS_FILE=requirements/features.txt
AI_AGENT_OUTPUT_DIR=generated/
AI_AGENT_AUTO_COMMIT=false
GITHUB_TOKEN=your_token_here  # For PR creation
```

## 🧪 Testing

### Test with Sample Features
```bash
# Uses built-in features.txt
python -m ai_agent.agent
```

### Test with Custom File
```bash
# Update AI_AGENT_REQUIREMENTS_FILE environment variable
python -m ai_agent.agent
```

### Verify Generated Code
```bash
ls generated/
python -m pytest generated/test_*.py
```

## 🔒 Security Notes

- AI Agent has no built-in authentication
- Use environment variables for sensitive data (GitHub tokens)
- Generated code should be reviewed before committing
- Run in `/generated/` folder first for safe testing

## 🐛 Troubleshooting

### "openpyxl not installed"
```bash
pip install openpyxl>=3.10.0
```

### "AI Agent not available"
Check `/ai/status` endpoint and install missing dependencies

### "Git not found"
- Linux/Mac: `sudo apt-get install git` or `brew install git`
- Windows: Download from https://git-scm.com/download/win

### "Generated code has errors"
1. Review the generated files in `generated/` folder
2. Check the implementation plan (IMPLEMENTATION_PLAN.md)
3. Manually fix if needed before committing

## 📚 Advanced Usage

### Custom Requirements Format
Modify `requirements_reader.py` to add support for new formats:

```python
def _read_custom_format(self, filepath):
    """Add support for your custom format"""
    # Your parsing logic here
    pass
```

### Custom Code Templates
Modify `coder.py` templates to change generated code style:

```python
def _generate_file_content(self, task):
    """Customize the generated code template"""
    # Your template logic here
    pass
```

### GitHub PR Creation
The PR creator handles git operations. Customize in `pr_creator.py`:

```python
def create_pr(self, plan, code, requirements):
    """Customize PR workflow"""
    # Your custom logic here
    pass
```

## 📞 Support

For issues or questions:
1. Check the logs in `generated/log.txt`
2. Review individual module documentation
3. Test each component independently
4. Check `IMPLEMENTATION_PLAN.md` in generated folder

## ✅ Checklist

- [ ] Install AI Agent dependencies: `pip install -r requirements.txt`
- [ ] Place requirements file in `requirements/` folder
- [ ] Review generated code in `generated/` folder
- [ ] Test generated code with pytest
- [ ] Manually review before git commit
- [ ] Use `/ai/generate` endpoint or CLI to run

---

**AI Agent Version**: 1.0.0  
**Last Updated**: 2025-02-12  
**Status**: Production Ready
