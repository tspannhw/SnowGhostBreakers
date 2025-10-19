# 🚀 GitHub Setup Guide

Complete guide to publishing SnowGhost Breakers to GitHub securely.

---

## ✅ Pre-Publish Security Checklist

Before pushing to GitHub, verify:

- [ ] No `.env` files (only `env.example`)
- [ ] No credentials in any files
- [ ] No API keys or passwords
- [ ] No Snowflake account information
- [ ] `.gitignore` is comprehensive
- [ ] All Python scripts use environment variables
- [ ] Config files use placeholders

---

## 🔍 Security Scan

Run these commands to check for potential leaks:

```bash
# Check for .env files
find . -name "*.env" ! -name "env.example" ! -name "*.env.example"

# Search for potential passwords
grep -r -i "password\s*=\s*['\"][^$]" --include="*.py" --include="*.sql" --exclude-dir=".git" .

# Search for potential API keys
grep -r -i "api.key\|apikey\|secret" --include="*.py" --include="*.json" --exclude-dir=".git" --exclude="*.md" .

# Check git history for secrets (install gitleaks first)
# brew install gitleaks (macOS)
# or download from https://github.com/gitleaks/gitleaks
gitleaks detect --source . --verbose
```

If any secrets are found, **DO NOT PROCEED**. Remove them first!

---

## 📦 Initial Setup

### 1. Initialize Git Repository

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers

# Initialize git (if not already done)
git init

# Check what files will be committed
git status

# Add all files (gitignore will exclude sensitive files)
git add .

# Review what's being committed
git status
git diff --cached --name-only
```

### 2. Verify No Secrets

```bash
# Double-check staged files
git diff --cached | grep -i "password\|secret\|api.key"

# If anything suspicious is found, unstage it:
git reset HEAD <filename>
```

### 3. Create Initial Commit

```bash
# First commit
git commit -m "feat: Initial commit - Ghost Detection System

- Complete Snowflake-native application
- Cortex AI integration
- Neo4j graph analytics
- Streamlit UI
- MCP server support
- Agentic AI system
- Comprehensive documentation
- Full test suite

Security: All credentials use environment variables
"
```

---

## 🌐 Create GitHub Repository

### Option A: GitHub CLI (Recommended)

```bash
# Install GitHub CLI if needed
# macOS: brew install gh
# Windows: winget install GitHub.cli
# Linux: see https://github.com/cli/cli#installation

# Login to GitHub
gh auth login

# Create repository (choose public or private)
gh repo create SnowGhostBreakers --public --source=. --remote=origin \
  --description="AI-powered ghost detection system for Snowflake with Cortex AI, Neo4j graph analytics, and autonomous agents" \
  --push

# Or create as private
gh repo create SnowGhostBreakers --private --source=. --remote=origin \
  --description="AI-powered ghost detection system for Snowflake" \
  --push
```

### Option B: GitHub Web UI

1. Go to https://github.com/new
2. **Repository name:** `SnowGhostBreakers`
3. **Description:** AI-powered ghost detection system for Snowflake with Cortex AI and graph analytics
4. **Visibility:** Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we have them)
6. Click **Create repository**

Then push:

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/SnowGhostBreakers.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🔒 Post-Publish Security

### 1. Enable GitHub Security Features

Go to your repository → **Settings** → **Security**

- ✅ Enable **Dependabot alerts**
- ✅ Enable **Dependabot security updates**
- ✅ Enable **Secret scanning** (if available)
- ✅ Enable **Code scanning** (GitHub Advanced Security)

### 2. Add Branch Protection Rules

Settings → **Branches** → **Add rule**

- Branch name pattern: `main`
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require conversation resolution
- ✅ Do not allow bypassing the above settings

### 3. Configure Secrets for CI/CD

If you want to run integration tests in GitHub Actions:

Settings → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets (for integration tests only):
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`

**Note:** These are ONLY for automated testing. Never commit actual credentials!

---

## 📝 Add Repository Topics

Settings → **About** → **Topics**

Add these topics for discoverability:
- `snowflake`
- `cortex-ai`
- `ai`
- `machine-learning`
- `data-science`
- `ghost-detection`
- `paranormal`
- `streamlit`
- `neo4j`
- `graph-analytics`
- `python`
- `sql`
- `mcp`
- `agents`

---

## 🏷️ Create First Release

### Tag the Release

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial Release

Features:
- Snowflake-native ghost detection system
- Cortex AI integration (Complete, Sentiment, Embeddings, Vision)
- Neo4j graph analytics with 10+ algorithms
- Streamlit interactive UI
- MCP server for AI agents
- Agentic AI system with autonomous agents
- Business vocabulary and ontology
- Comprehensive test suite
- Full documentation
"

# Push tag to GitHub
git push origin v1.0.0
```

### Create Release on GitHub

1. Go to **Releases** → **Draft a new release**
2. **Tag version:** v1.0.0
3. **Release title:** SnowGhost Breakers v1.0.0
4. **Description:**
   ```markdown
   # 🎉 SnowGhost Breakers v1.0.0

   The first official release of the AI-powered ghost detection system for Snowflake!

   ## ✨ Features

   - 📊 Complete data model with 8 core tables
   - 🤖 Snowflake Cortex AI integration
   - 🕸️ Neo4j graph analytics (10+ algorithms)
   - 🎨 Interactive Streamlit application
   - 📓 Jupyter notebooks for analysis
   - 🔌 MCP server for AI agent integration
   - 🤖 Agentic AI system with 5 autonomous agents
   - 📚 Business vocabulary and ghost ontology
   - 🧪 Comprehensive test suite
   - 📖 Complete documentation

   ## 🚀 Quick Start

   See [QUICKSTART.md](QUICKSTART.md) for installation instructions.

   ## 📚 Documentation

   - [README.md](README.md) - Main documentation
   - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions
   - [SECURITY.md](SECURITY.md) - Security best practices
   - [NEO4J_QUICKSTART.md](NEO4J_QUICKSTART.md) - Graph analytics guide

   ## ⚙️ Requirements

   - Snowflake account with Cortex AI enabled
   - Python 3.8+
   - Optional: Neo4j Graph Analytics from Snowflake Marketplace

   ## 🐛 Known Issues

   None at this time.

   ## 📞 Support

   - [GitHub Issues](https://github.com/YOUR_USERNAME/SnowGhostBreakers/issues)
   - [Discussions](https://github.com/YOUR_USERNAME/SnowGhostBreakers/discussions)
   ```

5. Check **Set as the latest release**
6. Click **Publish release**

---

## 📢 Promote Your Repository

### Add Badges to README

Add these at the top of your README.md:

```markdown
![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/SnowGhostBreakers)
![GitHub license](https://img.shields.io/github/license/YOUR_USERNAME/SnowGhostBreakers)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/SnowGhostBreakers)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/SnowGhostBreakers)
![Python version](https://img.shields.io/badge/python-3.8+-blue)
![Snowflake](https://img.shields.io/badge/Snowflake-Cortex%20AI-29B5E8)
```

### Share On

- Snowflake Community
- Medium/Dev.to (write a blog post)
- LinkedIn
- Twitter/X
- Reddit (r/snowflake, r/datascience)
- Hacker News

---

## 🔄 Ongoing Maintenance

### Keep Dependencies Updated

```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: Update dependencies"
git push
```

### Monitor Security Alerts

- Check **Security** tab regularly
- Respond to Dependabot alerts promptly
- Review secret scanning alerts immediately

### Respond to Issues and PRs

- Acknowledge issues within 48 hours
- Review pull requests promptly
- Be welcoming to new contributors

---

## 🚨 If Credentials Are Leaked

If you accidentally commit credentials:

### 1. Rotate Credentials Immediately

```sql
-- In Snowflake
ALTER USER your_username SET PASSWORD = 'NewSecurePassword123!';
```

### 2. Remove from Git History

```bash
# Install BFG Repo-Cleaner
# macOS: brew install bfg
# Or download from https://rtyley.github.io/bfg-repo-cleaner/

# Create passwords.txt with leaked credentials
echo "password123" > passwords.txt
echo "api_key_abc" >> passwords.txt

# Remove from history
bfg --replace-text passwords.txt

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: Rewrites history!)
git push --force
```

### 3. Invalidate the Repository

If credentials were public for any time:

- Consider the credentials compromised
- Create a new repository from clean state
- Archive the old repository
- Update all links and references

---

## ✅ Final Checklist

Before making repository public:

- [ ] No credentials in code
- [ ] No credentials in git history
- [ ] `.gitignore` is comprehensive
- [ ] `env.example` provided
- [ ] `SECURITY.md` present
- [ ] `LICENSE` file included
- [ ] README.md is complete
- [ ] All documentation files present
- [ ] Branch protection enabled
- [ ] Security features enabled
- [ ] Tests passing
- [ ] No sensitive data in issues/PRs

---

## 🎉 You're Done!

Your repository is now securely published on GitHub!

**Next steps:**
1. Star your own repository (why not? 😄)
2. Share with the community
3. Wait for contributions
4. Keep it maintained and secure

---

## 📞 Questions?

Open an issue or discussion on GitHub!

**Remember:** Security is not a one-time task. Monitor regularly and respond to alerts promptly.

🕸️👻✨ **Happy Ghost Hunting!**

