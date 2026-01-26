#!/bin/bash

# Create GitHub Issues for RENATA V2 Sprint 0 Tasks
# Run this from the RENATA_V2_2026 directory

echo "🚀 Creating GitHub Issues for Sprint 0 Tasks..."

REPO="mdthewzrd/renata-v2"

# Task 0.3: Define Acceptance Criteria Template
gh issue create \
  --repo "$REPO" \
  --title "✅ Task 0.3: Define Acceptance Criteria Template" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 1 hour
**Status**: Backlog
**Priority**: High

**Description**:
Create task acceptance criteria template, sprint acceptance criteria template, and feature acceptance criteria template. Document validation process.

**Acceptance Criteria**:
- [ ] Template can be applied to any task
- [ ] Template covers all quality dimensions (functional, technical, testing, documentation, performance)
- [ ] Validation process documented
- [ ] Templates saved in \`RENATA_V2_2026/templates/\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.3" \

# Task 0.4: Create Dependency Map
gh issue create \
  --repo "$REPO" \
  --title "📊 Task 0.4: Create Dependency Map" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 2 hours
**Status**: Backlog
**Priority**: High

**Description**:
Create a dependency map between all sprints and tasks. Identify blocking relationships and critical path.

**Acceptance Criteria**:
- [ ] All sprint dependencies mapped
- [ ] Task dependencies identified
- [ ] Critical path documented
- [ ] Visual dependency diagram created
- [ ] Saved in \`RENATA_V2_2026/DEPENDENCY_MAP.md\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.4" \

# Task 0.5: Risk Assessment & Mitigation
gh issue create \
  --repo "$REPO" \
  --title "⚠️ Task 0.5: Risk Assessment & Mitigation" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 3 hours
**Status**: Backlog
**Priority**: High

**Description**:
Identify all potential risks for the RENATA V2 build and create mitigation strategies for each risk.

**Acceptance Criteria**:
- [ ] Technical risks identified
- [ ] Timeline risks identified
- [ ] Resource risks identified
- [ ] Mitigation strategies documented
- [ ] Risk monitoring plan created
- [ ] Saved in \`RENATA_V2_2026/RISK_ASSESSMENT.md\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.5" \

# Task 0.6: Define Time Estimation Standards
gh issue create \
  --repo "$REPO" \
  --title "⏱️ Task 0.6: Define Time Estimation Standards" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 1 hour
**Status**: Backlog
**Priority**: Medium

**Description**:
Define standard approach for estimating task durations. Create guidelines for different task types.

**Acceptance Criteria**:
- [ ] Estimation guidelines documented
- [ ] Task complexity categories defined
- [ ] Time ranges for each category
- [ ] Buffer/risk factor guidelines
- [ ] Saved in \`RENATA_V2_2026/ESTIMATION_STANDARDS.md\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.6" \

# Task 0.7: Create Development Workflow
gh issue create \
  --repo "$REPO" \
  --title "🔄 Task 0.7: Create Development Workflow" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 2 hours
**Status**: Backlog
**Priority**: High

**Description**:
Document standard development process including coding standards, testing requirements, and PR process.

**Acceptance Criteria**:
- [ ] Development stages defined
- [ ] Code review process documented
- [ ] Testing requirements specified
- [ ] PR guidelines created
- [ ] CI/CD workflow documented
- [ ] Saved in \`RENATA_V2_2026/DEVELOPMENT_WORKFLOW.md\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.7" \

# Task 0.8: Validate Development Environment
gh issue create \
  --repo "$REPO" \
  --title "✅ Task 0.8: Validate Development Environment" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 1 hour
**Status**: Backlog
**Priority**: High

**Description**:
Ensure all development tools and services are properly configured and working.

**Acceptance Criteria**:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] CopilotKit configured
- [ ] Backend API (FastAPI) running
- [ ] Database connected (if needed)
- [ ] All environment variables set
- [ ] Validation checklist created

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.8" \

# Task 0.9: Create Communication Protocol
gh issue create \
  --repo "$REPO" \
  --title "💬 Task 0.9: Create Communication Protocol" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 1 hour
**Status**: Backlog
**Priority**: Medium

**Description**:
Define how to communicate progress, issues, and decisions throughout the project.

**Acceptance Criteria**:
- [ ] Daily standup format defined
- [ ] Progress reporting process
- [ ] Issue escalation protocol
- [ ] Decision documentation process
- [ ] Saved in \`RENATA_V2_2026/COMMUNICATION_PROTOCOL.md\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.9" \

# Task 0.10: Create Definition of Done
gh issue create \
  --repo "$REPO" \
  --title "✅ Task 0.10: Create Definition of Done" \
  --body "**Sprint**: Sprint 0 (Pre-Flight)

**Estimated**: 1 hour
**Status**: Backlog
**Priority**: High

**Description**:
Define clear criteria for when a task, feature, or sprint is considered "done".

**Acceptance Criteria**:
- [ ] Task DoD created
- [ ] Feature DoD created
- [ ] Sprint DoD created
- [ ] Validation checklist included
- [ ] Saved in \`RENATA_V2_2026/DEFINITION_OF_DONE.md\`

**References**: See SPRINT_00_PRE-FLIGHT.md Task 0.10" \

echo "✅ All issues created successfully!"
echo "📋 Next: Go to https://github.com/mdthewzrd/renata-v2/issues and add them to your project board"
