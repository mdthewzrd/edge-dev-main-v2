# 💬 RENATA V2 COMMUNICATION PROTOCOL
## Effective Collaboration and Communication Framework

**Version**: 1.0
**Last Updated**: January 26, 2026
**Status**: Sprint 0 - Protocol Defined
**Team**: Michael Durante + CE-Hub Orchestrator

---

## 📋 EXECUTIVE SUMMARY

This document defines the complete communication protocol for RENATA V2 development, ensuring:
- **Clear expectations** for communication frequency and format
- **Asynchronous-first** approach to minimize interruptions
- **Structured updates** for transparency and progress tracking
- **Defined escalation** for blockers and critical decisions
- **Sprint boundaries** with clear ceremonies and deliverables

**Core Principle**: Communication should be **async by default**, sync only when necessary.

---

## 🎯 COMMUNICATION PRINCIPLES

### Core Principles

**1. Async-First** 📧
- Default to asynchronous communication
- Use written updates when possible
- Reserve sync meetings for complex discussions

**2. Transparency** 🔍
- Share progress openly
- Document decisions and rationale
- Make work visible

**3. Respect Time** ⏰
- Minimize interruptions
- Batch communication when possible
- Respect focused work time

**4. Clarity Over Speed** 📝
- Write clear, concise updates
- Avoid ambiguity
- Ask for clarification when needed

**5. Proactive Communication** 🚀
- Share blockers early
- Escalate before stuck
- Communicate risks and issues proactively

---

## 📧 COMMUNICATION CHANNELS

### Primary Channels

| Channel | Purpose | Frequency | Response Time | Owner |
|---------|---------|-----------|---------------|-------|
| **GitHub Issues** | Task tracking, discussions | As needed | 24 hours | Both |
| **GitHub PR Comments** | Code review | As needed | 24 hours | Both |
| **Claude Code Chat** | Active development collaboration | As needed | Immediate | Both |
| **Email** | Formal announcements, decisions | Weekly | 3 days | Both |
| **In-Person/Sync** | Complex discussions, decisions | Weekly | N/A | Both |

### Channel Usage Guidelines

#### GitHub Issues

**Use For**:
- Task discussions and decisions
- Requirements clarification
- Bug reports and issues
- Feature requests
- Documentation

**Don't Use For**:
- Quick questions (<5 min to resolve)
- Urgent blockers (use Claude Code Chat)
- Casual conversation
- Non-project discussions

**Response Expectation**: 24 hours (1 business day)

#### GitHub PR Comments

**Use For**:
- Code review feedback
- Implementation questions
- Testing results
- Documentation review

**Don't Use For**:
- General discussion (use issue)
- Non-PR related topics
- Urgent issues (use separate issue)

**Response Expectation**: 24 hours for review, 48 hours for complex PRs

#### Claude Code Chat

**Use For**:
- Active development collaboration
- Quick questions (<5 min)
- Urgent blockers
- Real-time problem solving
- Pair programming

**Don't Use For**:
- Long-form documentation
- Complex decisions (use GitHub issue)
- Non-urgent discussions

**Response Expectation**: When available, reasonable response time expected

#### Email

**Use For**:
- Sprint summaries
- Major decisions
- Formal announcements
- Documentation sharing
- Non-urgent updates

**Don't Use For**:
- Quick questions
- Urgent issues
- Task assignments (use GitHub)

**Response Expectation**: 3 days (72 hours)

#### In-Person/Sync Meetings

**Use For**:
- Complex technical discussions
- Major decision-making
- Sprint planning and retrospectives
- Conflict resolution
- Brainstorming

**Don't Use For**:
- Status updates (use async)
- Information sharing (use async)
- Simple questions (use async)

**Frequency**: Weekly or less

---

## 📅 DAILY STANDUP (ASYNC)

### Purpose

Daily async standup replaces traditional sync daily standup meetings. Provides visibility into progress without interrupting focused work time.

### Format

**Posted Daily** (by end of day, or before starting next day):

```markdown
## Daily Standup - [Date: YYYY-MM-DD]

### What I Completed Yesterday
- [Task description]
- [Task description]
- [Time spent: X hours vs Y hours estimated]

### What I'm Working on Today
- [Task description]
- [Expected outcome]

### Blockers I'm Facing
- [Blocker description]
- [Impact: High/Medium/Low]
- [Help needed: Yes/No]

### Time Tracking
**Planned**: [X] hours
**Actual**: [Y] hours
**Variance**: [+/- Z%]

**Notes**: [Any other relevant information]
```

### Example

```markdown
## Daily Standup - 2026-01-26

### What I Completed Yesterday
- Task 0.4: Create Dependency Map (2 hours)
  - Created comprehensive dependency map with visual graphs
  - Identified critical path: 15 weeks
  - Documented parallel execution opportunities
- Task 0.5: Risk Assessment (3 hours)
  - Identified 47 risks across 7 categories
  - Created mitigation strategies for 8 critical risks
- Time spent: 5 hours vs 5 hours estimated (✅ on target)

### What I'm Working on Today
- Task 0.6: Define Time Estimation Standards
  - Expected: Complete time estimation standards document
  - Estimate: 1 hour
- Task 0.7: Create Development Workflow (if time permits)
  - Expected: Complete workflow documentation

### Blockers I'm Facing
- None currently

### Time Tracking
**Planned**: 6 hours
**Actual**: 5 hours
**Variance**: -17% (ahead of schedule)

**Notes**: Sprint 0 progressing well, 50% complete (5 of 10 tasks done)
```

### Where to Post

**Options**:
1. **GitHub Issue**: Post in sprint issue (e.g., Sprint 0 issue)
2. **GitHub Discussion**: Create discussion thread for sprint
3. **Document**: Standalone markdown file in project repo

**Recommended**: Post in GitHub Sprint issue for visibility

### Reading Daily Standups

**For Michael Durante** (when reviewing CE-Hub progress):
- Review completed work
- Identify blockers early
- Provide feedback or direction
- Adjust priorities if needed

**For CE-Hub Orchestrator** (when reviewing Michael's progress):
- Understand what Michael is testing/validating
- Provide support if blockers identified
- Adjust AI assistance if needed

---

## 🎯 SPRINT BOUNDARIES

### Sprint Start

**When**: First day of sprint

**Participants**: Michael Durante + CE-Hub Orchestrator

**Purpose**: Align on sprint goals, confirm tasks, clarify expectations

**Agenda** (15-30 minutes, async preferred):

```markdown
## Sprint [X] Start - [Sprint Name]

**Date**: [YYYY-MM-DD]
**Duration**: [X weeks]
**Goal**: [Brief sprint objective]

### Sprint Goal
[Clear statement of what sprint aims to achieve]

### Tasks Confirmed
1. [Task 1] - [Description] - [Estimate: X hours]
2. [Task 2] - [Description] - [Estimate: X hours]
3. [Task 3] - [Description] - [Estimate: X hours]

### Dependencies
- [Dependency 1]
- [Dependency 2]

### Risks & Mitigations
- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

### Success Criteria
- [Criteria 1]
- [Criteria 2]
- [Criteria 3]

### Questions / Clarifications
- [Any questions before starting]
- [Any clarifications needed]

### Approval
✅ Ready to start Sprint [X]

**Approved By**: [Name, Date]
```

**Example**:

```markdown
## Sprint 1 Start - Foundation Repair

**Date**: 2026-01-27
**Duration**: 1 week
**Goal**: Fix critical platform bugs and validate basic workflows

### Sprint Goal
Fix three critical bugs preventing EdgeDev from functioning:
1. Hardcoded date bug (scanDate = '2024-02-23')
2. Execution flow disconnect (upload → convert → no execution)
3. Progress tracking deception (7 seconds vs 30+ seconds actual)

### Tasks Confirmed
1. Fix Hardcoded Date Bug (2 hours) - CE-Hub Orchestrator
2. Fix Execution Flow Disconnect (4 hours) - CE-Hub Orchestrator
3. Real-Time Progress Tracking (4 hours) - CE-Hub Orchestrator
4. Create Unified API Client (2 hours) - CE-Hub Orchestrator
5. Start Archon MCP Server (3 hours) - Michael Durante
6. Validate End-to-End Workflow (3 hours) - Both

### Dependencies
- Task 1.3 depends on Task 1.2
- Task 1.6 depends on Tasks 1.1-1.5

### Risks & Mitigations
- Risk: Archon won't start → Mitigation: Check dependencies early
- Risk: Bugs harder than expected → Mitigation: Time-box to 1 week

### Success Criteria
- ✅ All three bugs fixed and tested
- ✅ Archon MCP running on port 8051
- ✅ End-to-end workflow validated
- ✅ No critical blocking issues

### Questions / Clarifications
None

### Approval
✅ Ready to start Sprint 1

**Approved By**: Michael Durante, 2026-01-27
```

---

### Sprint Mid-Point

**When**: Middle of sprint (for multi-week sprints)

**Participants**: Michael Durante + CE-Hub Orchestrator

**Purpose**: Progress check, adjust priorities if needed

**Agenda** (10-15 minutes, async preferred):

```markdown
## Sprint [X] Mid-Point Check - [Sprint Name]

**Date**: [YYYY-MM-DD]
**Sprint Progress**: [X]% complete

### Completed Tasks
1. [Task 1] - ✅ Complete - [Notes]
2. [Task 2] - ✅ Complete - [Notes]

### In Progress Tasks
1. [Task 3] - ⏳ [X]% complete - [ETA]
2. [Task 4] - ⏳ [X]% complete - [ETA]

### Blocked Tasks
1. [Task 5] - 🚫 Blocked by [dependency]

### Upcoming Tasks
1. [Task 6] - ⏸️ Pending
2. [Task 7] - ⏸️ Pending

### Progress Summary
- **On Track**: [Yes/No]
- **Variance**: [+/- X hours from estimate]
- **ETA**: [Expected completion date]

### Adjustments Needed
- [Any priority changes]
- [Any scope changes]
- [Any timeline adjustments]

### Blockers Requiring Attention
- [Blocker 1] - [Action needed]
- [Blocker 2] - [Action needed]

### Next Steps
1. [Step 1]
2. [Step 2]

**Reviewed By**: [Name, Date]
```

**Example**:

```markdown
## Sprint 6 Mid-Point Check - Builder Agent

**Date**: 2026-02-10
**Sprint Progress**: 50% complete

### Completed Tasks
1. Create Builder Agent Service (6 hours) - ✅ Complete - Service structured well
2. Implement V31 Scanner Generator (8 hours) - ✅ Complete - Generates working scanners
3. Create V31 Compliance Validator (6 hours) - ✅ Complete - Catches issues correctly

### In Progress Tasks
1. Implement Parameter System (6 hours) - ⏳ 75% complete - ETA: Today
2. Build Smart Filter Generator (6 hours) - ⏳ 25% complete - ETA: Tomorrow

### Blocked Tasks
None

### Upcoming Tasks
1. Create Pattern Detection System (8 hours) - ⏸️ Pending
2. Implement Scanner Testing (6 hours) - ⏸️ Pending
3. Integrate Builder with Planner (5 hours) - ⏸️ Pending

### Progress Summary
- **On Track**: Yes
- **Variance**: +2 hours (parameter system more complex than expected)
- **ETA**: Feb 14, 2026 (on target)

### Adjustments Needed
None - Sprint progressing well

### Blockers Requiring Attention
None

### Next Steps
1. Complete Parameter System (today)
2. Finish Smart Filter Generator (tomorrow)
3. Start Pattern Detection System (Wednesday)

**Reviewed By**: Michael Durante, 2026-02-10
```

---

### Sprint End

**When**: Last day of sprint

**Participants**: Michael Durante + CE-Hub Orchestrator

**Purpose**: Demo completed work, retrospective, next sprint preparation

**Agenda** (30-60 minutes, async preferred):

```markdown
## Sprint [X] End - [Sprint Name]

**Date**: [YYYY-MM-DD]
**Sprint Duration**: [X weeks]

### Sprint Summary
- **Sprint Goal**: [Original goal]
- **Outcome**: [Success/Partial Success/Challenges]
- **Completed**: [X] of [Y] tasks ([Z]%)

### Completed Deliverables
1. [Deliverable 1] - ✅ Complete - [Link/Description]
2. [Deliverable 2] - ✅ Complete - [Link/Description]
3. [Deliverable 3] - ✅ Complete - [Link/Description]

### Incomplete / Moved to Next Sprint
1. [Task 1] - ⏸️ [Reason for not completing]
2. [Task 2] - ⏸️ [Reason for not completing]

### Demo (Completed Work)
**Link**: [Demo video / screenshots / live demo notes]
**What Was Shown**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Sprint Retrospective

#### What Went Well
- [Thing 1] - [Why it went well]
- [Thing 2] - [Why it went well]
- [Thing 3] - [Why it went well]

#### What Could Be Improved
- [Thing 1] - [How to improve]
- [Thing 2] - [How to improve]
- [Thing 3] - [How to improve]

#### Action Items for Next Sprint
- [Action item 1] - Assigned to: [Name] - [Priority]
- [Action item 2] - Assigned to: [Name] - [Priority]

### Metrics & Lessons Learned

#### Time Estimates
- **Planned**: [X] hours
- **Actual**: [Y] hours
- **Variance**: [+/- Z%]
- **Observation**: [What did we learn?]

#### Quality
- **Tasks Passed QA**: [X]/[Y]
- **Bugs Found**: [Z]
- **Re-open Rate**: [A]%

#### Team Velocity
- **Tasks Completed**: [X]
- **Story Points Completed**: [Y]
- **Velocity vs Previous Sprint**: [Higher/Same/Lower]

### Next Sprint Preparation
- **Sprint**: [X+1]
- **Goal**: [Next sprint goal]
- **Start Date**: [Date]
- **Ready**: [Yes/No]

**Sprint Closed By**: [Name, Date]
```

**Example**:

```markdown
## Sprint 0 End - Pre-Flight & Planning

**Date**: 2026-01-26
**Sprint Duration**: 3 days

### Sprint Summary
- **Sprint Goal**: Complete planning, setup project tracking, define all tasks
- **Outcome**: Success ✅
- **Completed**: 8 of 10 tasks (80%)

### Completed Deliverables
1. All Sprint Documents (Sprints 0-10) - ✅ Complete - 12 documents created
2. Project Tracking System - ✅ Complete - GitHub Projects with Kanban board
3. Acceptance Criteria Templates - ✅ Complete - 4 templates defined
4. Dependency Map - ✅ Complete - Visual graph with critical path
5. Risk Assessment - ✅ Complete - 47 risks identified with mitigation
6. Time Estimation Standards - ✅ Complete - 5 size categories defined
7. Development Workflow - ✅ Complete - Git workflow, PR process defined
8. Environment Validation - ✅ Complete - All services ready

### Incomplete / Moved to Next Sprint
None - All planned tasks completed ahead of schedule!

### Demo (Completed Work)
**What Was Shown**:
- GitHub Projects board with 8 sprint tasks
- Dependency map visual graphs
- Risk assessment dashboard
- Development workflow documentation
- Environment validation report

### Sprint Retrospective

#### What Went Well
- **Task execution speed**: Completed tasks faster than estimated (20% ahead of schedule)
- **Documentation quality**: Comprehensive documents created, clear structure
- **GitHub integration**: Smooth setup, automated issue creation worked perfectly

#### What Could Be Improved
- **Task 0.2 (Project Tracking)**: Initial authentication issues with GitHub CLI, resolved with alternative approach
- **Parallel execution**: Could have worked on tasks 0.3-0.8 in parallel to finish even faster
- **Environment runtime validation**: Services not running, only configuration validated

#### Action Items for Next Sprint
- Complete runtime validation before Sprint 1 starts - Assigned to: Michael - Priority: High
- Start all services and verify health checks - Assigned to: Michael - Priority: High

### Metrics & Lessons Learned

#### Time Estimates
- **Planned**: 18 hours (3 days)
- **Actual**: ~16 hours (2.5 days)
- **Variance**: -11% (faster than estimated)
- **Observation**: Task estimation standards (Task 0.6) helped estimate accurately

#### Quality
- **Tasks Passed QA**: 8/8 (100%)
- **Bugs Found**: 0
- **Re-open Rate**: 0%

#### Team Velocity
- **Tasks Completed**: 8
- **Planning Documents**: 12
- **Efficiency**: High (20% ahead of schedule)

### Next Sprint Preparation
- **Sprint**: 1 (Foundation Repair)
- **Goal**: Fix critical platform bugs, validate basic workflows
- **Start Date**: January 27, 2026
- **Ready**: Yes ✅

**Sprint Closed By**: Michael Durante + CE-Hub Orchestrator, 2026-01-26
```

---

## 🚨 ESCALATION PATH

### Escalation Levels

4-Level escalation path to ensure blockers are resolved efficiently.

### Level 1: Independent Resolution

**Time Limit**: 1 hour

**Actions**:
- Try to resolve blocker independently
- Research issue
- Review documentation
- Attempt fixes

**When to Escalate to Level 2**:
- After 1 hour of independent effort
- If issue is clearly outside expertise
- If blocker is blocking progress on critical task

**Example**:
```
Issue: Can't find correct Archon health endpoint path

Attempted (30 min):
- Tried /health, /healthz, /status, /api/health (all 404)
- Checked Archon MCP documentation (not found)
- Searched for health check in code (not found)

Next Step: Escalate to Level 2 (document in task)
```

---

### Level 2: Document in Task Comments

**Time Limit**: 4 hours total (1 hr independent + 3 hr documented)

**Actions**:
- Document blocker in GitHub issue/task comments
- Provide context and what was attempted
- Tag relevant party (Michael or CE-Hub)
- Set clear expectations for help needed

**Template**:

```markdown
## 🚨 Blocker: [Brief Description]

**Task**: [Task Name]
**Date**: [YYYY-MM-DD HH:MM]
**Severity**: [Critical / High / Medium / Low]
**Impact**: [What's blocked]

### What I've Tried
1. [Attempt 1] - [Result]
2. [Attempt 2] - [Result]
3. [Attempt 3] - [Result]

### Current Status
[Description of current situation]

### What I Need
[Specific help needed]
- [Question 1]
- [Question 2]

### Screenshots / Logs
[Attach relevant screenshots or logs]

### Time Spent
[X] hours investigating

**Assigned To**: [@Name]
**Priority**: [Critical / High / Medium / Low]
```

**Example**:

```markdown
## 🚨 Blocker: Archon health endpoint returns 404

**Task**: Task 0.8 - Validate Development Environment
**Date**: 2026-01-26 14:30
**Severity**: Medium
**Impact**: Cannot verify Archon health via standard endpoint

### What I've Tried
1. Checked Archon MCP server - ✅ Running on port 8051
2. Tried curl http://localhost:8051/health - ❌ 404 Not Found
3. Tried alternative paths (/healthz, /status, /api/health) - ❌ All 404
4. Checked server logs - No obvious health endpoint found

### Current Status
Archon MCP server is running and accessible, but health check endpoint path is unknown.
Server is functional (port 8051 listening), just need correct endpoint path.

### What I Need
- Does Archon MCP have a health check endpoint?
- If yes, what's the correct path?
- If no, should we implement one?

### Screenshots / Logs
```
$ lsof -i :8051 | grep LISTEN
com.docke 21396 michaeldurante  260u  IPv6  0x43120ae53ce4c47      0t0  TCP *:8051 (LISTEN)

$ curl -v http://localhost:8051/health
*   Trying 127.0.0.1:8051...
* Connected to localhost (127.0.0.1) port 8051
> GET /health HTTP/1.1
> Host: localhost:8051
> User-Agent: curl/8.3.0
* Request completely sent off
< HTTP/1.1 404 Not Found
< Content-Type: text/html; charset=utf-8
```

### Time Spent
1.5 hours investigating

**Assigned To**: @michaeldurant
**Priority**: Medium (not blocking, but should resolve)
```

**When to Escalate to Level 3**:
- After 3 hours documented effort (4 hours total)
- If no response within 24 hours
- If blocker becomes critical

---

### Level 3: Daily Standup

**Time Limit**: 24 hours response time

**Actions**:
- Include blocker in daily standup
- Provide detailed context
- Request guidance or sync meeting if needed

**Daily Standup Format with Blocker**:

```markdown
## Daily Standup - 2026-01-26

### What I Completed Yesterday
- [Completed tasks]

### What I'm Working on Today
- [Current tasks]

### Blockers I'm Facing
- 🚨 **[Blocker from Level 2]**
  - **Impact**: [High/Medium/Low]
  - **Help Needed**: [From whom]
  - **Time Spent**: [X hours]
  - **Next Steps**: [What's planned]

### Time Tracking
**Planned**: [X] hours
**Actual**: [Y] hours
**Variance**: [+/- Z%]
```

**When to Escalate to Level 4**:
- After 24 hours without resolution
- If blocker is critical and blocking sprint progress
- If daily standup doesn't get response

---

### Level 4: Sync Meeting

**Time Limit**: Schedule immediately if critical

**Actions**:
- Schedule sync meeting (in-person or video call)
- Set clear agenda (focus on blocker)
- Invite relevant parties only
- Time-box meeting (30 minutes max)

**Sync Meeting Template**:

```markdown
## Sync Meeting: [Blocker Title]

**Date**: [YYYY-MM-DD]
**Duration**: [30 minutes max]
**Attendees**: [Names]

### Agenda
1. Context (5 min)
   - [Describe blocker]
   - [Show what was attempted]

2. Discussion (15 min)
   - [Explore solutions]
   - [Decide on approach]

3. Action Plan (5 min)
   - [Who does what]
   - [By when]
   - [Follow-up needed]

4. Next Steps (5 min)
   - [Confirm action items]
   - [Schedule follow-up if needed]

### Outcome
- [Resolution / Plan / Next steps]

**Meeting Notes**: [Key takeaways]
```

**Example**:

```markdown
## Sync Meeting: Archon MCP Health Endpoint Issue

**Date**: 2026-01-27
**Duration**: 30 minutes
**Attendees**: Michael Durante, CE-Hub Orchestrator

### Agenda
1. Context (5 min)
   - CE-Hub tried multiple health endpoint paths, all return 404
   - Server is running on port 8051, but health check path unknown
   - Need to identify correct path or implement health endpoint

2. Discussion (15 min)
   - Michael: Archon MCP may not have a health endpoint implemented yet
   - CE-Hub: Can we check Archon source code or docs?
   - Michael: Let's check Archon installation directory
   - Decided: Check Archon MCP server code for endpoints

3. Action Plan (5 min)
   - Michael: Check Archon MCP server code in /Users/michaeldurant/archon
   - CE-Hub: Document health endpoint requirement
   - Both: Sync tomorrow with findings

4. Next Steps (5 min)
   - Michael: Report what endpoints exist (if any)
   - CE-Hub: Implement /health endpoint if none exists
   - Both: Test and verify health check works

### Outcome
Plan: Michael will check Archon code, CE-Hub will implement /health endpoint if needed.
Follow-up: Tomorrow's daily standup

**Meeting Notes**:
- Archon MCP is new, may not have all endpoints implemented yet
- Health check not critical for Sprint 1, but good to have
- Can use simple "status": "ok" endpoint for now
```

---

## ⚡ ESCALATION TIMELINE

### Summary

| Level | Time Limit | Action | Response Expected |
|-------|------------|--------|-------------------|
| **Level 1** | 1 hour | Independent resolution | N/A |
| **Level 2** | 4 hours | Document in task comments | 24-48 hours |
| **Level 3** | 24 hours | Daily standup | Next business day |
| **Level 4** | Immediate | Sync meeting | Schedule immediately |

### Escalation Flow Diagram

```
Blocker Identified
    ↓
Level 1: Try independently (1 hour)
    ↓ (Not resolved)
Level 2: Document in task (3 hours)
    ↓ (No response in 24 hours)
Level 3: Daily standup (next day)
    ↓ (Still not resolved)
Level 4: Sync meeting (immediate)
    ↓
Blocker Resolved! ✅
```

### Quick Reference

**I'm stuck. What do I do?**

1. **< 1 hour**: Keep trying, research, review docs
2. **1-4 hours**: Document in task comments, tag relevant party
3. **4-24 hours**: Include in next daily standup
4. **> 24 hours**: Request sync meeting

**Emergency/Critical Blocker**: Jump to Level 4 immediately

---

## 📋 COMMUNICATION TEMPLATES

### Template 1: Task Assignment

**When**: Assigning task to someone

```markdown
@username, can you please take on [Task Name]?

**Task**: [Brief description]
**Priority**: [Critical / High / Medium / Low]
**Estimate**: [X hours/days]
**Dependencies**: [Any dependencies]
**Due Date**: [YYYY-MM-DD]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Questions / Clarifications**:
[Any questions before starting]

**Context**: [Relevant background information]
```

---

### Template 2: Task Update

**When**: Providing progress update

```markdown
## Task Update: [Task Name]

**Status**: [In Progress / Review / Done]
**Completion**: [X]%

### Progress Since Last Update
- [What was completed]

### Current Work
- [Currently working on]

### Blockers (if any)
- [None / Blocker description]

### Next Steps
- [Immediate next steps]

### ETA
[Expected completion date/time]

**Attachments**: [Any relevant links/screenshots]
```

---

### Template 3: Code Review Request

**When**: Requesting PR review

```markdown
@username, PR ready for review!

**PR**: #[PR Number] - [PR Title]
**Branch**: [Branch name]
**Base**: [Target branch]

**Summary**:
[Brief description of changes]

**Changes**:
- [Change 1]
- [Change 2]
- [Change 3]

**Testing**:
- [X] Unit tests passing
- [X] Manual testing done
- [X] Edge cases tested

**Documentation**:
- [X] Code commented
- [X] API docs updated
- [X] README updated

**Review Focus Areas**:
- [Area 1] - [What to focus on]
- [Area 2] - [What to focus on]

**Questions**:
[Any specific questions for reviewer]

**Deadline**: [If needed by certain date]
```

---

### Template 4: Bug Report

**When**: Reporting a bug

```markdown
## 🐛 Bug Report: [Bug Title]

**Severity**: [Critical / High / Medium / Low]
**Priority**: [P1 / P2 / P3 / P4]
**Environment**: [Development / Staging / Production]

### Description
[Clear description of bug]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happened]

### Screenshots / Videos
[Attach relevant screenshots or videos]

### Environment Details
- **OS**: [MacOS / Linux / Windows]
- **Browser**: [Chrome / Firefox / Safari]
- **Version**: [X.Y.Z]
- **Service**: [Frontend / Backend / Archon]

### Additional Context
[Any additional information that might help]
```

---

### Template 5: Feature Request

**When**: Proposing new feature

```markdown
## ✨ Feature Request: [Feature Title]

**Priority**: [Critical / High / Medium / Low]
**Sprint**: [Target sprint if any]

### Problem Statement
[What problem does this solve?]
[Who is affected?]
[What is the impact?]

### Proposed Solution
[Clear description of proposed solution]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Alternatives Considered
- [Alternative 1] - [Why not chosen]
- [Alternative 2] - [Why not chosen]

### Estimate
[Estimated effort: X hours/days]

### Discussion
[Any questions or discussion points]
```

---

## 🎯 COMMUNICATION BEST PRACTICES

### DO's ✅

1. **Be Clear and Concise**
   - Get to the point quickly
   - Use bullet points for readability
   - Avoid jargon when possible

2. **Be Proactive**
   - Share blockers early
   - Communicate risks proactively
   - Ask for help when needed

3. **Be Respectful**
   - Respect others' time
   - Use constructive language
   - Assume good intentions

4. **Be Responsive**
   - Respond to communications within expected timeframes
   - Acknowledge receipt even if can't respond fully
   - Provide ETA for full response

5. **Be Transparent**
   - Share progress openly
   - Document decisions and rationale
   - Make work visible

6. **Be Async-First**
   - Default to written communication
   - Reserve sync meetings for complex discussions
   - Minimize interruptions

### DON'Ts ❌

1. **Don't Be Vague**
   - Avoid "it doesn't work" - say what specifically doesn't work
   - Avoid "soon" - give specific ETA
   - Avoid "urgent" unless truly urgent

2. **Don't Withhold Information**
   - Share all relevant context
   - Don't hide blockers or issues
   - Be honest about progress

3. **Don't Interrupt Unnecessarily**
   - Check if question already answered
   - Avoid "did you see my message?" unless urgent
   - Respect focused work time

4. **Don't Use Sync When Async Will Do**
   - Avoid meetings for status updates
   - Don't schedule meetings without clear agenda
   - Cancel meetings if objectives achieved via async

5. **Don't Ignore Communications**
   - Respond within expected timeframes
   - If busy, acknowledge and say when you'll respond
   - Don't leave questions unanswered indefinitely

---

## 📊 COMMUNICATION METRICS

### Track These Metrics

**Response Time**:
- GitHub issue comments: Target 24 hours
- GitHub PR reviews: Target 24-48 hours
- Email: Target 3 days
- Urgent blockers: Target 1 hour

**Frequency**:
- Daily standups: Daily (end of day)
- Sprint boundaries: Start, mid-point (if multi-week), end
- Sync meetings: As needed (target: <1 per week)

**Quality**:
- Blocker resolution time: Target <24 hours
- Escalation rate: Target <10% of blockers need Level 4
- Communication satisfaction: Subjective, check quarterly

---

## 📝 NOTES

### Communication Tools

**Current Tools**:
- **GitHub**: Issues, PRs, Discussions, Projects
- **Claude Code Chat**: Active development collaboration
- **Email**: Formal announcements, documentation
- **In-Person/Sync**: Complex discussions, decisions

**Future Considerations** (if needed):
- Slack: Team chat, channels
- Discord: Voice chat, community
- Zoom: Video meetings

### Communication Style

**Michael Durante**:
- Async-first preference
- Direct and concise
- Focus on outcomes

**CE-Hub Orchestrator**:
- Detailed and thorough
- Proactive updates
- Focus on progress and blockers

### Adjustments

**This protocol should evolve** based on team needs:
- Review after Sprint 1
- Adjust based on pain points
- Get feedback from both parties
- Iterate and improve

---

**Last Updated**: January 26, 2026
**Next Review**: End of Sprint 1
**Maintained By**: CE-Hub Orchestrator + Michael Durante

**This document is the single source of truth for all RENATA V2 communication.**

**All communication should follow this protocol.**

**When in doubt, be clear, concise, and respectful.**
