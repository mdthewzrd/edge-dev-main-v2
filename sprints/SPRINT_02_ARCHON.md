# 🧠 SPRINT 2: ARCHON INTEGRATION
## Knowledge Graph Foundation and RAG Implementation

**Duration**: Week 2 (7 days)
**Objective**: Populate Archon knowledge base with V31, Lingua, and existing strategies
**Dependencies**: Sprint 1 (Archon running, platform stable)
**Status**: ⏳ READY TO START AFTER SPRINT 1

---

## 📋 SPRINT OBJECTIVE

Transform Archon from empty database to comprehensive knowledge base. Ingest all critical domain knowledge (V31 Gold Standard, Lingua framework, existing strategies) and validate RAG search functionality. This knowledge base will power all AI agents in subsequent sprints.

---

## 🎯 DELIVERABLES

- [ ] Archon knowledge base populated with core frameworks
- [ ] V31 Gold Standard ingested (searchable)
- [ ] Lingua framework ingested (772 lines)
- [ ] Existing systematized strategies ingested
- [ ] RAG search functional and tested
- [ ] Knowledge validation complete

---

## 📊 DETAILED TASK BREAKDOWN

### Task 2.1: Create Archon MCP Client Wrapper (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Sprint 1 (Archon running)

**Objective**:
Create TypeScript/Python client for interacting with Archon MCP server.

**Architecture**:
```typescript
// /src/services/archon/ArchonMCPClient.ts
export class ArchonMCPClient {
  private endpoint: string;

  constructor(endpoint: string = 'http://localhost:8051') {
    this.endpoint = endpoint;
  }

  // Health Check
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.endpoint}/health`);
    return response.json();
  }

  // Knowledge Ingestion
  async ingestKnowledge(params: {
    type: 'v31_spec' | 'lingua' | 'strategy' | 'pattern';
    content: string;
    metadata: Record<string, any>;
  }): Promise<{ success: boolean; artifact_id: string }> {
    const response = await fetch(`${this.endpoint}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return response.json();
  }

  // RAG Search
  async ragSearch(params: {
    query: string;
    domain?: string;
    limit?: number;
  }): Promise<{ results: any[]; metadata: any }> {
    const response = await fetch(`${this.endpoint}/rag_search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return response.json();
  }

  // Code Examples Search
  async searchCodeExamples(params: {
    pattern: string;
    limit?: number;
  }): Promise<{ examples: any[] }> {
    const response = await fetch(`${this.endpoint}/code_search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return response.json();
  }

  // Project Management
  async createProject(params: {
    name: string;
    description: string;
  }): Promise<{ project_id: string }> {
    const response = await fetch(`${this.endpoint}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return response.json();
  }

  // Task Management
  async createTask(params: {
    project_id: string;
    title: string;
    description: string;
  }): Promise<{ task_id: string }> {
    const response = await fetch(`${this.endpoint}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return response.json();
  }

  async updateTask(taskId: string, updates: any): Promise<void> {
    await fetch(`${this.endpoint}/tasks/${taskId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
  }
}
```

**Subtasks**:
- [ ] Create ArchonMCPClient class
- [ ] Implement healthCheck method
- [ ] Implement ingestKnowledge method
- [ ] Implement ragSearch method
- [ ] Implement searchCodeExamples method
- [ ] Implement project management methods
- [ ] Add TypeScript types
- [ ] Add error handling
- [ ] Add retry logic
- [ ] Test all methods against running Archon

**Files to Create**:
- `/src/services/archon/ArchonMCPClient.ts`
- `/src/services/archon/types.ts`

**Acceptance Criteria**:
- All methods implemented and tested
- Can connect to Archon on port 8051
- Error handling working
- TypeScript types complete

---

### Task 2.2: Ingest V31 Gold Standard (3 hours)
**Owner**: Michael Durante
**Priority**: CRITICAL
**Dependencies**: Task 2.1

**Objective**:
Ingest complete V31 Gold Standard specification into Archon knowledge base.

**Content to Ingest**:
- File: `/projects/edge-dev-main/V31_GOLD_STANDARD_SPECIFICATION.md`
- Size: 950+ lines
- Sections: Architecture, Single-Scan, Multi-Scan, Core Pillars, Stage Requirements, Code Structure, Parameter System, Transformation Rules

**Ingestion Strategy**:
```typescript
const v31Content = await readV31Spec();
const ingestionResult = await archonClient.ingestKnowledge({
  type: 'v31_spec',
  content: v31Content,
  metadata: {
    title: 'V31 Gold Standard Specification',
    version: '1.0',
    date: '2026-01-09',
    status: 'PRODUCTION STANDARD',
    keywords: [
      'v31', 'gold standard', 'scanner architecture',
      'grouped endpoint', 'per-ticker operations',
      'parallel processing', 'smart filters',
      'two-pass features', 'historical buffer'
    ],
    sections: [
      'architecture_overview',
      'single_scan_specification',
      'multi_scan_specification',
      'core_pillars',
      'stage_requirements',
      'code_structure_rules',
      'parameter_system',
      'transformation_rules'
    ]
  }
});

console.log(`V31 ingested with artifact_id: ${ingestionResult.artifact_id}`);
```

**Subtasks**:
- [ ] Read V31 specification file
- [ ] Parse into sections
- [ ] Extract key concepts
- [ ] Create metadata structure
- [ ] Ingest into Archon
- [ ] Verify ingestion success
- [ ] Test RAG search for V31 concepts

**Acceptance Criteria**:
- V31 spec fully ingested
- Search returns relevant V31 content
- Can query specific V31 concepts (e.g., "smart filters")
- Results include section references

---

### Task 2.3: Ingest Lingua Trading Framework (4 hours)
**Owner**: Michael Durante
**Priority**: CRITICAL
**Dependencies**: Task 2.1

**Objective**:
Ingest complete Lingua framework into Archon knowledge base.

**Content to Ingest**:
- File: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes 25ad8836ce438123afedd0b69b25be3f.md`
- Size: 772 lines
- Sections: Trend Cycle, Timeframes, Market Structure, Daily Context, Indicators, Setups, Execution Style

**Ingestion Strategy**:
```typescript
const linguaContent = await readLinguaNotes();
const ingestionResult = await archonClient.ingestKnowledge({
  type: 'lingua_framework',
  content: linguaContent,
  metadata: {
    title: 'Lingua Trading Framework',
    author: 'Michael Durante',
    version: '1.0',
    keywords: [
      'trend cycle', 'consolidation', 'breakout', 'uptrend',
      'extreme deviation', 'euphoric top', 'trend break',
      'backside', 'market structure', 'timeframes',
      'HTF', 'MTF', 'LTF', 'daily context',
      'frontside', 'backside', 'IPO', 'indicators',
      'EMA clouds', 'deviation bands', 'trail',
      'VWAP', 'PDC', 'execution', 'pyramiding'
    ],
    sections: [
      'trend_cycles',
      'timeframes',
      'market_structure',
      'daily_context',
      'indicators',
      'setups',
      'execution_style'
    ],
    setups: [
      'OS D1', 'G2G S1', 'SC DMR', 'SC MDR Swing',
      'Daily Para Run', 'EXT Uptrend Gap', 'Para FRD',
      'MDR', 'LC FBO', 'LC T30', 'LC Extended Trendbreak',
      'LC Breakdown', 'Backside Trend Pop', 'Backside Euphoric'
    ]
  }
});
```

**Subtasks**:
- [ ] Read Lingua notes file
- [ ] Parse into sections
- [ ] Extract all 13 setups
- [ ] Extract indicator systems
- [ ] Create comprehensive metadata
- [ ] Ingest into Archon
- [ ] Verify ingestion success
- [ ] Test RAG search for Lingua concepts

**Acceptance Criteria**:
- Lingua framework fully ingested
- All 13 setups indexed
- Can search for specific setups
- Can search for indicators
- Results include setup references

---

### Task 2.4: Ingest Existing Systematized Strategies (4 hours)
**Owner**: Michael Durante
**Priority**: HIGH
**Dependencies**: Task 2.1

**Objective**:
Ingest all 4 systematized strategies into Archon knowledge base.

**Strategies to Ingest**:

1. **OS D1** (Overnight Scanner D1)
   - File: Locate in projects/edge-dev-main/
   - Type: Systematized
   - Description: Overnight gap setup

2. **G2G S1** (Gap to Go Setup 1)
   - File: Locate in projects/edge-dev-main/
   - Type: Systematized
   - Description: Gap continuation setup

3. **SC DMR** (SC Daily Multiple Range)
   - File: `/backend/standardized_lc_d2_scanner.py`
   - Type: Systematized
   - Description: Multi-pattern scanner

4. **SC MDR Swing** (SC Multi-Day Range Swing)
   - File: Locate in projects/edge-dev-main/
   - Type: Systematized
   - Description: Swing trading variant

**Ingestion Strategy**:
```typescript
const strategies = [
  { name: 'OS D1', file: 'path/to/os_d1.py', type: 'systematized' },
  { name: 'G2G S1', file: 'path/to/g2g_s1.py', type: 'systematized' },
  { name: 'SC DMR', file: 'backend/standardized_lc_d2_scanner.py', type: 'systematized' },
  { name: 'SC MDR Swing', file: 'path/to/sc_mdr_swing.py', type: 'systematized' }
];

for (const strategy of strategies) {
  const code = await readFile(strategy.file);

  // Extract parameters
  const params = extractParameters(code);

  // Extract pattern logic
  const logic = extractPatternLogic(code);

  await archonClient.ingestKnowledge({
    type: 'strategy',
    content: code,
    metadata: {
      name: strategy.name,
      type: strategy.type,
      parameters: params,
      logic: logic,
      timeframe: detectTimeframe(code),
      v31_compliant: checkV31Compliance(code)
    }
  });
}
```

**Subtasks**:
- [ ] Locate all 4 systematized strategy files
- [ ] Parse Python code
- [ ] Extract parameters
- [ ] Extract pattern logic
- [ ] Detect timeframe
- [ ] Check V31 compliance
- [ ] Ingest into Archon
- [ ] Verify all strategies indexed
- [ ] Test search for strategies

**Acceptance Criteria**:
- All 4 strategies ingested
- Parameters extracted and indexed
- Pattern logic indexed
- Can search for strategies by parameter
- Can search for strategies by pattern

---

### Task 2.5: Ingest A+ Examples (3 hours)
**Owner**: Michael Durante
**Priority**: MEDIUM
**Dependencies**: Task 2.1

**Objective**:
Ingest catalog of A+ example charts for pattern matching.

**Content to Ingest**:
- A+ chart images (if available)
- A+ chart breakdowns (text descriptions)
- Parameter sets for each A+ example
- Results from running scans on A+ examples

**Ingestion Strategy**:
```typescript
const aPlusExamples = [
  {
    name: 'NVDA Backside B Example 1',
    date: '2024-11-15',
    description: 'Classic backside setup with euphoric top',
    parameters: {
      gap_over_atr: 0.8,
      open_over_ema9: 0.92,
      vol_mult: 1.2
    },
    result: 'Successful signal'
  },
  // ... more examples
];

for (const example of aPlusExamples) {
  await archonClient.ingestKnowledge({
    type: 'a_plus_example',
    content: example.description,
    metadata: {
      name: example.name,
      date: example.date,
      parameters: example.parameters,
      result: example.result,
      setup_type: detectSetupType(example.description)
    }
  });
}
```

**Subtasks**:
- [ ] Gather A+ examples from Michael's records
- [ ] Extract parameters for each example
- [ ] Extract descriptions
- [ ] Ingest into Archon
- [ ] Tag by setup type
- [ ] Test search for similar examples

**Acceptance Criteria**:
- A+ examples cataloged
- Parameter sets indexed
- Can search for similar examples
- Can retrieve parameters for analysis

---

### Task 2.6: Implement RAG Search Validation (3 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 2.2, 2.3, 2.4

**Objective**:
Create comprehensive test suite for RAG search functionality.

**Test Cases**:

**Test Case 1: V31 Concept Search**
```typescript
const query = "How do I implement smart filters in V31?";
const results = await archonClient.ragSearch({
  query,
  domain: 'v31_spec',
  limit: 5
});

// Validation:
assert(results.length > 0);
assert(results[0].content.includes('smart filters'));
assert(results[0].relevance_score > 0.7);
```

**Test Case 2: Lingua Setup Search**
```typescript
const query = "Explain the euphoric top setup";
const results = await archonClient.ragSearch({
  query,
  domain: 'lingua_framework',
  limit: 3
});

// Validation:
assert(results.length >= 3);
assert(results.some(r => r.content.includes('euphoric top')));
assert(results.every(r => r.relevance_score > 0.6));
```

**Test Case 3: Strategy Similarity Search**
```typescript
const query = "Find strategies that use gap_over_atr parameter";
const results = await archonClient.searchCodeExamples({
  pattern: 'gap_over_atr',
  limit: 10
});

// Validation:
assert(results.length > 0);
assert(results.every(r => r.parameters.gap_over_atr !== undefined));
```

**Test Case 4: Multi-Domain Search**
```typescript
const query = "How do I create a backtest for a mean reversion strategy?";
const results = await archonClient.ragSearch({
  query,
  limit: 5
});

// Should return results from multiple domains:
assert(results.some(r => r.domain === 'lingua_framework'));
assert(results.some(r => r.domain === 'v31_spec'));
```

**Subtasks**:
- [ ] Create test suite structure
- [ ] Implement V31 search tests
- [ ] Implement Lingua search tests
- [ ] Implement strategy search tests
- [ ] Implement multi-domain tests
- [ ] Implement relevance score validation
- [ ] Run all tests
- [ ] Document search quality metrics

**Output**: `/Users/michaeldurante/ai dev/ce-hub/tests/archon/rag_search_validation.test.ts`

**Acceptance Criteria**:
- All test cases pass
- Relevance scores > 0.6 threshold
- Search returns expected results
- Multi-domain search working

---

### Task 2.7: Create Archon-First Workflow Template (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: Task 2.1

**Objective**:
Create template workflow for Archon-First protocol (all agents must follow).

**Template Structure**:
```typescript
// /src/services/workflows/ArchonFirstWorkflow.ts
export class ArchonFirstWorkflow {

  static async execute(userRequest: string): Promise<WorkflowResult> {
    // STEP 1: Sync with Archon (MANDATORY)
    const projectStatus = await archonClient.syncProjectStatus();

    // STEP 2: Search knowledge base
    const similarStrategies = await archonClient.ragSearch({
      query: userRequest,
      domain: 'strategies',
      limit: 5
    });

    const v31Guidance = await archonClient.ragSearch({
      query: userRequest,
      domain: 'v31_spec',
      limit: 3
    });

    // STEP 3: Create or update task
    const task = await archonClient.createTask({
      project_id: projectStatus.current_project,
      title: userRequest,
      description: `Building strategy from: ${userRequest}`
    });

    // STEP 4: Execute workflow with context
    const result = await executeWithContext(
      userRequest,
      similarStrategies,
      v31Guidance
    );

    // STEP 5: Ingest learnings back to Archon
    await archonClient.ingestKnowledge({
      type: 'workflow_result',
      content: result.code,
      metadata: {
        input: userRequest,
        context: {
          similar_strategies: similarStrategies,
          v31_guidance: v31Guidance
        },
        performance: result.metrics
      }
    });

    // STEP 6: Update task status
    await archonClient.updateTask(task.task_id, {
      status: 'complete',
      result: result
    });

    return result;
  }
}
```

**Subtasks**:
- [ ] Create ArchonFirstWorkflow class
- [ ] Implement sync step
- [ ] Implement RAG search steps
- [ ] Implement task tracking
- [ ] Implement learning ingestion
- [ ] Document usage pattern
- [ ] Create examples

**Acceptance Criteria**:
- Template workflow documented
- All agents can follow template
- Archon sync is mandatory first step
- Learnings always ingested back

---

### Task 2.8: Performance Test Archon (2 hours)
**Owner**: Michael Durante
**Priority**: MEDIUM
**Dependencies**: Tasks 2.2-2.4 (knowledge ingested)

**Objective**:
Validate Archon performance under load.

**Tests**:

**Test 1: Single Query Performance**
```typescript
const start = Date.now();
await archonClient.ragSearch({ query: 'test query' });
const duration = Date.now() - start;

assert(duration < 2000, 'RAG search must return in <2s');
```

**Test 2: Concurrent Query Performance**
```typescript
const queries = Array(10).fill('test query');
const start = Date.now();

await Promise.all(
  queries.map(q => archonClient.ragSearch({ query: q }))
);

const duration = Date.now() - start;
assert(duration < 5000, '10 concurrent queries must complete in <5s');
```

**Test 3: Large Dataset Search**
```typescript
const start = Date.now();
await archonClient.ragSearch({
  query: 'complex query with many terms',
  domain: 'all',
  limit: 50
});
const duration = Date.now() - start;

assert(duration < 5000, 'Large search must return in <5s');
```

**Subtasks**:
- [ ] Create performance test suite
- [ ] Run single query tests
- [ ] Run concurrent query tests
- [ ] Run large dataset tests
- [ ] Document performance metrics
- [ ] Identify bottlenecks
- [ ] Optimize if needed

**Acceptance Criteria**:
- Single query <2s
- 10 concurrent queries <5s
- Large search <5s
- No performance degradation under load

---

## 📊 TIME ESTIMATE SUMMARY

| Task | Estimate | Owner |
|------|----------|-------|
| 2.1: Archon MCP client | 4 hours | CE-Hub |
| 2.2: Ingest V31 | 3 hours | Michael |
| 2.3: Ingest Lingua | 4 hours | Michael |
| 2.4: Ingest strategies | 4 hours | Michael |
| 2.5: Ingest A+ examples | 3 hours | Michael |
| 2.6: RAG validation | 3 hours | CE-Hub |
| 2.7: Workflow template | 2 hours | CE-Hub |
| 2.8: Performance test | 2 hours | Michael |
| **TOTAL** | **25 hours (~4 days)** | |

**Sprint Buffer**: Add 8-12 hours for unknowns = ~1 week total

---

## ✅ SPRINT VALIDATION GATE

Sprint 2 is complete when:
- [ ] Archon MCP client functional
- [ ] V31 Gold Standard ingested and searchable
- [ ] Lingua framework ingested and searchable
- [ ] All 4 strategies ingested and searchable
- [ ] A+ examples cataloged
- [ ] RAG search validated (all tests pass)
- [ ] Archon-First workflow template created
- [ ] Performance validated (<2s response time)

**Final Validation**:
Query Archon for "backside b scanner with gap setup" → Receive relevant results from V31 spec, Lingua, and strategy examples.

---

## 🚨 RISKS & MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Archon ingestion fails | Medium | High | Test ingestion early, have manual entry backup |
| RAG search poor quality | Medium | High | Tune embeddings, adjust chunking strategy |
| Performance too slow | Low | Medium | Implement caching, optimize queries |
| Archon unstable | Low | High | Restart daemon, implement watchdog |

**Fallback Plan**:
If Archon fails completely, build simple JSON/Vector DB knowledge base as temporary solution.

---

## 🎯 SUCCESS CRITERIA

Sprint 2 Success means:
- ✅ Knowledge base comprehensive and searchable
- ✅ RAG search returns relevant results (<2s)
- ✅ All domain knowledge ingested
- ✅ Ready to power AI agents (Sprint 4-8)
- ✅ Archon-First protocol established

---

## 📝 NOTES

- **Knowledge base quality determines AI agent quality**
- **Invest time in proper metadata and chunking**
- **Test search queries thoroughly**
- **Archon must be stable before Sprint 3**
- **This is the foundation for all AI intelligence**

---

**Sprint 2 creates the brain for the AI agents.**

**Quality knowledge in = Quality intelligence out.**

**Let's build a comprehensive knowledge base.**
