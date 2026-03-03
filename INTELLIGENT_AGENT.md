# Intelligent AI Agent - Complete Documentation

## 🤖 Overview

The **Intelligent AI Agent** is a powerful system for automated feature development that:

1. **Reads requirements** from Excel, text, markdown, or JSON files
2. **Understands your codebase** by analyzing FastAPI endpoints, models, and structure
3. **Uses Claude AI** to generate intelligent, scoped code changes
4. **Makes targeted changes** to your repository
5. **Commits to git** in a new feature branch
6. **Creates GitHub Pull Requests** for human review
7. **Keeps humans in the loop** with approval workflows

## 📋 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This adds:
- `anthropic>=0.25.0` - Claude API client
- `openpyxl>=3.10.0` - Excel file reading
- `gitpython>=3.1.27` - Git operations
- `PyGithub>=1.55` - GitHub API

### 2. Set Environment Variables

**Claude API (required):**
```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxx"
```
Get your key: https://console.anthropic.com/api_keys

**GitHub Token (optional - for auto PR):**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
```
Create token: https://github.com/settings/tokens
- Scopes: `repo` (full), `workflow`

### 3. Verify Installation

```bash
python -m ai_agent.intelligent_agent --help
```

## 🚀 Quick Start

### Basic Usage

```bash
# Run with default requirements file (requirements/features.txt)
python -m ai_agent.intelligent_agent

# Use custom requirements file
python -m ai_agent.intelligent_agent --file requirements/my_features.xlsx

# Run in automatic mode (skip approvals)
python -m ai_agent.intelligent_agent --no-interactive
```

### Python API

```python
from ai_agent.intelligent_agent import IntelligentAgent

# Create agent
agent = IntelligentAgent(
    requirements_file="requirements/features.txt",
    repo_path="."
)

# Run workflow
result = agent.run(interactive=True)

print(f"✅ {result['requirements_processed']} requirements processed")
print(f"📁 {result['changes_generated']} changes generated")
print(f"🔗 PR: {result['pr_result']['pr_url']}")
```

## 📊 Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. READ REQUIREMENTS                                   │
│  Excel/TXT/MD/JSON file → Parse into structured data    │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  2. ANALYZE CODEBASE                                    │
│  Scan FastAPI endpoints, models, dependencies            │
│  Get context for Claude about your architecture         │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  3. PROCESS WITH CLAUDE                                 │
│  For each requirement:                                   │
│  - Send requirement + codebase context to Claude AI     │
│  - Get implementation strategy                           │
│  - Receive proposed code changes                         │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  4. HUMAN APPROVAL                                      │
│  Show summary of all changes to developer               │
│  Ask: "Proceed with creating PR?" (yes/no)            │
└──────────────────┬──────────────────────────────────────┘
                   ↓ (if approved)
┌─────────────────────────────────────────────────────────┐
│  5. GIT & GITHUB                                        │
│  - Create feature branch: ai-feature/YYYYMMDD_HHMMSS    │
│  - Commit changes with AI-generated summary             │
│  - Push to origin                                        │
│  - Create GitHub PR with detailed description           │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  6. READY FOR REVIEW                                    │
│  - PR is on GitHub waiting for human review             │
│  - Code is on feature branch for testing                │
│  - Ready to merge after approval                        │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

### AI Agent Modules

```
ai-agent/
├── __init__.py                  # Module exports
├── intelligent_agent.py         # ⭐ Main orchestrator (350+ lines)
├── codebase_analyzer.py         # ⭐ Analyzes your FastAPI repo (200+ lines)
├── claude_codegen.py            # ⭐ Claude AI integration (250+ lines)
├── enhanced_pr_creator.py       # ⭐ Git & GitHub workflow (350+ lines)
├── requirements_reader.py       # Reads requirements files
├── planner.py                   # Task planning
├── coder.py                     # Template code generation
├── pr_creator.py                # Basic PR creation
└── README.md                    # Documentation
```

### New Intelligent Agent Modules (★ = NEW)

| File | Purpose | Features |
|------|---------|----------|
| **intelligent_agent.py** ⭐ | Main orchestrator | Coordinates entire workflow, human approval loops |
| **codebase_analyzer.py** ⭐ | Scans your repo | Extracts endpoints, models, structure for Claude |
| **claude_codegen.py** ⭐ | Claude API calls | Generates implementations, reviews code, creates tests |
| **enhanced_pr_creator.py** ⭐ | Git + GitHub | Git workflow, human approval, PR creation |

## 🧠 How Claude Understands Your Code

The `CodebaseAnalyzer` extracts:

```python
# 1. Endpoints
GET /health
POST /generate
GET /qr/{folder}
GET /metadata/{folder}
POST /cleanup

# 2. Pydantic Models
QRGenerateRequest
QRGenerateResponse
CleanupResponse
(+ AI Agent models)

# 3. File Structure
main.py (FastAPI app)
qr_code_generator.py (Core logic)
requirements.txt (Dependencies)
.github/workflows/ (CI/CD)

# 4. Dependencies Analysis
- FastAPI (REST framework)
- Uvicorn (Server)
- Qrcode (QR generation)
- Pydantic (Validation)
```

Claude uses this context to generate code that:
- ✅ Follows existing patterns
- ✅ Respects code style
- ✅ Integrates with current architecture
- ✅ Maintains backward compatibility
- ✅ Includes proper error handling

## 📝 Requirements Format

### Excel (.xlsx)

Columns: `ID | Feature | Description | Priority`

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| 1 | User Auth | JWT login system | High |
| 2 | Database | Store QR history | High |
| 3 | Analytics | Usage dashboard | Medium |

### Text (.txt)

```
User Authentication | Implement JWT-based login with refresh tokens | High
Database Integration | PostgreSQL with SQLAlchemy for QR storage | High
Analytics Dashboard | Display usage charts and statistics | Medium
```

### Markdown (.md)

```markdown
# Features

## High Priority
- User Authentication: JWT-based login system
- Database Integration: PostgreSQL ORM layer

## Medium Priority
- Analytics Dashboard: Charts and statistics
```

### JSON (.json)

```json
{
  "requirements": [
    {
      "feature": "User Authentication",
      "description": "JWT-based login",
      "priority": "High"
    }
  ]
}
```

## 👨‍💻 Human-in-the-Loop Workflow

### Step 1: Show Summary

```
==================================================
🔍 HUMAN APPROVAL REQUIRED - Code Review
==================================================

📝 PR DETAILS:
   Branch: ai-feature/20250225_143022
   Title: 🤖 AI-Generated: 3 new features
   Description: Automated feature generation

📁 Files Changed (3):
   - user_authentication.py
   - database_layer.py
   - analytics.py

📊 CHANGES SUMMARY:
- Added JWT authentication endpoints
- Created database models for QR history
- Implemented analytics dashboard
```

### Step 2: Get Approval

```
🤔 Proceed with creating PR? (yes/no): 
```

### Step 3: Create PR

```
✓ Branch: ai-feature/20250225_143022
✓ Staged changes
✓ Committed
✓ Pushed to origin/ai-feature/20250225_143022
✓ Created PR: https://github.com/nileshbutala123/.../pull/42

✅ PR Created and ready for review!
```

## 🔌 API Integration

The FastAPI app includes AI Agent endpoints:

### Check Status

```bash
curl http://localhost:8000/ai/status

{
  "available": true,
  "version": "1.0.0",
  "message": "AI Agent modules loaded"
}
```

### Trigger Generation

```bash
curl -X POST http://localhost:8000/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirements_file": "requirements/features.txt",
    "auto_commit": false,
    "description": "AI Generated Features"
  }'

{
  "success": true,
  "plan_id": "plan_20250225_143022",
  "total_tasks": 12,
  "files_generated": 4,
  "branch": "ai-feature/plan_20250225_143022",
  "message": "Code generation completed successfully"
}
```

## 🧪 Advanced Features

### Claude Code Review

Before committing, Claude can review proposed changes:

```python
review = claude.review_code_change(
    current_code="existing code",
    proposed_change="new code",
    context="description"
)

# Returns:
{
    'risks': ['...'],
    'suggestions': ['...'],
    'compat_score': 87,  # 0-100
    'security_concerns': ['...']
}
```

### Auto-Generate Tests

```python
tests = claude.generate_tests(
    feature_code="...",
    feature_name="User Authentication"
)

# Returns pytest test code
```

## 🛠️ Configuration

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional
export GITHUB_TOKEN="ghp_..."
export AI_AGENT_REQUIREMENTS_FILE="requirements/features.txt"
export AI_AGENT_OUTPUT_DIR="generated/"
export AI_AGENT_AUTO_COMMIT="false"
```

### Command Line Options

```bash
# Show help
python -m ai_agent.intelligent_agent --help

# Custom requirements file
python -m ai_agent.intelligent_agent --file requirements/my_features.xlsx

# Skip human approval
python -m ai_agent.intelligent_agent --no-interactive

# Combine options
python -m ai_agent.intelligent_agent --file custom.xlsx --no-interactive
```

## 📊 Example: Adding Feature

### 1. Create Requirements File

```bash
cat > requirements/new_features.txt << EOF
Email Notifications | Send QR code via email | High
Batch Generation | Generate multiple QR codes | Medium
Custom Branding | Add logo to QR codes | Low
EOF
```

### 2. Run Agent

```bash
python -m ai_agent.intelligent_agent --file requirements/new_features.txt
```

### 3. Review Summary

```
🤖 INTELLIGENT AI AGENT
========================

Requirements Loaded: 3
- Email Notifications (HIGH)
- Batch Generation (MEDIUM)  
- Custom Branding (LOW)

Claude Analysis:
✓ Email feature (analysis tokens: 1523 in, 487 out)
✓ Batch feature (analysis tokens: 1389 in, 521 out)
✓ Branding feature (analysis tokens: 1156 in: 398 out)

Total code generation: ~3500 tokens used
Branch: ai-feature/20250225_143022
```

### 4. Approve PR

```
🤔 Proceed with creating PR? (yes/no): yes

✓ Branch created
✓ Changes staged
✓ Committed
✓ Pushed to origin/ai-feature/20250225_143022
✓ PR created: https://github.com/nileshbutala123/.../pull/42

✅ Ready for code review on GitHub!
```

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
# Get key from https://console.anthropic.com/api_keys
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify
python -c "import anthropic; print('✓ API key configured')"
```

### "Module not found: anthropic"

```bash
pip install anthropic>=0.25.0
```

### "Git not found"

- **Windows**: Download from https://git-scm.com/download/win
- **macOS**: `brew install git`
- **Linux**: `sudo apt install git`

### "PR creation failed"

If using GitHub token:
1. Check token is valid: https://github.com/settings/tokens
2. Verify scopes: `repo` and `workflow`
3. Check token isn't expired

Without token, use manual PR link provided.

### Claude API Rate Limit

If you hit rate limits:
- Check your Claude API usage: https://console.anthropic.com/
- Wait before running again
- Consider processing fewer requirements per run

## 📈 Token Usage

The agent tracks API token usage:

```python
result = agent.run()
# Check token usage in result['plan']['requirements']
```

Typical usage per requirement:
- **Input tokens**: 1000-1500 (codebase context)
- **Output tokens**: 400-600 (implementation)
- **Per session**: 5-10k tokens (5-10 requirements)

## ✅ Checklist: Before First Run

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set ANTHROPIC_API_KEY environment variable
- [ ] Create requirements file (requirements/features.txt)
- [ ] Test Claude connection: `python -c "import anthropic; anthrop ic.Anthropic()"`
- [ ] Test Git: `git status`
- [ ] Review existing code structure
- [ ] Optional: Set GITHUB_TOKEN for auto PR creation

## 🎯 Best Practices

1. **Start small**: Test with 1-2 requirements first
2. **Review carefully**: Always review generated code before approval
3. **Test thoroughly**: Run `pytest tests/` after PR creation
4. **Monitor tokens**: Claude API has usage costs
5. **Use priorities**: Mark urgent features as HIGH priority
6. **Describe clearly**: Better descriptions = better generated code
7. **In the loop**: Don't approve changes you don't understand

## 🔗 Integration with CI/CD

The generated code includes:
- Pytest-compatible tests
- FastAPI endpoint structure
- Error handling
- Type hints and Pydantic models

Integrate with your CI/CD:
```yaml
# .github/workflows/test-ai-generated.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: python -m py compile *.py
```

## 📚 Advanced Topics

### Extending the Agent

Add custom requirement types:
```python
# In requirements_reader.py
def _read_custom_format(self, file_path):
    # Your parsing logic
    pass
```

### Custom Python Packages

Add requirements in generated code:
```python
# claude_codegen.py modifies this
NEW_DEPENDENCIES = ['requests', 'sqlalchemy']  
```

### Integration with LLMs

The architecture supports switching Claude for other models:
```python
# Replace claude_codegen.py with openai_codegen.py
from openai_codegen import OpenAICodeGen
claude = OpenAICodeGen()
```

## 📞 Support

For issues:
1. Check logs in terminal output
2. Review generated files in `generated/` folder
3. Check IMPLEMENTATION_PLAN.md in generated folder
4. Verify environment variables are set
5. Test individual components independently

### Example: Test Analyzer

```python
from ai_agent.codebase_analyzer import CodebaseAnalyzer

analyzer = CodebaseAnalyzer()
result = analyzer.analyze()
print(result['summary'])
```

### Example: Test Claude

```python
from ai_agent.claude_codegen import ClaudeCodeGen

claude = ClaudeCodeGen()
result = claude.generate_implementation(
    {'feature': 'Test', 'description': 'Test feature'},
    'Test context'
)
print(result['analysis'])
```

---

**Intelligent Agent Version**: 2.0.0  
**Last Updated**: February 25, 2025  
**Status**: Production Ready  
**Model**: Claude 3.5 Sonnet
