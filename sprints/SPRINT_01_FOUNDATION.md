# 🚨 SPRINT 1: FOUNDATION REPAIR
## Critical Bug Fixes and Platform Validation

**Duration**: Week 1 (7 days)
**Objective**: Fix critical platform bugs, enable basic workflows, validate infrastructure
**Dependencies**: Sprint 0 (Planning complete)
**Status**: ⏳ READY TO START AFTER SPRINT 0

---

## 📋 SPRINT OBJECTIVE

Fix the three critical bugs preventing EdgeDev from functioning:
1. Hardcoded date bug (scanDate = '2024-02-23')
2. Execution flow disconnect (upload → convert → no execution)
3. Progress tracking deception (7 seconds vs 30+ seconds actual)

Additionally, start Archon MCP server and validate the complete upload → execute → results workflow.

---

## 🎯 DELIVERABLES

- [ ] Hardcoded date bug fixed → Dynamic date selection
- [ ] Execution flow connected → Upload executes on backend
- [ ] Real-time progress tracking → Accurate UI updates
- [ ] Archon MCP running → Responding on port 8051
- [ ] End-to-end workflow validated → Upload → Execute → Results working

---

## 📊 DETAILED TASK BREAKDOWN

### Task 1.1: Fix Hardcoded Date Bug (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: None

**Problem**:
`/src/app/api/systematic/scan/route.ts` has hardcoded date:
```typescript
const scanDate = '2024-02-23';  // 9+ months old!
```

**Solution**:
```typescript
const scanDate = req.body.scanDate ||
                 new Date().toISOString().split('T')[0];

// Add validation
const dateValidation = validateTradingDate(scanDate);
if (!dateValidation.isValid) {
  return NextResponse.json({ error: dateValidation.error }, { status: 400 });
}
```

**Subtasks**:
- [ ] Locate all hardcoded date instances
- [ ] Implement dynamic date selection
- [ ] Add trading date validation
- [ ] Test with recent dates
- [ ] Test with weekend dates (should reject)
- [ ] Test with holiday dates (should reject)

**Files to Modify**:
- `/src/app/api/systematic/scan/route.ts`
- `/src/utils/tradingDays.ts` (validation helper)

**Acceptance Criteria**:
- No hardcoded dates in codebase
- Dynamic date selection working
- Invalid dates properly rejected
- Weekend/holiday validation working

**Testing**:
- Manual test: Run scan with today's date
- Manual test: Run scan with weekend date (should error)
- Manual test: Run scan with future date (should error)

---

### Task 1.2: Fix Execution Flow Disconnect (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: None

**Problem**:
`/src/app/exec/page.tsx` handleStrategyUpload() converts code but never executes:
```typescript
const handleStrategyUpload = async (file: File, code: string) => {
  const convertedStrategy = await converter.convertStrategy(code, file.name);
  setState(prev => ({ ...prev, strategy: convertedStrategy }));
  setShowUpload(false);  // Just closes dialog!
  // Missing: Actual execution call to backend
};
```

**Solution**:
```typescript
const handleStrategyUpload = async (file: File, code: string) => {
  // 1. Convert to V31
  const convertedStrategy = await converter.convertStrategy(code, file.name);

  // 2. Route to FastAPI backend for execution
  const response = await fetch('http://localhost:8000/api/scan/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      scanner_code: convertedStrategy,
      scan_date: new Date().toISOString().split('T')[0],
      scanner_name: file.name
    })
  });

  if (!response.ok) {
    throw new Error(`Execution failed: ${response.statusText}`);
  }

  const executionId = await response.json();

  // 3. Update state with execution info
  setState(prev => ({
    ...prev,
    strategy: convertedStrategy,
    executionId: executionId.scan_id,
    isExecuting: true
  }));

  setShowUpload(false);

  // 4. Start real-time progress tracking
  pollExecutionStatus(executionId.scan_id);
};
```

**Subtasks**:
- [ ] Locate handleStrategyUpload function
- [ ] Add FastAPI execution call
- [ ] Handle execution response
- [ ] Implement execution ID tracking
- [ ] Implement progress polling
- [ ] Test complete flow

**Files to Modify**:
- `/src/app/exec/page.tsx`
- May need to create `/src/services/edgeDevApi.ts` for API calls

**Acceptance Criteria**:
- Upload triggers backend execution
- Execution ID properly tracked
- Progress updates real-time
- Results display after completion

**Testing**:
- Manual test: Upload known good scanner
- Verify execution starts on backend
- Verify progress updates in UI
- Verify results display

---

### Task 1.3: Implement Real-Time Progress Tracking (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 1.2

**Problem**:
Progress bar completes in 7 seconds, actual execution takes 30+ seconds.

**Solution**:
```typescript
// Add execution polling
const pollExecutionStatus = async (executionId: string) => {
  const POLL_INTERVAL = 1000; // 1 second

  const poll = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/scan/status/${executionId}`
      );
      const status = await response.json();

      // Update UI with real progress
      setState(prev => ({
        ...prev,
        executionProgress: status.progress,
        executionStage: status.current_stage,
        isExecuting: status.state === 'running'
      }));

      // Check if complete
      if (status.state === 'complete') {
        setState(prev => ({
          ...prev,
          isExecuting: false,
          executionResults: status.results
        }));
        return; // Stop polling
      }

      // Continue polling
      setTimeout(poll, POLL_INTERVAL);

    } catch (error) {
      console.error('Polling error:', error);
      setTimeout(poll, POLL_INTERVAL);
    }
  };

  poll();
};
```

**Subtasks**:
- [ ] Implement polling function
- [ ] Add progress state management
- [ ] Update UI with real progress
- [ ] Handle completion state
- [ ] Handle error states
- [ ] Test with long-running scan

**Files to Modify**:
- `/src/app/exec/page.tsx`
- `/src/app/scan/page.tsx` (same logic)

**Acceptance Criteria**:
- Progress updates every 1 second
- Progress reflects actual backend status
- UI shows current stage (fetching, filtering, detecting)
- Completion state handled correctly

**Testing**:
- Run scanner and watch progress
- Verify progress matches actual backend work
- Verify completion triggers correctly

---

### Task 1.4: Create Unified API Client (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: None

**Problem**:
API calls scattered throughout codebase, inconsistent error handling.

**Solution**:
```typescript
// /src/services/edgeDevApi.ts
export class EdgeDevAPI {
  private baseUrl = 'http://localhost:8000';

  async executeScanner(params: {
    scannerCode: string;
    scanDate: string;
    scannerName?: string;
  }): Promise<{ scan_id: string }> {
    const response = await fetch(`${this.baseUrl}/api/scan/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error(`Execution failed: ${response.statusText}`);
    }

    return response.json();
  }

  async getExecutionStatus(scanId: string): Promise<ExecutionStatus> {
    const response = await fetch(
      `${this.baseUrl}/api/scan/status/${scanId}`
    );

    if (!response.ok) {
      throw new Error(`Status check failed: ${response.statusText}`);
    }

    return response.json();
  }

  async getExecutionResults(scanId: string): Promise<ScanResults> {
    const response = await fetch(
      `${this.baseUrl}/api/scan/results/${scanId}`
    );

    if (!response.ok) {
      throw new Error(`Results fetch failed: ${response.statusText}`);
    }

    return response.json();
  }
}

interface ExecutionStatus {
  scan_id: string;
  state: 'queued' | 'running' | 'complete' | 'failed';
  progress: number; // 0-100
  current_stage: string;
  results?: ScanResults;
  error?: string;
}

interface ScanResults {
  signals: any[];
  scan_metadata: any;
}
```

**Subtasks**:
- [ ] Create EdgeDevAPI class
- [ ] Implement executeScanner method
- [ ] Implement getExecutionStatus method
- [ ] Implement getExecutionResults method
- [ ] Add TypeScript interfaces
- [ ] Add error handling
- [ ] Add retry logic for failed requests

**Files to Create**:
- `/src/services/edgeDevApi.ts`

**Acceptance Criteria**:
- Unified API client for all backend calls
- Consistent error handling
- TypeScript type safety
- Retry logic for transient failures

---

### Task 1.5: Start Archon MCP Server (3 hours)
**Owner**: Michael Durante
**Priority**: HIGH
**Dependencies**: None

**Problem**:
Archon MCP server not running, knowledge base unavailable.

**Steps**:
1. Navigate to Archon directory
2. Verify dependencies installed
3. Start MCP server on port 8051
4. Verify health endpoint responds

**Commands**:
```bash
# Navigate to Archon
cd /Users/michaeldurante/archon

# Check if mcp_stdio_wrapper.py exists
ls -la mcp_stdio_wrapper.py

# Start MCP server
python mcp_stdio_wrapper.py --port 8051 &

# Wait for startup
sleep 5

# Verify health
curl http://localhost:8051/health

# Expected response: {"status": "healthy"}
```

**Subtasks**:
- [ ] Navigate to Archon directory
- [ ] Verify Archon installation exists
- [ ] Check dependencies installed
- [ ] Start MCP server on port 8051
- [ ] Verify server responds to health check
- [ ] Test basic RAG query
- [ ] Document startup procedure

**Acceptance Criteria**:
- Archon MCP server running on port 8051
- Health endpoint responds
- Can query knowledge base
- Server stable (doesn't crash)

**Testing**:
- Start server
- Run health check
- Run test query
- Leave running for 1 hour, verify stability

**Risks & Mitigations**:
- Risk: Archon doesn't start → Check logs, fix dependencies
- Risk: Port 8051 in use → Kill process or use different port
- Risk: Archon crashes → Check logs, reduce load, restart

---

### Task 1.6: Validate End-to-End Workflow (3 hours)
**Owner**: Michael Durante + CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 1.1, 1.2, 1.3, 1.4, 1.5

**Objective**:
Validate complete workflow: Upload scanner → Execute → View results

**Test Cases**:

**Test Case 1: Upload and Execute Known Good Scanner**
1. Get Backside B scanner (known working)
2. Upload to EdgeDev
3. Verify conversion to V31
4. Execute with today's date
5. Monitor progress updates
6. Verify results display

**Expected Results**:
- Upload succeeds
- Conversion produces V31 code
- Execution starts on backend
- Progress updates accurately
- Results show scan results

**Test Case 2: Invalid Date Handling**
1. Upload scanner
2. Try to execute with weekend date
3. Verify proper error message

**Expected Results**:
- Execution rejected
- Clear error message about invalid date

**Test Case 3: Long-Running Scan**
1. Upload full-market scanner
2. Execute
3. Monitor progress for full duration
4. Verify progress updates every 1-2 seconds

**Expected Results**:
- Progress reflects actual work
- No premature completion
- Final results accurate

**Test Case 4: Error Handling**
1. Upload scanner with syntax error
2. Try to execute
3. Verify graceful error handling

**Expected Results**:
- Error caught and displayed
- No crash
- Clear error message

**Subtasks**:
- [ ] Test Case 1: Known good scanner
- [ ] Test Case 2: Invalid date
- [ ] Test Case 3: Long-running scan
- [ ] Test Case 4: Error handling
- [ ] Document any issues found
- [ ] Fix critical issues
- [ ] Re-test until all pass

**Acceptance Criteria**:
- All test cases pass
- Complete workflow functional
- No critical bugs remaining
- Ready to proceed to Sprint 2

---

### Task 1.7: Document Current Issues (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: Tasks 1.1-1.6

**Objective**:
Document any remaining issues or known limitations for future reference.

**Sections**:
1. Fixed Issues (what we fixed)
2. Known Issues (what remains)
3. Workarounds (how to handle known issues)
4. Technical Debt (what needs refactoring)
5. Performance Observations

**Template**:
```markdown
# Sprint 1 - Current State Report

## Fixed Issues
- [x] Hardcoded date bug → Dynamic dates
- [x] Execution flow → Connected to backend
- [x] Progress tracking → Real-time updates

## Known Issues
- [ ] Issue description
  - Impact: Medium
  - Workaround: Description
  - Planned fix: Sprint X

## Technical Debt
- [ ] Debt description
  - Why it exists
  - Impact
  - Planned refactoring: Sprint X

## Performance Observations
- Current execution time: 315s for full market
- Bottlenecks identified
- Optimization opportunities

## Recommendations
- Short-term improvements
- Long-term improvements
```

**Subtasks**:
- [ ] Document all fixed issues
- [ ] Document any remaining known issues
- [ ] Document workarounds
- [ ] Document technical debt
- [ ] Document performance observations
- [ ] Create recommendations

**Output**: `/Users/michaeldurante/ai dev/ce-hub/SPRINT_1_STATE_REPORT.md`

**Acceptance Criteria**:
- All issues documented
- Workarounds provided
- Technical debt tracked
- Clear recommendations

---

## 📊 TIME ESTIMATE SUMMARY

| Task | Estimate | Owner |
|------|----------|-------|
| 1.1: Fix hardcoded date | 2 hours | CE-Hub |
| 1.2: Fix execution flow | 4 hours | CE-Hub |
| 1.3: Real-time progress | 4 hours | CE-Hub |
| 1.4: Unified API client | 2 hours | CE-Hub |
| 1.5: Start Archon | 3 hours | Michael |
| 1.6: Validate E2E workflow | 3 hours | Both |
| 1.7: Document issues | 2 hours | CE-Hub |
| **TOTAL** | **20 hours (~3 days)** | |

**Sprint Buffer**: Add 4-8 hours for unknowns = ~1 week total

---

## ✅ SPRINT VALIDATION GATE

Sprint 1 is complete when:
- [ ] Hardcoded date bug fixed and tested
- [ ] Execution flow connected and working
- [ ] Real-time progress tracking functional
- [ ] Archon MCP running on port 8051
- [ ] End-to-end workflow validated (all 4 test cases pass)
- [ ] Current state documented
- [ ] No critical blocking issues remaining

**Final Validation**:
Michael uploads a scanner → executes successfully → sees results with accurate progress tracking.

---

## 🚨 RISKS & MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Archon won't start | Medium | High | Check dependencies early, have fallback plan |
| Backend API changes break frontend | Low | High | Test integration early, keep backwards compatible |
| Date validation more complex than expected | Medium | Medium | Use existing tradingDays.ts utilities |
| Progress polling performance issue | Low | Medium | Implement efficient polling, consider WebSocket upgrade |

---

## 🎯 SUCCESS CRITERIA

Sprint 1 Success means:
- ✅ Upload → Execute → Results workflow working end-to-end
- ✅ Dynamic date selection functional
- ✅ Real-time progress tracking accurate
- ✅ Archon MCP running and stable
- ✅ Platform ready for CopilotKit rebuild (Sprint 3)

---

## 📝 NOTES

- **This sprint fixes the critical blockers**
- **Focus on getting basic workflow working**
- **Don't optimize, just make it work**
- **Document everything for future reference**
- **Archon stability is critical for Sprint 2**

---

**Sprint 1 clears the path for systematic AI agent development.**

**Fix the foundation before building the house.**

**Let's get EdgeDev working properly.**
