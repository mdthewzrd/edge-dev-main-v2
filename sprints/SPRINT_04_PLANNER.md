# 🧠 SPRINT 4: PLANNER AGENT
## A+ Example Analysis & Strategy Planning

**Duration**: Weeks 4-5 (14 days)
**Objective**: Build intelligent agent that transforms A+ examples into scanner plans
**Dependencies**: Sprint 2 (Archon ready), Sprint 3 (CopilotKit integrated)
**Status**: ⏳ READY TO START AFTER SPRINT 3

---

## 📋 SPRINT OBJECTIVE

Build the Planner Agent - an intelligent AI agent that works with Michael to transform A+ chart examples into comprehensive scanner build plans. The Planner agent:

1. **Analyzes A+ examples** (charts with breakdowns)
2. **Extracts parameters** from the example
3. **Creates mold parameters** to capture similar setups
4. **Builds systematic plan** for scanner creation
5. **Coordinates with Researcher** to find similar strategies
6. **Presents plan for human approval** before proceeding

This agent embodies Michael's actual A+ analysis workflow that he described earlier.

---

## 🎯 DELIVERABLES

- [ ] Planner agent service created
- [ ] A+ example analysis workflow implemented
- [ ] Parameter extraction from chart breakdowns
- [ ] Mold parameter generation
- [ ] Scanner build plan creation
- [ ] Human approval checkpoints
- [ ] Plan validation and refinement
- [ ] Integration with CopilotKit actions

---

## 📊 MICHAEL'S ACTUAL A+ WORKFLOW (REFERENCE)

As Michael described:

**Phase 1: Initial Analysis**
1. User sends A+ chart with breakdown
2. Together work on parameters that make the mold
3. Analyze A+ setup with potential params
4. Make scan that captures A+ name

**Phase 2: Market Testing**
5. Scan whole market, see how it looks
6. Optimize: add/remove params, dial in the mold
7. Run historical test

**Phase 3: Finalization**
8. Finalize scan

**Phase 4: Execution Logic**
9. Break down ideal execution on A+ names
10. Build backtest that expresses this
11. Analyze executions on A+ names, dial it in
12. Run in-sample test, optimize
13. Run optimized vs OOS to confirm edge
14. Run full backtest
15. Finalize scan and execution process

---

## 📊 DETAILED TASK BREAKDOWN

### Task 4.1: Create Planner Agent Service (6 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Sprint 2 (Archon MCP client)

**Service Structure**:
```typescript
// /src/services/agents/PlannerAgent.ts
export class PlannerAgent {
  private archonClient: ArchonMCPClient;

  constructor() {
    this.archonClient = new ArchonMCPClient('http://localhost:8051');
  }

  async analyzeAPlusExample(params: {
    chartImage?: string;
    breakdown: string;
    setupName: string;
    userNotes?: string;
  }): Promise<APlusAnalysis> {
    // Phase 1: Initial Analysis
    const analysis = await this.analyzeChartBreakdown(params.breakdown);
    const initialParams = await this.extractInitialParams(params.breakdown);
    const similarSetups = await this.findSimilarSetups(params.setupName);

    return {
      setupName: params.setupName,
      breakdownAnalysis: analysis,
      suggestedParameters: initialParams,
      similarSetups: similarSetups,
      recommendedApproach: this.determineApproach(analysis, similarSetups)
    };
  }

  async createScannerPlan(params: {
    aPlusAnalysis: APlusAnalysis;
    userCollaboration: UserCollaboration;
  }): Promise<ScannerBuildPlan> {
    // Phase 2: Create systematic plan
    const moldParameters = await this.generateMoldParameters(params);
    const historicalValidation = await this.validateHistorically(moldParameters);
    const optimizationStrategy = this.planOptimization(moldParameters);

    return {
      moldParameters,
      historicalValidation,
      optimizationStrategy,
      phases: this.defineBuildPhases(),
      estimatedComplexity: this.assessComplexity(moldParameters),
      timeline: this.estimateTimeline()
    };
  }

  async refinePlan(params: {
    plan: ScannerBuildPlan;
    userFeedback: UserFeedback;
  }): Promise<ScannerBuildPlan> {
    // Incorporate user feedback and refine
    return this.iterateOnPlan(params.plan, params.userFeedback);
  }

  // Helper methods
  private async analyzeChartBreakdown(breakdown: string): Promise<ChartAnalysis> {
    // Use AI to analyze the breakdown text
    const response = await fetch('/api/renata/analyze-breakdown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ breakdown })
    });
    return response.json();
  }

  private async extractInitialParams(breakdown: string): Promise<ParameterSet> {
    // Extract parameters mentioned in breakdown
    // Use NLP/AI to identify parameters
  }

  private async findSimilarSetups(setupName: string): Promise<SimilarSetup[]> {
    // Query Archon for similar strategies
    const response = await this.archonClient.ragSearch({
      query: `Similar to ${setupName}`,
      domain: 'strategies',
      limit: 5
    });
    return response.results;
  }

  private determineApproach(analysis: ChartAnalysis, similarSetups: SimilarSetup[]): string {
    // Determine if this is:
    // - Gap setup (needs gap parameters)
    // - Trend following (needs trend parameters)
    // - Mean reversion (needs deviation parameters)
    // - etc.
  }

  private async generateMoldParameters(params: any): Promise<MoldParameters> {
    // Generate initial mold parameters based on A+ analysis
  }

  private planOptimization(params: any): OptimizationStrategy {
    // Plan how to optimize parameters
    return {
      method: 'grid_search', // or 'bayesian_optimization'
      parameters: ['gap_over_atr', 'open_over_ema9', 'vol_mult'],
      validation: 'is_oos_split'
    };
  }

  private defineBuildPhases(): BuildPhase[] {
    return [
      { name: 'Mold Creation', tasks: ['Extract parameters', 'Create initial scan', 'Test on A+ names'] },
      { name: 'Market Scanning', tasks: ['Run on whole market', 'Analyze results', 'Optimize parameters'] },
      { name: 'Historical Testing', tasks: ['Run historical backtest', 'Validate IS/OOS', 'Confirm edge'] },
      { name: 'Execution Logic', tasks: ['Define entry/exit', 'Create backtest', 'Test on A+ names'] },
      { name: 'Final Validation', tasks: ['Full backtest', 'OOS confirmation', 'Finalize'] }
    ];
  }

  private assessComplexity(params: any): 'simple' | 'medium' | 'complex' {
    // Assess complexity based on:
    // - Number of parameters
    // - Execution logic complexity
    // - Timeframe requirements
  }

  private estimateTimeline(): Timeline {
    // Estimate timeline based on complexity
  }
}
```

**Subtasks**:
- [ ] Create PlannerAgent class structure
- [ ] Implement analyzeAPlusExample method
- [ ] Implement createScannerPlan method
- [ ] Implement refinePlan method
- [ ] Add helper methods
- [ ] Define TypeScript interfaces
- [ ] Add error handling
- [ ] Add logging

**Files to Create**:
- `/src/services/agents/PlannerAgent.ts`
- `/src/services/agents/types.ts` (shared types)

**Acceptance Criteria**:
- Planner agent service created
- All core methods implemented
- TypeScript types defined
- Ready for integration

---

### Task 4.2: Implement A+ Example Analysis (8 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 4.1

**Objective**:
Create workflow for analyzing A+ chart examples with breakdowns.

**A+ Example Structure**:
```typescript
interface APlusExample {
  // Chart information
  chartImage?: string; // URL or base64
  ticker: string;
  date: string;
  timeframe: string;

  // Breakdown
  breakdown: string; // User's explanation
  setupName: string; // e.g., "Backside B", "LC D2"

  // User's notes
  userNotes?: string;
  keyObservations?: string[];

  // Context
  marketContext?: string; // Bull, bear, ranging
  dailyContext?: string; // Frontside, backside, IPO
}

interface APlusAnalysis {
  setupName: string;
  breakdownAnalysis: ChartAnalysis;
  suggestedParameters: ParameterSet;
  similarSetups: SimilarSetup[];
  recommendedApproach: string;
  confidence: number; // 0-1
}

interface ChartAnalysis {
  setupType: SetupType;
  keyFeatures: string[];
  patterns: Pattern[];
  marketConditions: MarketConditions;
  timeframe: Timeframe;
}

interface ParameterSet {
  // Mass parameters
  price_min?: number;
  adv20_min_usd?: number;
  volume_min?: number;

  // Setup-specific parameters
  gap_over_atr?: number;
  open_over_ema9?: number;
  vol_mult?: number;
  atr_mult?: number;

  // Trend context
  trend_lookback_days?: number;
  abs_lookback_days?: number;
  abs_exclude_days?: number;

  // Execution parameters
  trigger_mode?: string;
  d1_green_atr_min?: number;
  // ... etc
}

interface SimilarSetup {
  setupName: string;
  similarity: number; // 0-1
  parameters: ParameterSet;
  performance: PerformanceMetrics;
}
```

**Analysis Workflow**:
```typescript
async function analyzeAPlusExample(example: APlusExample): Promise<APlusAnalysis> {
  // Step 1: Parse breakdown
  const analysis = await parseBreakdown(example.breakdown);

  // Step 2: Extract parameters from breakdown
  const params = extractParameters(example.breakdown);

  // Step 3: Search Archon for similar setups
  const similar = await searchArchon(example.setupName, params);

  // Step 4: Determine approach
  const approach = determineApproach(analysis, similar);

  // Step 5: Generate suggested parameters
  const suggestedParams = generateSuggestedParams(analysis, similar);

  return {
    setupName: example.setupName,
    breakdownAnalysis: analysis,
    suggestedParameters: suggestedParams,
    similarSetups: similar,
    recommendedApproach: approach,
    confidence: calculateConfidence(analysis, similar)
  };
}
```

**Subtasks**:
- [ ] Define TypeScript interfaces
- [ ] Implement breakdown parser
- [ ] Implement parameter extractor
- [ ] Implement Archon search integration
- [ ] Implement approach determination logic
- [ ] Implement confidence calculation
- [ ] Add example usage
- [ ] Test with real A+ examples

**Acceptance Criteria**:
- Can analyze A+ chart breakdown
- Extracts parameters accurately
- Finds similar setups from Archon
- Generates reasonable suggestions
- Confidence scores are meaningful

---

### Task 4.3: Implement Mold Parameter Generation (6 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 4.2

**Objective**:
Generate mold parameters that will capture setups similar to the A+ example.

**Mold Parameter Strategy**:
```typescript
interface MoldParameters {
  // Core identification parameters
  core: {
    setupType: 'backside_b' | 'lc_d2' | 'gap_up' | 'mean_reversion';
    triggerConditions: string[];
    contextualRequirements: string[];
  };

  // Flexible parameters (what to vary)
  flexible: {
    // Range-based parameters
    ranges: {
      gap_over_atr: { min: 0.5, max: 1.5, default: 0.75 },
      open_over_ema9: { min: 0.85, max: 0.95, default: 0.90 },
      vol_mult: { min: 0.8, max: 1.5, default: 1.0 },
      // ... more
    };

    // Categorical parameters
    categories: {
      trigger_mode: {
        options: ['D1_or_D2', 'D1_only', 'D2_only'],
        default: 'D1_or_D2'
      },
      d0_gate: {
        options: ['strict', 'moderate', 'flexible'],
        default: 'moderate'
      }
    }
  };

  // Fixed parameters (from A+ example)
  fixed: {
    // These should match the A+ example exactly
    aPlusDate: string;
    aPlusTicker: string;
    exactConditions: string[];
  };

  // Optimization parameters
  optimization: {
    primaryMetric: 'edge_strength' | 'win_rate' | 'risk_reward';
    validationMethod: 'is_oos_split' | 'walk_forward';
    optimizationMethod: 'grid_search' | 'bayesian';
  };
}
```

**Implementation**:
```typescript
async function generateMoldParameters(params: {
  aPlusAnalysis: APlusAnalysis;
  userCollaboration?: UserCollaborationSession;
}): Promise<MoldParameters> {
  // Start with A+ example's exact parameters
  const baseParams = params.aPlusAnalysis.suggestedParameters;

  // Identify which parameters to make flexible
  const flexibleParams = identifyFlexibleParameters(baseParams);

  // Define ranges for flexible parameters
  const ranges = defineParameterRanges(flexibleParams, params.similarSetups);

  // Define optimization strategy
  const optimization = {
    primaryMetric: 'edge_strength',
    validationMethod: 'is_oos_split',
    optimizationMethod: 'grid_search'
  };

  return {
    core: determineCoreSetup(params.aPlusAnalysis),
    flexible: {
      ranges,
      categories: determineCategories(params.aPlusAnalysis)
    },
    fixed: extractFixedParams(baseParams),
    optimization
  };
}
```

**Subtasks**:
- [ ] Define MoldParameters interface
- [ ] Implement parameter range analysis
- [ ] Implement category determination
- [ ] Implement optimization strategy
- [ ] Add validation logic
- [ ] Test with known A+ examples
- [ ] Validate against Michael's workflow

**Acceptance Criteria**:
- Generates reasonable mold parameters
- Ranges are appropriate (not too wide, not too narrow)
- Optimization strategy defined
- Ready for execution phase

---

### Task 4.4: Create Scanner Build Plan Generator (6 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 4.3

**Objective**:
Create systematic plan for building scanner from A+ analysis.

**Plan Structure**:
```typescript
interface ScannerBuildPlan {
  // Phase 1: Mold Creation
  moldCreation: {
    tasks: Task[];
    estimatedTime: string;
    deliverables: string[];
    approvalRequired: boolean;
  };

  // Phase 2: Market Scanning
  marketScanning: {
    tasks: Task[];
    estimatedTime: string;
    deliverables: string[];
    approvalRequired: boolean;
  };

  // Phase 3: Historical Testing
  historicalTesting: {
    tasks: Task[];
    estimatedTime: string;
    deliverables: string[];
    approvalRequired: boolean;
  };

  // Phase 4: Execution Logic
  executionLogic: {
    tasks: Task[];
    estimatedTime: string;
    deliverables: string[];
    approvalRequired: boolean;
  };

  // Phase 5: Final Validation
  finalValidation: {
    tasks: Task[];
    estimatedTime: string;
    deliverables: string[];
    approvalRequired: boolean;
  };

  // Metadata
  metadata: {
    totalEstimatedTime: string;
    complexity: 'simple' | 'medium' | 'complex';
    riskFactors: string[];
    dependencies: string[];
  };
}

interface Task {
  id: string;
  name: string;
  description: string;
  assignee: 'planner' | 'researcher' | 'builder' | 'executor' | 'analyst' | 'user';
  estimatedTime: string;
  dependencies: string[];
  acceptanceCriteria: string[];
}

async function generateScannerBuildPlan(params: {
  aPlusAnalysis: APlusAnalysis;
  moldParameters: MoldParameters;
}): Promise<ScannerBuildPlan> {
  // Phase 1: Mold Creation
  const moldCreation = {
    tasks: [
      {
        id: '1.1',
        name: 'Extract parameters from A+ example',
        description: 'Get exact parameters from A+ example',
        assignee: 'planner',
        estimatedTime: '30 min',
        dependencies: [],
        acceptanceCriteria: ['All parameters extracted', 'Documented in plan']
      },
      {
        id: '1.2',
        name: 'Create initial scanner code',
        description: 'Generate V31 scanner with extracted parameters',
        assignee: 'builder',
        estimatedTime: '2 hours',
        dependencies: ['1.1'],
        acceptanceCriteria: ['V31 compliant code', 'Validated syntax', 'Ready to test']
      },
      {
        id: '1.3',
        name: 'Test on A+ names',
        description: 'Run scanner and verify it captures A+ example',
        assignee: 'executor',
        estimatedTime: '30 min',
        dependencies: ['1.2'],
        acceptanceCriteria: ['Captures A+ setup', 'No false negatives', 'Ready to proceed']
      }
    ],
    estimatedTime: '3 hours',
    deliverables: ['Initial scanner code', 'Test results on A+ names'],
    approvalRequired: true
  };

  // Phase 2: Market Scanning
  const marketScanning = {
    tasks: [
      {
        id: '2.1',
        name: 'Run on whole market',
        description: 'Execute scanner on entire market',
        assignee: 'executor',
        estimatedTime: '2 min',
        dependencies: ['1.3'],
        acceptanceCriteria: ['Scan completes', 'Results collected', 'No errors']
      },
      {
        id: '2.2',
        name: 'Analyze results',
        description: 'Review scanner results, analyze quality',
        assignee: 'analyst',
        estimatedTime: '1 hour',
        dependencies: ['2.1'],
        acceptanceCriteria: ['Results analyzed', 'Quality metrics calculated', 'Issues documented']
      },
      {
        id: '2.3',
        name: 'Optimize parameters',
        description: 'Refine parameters based on results',
        assignee: 'analyst',
        estimatedTime: '2 hours',
        dependencies: ['2.2'],
        acceptanceCriteria: ['Parameters optimized', 'Edge preserved', 'Overfitting avoided']
      }
    ],
    estimatedTime: '3-4 hours',
    deliverables: ['Full market scan results', 'Optimized parameters', 'Analysis report'],
    approvalRequired: true
  };

  // Continue for phases 3-5...

  return {
    moldCreation,
    marketScanning,
    historicalTesting,
    executionLogic,
    finalValidation,
    metadata: {
      totalEstimatedTime: '~10 hours',
      complexity: assessComplexity(params),
      riskFactors: identifyRisks(params),
      dependencies: ['Archon ready', 'Backend stable']
    }
  };
}
```

**Subtasks**:
- [ ] Define plan structure
- [ ] Implement phase generators
- [ ] Implement task breakdown
- [ ] Add time estimation logic
- [ ] Add dependency tracking
- [ ] Add approval checkpoint logic
- [ ] Test plan generation
- [ ] Validate against Michael's actual workflow

**Acceptance Criteria**:
- Generates complete build plan
- Phases match Michael's workflow
- Tasks are clearly defined
- Time estimates reasonable
- Approval checkpoints at key points

---

### Task 4.5: Implement Human Approval Workflow (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 4.4

**Objective**:
Create interactive approval workflow where Michael reviews and approves each phase.

**Workflow**:
```typescript
interface ApprovalCheckpoint {
  phase: string;
  plan: ScannerBuildPlan;
  artifacts: any[];
  questions: string[];
  approvalStatus: 'pending' | 'approved' | 'rejected' | 'modified';
}

async function requestApproval(checkpoint: ApprovalCheckpoint): Promise<ApprovalResult> {
  // Present plan to user
  // Collect questions/concerns
  // Get user decision

  return {
    approved: boolean,
    feedback: string,
    modifications: string[]
  };
}

// Integration with CopilotKit
useCopilotAction({
  name: 'presentPlanForApproval',
  description: 'Present scanner build plan and request user approval',
  parameters: [
    {
      name: 'plan',
      type: 'string',
      description: 'JSON string of ScannerBuildPlan'
    },
    {
      name: 'phase',
      type: 'string',
      description: 'Which phase to approve (e.g., "moldCreation")',
      required: true
    }
  ],
  handler: async ({ plan, phase }) => {
    const checkpoint = {
      phase: phase,
      plan: JSON.parse(plan),
      artifacts: [], // Will be populated
      questions: [], // Will be generated if needed
      approvalStatus: 'pending'
    };

    // Present to UI
    showApprovalModal(checkpoint);

    return {
      success: true,
      checkpoint: checkpoint
    };
  }
});
```

**UI Component**:
```typescript
// /src/components/renata/PlanApprovalModal.tsx
interface PlanApprovalModalProps {
  checkpoint: ApprovalCheckpoint;
  onApprove: () => void;
  onReject: () => void;
  onModify: (modifications: string[]) => void;
}

export function PlanApprovalModal({ checkpoint, onApprove, onReject, onModify }: PlanApprovalModalProps) {
  return (
    <div className="approval-modal">
      <h2>Review Plan: {checkpoint.phase}</h2>

      <div className="plan-details">
        <h3>Tasks:</h3>
        {checkpoint.plan[checkpoint.phase].tasks.map(task => (
          <div key={task.id}>
            <h4>{task.name}</h4>
            <p>{task.description}</p>
            <p><strong>Estimated time:</strong> {task.estimatedTime}</p>
            <p><strong>Assignee:</strong> {task.assignee}</p>
          </div>
        ))}
      </div>

      <div className="approval-section">
        <h3>Do you approve this phase?</h3>
        <button onClick={() => onApprove()}>✅ Approve</button>
        <button onClick={() => onModify()}>✏️ Modify</button>
        <button onClick={() => onReject()}>❌ Reject</button>
      </div>
    </div>
  );
}
```

**Subtasks**:
- [ ] Define approval workflow
- [ ] Create ApprovalCheckpoint interface
- [ ] Implement requestApproval function
- [ ] Register CopilotKit action
- [ ] Create PlanApprovalModal component
- [ ] Style approval modal (clean, intuitive)
- [ ] Test approval workflow
- [ ] Test modification workflow
- [ ] Test rejection workflow

**Files to Create**:
- `/src/components/renata/PlanApprovalModal.tsx`
- `/src/components/renata/PlanApprovalModal.module.css`

**Acceptance Criteria**:
- Approval modal displays clearly
- User can approve, modify, or reject
- Modifications fed back to Planner agent
- Workflow is intuitive

---

### Task 4.6: Integrate with Researcher Agent (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: Task 4.1, Sprint 5 (Researcher Agent)

**Objective**:
Planner coordinates with Researcher to find similar strategies and patterns.

**Coordination**:
```typescript
async function createScannerPlanWithResearch(params: {
  aPlusExample: APlusExample;
}): Promise<ScannerBuildPlan> {
  // 1. Initial analysis
  const initialAnalysis = await this.analyzeAPlusExample(params);

  // 2. Consult Researcher for similar strategies
  const similarStrategies = await this.researcherAgent.findSimilarStrategies({
    setupName: params.aPlusExample.setupName,
    parameters: initialAnalysis.suggestedParameters
  });

  // 3. Incorporate findings into plan
  const enhancedPlan = this.enhancePlanWithResearch(initialAnalysis, similarStrategies);

  return enhancedPlan;
}
```

**Subtasks**:
- [ ] Define ResearcherAgent interface
- [ ] Implement coordination workflow
- [ ] Add Archon RAG calls
- [ ] Integrate similar strategy findings
- [ ] Test coordination
- [ ] Document handoff protocol

**Acceptance Criteria**:
- Planner can call Researcher
- Researcher results integrated into plans
- Handoff is smooth
- No context loss

---

### Task 4.7: Test Complete A+ Workflow (6 hours)
**Owner**: Michael Durante + CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 4.1-4.6

**End-to-End Test**:
```
Input: A+ chart example with breakdown

Phase 1: Analysis
1. Renata analyzes breakdown
2. Renata extracts parameters
3. Renata searches Archon for similar setups
4. Renata presents initial plan

User: Review and approve plan (with modifications)

Phase 2: Mold Creation
5. Renata creates scanner code
6. Renata tests on A+ names
7. Results presented

User: Approve and proceed

Phase 3: Market Scanning
8. Renata runs whole market scan
9. Results presented with analysis

User: Review and optimize parameters

Phase 4: Execution Logic
10. Renata helps define entry/exit
11. Backtest created
12. Tested on A+ names

Phase 5: Final Validation
13. Full backtest run
14. OOS validation
15. Final scanner + execution complete
```

**Subtasks**:
- [ ] Test with real A+ example
- [ ] Test approval workflow
- [ ] Test modification workflow
- [ ] Test rejection workflow
- [ ] Test agent coordination
- [ ] Validate results match expectations
- [ ] Document any issues

**Output**: `/Users/michaeldurante/ai dev/ce-hub/projects/edge-dev-main/RENATA_2026/SPRINT_4_TEST_RESULTS.md`

**Acceptance Criteria**:
- Complete workflow functional
- Matches Michael's actual process
- Approval checkpoints work
- Agent coordination smooth
- Results accurate

---

### Task 4.8: Create Planner CopilotKit Action (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 4.1-4.7

**CopilotKit Action Registration**:
```typescript
// In RenataV2Sidebar component

useCopilotAction({
  name: 'planScannerFromAPlus',
  description: 'Plan scanner build from A+ example with breakdown',
  parameters: [
    {
      name: 'chartBreakdown',
      type: 'string',
      description: 'Full breakdown of the setup from the chart',
      required: true
    },
    {
      name: 'setupName',
      type: 'string',
      description: 'Name of the setup (e.g., "Backside B", "LC D2")',
      required: true
    },
    {
      name: 'userNotes',
      type: 'string',
      description: 'Any additional notes or observations',
      required: false
    }
  ],
  handler: async ({ chartBreakdown, setupName, userNotes }) => {
    // Call Planner agent
    const plan = await plannerAgent.analyzeAPlusExample({
      breakdown: chartBreakdown,
      setupName: setupName
    });

    // Present plan to user
    showPlanModal(plan);

    return {
      success: true,
      plan: plan
    };
  }
});
```

**Subtasks**:
- [ ] Register CopilotKit action
- [ ] Connect to PlannerAgent service
- [ ] Implement plan presentation UI
- [ ] Test action with real A+ example
- [ ] Validate plan format

**Acceptance**:
- Action registered in CopilotKit
- Can be called from chat
- Planner agent executes
- Plan presented clearly

---

## 📊 TIME ESTIMATE SUMMARY

| Task | Estimate | Owner |
|------|----------|-------|
| 4.1: Create Planner service | 6 hours | CE-Hub |
| 4.2: A+ analysis workflow | 8 hours | CE-Hub |
| 4.3: Mold parameters | 6 hours | CE-Hub |
| 4.4: Build plan generator | 6 hours | CE-Hub |
| 4.5: Approval workflow | 4 hours | CE-Hub |
| 4.6: Researcher integration | 4 hours | CE-Hub |
| 4.7: Test complete workflow | 6 hours | Both |
| 4.8: CopilotKit action | 2 hours | CE-Hub |
| **TOTAL** | **42 hours (~6 days)** | |

**Sprint Buffer**: Add 8-12 hours for unknowns = ~7 days (1 week)

**Actual Duration**: Weeks 4-5 (14 days) allows for parallel work and buffer

---

## ✅ SPRINT VALIDATION GATE

Sprint 4 is complete when:
- [ ] Planner agent service created
- [ ] A+ analysis workflow functional
- [ ] Mold parameters generated accurately
- [ ] Scanner build plans created systematically
- [ ] Human approval workflow working
- [ ] Researcher agent integration working
- [ ] Complete A+ workflow tested end-to-end
- [ ] Results match Michael's actual process

**Final Validation**:
Michael takes an A+ example from his files → Renata analyzes it → presents plan → Michael approves → Renata executes plan → produces scanner ready for optimization.

---

## 🚨 RISKS & MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Parameter extraction inaccurate | Medium | High | Test with known examples, refine with feedback |
| Plan doesn't match Michael's workflow | Medium | High | Continuous validation, Michael reviews each phase |
| Agent coordination fails | Low | Medium | Test integration thoroughly, have fallback |
| Approval workflow too rigid | Low | Medium | Make it flexible, allow modifications |

---

## 🎯 SUCCESS CRITERIA

Sprint 4 Success means:
- ✅ Can analyze A+ chart breakdowns
- ✅ Extracts parameters intelligently
- ✅ Finds similar strategies from Archon
- ✅ Creates systematic build plans
- ✅ Approval workflow intuitive
- ✅ Matches Michael's actual workflow
- ✅ Ready for Builder agent to execute plans

---

## 📝 NOTES

- **This sprint embodies Michael's actual A+ workflow**
- **Approval checkpoints are critical - Michael stays in control**
- **Plans are systematic and actionable**
- **Coordination with Researcher agent enhances plans**
- **Flexible workflow allows iteration and refinement**

---

**Sprint 4 brings Michael's actual workflow to the AI platform.**

**The Planner agent becomes Michael's AI assistant for strategy planning.**

**Let's build this right.**
