# 🔄 RENATA V2 DEVELOPMENT WORKFLOW
## Complete Development Process and Git Workflow

**Version**: 1.0
**Last Updated**: January 26, 2026
**Status**: Sprint 0 - Workflow Defined
**Repository**: mdthewzrd/renata-v2

---

## 📋 EXECUTIVE SUMMARY

This document defines the complete development workflow for RENATA V2, ensuring:
- **Clear process** for all development work
- **Consistent git practices** across all contributors
- **Quality gates** prevent bad code from merging
- **Safe deployments** with rollback plans
- **Traceability** from task to production

**Core Principle**: Protect the `main` branch at all costs. It should always be deployable.

---

## 🎯 WORKFLOW STAGES

### Stage Overview

```
┌──────────┐
│ BACKLOG  │  Tasks prioritized, not yet started
└────┬─────┘
     │ (Task assigned, work begins)
     ↓
┌──────────┐
│IN PROGRESS│  Active development, local commits
└────┬─────┘
     │ (Feature complete, PR created)
     ↓
┌──────────┐
│ IN REVIEW │  Code review, testing, feedback
└────┬─────┘
     │ (Approved, checks passing)
     ↓
┌──────────┐
│VALIDATION│  Acceptance criteria verification
└────┬─────┘
     │ (All criteria met, merged to main)
     ↓
┌──────────┐
│   DONE   │  Merged, deployed, closed
└──────────┘
```

### Stage Definitions

#### 1. BACKLOG
**Status**: Tasks not yet started
**Criteria**:
- Task documented with clear requirements
- Prioritized by importance
- Assigned to owner (optional)
- Estimated (time, complexity)

**Entry**: Any new task or bug
**Exit**: Task assigned, owner starts work

**Actions**:
- Refine task requirements
- Estimate effort
- Prioritize against other tasks
- Assign to sprint/milestone

---

#### 2. IN PROGRESS
**Status**: Active development
**Criteria**:
- Task assigned to owner
- Feature branch created
- Work in progress

**Entry**: Owner starts working on task
**Exit**: Feature complete, PR created

**Actions**:
- Create feature branch
- Write code
- Commit locally
- Run tests locally
- Create PR when ready

**Guidelines**:
- Commit frequently (every 1-2 hours)
- Write descriptive commit messages
- Keep PRs focused (one task per PR)
- Don't break the build

---

#### 3. IN REVIEW
**Status**: Code review and testing
**Criteria**:
- Pull request created
- All checks passing (tests, linting)
- Ready for review

**Entry**: PR created and checks passing
**Exit**: PR approved

**Actions**:
- Self-review (review your own code first)
- Request peer review
- Address feedback
- Update PR as needed

**Guidelines**:
- PR should be reviewable within 30-60 minutes
- Include description of changes
- Link to related task/issue
- Add screenshots if UI changes

---

#### 4. VALIDATION
**Status**: Acceptance criteria verification
**Criteria**:
- PR approved and merged
- Feature deployed to staging
- Acceptance criteria verified

**Entry**: PR merged to main
**Exit**: All acceptance criteria met

**Actions**:
- Deploy to staging
- Test acceptance criteria
- Verify functionality
- Document issues

**Guidelines**:
- Test against original requirements
- Test edge cases
- Perform manual testing if needed
- Get stakeholder sign-off

---

#### 5. DONE
**Status**: Complete and deployed
**Criteria**:
- All acceptance criteria met
- Merged to main branch
- Deployed to production (if applicable)
- Task closed

**Entry**: Validation complete
**Exit**: None (terminal state)

**Actions**:
- Close task/issue
- Update documentation
- Celebrate 🎉

**Guidelines**:
- Task is truly done when deployed
- Don't close tasks prematurely
- Document any deviations

---

## 🌿 GIT WORKFLOW

### Branching Strategy

**Branch Structure**:
```
main (production)
├── develop (staging/integration)
    ├── feature/task-0.4-dependency-map
    ├── feature/task-0.5-risk-assessment
    ├── feature/sprint-1-archon-integration
    └── bugfix/hardcoded-date-fix
```

### Branch Types

#### `main` Branch
- **Purpose**: Production-ready code
- **Protection**:
  - No direct commits allowed
  - PR reviews required
  - All checks must pass
  - At least 1 approval required
- **Deployment**: Automatically deploys to production
- **Stability**: Always deployable, never broken

**Rules**:
- NEVER commit directly to main
- ALWAYS merge via PR
- NEVER merge if checks are failing
- NEVER merge without approval

#### `develop` Branch (Optional)
- **Purpose**: Integration branch for features
- **Protection**: Same as main
- **Deployment**: Deploys to staging environment
- **Stability**: Should be stable, but minor issues acceptable

**When to Use**:
- For features that need integration testing
- When multiple developers working on related features
- When features need staging validation before main

**Rules**:
- Merge feature branches to develop
- Test integration on staging
- Merge develop to main when stable

#### Feature Branches
- **Purpose**: Develop individual features/tasks
- **Naming**: `feature/task-{number}-{short-name}` or `feature/{short-name}`
- **Lifespan**: Short-lived (hours to days, not weeks)
- **Base**: Branch off `main` (or `develop` if using)

**Examples**:
- `feature/task-0.4-dependency-map`
- `feature/task-0.5-risk-assessment`
- `feature/sprint-2-archon-integration`
- `feature/builder-agent-scanner-generator`

**Rules**:
- One feature per branch
- Keep branches focused
- Delete after merge (don't accumulate)
- Rebase frequently to avoid conflicts

#### Bugfix Branches
- **Purpose**: Fix bugs
- **Naming**: `bugfix/{short-name}` or `hotfix/{short-name}`
- **Lifespan**: Very short-lived (hours)
- **Base**: Branch off `main`

**Examples**:
- `bugfix/hardcoded-date-crash`
- `hotfix/archon-connection-timeout`
- `bugfix/rag-search-latency`

**Rules**:
- For critical bugs, use `hotfix` prefix
- For regular bugs, use `bugfix` prefix
- Merge directly to main (bypass develop)
- Test thoroughly before merging

#### Release Branches (Optional)
- **Purpose**: Prepare for production release
- **Naming**: `release/v{version}` (e.g., `release/v1.0.0`)
- **Lifespan**: Short-lived (days)
- **Base**: Branch off `develop`

**When to Use**:
- When preparing for production deployment
- When testing release candidates
- When coordinating multiple features

**Rules**:
- Create from develop
- Test thoroughly
- Merge to main when ready
- Tag release version
- Merge back to develop

---

### Git Commands Workflow

#### Starting a New Task

```bash
# 1. Ensure main is up-to-date
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/task-0.4-dependency-map

# 3. Verify you're on the right branch
git branch
# * feature/task-0.4-dependency-map
#   main

# 4. Start working!
```

#### During Development

```bash
# 1. Check status
git status

# 2. Stage changes
git add path/to/file
# OR stage all changes
git add .

# 3. Commit changes
git commit -m "feat: create dependency map document

- Sprint-to-sprint dependency graph
- Task-to-task dependencies
- External dependency analysis
- Critical path identification

Refs: #2"

# 4. Push frequently (backup your work)
git push origin feature/task-0.4-dependency-map
```

#### Rebase Frequently (Recommended)

```bash
# Once per day, rebase onto main
git fetch origin main
git rebase origin/main

# If conflicts occur, resolve them:
# 1. Open conflicted files
# 2. Resolve conflicts (look for <<<<<<<, =======, >>>>>>>)
# 3. git add resolved files
# 4. git rebase --continue

# After rebase, force push (only on feature branches!)
git push origin feature/task-0.4-dependency-map --force-with-lease
```

#### Creating Pull Request

```bash
# 1. Push your branch
git push origin feature/task-0.4-dependency-map

# 2. Create PR via GitHub CLI
gh pr create \
  --repo mdthewzrd/renata-v2 \
  --title "✅ Task 0.4: Create Dependency Map" \
  --body "## Summary
Created comprehensive dependency map for RENATA V2.

## Changes
- Sprint-to-sprint dependency graph
- Task-to-task dependencies for all sprints
- External dependency analysis
- Critical path identified (15 weeks)
- Parallel execution opportunities (3 weeks savings)

## Testing
- Manual review of all dependencies
- Verified critical path accuracy
- Validated against sprint documents

## Checklist
- [x] Code follows style guide
- [x] All tests passing
- [x] Documentation updated
- [x] Ready for review

Refs: #2" \
  --base main \
  --head feature/task-0.4-dependency-map

# 3. Request review
gh pr edit 123 --add-reviewer mdthewzrd
```

#### After PR Approval

```bash
# 1. Merge PR (via GitHub button or gh CLI)
gh pr merge 123 --squash --delete-branch

# 2. Pull main locally
git checkout main
git pull origin main

# 3. Delete local branch
git branch -d feature/task-0.4-dependency-map
```

---

## 📝 COMMIT MESSAGE STANDARDS

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (neither fix nor feature)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, build process, etc.
- **perf**: Performance improvements
- **ci**: CI/CD changes

### Scopes

Common scopes:
- `sprint-0`, `sprint-1`, etc.
- `archon`, `copilotkit`, `agents`
- `planner`, `researcher`, `builder`, `executor`, `analyst`
- `ui`, `api`, `database`
- `docs`, `tests`, `build`

### Examples

**Good Commits**:
```
feat(sprint-0): create dependency map document

- Sprint-to-sprint dependency graph
- Task-to-task dependencies for all sprints
- External dependency analysis (5 critical systems)
- Critical path identified: 15 weeks
- Parallel execution opportunities: 3 weeks savings

Closes #2
```

```
fix(sprint-1): resolve hardcoded date bug

Changed scanDate from hardcoded '2024-02-23' to dynamic date selection.
Added trading date validation to reject weekends and holidays.

Fixes #10
```

```
docs(readme): update installation instructions

Added Python version requirement (3.9+).
 clarified Archon setup steps.
Added troubleshooting section.
```

**Bad Commits**:
```
update
fix stuff
wip
changes
```

### Commit Message Guidelines

**DO's** ✅:
- Use imperative mood ("add" not "added" or "adds")
- Capitalize subject line
- Limit subject line to 72 characters
- Wrap body at 72 characters
- Explain WHAT and WHY (not HOW)
- Reference issue/PR numbers

**DON'Ts** ❌:
- Don't use "and" (split into multiple commits)
- Don't mix unrelated changes
- Don't commit debug code
- Don't commit broken code
- Don't commit directly to main

---

## 👥 CODE REVIEW PROCESS

### Review Responsibilities

**Author** (Person requesting review):
1. Self-review your code first
2. Ensure all checks passing
3. Write clear PR description
4. Link to related task/issue
5. Request appropriate reviewer

**Reviewer** (Person reviewing code):
1. Review within 24 hours
2. Provide constructive feedback
3. Approve or request changes
4. Verify fixes if requested changes

**Both**:
1. Be respectful and professional
2. Assume good intentions
3. Focus on code, not person
4. Learn from each other

### Review Checklist

**Functionality**:
- [ ] Code implements requirements correctly
- [ ] Edge cases handled
- [ ] Error handling in place
- [ ] User acceptance criteria met

**Code Quality**:
- [ ] Code is readable and understandable
- [ ] Variable/function names are descriptive
- [ ] Code is properly decomposed (not too complex)
- [ ] No unnecessary complexity
- [ ] Follows DRY principle (don't repeat yourself)

**Testing**:
- [ ] Unit tests included (if applicable)
- [ ] Tests cover critical paths
- [ ] Tests pass
- [ ] Edge cases tested

**Documentation**:
- [ ] Complex code commented
- [ ] Function/methods have docstrings
- [ ] API documentation updated (if applicable)
- [ ] README updated (if user-facing)

**Security**:
- [ ] No hardcoded secrets/keys
- [ ] Inputs validated
- [ ] Outputs sanitized
- [ ] No obvious vulnerabilities

**Performance**:
- [ ] No obvious performance issues
- [ ] Efficient algorithms used
- [ ] No unnecessary database/API calls
- [ ] Caching used where appropriate

### Review Process Flow

```
┌──────────────┐
│ Author       │
│ Create PR    │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Author       │
│ Self-Review  │
└──────┬───────┘
       │ (All checks passing?)
       ↓
┌──────────────┐
│ Reviewer     │
│ Review Code  │
└──────┬───────┘
       │
       ├─→ Changes Needed ──┐
       │                    │
       │                    ↓
       │              ┌──────────────┐
       │              │ Author       │
       │              │ Make Changes │
       │              └──────┬───────┘
       │                     │
       └─────────────────────┘
       │
       ↓
┌──────────────┐
│ Reviewer     │
│ Approve PR   │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Merge PR     │
└──────────────┘
```

### Review Feedback Guidelines

**Giving Feedback**:
- Be specific (not "this is bad" but "this function is hard to understand because...")
- Be constructive (suggest improvements)
- Be respectful (avoid "you should", use "consider")
- Explain why (not just "change this" but "change this because...")
- Praise good code (positive reinforcement)

**Receiving Feedback**:
- Don't take it personally
- Ask clarifying questions
- Explain your reasoning if you disagree
- Make requested changes or explain why not
- Learn and improve

### Review Turnaround Targets

- **Small PRs** (<200 lines): Review within 4 hours
- **Medium PRs** (200-500 lines): Review within 24 hours
- **Large PRs** (500+ lines): Review within 48 hours

**If reviewer unavailable**:
- Request alternative reviewer
- After 24 hours, ping reviewer
- After 48 hours, can self-merge (with caution)

---

## 🧪 TESTING PROCESS

### Testing Pyramid

```
        ┌──────────┐
        │  Manual  │  ← Few manual tests (exploratory, UAT)
        └────┬─────┘
             │
        ┌─────┴─────┐
        │ Integration│ ← Integration tests (APIs, workflows)
        └─────┬─────┘
              │
        ┌─────┴─────┐
        │   Unit    │  ← Many unit tests (functions, components)
        └───────────┘
```

### Unit Testing

**Purpose**: Test individual functions/components in isolation

**When to Write**:
- All new functions
- All new components
- Bug fixes (add test for bug)
- Edge cases

**Tools**:
- **Python**: `pytest`, `unittest`
- **TypeScript/JavaScript**: `jest`, `vitest`

**Example**:
```python
# tests/test_dependency_map.py

def test_critical_path_length():
    """Test that critical path is correctly calculated."""
    dep_map = DependencyMap()
    critical_path = dep_map.get_critical_path()

    assert critical_path.duration == 15  # weeks
    assert len(critical_path.sprints) == 9

def test_parallel_opportunities():
    """Test that parallel opportunities are identified."""
    dep_map = DependencyMap()
    parallel = dep_map.get_parallel_opportunities()

    assert parallel.total_savings == 3  # weeks
```

**Coverage Target**: 80%+ for critical code

---

### Integration Testing

**Purpose**: Test how components work together

**When to Write**:
- API integrations
- Agent workflows
- Database interactions
- External service calls

**Example**:
```typescript
// tests/integration/archon.test.ts

describe('Archon Integration', () => {
  test('should ingest and retrieve knowledge', async () => {
    const archon = new ArchonMCPClient();

    // Ingest knowledge
    await archon.ingestKnowledge({
      type: 'v31_spec',
      content: v31SpecContent,
      metadata: { version: '1.0' }
    });

    // Retrieve knowledge
    const results = await archon.ragSearch({
      query: 'smart filters',
      limit: 5
    });

    expect(results.length).toBeGreaterThan(0);
    expect(results[0].relevance).toBeGreaterThan(0.7);
  });
});
```

---

### Manual Testing

**Purpose**: Exploratory testing, user acceptance

**When to Perform**:
- Before creating PR (smoke test)
- After deployment to staging
- For complex UI flows
- For user acceptance testing (UAT)

**Checklist**:
- [ ] Basic functionality works
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] UI/UX verified
- [ ] Performance acceptable

**Example Test Plan**:
```
Task: Task 0.4 - Create Dependency Map

Manual Test Plan:
1. Open DEPENDENCY_MAP.md
2. Verify sprint-to-sprint graph is visible
3. Verify critical path is documented
4. Verify external dependencies are listed
5. Verify parallel opportunities are identified
6. Check document formatting is correct
7. Verify all links work

Result: ✅ All tests passed
```

---

### Testing Workflow

```
┌──────────────┐
│ Developer    │
│ Write Code   │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Developer    │
│ Write Tests  │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Developer    │
│ Run Locally  │
└──────┬───────┘
       │ (All passing?)
       ↓
┌──────────────┐
│ Git Push    │
│ CI Runs      │
└──────┬───────┘
       │ (All passing?)
       ↓
┌──────────────┐
│ Create PR    │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Code Review  │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Manual Test  │
│ (Staging)    │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Merge &      │
│ Deploy       │
└──────────────┘
```

---

## 🚀 DEPLOYMENT PROCESS

### Deployment Environments

```
Development → Staging → Production
    ↓            ↓           ↓
 Local       Testing     Live
  Laptop      Server      Users
```

#### Development Environment
- **Location**: Local machine
- **Purpose**: Active development
- **Data**: Test data, mock data
- **Deployment**: Manual (run locally)
- **Frequency**: Every commit

#### Staging Environment
- **Location**: Testing server
- **Purpose**: Pre-production testing
- **Data**: Staging data (close to production)
- **Deployment**: Automated (CI/CD)
- **Frequency**: Every merged PR

#### Production Environment
- **Location**: Production server
- **Purpose**: Live system
- **Data**: Real production data
- **Deployment**: Automated (CI/CD) with approval
- **Frequency**: As needed (daily, weekly, etc.)

### Deployment Steps

#### Pre-Deployment Checklist

**Before deploying to staging**:
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Environment variables configured
- [ ] Database migrations prepared

**Before deploying to production**:
- [ ] Staging testing complete
- [ ] Stakeholder approval obtained
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Backup plan confirmed
- [ ] Deploy during low-traffic window (if applicable)

#### Deployment Commands

**Deploy to Staging**:
```bash
# 1. Ensure main is up-to-date
git checkout main
git pull origin main

# 2. Run tests
npm test
# OR
pytest

# 3. Deploy to staging
./deploy.sh staging

# 4. Verify deployment
curl https://staging.renata.edge-dev.com/health
```

**Deploy to Production**:
```bash
# 1. Create release tag
git tag -a v1.0.0 -m "Release v1.0.0: Sprint 0 complete"
git push origin v1.0.0

# 2. Deploy to production (requires approval)
./deploy.sh production

# 3. Verify deployment
curl https://renata.edge-dev.com/health

# 4. Monitor logs
tail -f /var/log/renata/production.log
```

### Deployment Script Template

```bash
#!/bin/bash
# deploy.sh

set -e  # Exit on error

ENVIRONMENT=$1  # staging or production

echo "🚀 Deploying to $ENVIRONMENT..."

# Pre-deployment checks
if [ "$ENVIRONMENT" = "production" ]; then
  read -p "Are you sure you want to deploy to production? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Deployment cancelled"
    exit 1
  fi
fi

# Backup current deployment
echo "📦 Backing up current deployment..."
./scripts/backup.sh $ENVIRONMENT

# Run tests
echo "🧪 Running tests..."
npm test
pytest

# Build application
echo "🔨 Building application..."
npm run build
# OR
docker build -t renata:$ENVIRONMENT .

# Deploy
echo "📤 Deploying to $ENVIRONMENT..."
if [ "$ENVIRONMENT" = "staging" ]; then
  docker-compose -f docker-compose.staging.yml up -d
else
  docker-compose -f docker-compose.prod.yml up -d
fi

# Run smoke tests
echo "🔍 Running smoke tests..."
./scripts/smoke-tests.sh $ENVIRONMENT

# Verify deployment
echo "✅ Verifying deployment..."
sleep 10  # Wait for services to start
curl -f https://$ENVIRONMENT.renata.edge-dev.com/health || exit 1

echo "✅ Deployment to $ENVIRONMENT complete!"
```

---

## 🔙 ROLLBACK PROCESS

### When to Rollback

**Immediate Rollback** (within 5 minutes):
- Critical bug causing data loss
- Security vulnerability
- Complete system failure
- Performance degradation (100% slowdown)

**Planned Rollback** (within 1 hour):
- Non-critical bugs discovered
- Feature not working as expected
- User complaints >10% of users

### Rollback Steps

#### Automatic Rollback (If Smoke Tests Fail)

```bash
#!/bin/bash
# deploy.sh (continued)

# After deployment, if smoke tests fail:
if ! ./scripts/smoke-tests.sh $ENVIRONMENT; then
  echo "❌ Smoke tests failed! Rolling back..."
  ./scripts/rollback.sh $ENVIRONMENT
  exit 1
fi
```

#### Manual Rollback

```bash
#!/bin/bash
# rollback.sh

ENVIRONMENT=$1

echo "🔙 Rolling back $ENVIRONMENT deployment..."

# Stop current deployment
echo "⏹️ Stopping services..."
if [ "$ENVIRONMENT" = "staging" ]; then
  docker-compose -f docker-compose.staging.yml down
else
  docker-compose -f docker-compose.prod.yml down
fi

# Restore from backup
echo "📦 Restoring from backup..."
./scripts/restore.sh $ENVIRONMENT

# Start previous version
echo "▶️ Starting previous version..."
if [ "$ENVIRONMENT" = "staging" ]; then
  docker-compose -f docker-compose.staging.yml up -d
else
  docker-compose -f docker-compose.prod.yml up -d
fi

# Verify rollback
echo "🔍 Verifying rollback..."
sleep 10
curl -f https://$ENVIRONMENT.renata.edge-dev.com/health || exit 1

echo "✅ Rollback complete!"
```

#### Git Rollback (Revert Commit)

```bash
# 1. Identify bad commit
git log --oneline

# 2. Revert the commit
git revert <commit-hash>

# 3. Push the revert
git push origin main

# 4. Deploy the revert
./deploy.sh production
```

### Rollback Decision Tree

```
Deployment Complete
    ↓
Run Smoke Tests
    ↓
    ├─→ Pass → Success! 🎉
    │
    └─→ Fail
        ↓
    Critical Failure?
        ↓
        ├─→ Yes → Immediate Rollback (<5 min)
        │          ↓
        │      Investigate Issue
        │          ↓
        │      Fix and Redeploy
        │
        └─→ No → Planned Rollback (<1 hour)
                 ↓
             Investigate Issue
                 ↓
             Fix and Redeploy
```

### Rollback Communication

**When rolling back**:
1. **Immediate**: Notify team (Slack/Discord)
   - "Rolling back production deployment due to [issue]"
   - ETA for rollback: [X minutes]

2. **After Rollback**: Notify stakeholders
   - "Rollback complete"
   - "Issue: [description]"
   - "Next steps: [plan]"

3. **Post-Mortem**: Within 24 hours
   - Document what happened
   - Root cause analysis
   - Preventive measures

---

## 📋 WORKFLOW STATE TRANSITIONS

### State Transition Rules

```
BACKLOG → IN PROGRESS
- Condition: Task assigned, owner starts work
- Action: Create feature branch
- Validation: Branch exists, task marked in progress

IN PROGRESS → IN REVIEW
- Condition: Feature complete, tests passing
- Action: Create PR, push branch
- Validation: PR exists, all checks passing

IN REVIEW → VALIDATION
- Condition: PR approved, merged to main
- Action: Merge PR, delete branch
- Validation: Code in main, task in validation

VALIDATION → DONE
- Condition: All acceptance criteria met
- Action: Close task, deploy (if applicable)
- Validation: Task closed, deployed
```

### Invalid Transitions

**NOT Allowed**:
- ❌ BACKLOG → IN REVIEW (must be IN PROGRESS first)
- ❌ IN PROGRESS → DONE (must be reviewed first)
- ❌ IN REVIEW → BACKLOG (must resolve review or reject)
- ❌ VALIDATION → IN PROGRESS (must complete validation or rollback)

### State Tracking

**In GitHub Issues**:
- Use labels: `backlog`, `in-progress`, `in-review`, `validation`, `done`
- Update labels when state changes
- Automate with GitHub Actions if possible

**In Project Board**:
- Drag tasks between columns
- Columns: Backlog, In Progress, In Review, Validation, Done
- Keep board up-to-date

---

## ✅ WORKFLOW CHECKLISTS

### Pre-Commit Checklist

Before committing code:
- [ ] Code follows style guide
- [ ] No linting errors
- [ ] Tests added/updated
- [ ] Tests passing locally
- [ ] No debug code (console.log, print statements)
- [ ] No hardcoded secrets
- [ ] Commit message follows standards
- [ ] Changes focused on single task

### Pre-PR Checklist

Before creating PR:
- [ ] All commits pushed to branch
- [ ] Branch up-to-date with main
- [ ] All checks passing (CI)
- [ ] Self-review completed
- [ ] PR description written
- [ ] Linked to task/issue
- [ ] Ready for review

### Pre-Merge Checklist

Before merging PR:
- [ ] All approvals received
- [ ] All checks passing
- [ ] Reviewer feedback addressed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Ready for production

### Pre-Deploy Checklist

Before deploying to production:
- [ ] Staging testing complete
- [ ] Stakeholder approval obtained
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Backup confirmed
- [ ] Low-traffic window (if applicable)

---

## 🎯 QUALITY GATES

### Gate 1: Commit to Feature Branch

**Criteria**:
- [ ] Code compiles/runs
- [ ] No obvious bugs
- [ ] Commit message follows standards

**Gatekeeper**: Developer self-check

### Gate 2: Create Pull Request

**Criteria**:
- [ ] All tests passing
- [ ] No linting errors
- [ ] Code reviewed by author
- [ ] PR description complete

**Gatekeeper**: Automated CI checks

### Gate 3: Merge Pull Request

**Criteria**:
- [ ] At least 1 approval
- [ ] All checks passing
- [ ] Reviewer feedback addressed
- [ ] No merge conflicts

**Gatekeeper**: Code reviewer approval

### Gate 4: Deploy to Production

**Criteria**:
- [ ] Staging tests passing
- [ ] Stakeholder approval
- [ ] Rollback plan ready
- [ ] Monitoring configured

**Gatekeeper**: Michael Durante (or delegate)

---

## 📚 WORKFLOW DOCUMENTATION

### Required Documentation

**For Each Feature**:
- PR description (what and why)
- Code comments (complex logic)
- API documentation (if applicable)
- User documentation (if user-facing)

**For Each Bug Fix**:
- Bug description
- Root cause analysis
- Fix description
- Test to prevent regression

**For Each Deployment**:
- Release notes (what changed)
- Known issues (if any)
- Migration guide (if needed)

---

## 🎯 BEST PRACTICES

### DO's ✅

1. **Branch Frequently**: Create feature branches for all work
2. **Commit Often**: Small, focused commits
3. **Push Regularly**: Backup your work frequently
4. **Review Your Code**: Self-review before requesting review
5. **Test Locally**: Run tests before pushing
6. **Write Clear Messages**: Describe what and why
7. **Keep PRs Focused**: One task per PR
8. **Delete Branches**: Clean up after merge
9. **Update Docs**: Keep documentation current
10. **Communicate**: Notify team of blockers

### DON'Ts ❌

1. **Don't Commit to Main**: Always use branches
2. **Don't Write Huge Commits**: Break into smaller commits
3. **Don't Ignore Check Failures**: Fix before proceeding
4. **Don't Bypass Review**: Always get approval
5. **Don't Merge Broken Code**: Ensure tests pass
6. **Don't Leave PRs Open**: Review within 24-48 hours
7. **Don't Accumulate Branches**: Delete after merge
8. **Don't Forget Documentation**: Update as you go
9. **Don't Deploy Without Testing**: Always test first
10. **Don't Ignore Rollback Plan**: Always have backup

---

## 📊 WORKFLOW METRICS

### Track These Metrics

**Velocity**:
- PRs merged per week
- Tasks completed per sprint
- Cycle time (commit to merge)

**Quality**:
- PR re-open rate (merged, then issues found)
- Bug rate per release
- Test coverage percentage

**Efficiency**:
- Time to first review
- Time to merge (after approval)
- Rollback frequency

**Targets**:
- PRs merged: 5-10 per week
- Cycle time: <3 days average
- Re-open rate: <5%
- Bug rate: <2 bugs per release
- Test coverage: >80%

---

## 📝 NOTES

### Workflow Evolution

This workflow should evolve based on team needs:
- Review quarterly
- Adjust based on pain points
- Get team feedback
- Iterate and improve

### Escalation

If workflow blockers occur:
1. Try to resolve independently (1 hour)
2. Document issue in task comments
3. Escalate to daily standup
4. Sync meeting if blocking

---

**Last Updated**: January 26, 2026
**Next Review**: End of Sprint 0
**Maintained By**: CE-Hub Orchestrator + Michael Durante

**This document is the single source of truth for all RENATA V2 development workflow.**

**All development work should follow this workflow.**

**When in doubt, protect the main branch.**
