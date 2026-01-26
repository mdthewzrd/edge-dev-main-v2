# Validation Process Guide

**Purpose**: Define systematic approach to validate tasks, sprints, and features
**Version**: 1.0
**Last Updated**: January 26, 2026

---

## 🎯 Validation Overview

**Objective**: Ensure all work meets quality standards before considering it "done"

**Validation Principles**:
1. **Validate Early**: Validate continuously, not just at the end
2. **Validate Completely**: Cover all quality dimensions
3. **Validate Objectively**: Use clear, measurable criteria
4. **Validate Consistently**: Apply same standards across all work

---

## 📋 Validation Workflow

### Phase 1: Self-Validation (Developer)

**When**: Before requesting review
**Time**: 15-30 minutes per task

**Checklist**:
- [ ] Review acceptance criteria template for task type
- [ ] Complete all checklist items in template
- [ ] Run all tests (unit, integration, manual)
- [ ] Check code quality standards
- [ ] Verify documentation is complete
- [ ] Test locally on your machine
- [ ] Update task with validation results

**Tools**:
- Run unit tests: `pytest` or `npm test`
- Run linters: `flake8`, `eslint`, etc.
- Check test coverage
- Manual smoke test

**Output**: Mark task as "Ready for Review" in project board

---

### Phase 2: Peer Review (Reviewer)

**When**: After developer marks as ready
**Time**: 30-60 minutes per task

**Checklist**:
- [ ] Review acceptance criteria checklist
- [ ] Review code changes line-by-line
- [ ] Verify all tests pass
- [ ] Check documentation is accurate
- [ ] Test functionality manually if needed
- [ ] Verify performance requirements
- [ ] Check for edge cases
- [ ] Provide constructive feedback

**Review Process**:
1. **Code Review**: Review code in GitHub PR or IDE
2. **Functional Review**: Test the feature
3. **Documentation Review**: Check docs are accurate
4. **Approval**: Approve or request changes

**Output**: Approve task or request revisions

---

### Phase 3: QA Validation (Tester)

**When**: After peer review approved
**Time**: 1-2 hours per feature

**Checklist**:
- [ ] Create test plan based on acceptance criteria
- [ ] Execute test plan
- [ ] Document test results
- [ ] Log bugs/issues found
- [ ] Retest after fixes
- [ ] Sign off on validation

**Test Plan Components**:
1. **Functional Tests**: Test all requirements
2. **Integration Tests**: Test with other components
3. **E2E Tests**: Test user journeys
4. **Performance Tests**: Verify performance requirements
5. **Edge Cases**: Test boundary conditions

**Output**: Validation report with pass/fail status

---

### Phase 4: Stakeholder Acceptance (Product Owner)

**When**: After QA validation passed
**Time**: 30 minutes per feature

**Checklist**:
- [ ] Demo feature to stakeholder
- [ ] Verify user value is delivered
- [ ] Confirm requirements met
- [ ] Check for any issues
- [ ] Obtain sign-off

**Output**: Stakeholder approval

---

## 🔍 Validation by Work Type

### Code Development

**Validation Focus**:
- V31 compliance
- Code quality
- Test coverage
- Documentation

**Tools**:
- `flake8` (Python linting)
- `eslint` (JavaScript linting)
- `pytest` (Python tests)
- `jest` (JavaScript tests)
- Coverage tools

**Checklist**:
- [ ] Code follows style guide
- [ ] No linting errors
- [ ] All tests pass
- [ ] Coverage >80%
- [ ] No hardcoded secrets
- [ ] Error handling in place

### Documentation

**Validation Focus**:
- Completeness
- Accuracy
- Clarity
- Examples work

**Checklist**:
- [ ] All parameters documented
- [ ] All functions described
- [ ] Examples provided
- [ ] Links work
- [ ] Screenshots included (if UI)
- [ ] Code examples tested

### Infrastructure

**Validation Focus**:
- Service is running
- API endpoints respond
- Database connected
- Monitoring works

**Checklist**:
- [ ] Service starts successfully
- [ ] Health check passes
- [ ] APIs respond correctly
- [ ] Database migrations applied
- [ ] Logs are being captured
- [ ] Alerts configured

---

## 📏 Acceptance Criteria Checklist

### Task-Level Validation

**For each task, verify**:

**Functional** ✅
- [ ] All requirements implemented
- [ ] User stories satisfied
- [ ] Edge cases handled
- [ ] Error cases handled

**Technical** ✅
- [ ] V31 standard followed (if applicable)
- [ ] No lookahead bias
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Code is modular

**Testing** ✅
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing done
- [ ] Edge cases tested

**Documentation** ✅
- [ ] Code commented
- [ ] API docs updated
- [ ] User docs updated
- [ ] Examples provided

**Performance** ✅
- [ ] Response time acceptable
- [ ] Memory usage acceptable
- [ ] No obvious bottlenecks

---

## 🚫 Common Validation Failures

### Critical Failures (Must Fix)
- ❌ Tests don't pass
- ❌ Look-ahead bias detected
- ❌ Hardcoded secrets/keys
- ❌ No error handling
- ❌ Missing documentation

### Major Failures (Should Fix)
- ⚠️ Test coverage below 80%
- ⚠️ Performance not meeting targets
- ⚠️ Incomplete documentation
- ⚠️ Edge cases not handled

### Minor Failures (Can Defer)
- ⚡ Code style inconsistencies
- ⚡ Missing some comments
- ⚡ Could optimize further

---

## 🔄 Iterative Validation Process

### Continuous Validation

**During Development**:
1. Write code → Run tests → Fix issues
2. Update docs → Verify accuracy → Fix issues
3. Test manually → Fix UX issues

**Before Marking "Ready for Review"**:
1. All acceptance criteria met
2. All tests passing
3. Documentation complete
4. Local testing successful

**After Review Feedback**:
1. Address review comments
2. Re-run tests
3. Update documentation
4. Re-mark as ready

---

## 📊 Validation Metrics

### Sprint-Level Metrics

**Track Each Sprint**:
- **Tasks Completed**: [X] / [Y] planned tasks
- **Tasks Passed QA**: [X] / [Y] completed tasks
- **Tasks Rejected**: [X] (tasks that didn't meet criteria)
- **Rework Time**: [X] hours spent on revisions

### Quality Metrics

**Track Quality Over Time**:
- **Defect Rate**: [Defects found] / [Lines of code]
- **Test Coverage**: [X]% average coverage
- **Documentation Coverage**: [X]% of tasks documented
- **First-Time Pass Rate**: [X]% of tasks pass review on first try

---

## 🎯 Validation Gates

### Gate 1: Ready for Review
**Criteria**:
- All acceptance criteria checked
- All tests passing
- Documentation complete
- Local testing successful

**Gatekeeper**: Developer self-validation

### Gate 2: Ready for QA
**Criteria**:
- Code review approved
- All acceptance criteria met
- No critical failures
- No major failures (or documented)

**Gatekeeper**: Peer reviewer

### Gate 3: Ready for Production
**Criteria**:
- QA validation passed
- Stakeholder approved
- No blockers outstanding
- Deployment successful

**Gatekeeper**: QA + Product Owner

---

## 📝 Validation Documentation

### For Each Task/Feature

**Create**:
1. **Validation Report**: Summary of testing performed
2. **Test Results**: Pass/fail status for all tests
3. **Issues Log**: Bugs found and fixed
4. **Sign-off**: Approval from reviewer/QA/PO

**Template**:
```markdown
## Validation Report: [Task Name]

**Date**: [YYYY-MM-DD]
**Validator**: [Name]

### Summary
- **Status**: Pass | Fail
- **Tests Run**: [X]
- **Tests Passed**: [Y]
- **Bugs Found**: [Z]

### Test Results
[Test details...]

### Issues Found
[Bug descriptions...]

### Sign-off
Validated by: [Name], [Date]
```

---

## 🚀 Quick Validation Checklist

**5-minute validation** (before requesting review):
- [ ] I followed the acceptance criteria template
- [ ] All my tests pass locally
- [ ] I documented my changes
- [ ] I tested manually in browser
- [ ] No obvious bugs or errors
- [ ] Ready for review

---

**Last Updated**: January 26, 2026
**Maintained By**: Development Team

**Related Documents**:
- [Task Acceptance Criteria](templates/ACCEPTANCE_CRITERIA_TASK.md)
- [Sprint Acceptance Criteria](templates/ACCEPTANCE_CRITERIA_SPRINT.md)
- [Feature Acceptance Criteria](templates/ACCEPTANCE_CRITERIA_FEATURE.md)
