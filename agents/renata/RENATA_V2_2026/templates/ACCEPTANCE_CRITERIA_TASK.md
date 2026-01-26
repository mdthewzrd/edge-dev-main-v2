# Task Acceptance Criteria Template

**Task Name**: [Task Name]
**Sprint**: [Sprint Number]
**Assigned To**: [Name]
**Estimated**: [X hours]

---

## 🎯 Overview

**Objective**: [Brief description of what this task accomplishes]

**Success Definition**: Task is complete when all checklist items below are checked ✅

---

## ✅ Functional Requirements

- [ ] **Requirement 1**: [Specific functional requirement]
  - **Validation Method**: [How to verify]
  - **Evidence**: [What to show as proof]

- [ ] **Requirement 2**: [Specific functional requirement]
  - **Validation Method**: [How to verify]
  - **Evidence**: [What to show as proof]

- [ ] **Requirement 3**: [Specific functional requirement]
  - **Validation Method**: [How to verify]
  - **Evidence**: [What to show as proof]

---

## 🛠️ Technical Requirements

### Code Quality
- [ ] **V31 Standard**: Code follows V31 Gold Standard architecture
  - 5 required methods implemented: `fetch_grouped_data`, `apply_smart_filters`, `detect_patterns`, `format_results`, `run_scan`
  - Per-ticker operations (no lookahead bias)
  - Market scanning pillar compatible

- [ ] **Error Handling**: Comprehensive error handling implemented
  - Try-except blocks for all external calls
  - Graceful degradation on failures
  - Error messages logged and actionable

- [ ] **Logging**: Appropriate logging added
  - Debug logs for development
  - Info logs for normal operations
  - Error logs for failures
  - Performance logs (timing)

### Code Structure
- [ ] **Modular Design**: Code is modular and reusable
- [ ] **Type Hints**: All functions have type annotations
- [ ] **Documentation**: Functions documented with docstrings
- [ ] **Naming**: Clear, descriptive variable/function names

---

## 🧪 Testing Requirements

### Unit Tests
- [ ] **Coverage**: Unit tests written for all functions
- [ ] **Pass Rate**: All unit tests passing (>95% pass rate)
- [ ] **Edge Cases**: Edge cases tested and handled

### Integration Tests
- [ ] **Integration**: Works with other system components
- [ ] **API Compatibility**: Compatible with existing APIs
- [ ] **Data Flow**: Data flows correctly through system

### Manual Testing
- [ ] **Smoke Test**: Basic functionality works
- [ ] **User Scenario**: Tested against real use case
- [ ] **Error Recovery**: System recovers from errors

---

## 📚 Documentation Requirements

### Code Documentation
- [ ] **Comments**: Code is commented where complex
- [ ] **Docstrings**: All public functions have docstrings
- [ ] **README**: Updated README if applicable

### User Documentation
- [ ] **API Docs**: API documentation updated
- [ ] **User Guide**: User-facing documentation updated
- [ ] **Examples**: Usage examples provided

### Change Documentation
- [ ] **Changelog**: CHANGELOG.md updated
- [ ] **Migration Guide**: Migration guide if breaking changes

---

## ⚡ Performance Requirements

### Response Time
- [ ] **Target**: [Specific target, e.g., <2 seconds for scanner generation]
- [ ] **Measured**: [Actual measured performance]
- [ ] **Acceptable**: [Is performance acceptable?]

### Resource Usage
- [ ] **Memory**: Memory usage within acceptable limits
- [ ] **CPU**: CPU usage reasonable
- [ ] **I/O**: Efficient use of resources

### Scalability
- [ ] **Concurrent Load**: Can handle concurrent requests
- [ ] **Data Volume**: Can handle expected data volumes
- [ ] **User Load**: Can handle expected user load

---

## 🔒 Security & Compliance

### Security
- [ ] **No Secrets**: No hardcoded secrets/keys
- [ ] **Input Validation**: All inputs validated
- [ ] **Output Sanitization**: Outputs properly sanitized

### Compliance
- [ ] **V31 Compliance**: Meets V31 Gold Standard requirements
- [ ] **No Look-Ahead Bias**: No future data used inappropriately
- [ ] **Data Integrity**: Data integrity maintained

---

## 🎬 Sign-Off

**Developer**: [Name] - Date: [YYYY-MM-DD]
- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Ready for next sprint phase

**Reviewer**: [Name] - Date: [YYYY-MM-DD]
- [ ] Task validated against requirements
- [ ] Testing verified
- [ ] Documentation complete

---

## 📝 Notes

[Any additional context, blockers, or special considerations]

---

**Last Updated**: [Date]
**Template Version**: 1.0
