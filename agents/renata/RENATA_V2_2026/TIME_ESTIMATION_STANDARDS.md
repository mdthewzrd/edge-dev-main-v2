# ⏱️ RENATA V2 TIME ESTIMATION STANDARDS
## Consistent Task Sizing and Duration Estimation

**Version**: 1.0
**Last Updated**: January 26, 2026
**Status**: Sprint 0 - Standards Defined
**Project Duration**: 16 weeks (optimized timeline)

---

## 📋 EXECUTIVE SUMMARY

This document defines consistent time estimation standards for all RENATA V2 work. It ensures:
- **Consistent estimates** across all tasks and sprints
- **Realistic timelines** with built-in buffers
- **Traceable accuracy** through tracking
- **Continuous improvement** through re-estimation

**Core Principle**: Better to under-promise and over-deliver than over-promise and under-deliver.

---

## 🎯 TASK SIZE CATEGORIES

### Overview

All work is categorized into **5 sizes** based on complexity, uncertainty, and duration:

| Size | Complexity | Uncertainty | Duration | Examples |
|------|-----------|-------------|----------|----------|
| **XS** | Trivial | None | 30min - 2hr | Fix typo, update config, add comment |
| **S** | Simple | Low | 2-4hr | Add endpoint, small feature, write test |
| **M** | Moderate | Some | 1 day (4-8hr) | Add agent action, integration, refactor |
| **L** | Complex | Multiple | 2-3 days | New agent, major feature, architecture |
| **XL** | Very Complex | High | 1 week+ | Sprint-level work, research, infrastructure |

**Rule of Thumb**: If you're unsure, **round up** to the next size. It's better to overestimate than underestimate.

---

## 📏 SIZE DEFINITIONS

### XS (Extra Small): 30min - 2hr

**Characteristics**:
- Well-understood problem
- Clear solution path
- No unknowns or risks
- Can be done independently
- No coordination needed

**Examples**:
- Fix typo in documentation
- Update configuration value
- Add console.log for debugging
- Update import statement
- Add single line of code
- Rename variable/function
- Update CSS style
- Add single test case

**Estimation Approach**:
- Break into 15-minute increments
- Round up to nearest 30 minutes
- Example: "Fix typo in README" = 15min → round to 30min

**Buffer**: 0% (no buffer needed for XS tasks)

---

### S (Small): 2-4hr

**Characteristics**:
- Simple problem
- Clear solution path
- Low uncertainty
- Minimal coordination
- Limited testing needed

**Examples**:
- Add single API endpoint
- Create simple component (button, input)
- Write unit tests for one function
- Add error handling to existing code
- Update database schema (simple change)
- Add validation logic
- Create simple utility function
- Write documentation for one feature

**Estimation Approach**:
- Break into 1-hour increments
- Minimum: 2 hours
- Maximum: 4 hours
- Example: "Add user authentication endpoint" = 3 hours

**Buffer**: 10% (adds 12-24 minutes)

---

### M (Medium): 1 day (4-8hr)

**Characteristics**:
- Moderate complexity
- Some unknowns
- Requires research
- May need coordination
- Testing required

**Examples**:
- Add agent action (requires understanding agent architecture)
- Integrate two systems (e.g., Archon + CopilotKit)
- Refactor module (requires understanding existing code)
- Create comprehensive test suite
- Build new UI component with state
- Implement feature with multiple steps
- Debug complex issue
- Performance optimization

**Estimation Approach**:
- Break into 2-hour increments
- Minimum: 4 hours (half day)
- Maximum: 8 hours (full day)
- Identify subtasks and estimate each
- Add buffer for unknowns
- Example: "Integrate Archon MCP client" = 6 hours

**Buffer**: 20% (adds 1-2 hours)

---

### L (Large): 2-3 days

**Characteristics**:
- High complexity
- Multiple unknowns
- Requires significant research
- Heavy coordination
- Extensive testing
- Multiple components affected

**Examples**:
- Build new agent (Planner, Researcher, Builder, etc.)
- Implement major feature (scanner generation, backtesting)
- Architectural refactoring
- Database migration
- Performance optimization across system
- Security audit and fixes
- Integration testing suite

**Estimation Approach**:
- Break into half-day increments (4 hours)
- Minimum: 2 days (16 hours)
- Maximum: 3 days (24 hours)
- Identify all subtasks and dependencies
- Estimate each subtask separately
- Sum + add buffer
- Example: "Build Builder Agent" = 3 days

**Buffer**: 25% (adds 8-12 hours)

---

### XL (Extra Large): 1 week+

**Characteristics**:
- Very high complexity
- Many unknowns
- Research-heavy
- High coordination needs
- Comprehensive testing
- Cross-cutting concerns
- Multiple stakeholders

**Examples**:
- Complete sprint (Sprint 1, 2, 3, etc.)
- New infrastructure (Archon setup, CI/CD)
- Major research project (tool extraction, architecture design)
- System-wide refactoring
- Production deployment
- Comprehensive documentation suite
- Performance optimization program

**Estimation Approach**:
- Break into day increments
- Minimum: 5 days (1 week)
- Maximum: As long as needed
- Identify phases and milestones
- Estimate each phase separately
- Sum + add buffer
- Add contingency for major unknowns
- Example: "Sprint 2: Archon Integration" = 1 week

**Buffer**: 30% (adds 1.5-3+ days)

---

## 🛠️ ESTIMATION BY WORK TYPE

### Code Development

**Factors to Consider**:
- **Complexity**: Simple (1x) → Moderate (1.5x) → Complex (2x)
- **Familiarity**: Well-known (1x) → Some unknowns (1.3x) → New domain (1.6x)
- **Testing**: None (0x) → Unit tests (1.2x) → Integration tests (1.5x)
- **Documentation**: None (0x) → Comments (1.1x) → Full docs (1.3x)

**Base Estimates**:
- **Single function/method**: S (2-4hr)
- **Small component**: S (2-4hr)
- **Medium component**: M (1 day)
- **Large component**: L (2-3 days)
- **New agent/service**: XL (1 week+)

**Formula**:
```
Base Estimate × Complexity × Familiarity × Testing × Documentation = Final Estimate
```

**Example**:
```
Task: Build scanner generator function
Base: M (1 day = 8hr)
Complexity: Complex (2x)
Familiarity: New domain (1.6x)
Testing: Integration tests (1.5x)
Documentation: Full docs (1.3x)

Calculation: 8 × 2 × 1.6 × 1.5 × 1.3 = 50 hours ≈ 6 days
Apply XL category: Round to 1 week (5 days)
Buffer: +30% = 6.5 days ≈ 1.5 weeks
```

---

### Testing

**Factors to Consider**:
- **Test Type**: Unit (1x) → Integration (1.5x) → E2E (2x)
- **Coverage**: Single path (1x) → Main paths (1.3x) → All paths (1.6x)
- **Setup Needed**: None (0x) → Test fixtures (1.2x) → Mock data (1.4x)

**Base Estimates**:
- **Single unit test**: XS (30min)
- **Unit test suite (small)**: S (2-4hr)
- **Unit test suite (medium)**: M (1 day)
- **Integration test suite**: L (2-3 days)
- **E2E test suite**: XL (1 week+)

**Examples**:
- "Write 5 unit tests for function" = S (3hr)
- "Test agent integration" = M (1 day)
- "Complete integration test suite" = L (2-3 days)

---

### Documentation

**Factors to Consider**:
- **Type**: Comment (1x) → README (1.5x) → API docs (2x) → Tutorial (2.5x)
- **Detail**: Brief (1x) → Standard (1.3x) → Comprehensive (1.6x)
- **Audience**: Internal (1x) → External (1.3x)

**Base Estimates**:
- **Code comments**: XS (30min - 1hr)
- **Single file documentation**: S (2-4hr)
- **Feature documentation**: M (1 day)
- **API documentation**: L (2-3 days)
- **Complete user guide**: XL (1 week+)

**Examples**:
- "Add docstrings to module" = S (3hr)
- "Write feature guide" = M (1 day)
- "Complete API documentation" = L (3 days)

---

### Infrastructure

**Factors to Consider**:
- **Complexity**: Simple (1x) → Moderate (1.5x) → Complex (2x)
- **Environment**: Dev (1x) → Staging (1.3x) → Production (1.6x)
- **Automation**: Manual (1x) → Semi-automated (1.4x) → Fully automated (1.8x)

**Base Estimates**:
- **Configuration change**: XS (30min - 1hr)
- **Service setup**: S (2-4hr)
- **Environment configuration**: M (1 day)
- **CI/CD pipeline**: L (2-3 days)
- **Infrastructure migration**: XL (1 week+)

**Examples**:
- "Configure environment variable" = XS (30min)
- "Setup Archon MCP server" = S (3hr)
- "Build CI/CD pipeline" = L (2-3 days)

---

### Research

**Factors to Consider**:
- **Scope**: Narrow (1x) → Moderate (1.5x) → Broad (2x)
- **Depth**: Surface (1x) → Moderate (1.5x) → Deep (2x)
- **Uncertainty**: Low (1x) → Medium (1.5x) → High (2x)

**Base Estimates**:
- **Quick investigation**: XS (30min - 1hr)
- **Targeted research**: S (2-4hr)
- **Exploratory research**: M (1 day)
- **Comprehensive analysis**: L (2-3 days)
- **Major research project**: XL (1 week+)

**Examples**:
- "Investigate error message" = XS (1hr)
- "Research best practices for X" = S (3hr)
- "Analyze architecture options" = M (1 day)

---

## 🔋 BUFFER POLICY

### Buffer by Task Size

| Task Size | Base Estimate | Buffer | Total Estimate |
|-----------|--------------|--------|----------------|
| **XS** | 30min - 2hr | 0% | 30min - 2hr |
| **S** | 2-4hr | 10% | 2.2 - 4.4hr |
| **M** | 1 day (8hr) | 20% | 1.0 day (9.6hr) |
| **L** | 2-3 days (16-24hr) | 25% | 2.5 - 3.8 days |
| **XL** | 1 week (40hr) | 30% | 1.3 weeks (52hr) |

### Why Buffers Are Necessary

**Uncertainties** that justify buffers:
1. **Unknowns**: Always more than expected
2. **Distractions**: Context switching, meetings, interruptions
3. **Debugging**: Always takes longer than coding
4. **Testing**: Test failures require fixes
5. **Documentation**: Takes time to write well
6. **Review**: Code review feedback requires revisions

### When to Apply Buffers

**Always apply buffers** for:
- All new estimates (before committing)
- Re-estimations (if estimate increases)
- Sprint planning (aggregate estimates)

**Don't apply buffers** to:
- Actual time spent (historical data)
- Already completed tasks
- Trivial changes (XS tasks)

### Buffer Calculation Examples

**Example 1: S Task**
```
Task: Add user authentication endpoint
Base Estimate: 3 hours
Buffer: 10%
Total: 3 × 1.10 = 3.3 hours ≈ 3.5 hours
```

**Example 2: M Task**
```
Task: Integrate Archon MCP client
Base Estimate: 6 hours
Buffer: 20%
Total: 6 × 1.20 = 7.2 hours ≈ 1 day
```

**Example 3: L Task**
```
Task: Build Builder Agent
Base Estimate: 3 days (24 hours)
Buffer: 25%
Total: 24 × 1.25 = 30 hours ≈ 4 days
```

**Example 4: XL Task**
```
Task: Sprint 2 (Archon Integration)
Base Estimate: 1 week (40 hours)
Buffer: 30%
Total: 40 × 1.30 = 52 hours ≈ 1.5 weeks
```

---

## 🔄 RE-ESTIMATION PROCESS

### When to Re-estimate

**Trigger Conditions** (re-estimate if ANY occur):
1. **Task is 50% complete** and estimate was wrong by >25%
2. **New information discovered** that significantly changes scope
3. **Dependencies blocked** causing delays
4. **Technical debt discovered** that wasn't anticipated
5. **External factors** (API changes, third-party issues)
6. **Sprint progress shows** consistent underestimation

**Don't Re-estimate** for:
- Normal variations in work pace
- Minor scope changes (<10%)
- Temporary delays (<1 day)
- Learning curve adjustments (first time doing X)

### Re-estimation Steps

**Step 1: Pause and Assess**
- Document current progress (% complete)
- Identify what changed (new scope, blocked, complexity)
- Calculate remaining work

**Step 2: Create New Estimate**
- Use same sizing methodology as original
- Only re-estimate remaining work (not work already done)
- Apply appropriate buffer

**Step 3: Compare to Original**
- Calculate difference: New Estimate - Original Estimate
- If difference >25%, requires approval
- Document reason for change

**Step 4: Communicate**
- Update task with new estimate
- Notify stakeholders (Michael, CE-Hub Orchestrator)
- Explain why estimate changed
- Get approval if increase >25%

**Step 5: Track for Learning**
- Record re-estimation in task history
- Track original vs. actual time
- Use data to improve future estimates

### Re-estimation Example

**Original Estimate**:
```
Task: Build Builder Agent
Original Estimate: L (3 days)
Breakdown:
- Create service: 1 day
- Implement scanner generator: 1 day
- Implement validator: 0.5 days
- Testing: 0.5 days
Buffer: 25% = 0.75 days
Total: 3.75 days ≈ 4 days
```

**At 50% Complete** (2 days elapsed, 50% done):
```
Progress:
- Create service: ✅ Complete (took 1.5 days vs 1 day estimated)
- Scanner generator: ⏳ In progress, more complex than expected

Re-estimate Remaining Work:
- Scanner generator: Need 2 more days (was 1 day)
- Validator: Still 0.5 days
- Testing: Increased to 1 day (more complex)
Subtotal: 3.5 days remaining
Buffer: 25% = 0.9 days
New Total: 3.5 + 0.9 = 4.4 days ≈ 5 days remaining

New Overall Estimate:
2 days spent + 5 days remaining = 7 days total
Original was 4 days, increase of 75%
Requires approval (increase >25%)
```

**Reason for Change**:
- Scanner generation more complex than anticipated
- Additional validation requirements discovered
- Testing scope expanded

---

## 📊 ESTIMATION ACCURACY TRACKING

### Metrics to Track

**Track for Every Completed Task**:
1. **Original Estimate**: What was initially estimated
2. **Actual Time**: How long it actually took
3. **Variance**: (Actual - Estimate) / Estimate × 100%
4. **Task Size**: XS, S, M, L, or XL
5. **Work Type**: Code, Test, Docs, Infrastructure, Research
6. **Re-estimated**: Yes/No (if yes, how many times)

### Accuracy Targets

**By Task Size**:
| Task Size | Target Accuracy | Acceptable Range |
|-----------|-----------------|------------------|
| **XS** | ±25% | 0.75x - 1.25x |
| **S** | ±30% | 0.70x - 1.30x |
| **M** | ±40% | 0.60x - 1.40x |
| **L** | ±50% | 0.50x - 1.50x |
| **XL** | ±60% | 0.40x - 1.60x |

**By Work Type**:
| Work Type | Target Accuracy | Acceptable Range |
|-----------|-----------------|------------------|
| **Code** | ±40% | 0.60x - 1.40x |
| **Testing** | ±30% | 0.70x - 1.30x |
| **Documentation** | ±50% | 0.50x - 1.50x |
| **Infrastructure** | ±50% | 0.50x - 1.50x |
| **Research** | ±60% | 0.40x - 1.60x |

### Tracking Template

```markdown
## Task: [Task Name]

**Original Estimate**: S (3 hours)
**Actual Time**: 4 hours
**Variance**: +33% (acceptable, within ±30% target)
**Task Size**: S
**Work Type**: Code
**Re-estimated**: No

**Lessons Learned**:
- Underestimated complexity of validation logic
- Testing took longer than expected
- Next time: Account for edge cases in S tasks
```

### Weekly Review

**Every Friday**, review estimation accuracy:
1. Calculate variance for all completed tasks that week
2. Compare to targets
3. Identify patterns (consistently over/under-estimating)
4. Adjust estimation approach if needed
5. Document lessons learned

**Example Weekly Review**:
```
Week of Jan 20-24, 2026

Tasks Completed: 8
Average Variance: +28% (overestimated by 28%)

Breakdown by Size:
- XS (2 tasks): +15% average ✓ Within target
- S (3 tasks): +22% average ✓ Within target
- M (2 tasks): +35% average ⚠ Slightly over target
- L (1 task): +45% average ✓ Within target

Breakdown by Work Type:
- Code (5 tasks): +32% average ✓ Within target
- Testing (2 tasks): +18% average ✓ Within target
- Documentation (1 task): +25% average ✓ Within target

Observation: Consistently overestimating by ~25-30%
Action: Consider reducing buffer from 20% to 15% for M tasks
```

---

## 📐 ESTIMATION WORKSHEET

Use this worksheet when estimating new tasks:

### Step 1: Categorize Task Size

**Question**: What size category does this task fit?

**Decision Tree**:
```
Can it be done in <2 hours with no unknowns?
├─ Yes → XS (30min - 2hr)
└─ No
    Can it be done in <4 hours with low uncertainty?
    ├─ Yes → S (2-4hr)
    └─ No
        Can it be done in 1 day with some unknowns?
        ├─ Yes → M (1 day)
        └─ No
            Can it be done in 2-3 days with multiple unknowns?
            ├─ Yes → L (2-3 days)
            └─ No → XL (1 week+)
```

### Step 2: Identify Factors

**Check all that apply**:
- [ ] High complexity
- [ ] New domain (not familiar)
- [ ] Requires research
- [ ] Multiple components
- [ ] Heavy testing needed
- [ ] Documentation required
- [ ] Coordination needed
- [ ] External dependencies

**Multiply base estimate by 1.1 for each factor checked** (max 2x multiplier)

### Step 3: Calculate Base Estimate

```
Task Size Base: ___ hours
× Complexity Multiplier: ___
= Adjusted Base: ___ hours
```

### Step 4: Add Buffer

```
Adjusted Base: ___ hours
+ Buffer (0-30%): ___ hours
= Final Estimate: ___ hours
```

### Step 5: Round to Size Category

```
Final Estimate: ___ hours
→ Round to: XS / S / M / L / XL
```

### Example Worksheet

**Task**: Build Builder Agent scanner generator

**Step 1: Task Size**
- Answer: "No" to all → XL (1 week+)

**Step 2: Factors**
- [x] High complexity
- [x] New domain
- [x] Requires research
- [x] Multiple components
- [x] Heavy testing needed
- [ ] Documentation required
- [x] Coordination needed
- [ ] External dependencies
**7 factors × 1.1 = 1.7x multiplier** (cap at 2x)

**Step 3: Calculate Base**
```
Task Size Base: 40 hours (1 week)
× Complexity Multiplier: 1.7
= Adjusted Base: 68 hours
```

**Step 4: Add Buffer**
```
Adjusted Base: 68 hours
+ Buffer (30% for XL): 20 hours
= Final Estimate: 88 hours
```

**Step 5: Round**
```
Final Estimate: 88 hours
→ Round to: XL (2 weeks)
```

---

## 📈 ESTIMATION BEST PRACTICES

### DO's ✅

1. **Break Down Large Tasks**
   - Break L/XL tasks into smaller pieces
   - Estimate each piece separately
   - Sum + add buffer

2. **Use Historical Data**
   - Look at similar past tasks
   - Use actual times as reference
   - Adjust based on differences

3. **Identify Unknowns**
   - Explicitly list what you don't know
   - Add buffer for unknowns
   - Research unknowns before estimating

4. **Get Second Opinion**
   - For L/XL tasks, get another estimate
   - Compare and discuss differences
   - Average or take higher estimate

5. **Document Assumptions**
   - What are you assuming about the task?
   - What could go wrong?
   - What dependencies exist?

6. **Be Conservative**
   - Better to overestimate than underestimate
   - Stakeholders happy when you finish early
   - Stakeholders unhappy when you finish late

### DON'Ts ❌

1. **Don't Estimate Under Pressure**
   - Take time to think through the task
   - Don't let urgency force optimistic estimates
   - Say "I need time to estimate properly"

2. **Don't Forget Testing**
   - Testing always takes longer than expected
   - Add 20-50% for testing depending on complexity
   - Include test writing, execution, debugging

3. **Don't Ignore Dependencies**
   - Check what you're waiting on
   - Add buffer if dependency is uncertain
   - Document dependency risks

4. **Don't Assume Best Case**
   - Assume things will go wrong
   - Use P50 (50th percentile) or P75 (75th percentile)
   - Never use P10 (best case) for commitments

5. **Don't Forget Buffer**
   - Always apply appropriate buffer
   - XS: 0%, S: 10%, M: 20%, L: 25%, XL: 30%
   - Buffer is for uncertainty, not padding

6. **Don't Ignore Past Performance**
   - If you consistently underestimate by 30%, adjust estimates
   - Track your accuracy over time
   - Learn from past mistakes

---

## 🎯 SPRINT-LEVEL ESTIMATION

### Sprint Duration Standards

| Sprint | Duration (Hours) | Duration (Days) | Duration (Weeks) |
|--------|------------------|-----------------|-----------------|
| **Sprint 0** | 18 hours | 3 days | 0.6 weeks |
| **Sprint 1** | 20-25 hours | 3-5 days | 1 week |
| **Sprint 2** | 25-30 hours | 4-6 days | 1 week |
| **Sprint 3** | 40-50 hours | 6-8 days | 2 weeks |
| **Sprint 4** | 40-50 hours | 6-8 days | 2 weeks |
| **Sprint 5** | 40-50 hours | 6-8 days | 2 weeks |
| **Sprint 6** | 60-75 hours | 9-12 days | 3 weeks |
| **Sprint 7** | 40-50 hours | 6-8 days | 2 weeks |
| **Sprint 8** | 40-50 hours | 6-8 days | 2 weeks |
| **Sprint 9** | 40-50 hours | 6-8 days | 2 weeks |
| **Sprint 10** | 40-50 hours | 6-8 days | 2 weeks |

### Sprint Estimation Process

**Step 1: List All Tasks**
- List every task in sprint
- Include development, testing, documentation
- Don't forget meetings, reviews, overhead

**Step 2: Size Each Task**
- Use size categories (XS, S, M, L, XL)
- Estimate each task individually
- Apply buffers

**Step 3: Sum Estimates**
- Add all task estimates
- Add sprint overhead (10% for meetings, reviews, context switching)

**Step 4: Check Against Target**
- Compare total to sprint duration target
- If over target: remove tasks, move to next sprint, or extend sprint
- If under target: add tasks or reduce scope

**Step 5: Add Sprint Buffer**
- Add 10% sprint-level buffer for unknowns
- Final total should fit within sprint duration

**Example Sprint Estimation**:
```
Sprint 1: Foundation Repair

Tasks:
1. Fix hardcoded date bug: S (3 hours)
2. Fix execution flow: M (8 hours)
3. Real-time progress tracking: M (8 hours)
4. Unified API client: S (4 hours)
5. Start Archon: S (3 hours)
6. Validate E2E workflow: M (6 hours)
7. Document issues: S (3 hours)

Subtotal: 35 hours
Sprint Overhead (10%): 3.5 hours
Running Total: 38.5 hours
Sprint Buffer (10%): 3.9 hours
Final Total: 42.4 hours ≈ 5.3 days

Target: 1 week (5 days, 40 hours)
Action: Fits within target with small buffer remaining ✓
```

---

## 📚 ESTIMATION EXAMPLES

### Example 1: XS Task

**Task**: Fix typo in README.md

**Estimation**:
- Size: XS (well-understood, no unknowns)
- Base: 15 minutes (find typo + fix)
- Buffer: 0%
- Total: 15 minutes → round to 30 minutes (XS minimum)

**Actual**: 20 minutes
**Variance**: -33% (faster than estimated) ✓

---

### Example 2: S Task

**Task**: Add user authentication endpoint

**Estimation**:
- Size: S (simple, clear path)
- Base: 3 hours (development: 2hr, testing: 1hr)
- Factors: None
- Buffer: 10% = 0.3 hours
- Total: 3.3 hours → round to 3.5 hours

**Actual**: 4 hours
**Variance**: +14% (within ±30% target) ✓

---

### Example 3: M Task

**Task**: Integrate Archon MCP client

**Estimation**:
- Size: M (moderate complexity, some unknowns)
- Base: 6 hours
- Factors: New domain (1.3x), Testing (1.2x)
- Adjusted: 6 × 1.3 × 1.2 = 9.4 hours
- Buffer: 20% = 1.9 hours
- Total: 11.3 hours → round to 1 day (8 hours)

**Note**: Rounded down because adjusted base already includes complexity buffers

**Actual**: 10 hours
**Variance**: +25% (within ±40% target) ✓

---

### Example 4: L Task

**Task**: Build Builder Agent

**Estimation**:
- Size: L (complex, multiple unknowns)
- Base: 24 hours (3 days)
- Factors: High complexity (1.5x), New domain (1.3x), Research (1.3x), Testing (1.4x)
- Adjusted: 24 × 1.5 × 1.3 × 1.3 × 1.4 = 85 hours (cap at 2x = 48 hours)
- Buffer: 25% = 12 hours
- Total: 60 hours → 7.5 days → round to 2 weeks (10 days)

**Actual**: 55 hours
**Variance**: -8% (within ±50% target) ✓

---

### Example 5: XL Task

**Task**: Sprint 2: Archon Integration

**Estimation**:
- Size: XL (very complex, sprint-level work)
- Base: 40 hours (1 week)
- Factors: Multiple components (1.4x), Research (1.3x), Testing (1.3x), Documentation (1.2x)
- Adjusted: 40 × 1.4 × 1.3 × 1.3 × 1.2 = 114 hours (cap at 2x = 80 hours)
- Buffer: 30% = 24 hours
- Total: 104 hours → 13 days → round to 2.5 weeks

**Actual**: 90 hours
**Variance**: -13% (within ±60% target) ✓

---

## 🎯 ESTIMATION CHECKLIST

Use this checklist before finalizing any estimate:

### Task Understanding
- [ ] I understand what needs to be done
- [ ] I've reviewed requirements/user stories
- [ ] I've identified all subtasks
- [ ] I've checked dependencies

### Complexity Assessment
- [ ] I've assessed task complexity (simple/moderate/complex)
- [ ] I've identified unknowns/risks
- [ ] I've determined if research is needed
- [ ] I've checked if similar work exists (for reference)

### Effort Calculation
- [ ] I've estimated development time
- [ ] I've estimated testing time
- [ ] I've estimated documentation time
- [ ] I've added appropriate buffer (0-30%)

### Validation
- [ ] Estimate is consistent with past similar tasks
- [ ] I've gotten second opinion for L/XL tasks
- [ ] I've documented assumptions
- [ ] Estimate fits within sprint/project timeline

### Communication
- [ ] I've communicated estimate to stakeholders
- [ ] I've documented estimate in task tracker
- [ ] I've explained assumptions if needed
- [ ] I've committed to estimate

---

## 📊 ESTIMATION METRICS DASHBOARD

### Track These Metrics Weekly

**Estimation Accuracy**:
```
Week of: ___

Tasks Completed: ___
Average Variance: ___%
Within Target: ___/___ (___%)
Over Target: ___/___ (___%)
Under Target: ___/___ (___%)
```

**By Task Size**:
```
XS Tasks: ___ completed, avg variance ___%
S Tasks: ___ completed, avg variance ___%
M Tasks: ___ completed, avg variance ___%
L Tasks: ___ completed, avg variance ___%
XL Tasks: ___ completed, avg variance ___%
```

**By Work Type**:
```
Code: ___ completed, avg variance ___%
Testing: ___ completed, avg variance ___%
Documentation: ___ completed, avg variance ___%
Infrastructure: ___ completed, avg variance ___%
Research: ___ completed, avg variance ___%
```

**Trends**:
```
Last 4 weeks average variance: ___%
Improving/Stable/Worsening: ___
Action taken: ___
```

---

## 📝 NOTES

### Why Estimation Standards Matter

1. **Predictability**: Consistent estimates enable reliable planning
2. **Trust**: Accurate estimates build stakeholder trust
3. **Efficiency**: Good estimates prevent overtime and crunch
4. **Quality**: Realistic timelines allow quality work
5. **Continuous Improvement**: Tracking enables learning

### Common Estimation Mistakes

1. **Optimism Bias**: Assuming best case
2. **Forgetting Testing**: Not including test time
3. **Ignoring Dependencies**: Not accounting for blockers
4. **Underestimating Complexity**: "It's just a simple feature"
5. **No Buffer**: Not accounting for unknowns
6. **Peer Pressure": Estimating what others want to hear

### How to Improve Estimation Skills

1. **Track Everything**: Record estimates and actuals
2. **Review Weekly**: Analyze variances, learn patterns
3. **Use Historical Data**: Reference past similar tasks
4. **Break Down Tasks**: Smaller tasks = better estimates
5. **Get Feedback**: Ask others to review your estimates
6. **Be Honest**: Don't promise what you can't deliver

---

**Last Updated**: January 26, 2026
**Next Review**: End of Sprint 0
**Maintained By**: CE-Hub Orchestrator + Michael Durante

**This document is the single source of truth for all RENATA V2 time estimation.**

**All time estimates should follow these standards.**

**When in doubt, be conservative and add buffer.**
