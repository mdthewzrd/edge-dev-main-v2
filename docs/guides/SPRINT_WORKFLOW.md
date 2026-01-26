# Sprint-Based Development Workflow

This document defines the sprint-based development workflow for edge-dev-main.

## Sprint Structure

Each sprint is **1 week** (5 business days) with clear deliverables.

### Sprint Lifecycle

1. **Sprint Planning** (Monday, 1 hour)
   - Review sprint goals
   - Assign tasks
   - Identify dependencies
   - Estimate effort

2. **Sprint Execution** (Tuesday-Thursday)
   - Complete tasks
   - Daily progress updates
   - Blocker resolution

3. **Sprint Review** (Friday, 1 hour)
   - Demo completed features
   - Validate acceptance criteria
   - Stakeholder feedback

4. **Sprint Retrospective** (Friday, 30 min)
   - What went well
   - What could be improved
   - Action items for next sprint

## Task Workflow

### Task States

```
[Backlog] → [In Progress] → [In Review] → [Validation] → [Done]
```

### Task DoD (Definition of Done)

Every task must meet these criteria before marking as "Done":

- [ ] Code written and committed
- [ ] Code follows V31 standard (if applicable)
- [ ] Acceptance criteria met
- [ ] Code reviewed (if complex)
- [ ] Tested manually
- [ ] Documentation updated
- [ ] No known bugs
- [ ] Performance acceptable
- [ ] Task marked as Done

## File Organization Rules

### Where Files Go

**New Feature Code**:
- Frontend: `frontend/src/app/[feature]/`
- Backend: `backend/src/api/[feature]/`

**Reusable Components**:
- UI Components: `frontend/src/components/ui/`
- Business Logic: `backend/src/core/[domain]/`

**Documentation**:
- Architecture: `docs/architecture/`
- Guides: `docs/guides/`
- API Docs: `docs/api/`
- Sprint Retrospectives: `docs/retrospectives/`

**Tests**:
- Unit Tests: `backend/tests/unit/` or `frontend/tests/unit/`
- E2E Tests: `tests/e2e/`

### What NOT to Commit

- Generated code (scanners, formatted output)
- Temporary files
- Cache files
- Environment files with secrets
- Build artifacts
- Dependencies (node_modules, venv)

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
```
feat(scanner): add V31 standard compliance checker

- Implement 5 required methods check
- Add per-ticker operation validation
- Include market scanning pillar check

Closes #123
```

### Branch Strategy

- `main` - Production-ready code
- `sprint/<n>` - Sprint branch (e.g., sprint/1)
- `feat/<task-id>` - Feature branch
- `fix/<bug-id>` - Bugfix branch

## Daily Workflow

### Morning Standup (Async)

Update your task with:
1. What I completed yesterday
2. What I'll work on today
3. Blockers (if any)

### End of Day

1. Commit and push your work
2. Update task status
3. Document any decisions

## Sprint Handoff

### End of Sprint Checklist

- [ ] All tasks marked Done
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Demo prepared
- [ ] Retrospective completed
- [ ] Next sprint tasks identified

## Keeping Repository Clean

### During Sprints

1. **Daily Commits**: Commit at least once per day
2. **Clean Branches**: Delete merged branches
3. **Update Docs**: Document as you code
4. **Review PRs**: Don't let them pile up

### Weekly Cleanup

```bash
# Delete merged branches
git branch --merged | grep -v "main" | xargs git branch -d

# Clean untracked files
git clean -fd

# Update dependencies
npm audit fix
pip install --upgrade -r requirements.txt
```

## Quality Gates

### Before Merging to Main

1. **Code Review**: All PRs reviewed
2. **Tests Pass**: All tests green
3. **Documentation**: Docs updated
4. **Performance**: No performance regression
5. **Security**: No new vulnerabilities

### Sprint Completion

1. **Deliverables Met**: All sprint goals achieved
2. **Stakeholder Approval**: Features validated
3. **Retrospective Done**: Lessons learned
4. **Next Sprint Ready**: Tasks identified

## Tools & Resources

- **Project Tracking**: GitHub Projects
- **Documentation**: Markdown in `docs/`
- **Communication**: GitHub Issues + PRs
- **Code Review**: GitHub PR reviews

## Emergency Process

If sprint goals can't be met:

1. **Immediate**: Notify stakeholders
2. **Assess**: What's achievable?
3. **Reprioritize**: Must-have vs nice-to-have
4. **Adjust**: Update sprint plan
5. **Document**: Why adjustment was needed
