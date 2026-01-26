# 🧪 SPRINT 9: INTEGRATION TESTING
## End-to-End Workflow Validation

**Duration**: Weeks 9-10 (14 days)
**Objective**: Validate all three priority workflows end-to-end, test agent coordination, perform system integration testing, and ensure production readiness

**Success Criteria**:
- [ ] A+ Example → Scanner workflow validated
- [ ] Code Transform → Scanner workflow validated
- [ ] Idea → Scanner workflow validated
- [ ] All agent coordination tested
- [ ] Performance benchmarks met
- [ ] System stability verified
- [ ] Production readiness confirmed

---

## 📋 DELIVERABLES

### Core Deliverables
- [ ] Complete workflow test suite
- [ ] End-to-end integration tests
- [ ] Agent coordination validation
- [ ] Performance test suite
- [ ] Load testing results
- [ ] Security validation
- [ ] User acceptance testing
- [ ] Production deployment checklist

### Integration Points
- **All Agents**: Planner, Researcher, Builder, Executor, Analyst
- **All Workflows**: A+ Example, Code Transform, Idea → Scanner
- **All Systems**: Archon, CopilotKit, FastAPI, Next.js

---

## 🎯 DETAILED TASKS

### Task 9.1: Test A+ Example → Scanner Workflow (8 hours)

**Subtasks**:
1. Create end-to-end test for A+ workflow
2. Test Planner agent analysis
3. Test Researcher agent pattern matching
4. Test Builder agent code generation
5. Test Executor agent A+ name testing
6. Test Analyst agent validation
7. Validate complete workflow
8. Document workflow execution time

**Code Example**:
```typescript
// src/tests/integration/aPlusWorkflow.test.ts

import { PlannerAgent } from '../../services/plannerAgent';
import { ResearcherAgent } from '../../services/researcherAgent';
import { BuilderAgent } from '../../services/builderAgent';
import { ExecutorAgent } from '../../services/executorAgent';
import { AnalystAgent } from '../../services/analystAgent';

describe('A+ Example → Scanner Workflow', () => {
  let planner: PlannerAgent;
  let researcher: ResearcherAgent;
  let builder: BuilderAgent;
  let executor: ExecutorAgent;
  let analyst: AnalystAgent;

  beforeEach(() => {
    planner = new PlannerAgent();
    researcher = new ResearcherAgent();
    builder = new BuilderAgent();
    executor = new ExecutorAgent();
    analyst = new AnalystAgent();
  });

  test('Complete A+ workflow: OS D1 example', async () => {
    // Step 1: Analyze A+ example
    const aPlusExample = {
      setupName: 'OS D1',
      breakdown: `
        Entry: Price closes > 2.5 SD below lower EMA cloud (20/50)
        Exit: Price closes above EMA 20
        Stop: 2x ATR below entry
        Target: Return to cloud midline
      `,
      aPlusNames: ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA'],
      dateRange: { start: '2024-01-01', end: '2024-12-31' }
    };

    console.log('Step 1: Analyzing A+ example...');
    const plan = await planner.analyzeAPlusExample(aPlusExample);

    expect(plan.setupName).toBe('OS D1');
    expect(plan.suggestedParameters).toBeDefined();
    expect(plan.confidence).toBeGreaterThan(0.7);
    console.log(`✓ Plan created with confidence: ${plan.confidence}`);

    // Step 2: Research similar strategies
    console.log('\nStep 2: Researching similar strategies...');
    const research = await researcher.research({
      query: 'OS D1 oversold daily setup',
      domain: 'scanner',
      setupType: 'OS D1'
    });

    expect(research.relevantStrategies.length).toBeGreaterThan(0);
    expect(research.relevantPatterns.length).toBeGreaterThan(0);
    console.log(`✓ Found ${research.relevantStrategies.length} similar strategies`);
    console.log(`✓ Detected ${research.relevantPatterns.length} patterns`);

    // Step 3: Build scanner from A+ mold
    console.log('\nStep 3: Building scanner from A+ mold...');
    const buildResult = await builder.build({
      type: 'mold',
      input: {
        setupName: aPlusExample.setupName,
        breakdown: aPlusExample.breakdown,
        aPlusNames: aPlusExample.aPlusNames
      }
    });

    expect(buildResult.scannerCode).toBeDefined();
    expect(buildResult.v31Compliant).toBe(true);
    expect(buildResult.validationResults.every(v => v.compliant || v.severity !== 'critical')).toBe(true);
    console.log(`✓ Scanner built, V31 compliant: ${buildResult.v31Compliant}`);
    console.log(`✓ Quality score: ${Math.round(buildResult.qualityScore * 100)}%`);

    // Step 4: Test on A+ names
    console.log('\nStep 4: Testing on A+ names...');
    const execution = await executor.execute({
      scannerCode: buildResult.scannerCode,
      scannerName: `OS_D1_${Date.now()}`,
      executionType: 'test',
      aPlusNames: aPlusExample.aPlusNames,
      dateRange: aPlusExample.dateRange
    });

    expect(execution.status).toBe('completed');
    expect(execution.results).toBeDefined();
    expect(execution.results!.length).toBeGreaterThan(0);
    console.log(`✓ Execution completed`);
    console.log(`✓ Found ${execution.results!.length} signals from A+ names`);

    // Step 5: Analyze results
    console.log('\nStep 5: Analyzing results...');
    const analysis = await analyst.analyze({
      backtestId: execution.executionId,
      analysisType: 'performance'
    });

    expect(analysis.metrics).toBeDefined();
    expect(analysis.insights.length).toBeGreaterThan(0);
    expect(analysis.recommendations.length).toBeGreaterThan(0);
    console.log(`✓ Analysis complete`);
    console.log(`✓ Sharpe Ratio: ${analysis.metrics.sharpeRatio.toFixed(2)}`);
    console.log(`✓ Win Rate: ${(analysis.metrics.winRate * 100).toFixed(1)}%`);

    // Validate workflow success
    console.log('\n✅ COMPLETE A+ WORKFLOW VALIDATED');
    console.log(`Total execution time: ${execution.endTime!.getTime() - execution.startTime.getTime()}ms`);
  }, 120000); // 2 minute timeout

  test('A+ workflow: G2G S1 example', async () => {
    const aPlusExample = {
      setupName: 'G2G S1',
      breakdown: `
        Entry: Gap up into resistance zone
        Exit: Gap fill or target hit
        Stop: Below gap low
        Target: Prior high
      `,
      aPlusNames: ['AMD', 'META', 'AMZN'],
      dateRange: { start: '2024-01-01', end: '2024-12-31' }
    };

    // Run complete workflow
    const plan = await planner.analyzeAPlusExample(aPlusExample);
    expect(plan.setupName).toBe('G2G S1');

    const buildResult = await builder.build({
      type: 'mold',
      input: aPlusExample
    });

    expect(buildResult.v31Compliant).toBe(true);

    const execution = await executor.execute({
      scannerCode: buildResult.scannerCode,
      scannerName: `G2G_S1_${Date.now()}`,
      executionType: 'test',
      aPlusNames: aPlusExample.aPlusNames,
      dateRange: aPlusExample.dateRange
    });

    expect(execution.status).toBe('completed');
  }, 120000);
});
```

**Acceptance Criteria**:
- [ ] A+ workflow test passes for OS D1
- [ ] A+ workflow test passes for G2G S1
- [ ] A+ workflow test passes for SC DMR
- [ ] A+ workflow test passes for Backside B
- [ ] All 5 agents coordinate successfully
- [ ] Workflow completes in <2 minutes
- [ ] V31 compliance maintained throughout

**Dependencies**:
- All agents built (Sprints 4-8)

**Risks**:
- **Risk**: Workflow fails mid-execution
  - **Mitigation**: Checkpoint/resume, error recovery

---

### Task 9.2: Test Code Transform → Scanner Workflow (6 hours)

**Subtasks**:
1. Create end-to-end test for transform workflow
2. Test non-V31 scanner detection
3. Test V31 transformation
4. Test transformed scanner execution
5. Test result comparison
6. Validate improvement

**Code Example**:
```typescript
// src/tests/integration/transformWorkflow.test.ts

describe('Code Transform → Scanner Workflow', () => {
  let researcher: ResearcherAgent;
  let builder: BuilderAgent;
  let executor: ExecutorAgent;
  let analyst: AnalystAgent;

  beforeEach(() => {
    researcher = new ResearcherAgent();
    builder = new BuilderAgent();
    executor = new ExecutorAgent();
    analyst = new AnalystAgent();
  });

  test('Transform non-V31 scanner to V31', async () => {
    // Non-V31 scanner code (old architecture)
    const nonV31Scanner = `
def scan(data):
    # Single function, no grouped endpoint
    data['ema_20'] = data['close'].ewm(span=20).mean()
    data['ema_50'] = data['close'].ewm(span=50).mean()
    data['signal'] = (data['close'] > data['ema_20']) & (data['close'] > data['ema_50'])
    return data[data['signal']]
    `.trim();

    console.log('Step 1: Detecting V31 violations...');
    const transformer = new V31Transformer();
    const violations = await transformer['validator'].identifyViolations(nonV31Scanner);

    expect(violations.length).toBeGreaterThan(0);
    console.log(`✓ Detected ${violations.length} V31 violations`);

    // Step 2: Transform to V31
    console.log('\nStep 2: Transforming to V31...');
    const transformResult = await transformer.transformToV31({
      existingCode: nonV31Scanner,
      scannerName: 'Test_Scanner'
    });

    expect(transformResult.v31Compliant).toBe(true);
    expect(transformResult.changes.length).toBeGreaterThan(0);
    console.log(`✓ Transformed to V31`);
    console.log(`✓ Applied ${transformResult.changes.length} changes`);

    // Step 3: Validate transformed code
    console.log('\nStep 3: Validating transformed code...');
    const validation = await transformer['validator'].validate(transformResult.transformedCode);

    const criticalIssues = validation.filter(v => v.severity === 'critical');
    expect(criticalIssues.length).toBe(0);
    console.log(`✓ No critical V31 violations`);

    // Step 4: Execute both scanners and compare
    console.log('\nStep 4: Executing and comparing...');
    const tickers = ['AAPL', 'MSFT', 'GOOGL'];
    const dateRange = { start: '2024-01-01', end: '2024-03-31' };

    // Execute original
    const originalExecution = await executor.execute({
      scannerCode: nonV31Scanner,
      scannerName: 'Original_Scanner',
      executionType: 'scan',
      tickers,
      dateRange
    });

    // Execute transformed
    const transformedExecution = await executor.execute({
      scannerCode: transformResult.transformedCode,
      scannerName: 'Transformed_Scanner_V31',
      executionType: 'scan',
      tickers,
      dateRange
    });

    expect(originalExecution.status).toBe('completed');
    expect(transformedExecution.status).toBe('completed');
    console.log(`✓ Both scanners executed successfully`);
    console.log(`Original signals: ${originalExecution.results?.length || 0}`);
    console.log(`Transformed signals: ${transformedExecution.results?.length || 0}`);

    // Step 5: Analyze improvement
    console.log('\nStep 5: Analyzing improvement...');
    const originalAnalysis = await analyst.analyze({
      backtestId: originalExecution.executionId,
      analysisType: 'performance'
    });

    const transformedAnalysis = await analyst.analyze({
      backtestId: transformedExecution.executionId,
      analysisType: 'performance'
    });

    console.log(`Original Sharpe: ${originalAnalysis.metrics.sharpeRatio.toFixed(2)}`);
    console.log(`Transformed Sharpe: ${transformedAnalysis.metrics.sharpeRatio.toFixed(2)}`);

    console.log('\n✅ TRANSFORM WORKFLOW VALIDATED');
  }, 120000);
});
```

**Acceptance Criteria**:
- [ ] Transform workflow test passes
- [ ] Non-V31 violations detected correctly
- [ ] Transformation produces V31-compliant code
- [ ] Transformed scanner executes successfully
- [ ] Results improved or maintained

**Dependencies**:
- All agents built (Sprints 4-8)

**Risks**:
- **Risk**: Transformation breaks scanner logic
  - **Mitigation**: Side-by-side comparison, manual validation

---

### Task 9.3: Test Idea → Scanner Workflow (6 hours)

**Subtasks**:
1. Create end-to-end test for idea workflow
2. Test natural language parsing
3. Test parameter extraction
4. Test code generation
5. Test execution and validation
6. Test iteration and refinement

**Code Example**:
```typescript
// src/tests/integration/ideaWorkflow.test.ts

describe('Idea → Scanner Workflow', () => {
  let researcher: ResearcherAgent;
  let builder: BuilderAgent;
  let executor: ExecutorAgent;
  let analyst: AnalystAgent;

  beforeEach(() => {
    researcher = new ResearcherAgent();
    builder = new BuilderAgent();
    executor = new ExecutorAgent();
    analyst = new AnalystAgent();
  });

  test('Generate scanner from natural language idea', async () => {
    const idea = {
      description: `
        I want to scan for oversold conditions on the daily timeframe.
        The stock should be trading at least 2.5 standard deviations below the 20/50 EMA cloud.
        Volume should be above 1.5x average.
        RSI should be below 30.
        Only look at tech stocks with market cap > 1B.
      `,
      setupType: 'OS D1',
      requirements: [
        'V31 compliant',
        'Per-ticker operations',
        'Smart filtering'
      ]
    };

    console.log('Step 1: Researching similar strategies...');
    const research = await researcher.research({
      query: idea.description,
      domain: 'scanner',
      setupType: idea.setupType
    });

    expect(research.relevantStrategies.length).toBeGreaterThan(0);
    console.log(`✓ Found ${research.relevantStrategies.length} similar strategies`);

    // Step 2: Generate scanner from idea
    console.log('\nStep 2: Generating scanner from idea...');
    const buildResult = await builder.build({
      type: 'idea',
      input: {
        description: idea.description,
        requirements: idea.requirements
      },
      setupType: idea.setupType
    });

    expect(buildResult.scannerCode).toBeDefined();
    expect(buildResult.v31Compliant).toBe(true);
    console.log(`✓ Scanner generated from idea`);
    console.log(`✓ V31 compliant: ${buildResult.v31Compliant}`);

    // Step 3: Test generated scanner
    console.log('\nStep 3: Testing generated scanner...');
    const tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'];
    const execution = await executor.execute({
      scannerCode: buildResult.scannerCode,
      scannerName: `Idea_Generated_${Date.now()}`,
      executionType: 'scan',
      tickers,
      dateRange: { start: '2024-01-01', end: '2024-03-31' }
    });

    expect(execution.status).toBe('completed');
    console.log(`✓ Scanner executed successfully`);
    console.log(`✓ Found ${execution.results?.length || 0} signals`);

    // Step 4: Analyze and get recommendations
    console.log('\nStep 4: Analyzing results...');
    const analysis = await analyst.analyze({
      backtestId: execution.executionId,
      analysisType: 'performance'
    });

    expect(analysis.insights.length).toBeGreaterThan(0);
    expect(analysis.recommendations.length).toBeGreaterThan(0);
    console.log(`✓ Generated ${analysis.insights.length} insights`);
    console.log(`✓ Generated ${analysis.recommendations.length} recommendations`);

    // Display top recommendations
    console.log('\nTop recommendations:');
    analysis.recommendations.slice(0, 3).forEach((rec, i) => {
      console.log(`  ${i + 1}. [${rec.priority}] ${rec.action}`);
    });

    console.log('\n✅ IDEA WORKFLOW VALIDATED');
  }, 120000);

  test('Generate scanner from vague idea with refinement', async () => {
    const vagueIdea = {
      description: 'Find me stocks that are oversold and ready to bounce',
      setupType: undefined
    };

    console.log('Testing vague idea handling...');

    // Research should provide clarification
    const research = await researcher.research({
      query: vagueIdea.description,
      domain: 'scanner'
    });

    expect(research.relevantStrategies.length).toBeGreaterThan(0);
    console.log(`✓ Research provided ${research.relevantStrategies.length} template strategies`);

    // Build with generic template
    const buildResult = await builder.build({
      type: 'idea',
      input: vagueIdea
    });

    expect(buildResult.scannerCode).toBeDefined();
    console.log(`✓ Generated scanner from vague idea using generic template`);
  }, 120000);
});
```

**Acceptance Criteria**:
- [ ] Idea workflow test passes
- [ ] Natural language parsed correctly
- [ ] Scanner generated from idea
- [ ] Generated scanner executes
- [ ] Recommendations provided for refinement

**Dependencies**:
- All agents built (Sprints 4-8)

**Risks**:
- **Risk**: Vague ideas produce poor scanners
  - **Mitigation**: Interactive clarification, template fallback

---

### Task 9.4: Test Agent Coordination (5 hours)

**Subtasks**:
1. Create agent handoff tests
2. Test context preservation
3. Test parallel execution
4. Test error propagation
5. Test resource management
6. Validate agent communication

**Code Example**:
```typescript
// src/tests/integration/agentCoordination.test.ts

describe('Agent Coordination', () => {
  test('Planner → Researcher handoff preserves context', async () => {
    const planner = new PlannerAgent();
    const researcher = new ResearcherAgent();

    // Planner creates plan
    const plan = await planner.analyzeAPlusExample({
      setupName: 'OS D1',
      breakdown: 'Entry: Oversold conditions',
      aPlusNames: ['AAPL', 'MSFT'],
      dateRange: { start: '2024-01-01', end: '2024-12-31' }
    });

    // Researcher receives context from planner
    const research = await researcher.research({
      query: plan.setupName,
      domain: 'scanner',
      setupType: plan.setupName,
      parameters: plan.suggestedParameters
    });

    // Verify context preserved
    expect(research.relevantStrategies.length).toBeGreaterThan(0);
    console.log('✓ Planner → Researcher handoff successful');
  });

  test('Researcher → Builder handoff provides templates', async () => {
    const researcher = new ResearcherAgent();
    const builder = new BuilderAgent();

    // Researcher finds similar strategies
    const research = await researcher.research({
      query: 'OS D1',
      domain: 'scanner',
      setupType: 'OS D1'
    });

    // Builder receives research insights
    const buildResult = await builder.build({
      type: 'mold',
      input: {
        setupName: 'OS D1',
        breakdown: 'Entry: Oversold',
        aPlusNames: ['AAPL']
      }
    });

    // Verify research used in build
    expect(buildResult.scannerCode).toBeDefined();
    console.log('✓ Researcher → Builder handoff successful');
  });

  test('Builder → Executor → Analyst pipeline', async () => {
    const builder = new BuilderAgent();
    const executor = new ExecutorAgent();
    const analyst = new AnalystAgent();

    // Builder creates scanner
    const buildResult = await builder.build({
      type: 'idea',
      input: { description: 'Simple RSI scanner' }
    });

    // Executor runs scanner
    const execution = await executor.execute({
      scannerCode: buildResult.scannerCode,
      scannerName: 'Test_Scanner',
      executionType: 'scan',
      tickers: ['AAPL'],
      dateRange: { start: '2024-01-01', end: '2024-03-31' }
    });

    // Analyst analyzes results
    const analysis = await analyst.analyze({
      backtestId: execution.executionId,
      analysisType: 'performance'
    });

    // Verify pipeline success
    expect(buildResult.v31Compliant).toBe(true);
    expect(execution.status).toBe('completed');
    expect(analysis.metrics).toBeDefined();
    console.log('✓ Builder → Executor → Analyst pipeline successful');
  });

  test('Parallel agent execution', async () => {
    const researcher1 = new ResearcherAgent();
    const researcher2 = new ResearcherAgent();
    const builder = new BuilderAgent();

    // Run research in parallel
    const [research1, research2] = await Promise.all([
      researcher1.research({ query: 'OS D1', domain: 'scanner' }),
      researcher2.research({ query: 'G2G S1', domain: 'scanner' })
    ]);

    expect(research1.relevantStrategies.length).toBeGreaterThan(0);
    expect(research2.relevantStrategies.length).toBeGreaterThan(0);

    // Builder uses both research results
    const build1 = builder.build({
      type: 'idea',
      input: { description: 'OS D1 scanner' }
    });

    const build2 = builder.build({
      type: 'idea',
      input: { description: 'G2G S1 scanner' }
    });

    const [result1, result2] = await Promise.all([build1, build2]);

    expect(result1.v31Compliant).toBe(true);
    expect(result2.v31Compliant).toBe(true);
    console.log('✓ Parallel agent execution successful');
  });

  test('Error propagation across agents', async () => {
    const builder = new BuilderAgent();
    const executor = new ExecutorAgent();

    // Builder generates invalid code
    const invalidCode = 'def invalid():\n    syntax error';

    // Executor should handle gracefully
    try {
      const execution = await executor.execute({
        scannerCode: invalidCode,
        scannerName: 'Invalid_Scanner',
        executionType: 'test',
        aPlusNames: ['AAPL'],
        dateRange: { start: '2024-01-01', end: '2024-12-31' }
      });

      // Should fail gracefully
      expect(execution.status).toBe('failed');
      expect(execution.error).toBeDefined();
      console.log('✓ Error propagated correctly');
    } catch (error) {
      console.log('✓ Error caught and handled');
    }
  });
});
```

**Acceptance Criteria**:
- [ ] All agent handoffs work
- [ ] Context preserved across agents
- [ ] Parallel execution supported
- [ ] Errors propagated correctly
- [ ] No memory leaks or resource issues

**Dependencies**:
- All agents built (Sprints 4-8)

**Risks**:
- **Risk**: Context loss during handoff
  - **Mitigation**: Explicit context passing, validation

---

### Task 9.5: Performance Testing (5 hours)

**Subtasks**:
1. Define performance benchmarks
2. Test API response times
3. Test scanner execution speed
4. Test database query performance
5. Test WebSocket latency
6. Generate performance report

**Code Example**:
```typescript
// src/tests/performance/benchmarks.test.ts

describe('Performance Benchmarks', () => {
  test('API response times', async () => {
    const benchmarks = {
      research: '< 3s',
      build: '< 10s',
      execute: '< 30s',
      analyze: '< 5s'
    };

    console.log('Testing API response times...');

    // Test research API
    const researchStart = Date.now();
    const researcher = new ResearcherAgent();
    await researcher.research({ query: 'OS D1', domain: 'scanner' });
    const researchTime = Date.now() - researchStart;

    console.log(`Research API: ${researchTime}ms (target: ${benchmarks.research})`);
    expect(researchTime).toBeLessThan(3000);

    // Test build API
    const buildStart = Date.now();
    const builder = new BuilderAgent();
    await builder.build({
      type: 'idea',
      input: { description: 'Test scanner' }
    });
    const buildTime = Date.now() - buildStart;

    console.log(`Build API: ${buildTime}ms (target: ${benchmarks.build})`);
    expect(buildTime).toBeLessThan(10000);

    console.log('✅ All API response times within targets');
  });

  test('Scanner execution performance', async () => {
    const executor = new ExecutorAgent();

    const testCases = [
      { tickers: 1, target: 5000 },
      { tickers: 10, target: 15000 },
      { tickers: 100, target: 60000 }
    ];

    for (const testCase of testCases) {
      const start = Date.now();

      const execution = await executor.execute({
        scannerCode: 'def scan(df): return df',
        scannerName: 'Performance_Test',
        executionType: 'scan',
        tickers: Array.from({ length: testCase.tickers }, (_, i) => `TICKER${i}`),
        dateRange: { start: '2024-01-01', end: '2024-03-31' }
      });

      const time = Date.now() - start;

      console.log(`${testCase.tickers} tickers: ${time}ms (target: <${testCase.target}ms)`);
      expect(time).toBeLessThan(testCase.target);
      expect(execution.status).toBe('completed');
    }

    console.log('✅ Scanner execution performance validated');
  }, 120000);

  test('Database query performance', async () => {
    const archon = new ArchonMCPClient();

    const queries = [
      { name: 'Project search', query: () => archon.findProjects('test') },
      { name: 'Task search', query: () => archon.findTasks('test') },
      { name: 'RAG search', query: () => archon.ragSearchKnowledgeBase('test query') }
    ];

    for (const queryTest of queries) {
      const start = Date.now();
      await queryTest.query();
      const time = Date.now() - start;

      console.log(`${queryTest.name}: ${time}ms (target: <2000ms)`);
      expect(time).toBeLessThan(2000);
    }

    console.log('✅ Database query performance validated');
  });

  test('WebSocket latency', async () => {
    const tracker = new WebSocketProgressTracker();
    const executionId = 'test_execution';

    const connectStart = Date.now();
    tracker.connect(executionId);

    // Wait for connection
    await new Promise(resolve => setTimeout(resolve, 1000));

    const connectTime = Date.now() - connectStart;

    console.log(`WebSocket connect: ${connectTime}ms (target: <1000ms)`);
    expect(connectTime).toBeLessThan(1000);

    tracker.disconnect();
    console.log('✅ WebSocket latency validated');
  });
});
```

**Acceptance Criteria**:
- [ ] All API response times meet targets
- [ ] Scanner execution scales with tickers
- [ ] Database queries under 2 seconds
- [ ] WebSocket connects under 1 second
- [ ] Performance report generated

**Dependencies**:
- All systems integrated

**Risks**:
- **Risk**: Performance degrades under load
  - **Mitigation**: Caching, pagination, optimization

---

### Task 9.6: Load Testing (4 hours)

**Subtasks**:
1. Design load test scenarios
2. Test concurrent scanner executions
3. Test concurrent research queries
4. Test concurrent builds
5. Identify bottlenecks
6. Generate load test report

**Code Example**:
```typescript
// src/tests/load/concurrentExecution.test.ts

describe('Load Testing', () => {
  test('Concurrent scanner executions', async () => {
    const executor = new ExecutorAgent();
    const concurrentExecutions = 10;

    console.log(`Testing ${concurrentExecutions} concurrent executions...`);

    const executions = Array.from({ length: concurrentExecutions }, (_, i) =>
      executor.execute({
        scannerCode: 'def scan(df): return df',
        scannerName: `Load_Test_${i}`,
        executionType: 'scan',
        tickers: ['AAPL', 'MSFT', 'GOOGL'],
        dateRange: { start: '2024-01-01', end: '2024-03-31' }
      })
    );

    const start = Date.now();
    const results = await Promise.all(executions);
    const totalTime = Date.now() - start;

    const successful = results.filter(r => r.status === 'completed').length;
    const failed = results.filter(r => r.status === 'failed').length;

    console.log(`Total time: ${totalTime}ms`);
    console.log(`Successful: ${successful}/${concurrentExecutions}`);
    console.log(`Failed: ${failed}/${concurrentExecutions}`);

    expect(successful).toBeGreaterThanOrEqual(concurrentExecutions * 0.9); // 90% success rate
    expect(totalTime).toBeLessThan(120000); // Complete all in <2 minutes

    console.log('✅ Concurrent executions handled successfully');
  }, 180000);

  test('Concurrent research queries', async () => {
    const researcher = new ResearcherAgent();
    const concurrentQueries = 20;

    console.log(`Testing ${concurrentQueries} concurrent queries...`);

    const queries = Array.from({ length: concurrentQueries }, () =>
      researcher.research({ query: 'test query', domain: 'scanner' })
    );

    const start = Date.now();
    const results = await Promise.all(queries);
    const totalTime = Date.now() - start;

    console.log(`Total time: ${totalTime}ms`);
    console.log(`Avg per query: ${(totalTime / concurrentQueries).toFixed(0)}ms`);

    expect(totalTime).toBeLessThan(30000); // Complete all in <30 seconds
    console.log('✅ Concurrent queries handled successfully');
  });
});
```

**Acceptance Criteria**:
- [ ] System handles 10 concurrent executions
- [ ] System handles 20 concurrent research queries
- [ ] Success rate > 90%
- [ ] No deadlocks or race conditions
- [ ] Load test report generated

**Dependencies**:
- All systems integrated

**Risks**:
- **Risk**: System crashes under load
  - **Mitigation**: Rate limiting, queue management

---

### Task 9.7: Security Validation (4 hours)

**Subtasks**:
1. Test input validation
2. Test SQL injection prevention
3. Test XSS prevention
4. Test authentication/authorization
5. Test data sanitization
6. Generate security report

**Code Example**:
```typescript
// src/tests/security/securityValidation.test.ts

describe('Security Validation', () => {
  test('Input validation', async () => {
    const builder = new BuilderAgent();

    const maliciousInputs = [
      { description: "'; DROP TABLE scanners; --" },
      { description: '<script>alert("xss")</script>' },
      { description: '../../../etc/passwd' }
    ];

    for (const input of maliciousInputs) {
      try {
        const result = await builder.build({
          type: 'idea',
          input
        });

        // Should sanitize input, not fail
        expect(result.scannerCode).toBeDefined();
        expect(result.scannerCode).not.toContain('DROP TABLE');
        expect(result.scannerCode).not.toContain('<script>');
        console.log(`✓ Sanitized: ${input.description.substring(0, 20)}...`);
      } catch (error) {
        // Should handle gracefully
        console.log(`✓ Handled: ${input.description.substring(0, 20)}...`);
      }
    }

    console.log('✅ Input validation working correctly');
  });

  test('Scanner code safety', async () => {
    const executor = new ExecutorAgent();

    const dangerousCode = `
def scan(df):
    import os
    os.system('rm -rf /')
    return df
    `.trim();

    try {
      const execution = await executor.execute({
        scannerCode: dangerousCode,
        scannerName: 'Dangerous',
        executionType: 'test',
        aPlusNames: ['AAPL'],
        dateRange: { start: '2024-01-01', end: '2024-12-31' }
      });

      // Should prevent execution
      expect(execution.status).toBe('failed');
      expect(execution.error).toBeDefined();
      console.log('✅ Dangerous code blocked');
    } catch (error) {
      console.log('✅ Dangerous code prevented');
    }
  });

  test('Data sanitization', async () => {
    const analyst = new AnalystAgent();

    // Test that user data is properly escaped
    const userInput = "'; SELECT * FROM users; --";
    const analysis = await analyst.analyze({
      backtestId: 'test',
      analysisType: 'performance'
    });

    // Should not contain SQL injection
    expect(JSON.stringify(analysis)).not.toContain('SELECT * FROM');
    console.log('✅ Data properly sanitized');
  });
});
```

**Acceptance Criteria**:
- [ ] All malicious inputs sanitized
- [ ] Dangerous code blocked
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Security report generated

**Dependencies**:
- All systems integrated

**Risks**:
- **Risk**: Security vulnerabilities
  - **Mitigation**: Input validation, sandboxing, code review

---

### Task 9.8: User Acceptance Testing (6 hours)

**Subtasks**:
1. Create UAT scenarios
2. Test with real A+ examples
3. Test with real non-V31 code
4. Test with real ideas
5. Gather feedback
6. Document findings
7. Create improvement recommendations

**Code Example**:
```typescript
// src/tests/uat/userAcceptance.test.ts

describe('User Acceptance Testing', () => {
  test('UAT Scenario 1: Michael creates OS D1 scanner from A+ example', async () => {
    console.log('\n=== UAT Scenario 1: A+ Example Workflow ===\n');

    // Michael's actual A+ OS D1 example
    const aPlusExample = {
      setupName: 'OS D1',
      breakdown: `
        ENTRY: Close > 2.5 SD below lower EMA cloud (20/50)
        EXIT: Close above EMA 20
        STOP: 2x ATR below entry
      `,
      aPlusNames: ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'META', 'AMD'],
      dateRange: { start: '2024-01-01', end: '2024-12-31' }
    };

    // Step 1: Michael provides A+ example to Renata
    console.log('Michael: "Here\'s my OS D1 A+ example..."');
    const planner = new PlannerAgent();
    const plan = await planner.analyzeAPlusExample(aPlusExample);

    console.log(`Renata: I've analyzed your A+ example. Confidence: ${Math.round(plan.confidence * 100)}%`);
    console.log(`Suggested parameters: ${JSON.stringify(plan.suggestedParameters, null, 2)}`);

    // Step 2: Michael reviews and approves
    console.log('\nMichael: "Looks good, build the scanner."');

    // Step 3: Renata builds scanner
    const builder = new BuilderAgent();
    const buildResult = await builder.build({
      type: 'mold',
      input: aPlusExample
    });

    console.log(`\nRenata: Scanner built! V31 compliant: ${buildResult.v31Compliant}`);
    console.log(`Quality score: ${Math.round(buildResult.qualityScore * 100)}%`);

    // Step 4: Michael tests on A+ names
    console.log('\nMichael: "Test it on my A+ names."');
    const executor = new ExecutorAgent();
    const execution = await executor.execute({
      scannerCode: buildResult.scannerCode,
      scannerName: 'OS_D1_UAT',
      executionType: 'test',
      aPlusNames: aPlusExample.aPlusNames,
      dateRange: aPlusExample.dateRange
    });

    console.log(`\nRenata: Testing complete! Found ${execution.results?.length || 0} signals.`);
    execution.results?.forEach(result => {
      console.log(`  - ${result.ticker}: ${result.date}`);
    });

    // Step 5: Michael reviews results
    console.log('\nMichael: "Perfect! Exactly what I expected."');
    console.log('✅ UAT Scenario 1: PASSED');

    expect(plan.confidence).toBeGreaterThan(0.7);
    expect(buildResult.v31Compliant).toBe(true);
    expect(execution.status).toBe('completed');
  }, 180000);

  test('UAT Scenario 2: Michael transforms existing scanner to V31', async () => {
    console.log('\n=== UAT Scenario 2: Code Transform Workflow ===\n');

    // Michael's existing non-V31 scanner
    const existingScanner = `
def backside_b_scanner(data):
    # My current Backside B scanner
    data['ema_20'] = data['close'].ewm(span=20).mean()
    data['ema_50'] = data['close'].ewm(span=50).mean()
    data['cloud_upper'] = (data['ema_20'] + data['ema_50']) / 2 + data['close'].rolling(20).std()
    data['cloud_lower'] = (data['ema_20'] + data['ema_50']) / 2 - data['close'].rolling(20).std()

    # Trend break detection
    data['trend_break'] = (data['close'] < data['cloud_lower']) & (data['close'].shift(1) > data['cloud_lower'].shift(1))

    return data[data['trend_break']]
    `.trim();

    console.log('Michael: "Transform this to V31 for me."');
    const transformer = new V31Transformer();
    const result = await transformer.transformToV31({
      existingCode: existingScanner,
      scannerName: 'Backside_B'
    });

    console.log(`\nRenata: Done! V31 compliant: ${result.v31Compliant}`);
    console.log(`Applied ${result.changes.length} improvements:`);
    result.changes.slice(0, 5).forEach(change => {
      console.log(`  - ${change.type}: ${change.description}`);
    });

    console.log('\nMichael: "Great, let me test it."');
    const executor = new ExecutorAgent();
    const execution = await executor.execute({
      scannerCode: result.transformedCode,
      scannerName: 'Backside_B_V31',
      executionType: 'scan',
      tickers: ['AAPL', 'MSFT'],
      dateRange: { start: '2024-01-01', end: '2024-06-30' }
    });

    console.log(`\nRenata: Execution complete! Status: ${execution.status}`);
    console.log('Michael: "Perfect, it works!"');
    console.log('✅ UAT Scenario 2: PASSED');

    expect(result.v31Compliant).toBe(true);
    expect(execution.status).toBe('completed');
  }, 180000);

  test('UAT Scenario 3: Michael generates scanner from idea', async () => {
    console.log('\n=== UAT Scenario 3: Idea → Scanner Workflow ===\n');

    const idea = {
      description: 'I want to find stocks that are gapping up on high volume at the open. The gap should be at least 2% and volume should be 2x the 30-day average. Only look at tech stocks.',
      setupType: 'G2G S1'
    };

    console.log(`Michael: "${idea.description}"`);
    console.log('Renata: "Let me research similar strategies and build that for you..."');

    const builder = new BuilderAgent();
    const buildResult = await builder.build({
      type: 'idea',
      input: idea,
      setupType: idea.setupType
    });

    console.log(`\nRenata: I\'ve generated a ${idea.setupType} scanner based on your idea.`);
    console.log(`V31 compliant: ${buildResult.v31Compliant}`);
    console.log(`Warnings: ${buildResult.warnings.length}`);

    console.log('\nMichael: "Run it on the market."');
    const executor = new ExecutorAgent();
    const execution = await executor.execute({
      scannerCode: buildResult.scannerCode,
      scannerName: 'G2G_S1_Idea',
      executionType: 'scan',
      tickers: ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD'],
      dateRange: { start: '2024-01-01', end: '2024-03-31' }
    });

    console.log(`\nRenata: Found ${execution.results?.length || 0} signals!`);
    console.log('Michael: "Nice! Let me analyze the results."');

    const analyst = new AnalystAgent();
    const analysis = await analyst.analyze({
      backtestId: execution.executionId,
      analysisType: 'performance'
    });

    console.log(`\nRenata: Sharpe Ratio: ${analysis.metrics.sharpeRatio.toFixed(2)}`);
    console.log(`Win Rate: ${(analysis.metrics.winRate * 100).toFixed(1)}%`);
    console.log(`Recommendations: ${analysis.recommendations.length}`);

    console.log('\nMichael: "This is exactly what I needed!"');
    console.log('✅ UAT Scenario 3: PASSED');

    expect(buildResult.vannerCode).toBeDefined();
    expect(execution.status).toBe('completed');
    expect(analysis.recommendations.length).toBeGreaterThan(0);
  }, 180000);
});
```

**Acceptance Criteria**:
- [ ] All UAT scenarios pass
- [ ] Michael can use all three workflows
- [ ] Results meet expectations
- [ ] Feedback documented
- [ ] Improvements identified

**Dependencies**:
- All workflows tested (Tasks 9.1-9.3)

**Risks**:
- **Risk**: UAT reveals major issues
  - **Mitigation**: Iterative fixes, retesting

---

## 📊 SPRINT 9 SUMMARY

### Time Investment
| Task | Hours | Priority |
|------|-------|----------|
| 9.1 Test A+ Example → Scanner Workflow | 8 | Critical |
| 9.2 Test Code Transform → Scanner Workflow | 6 | Critical |
| 9.3 Test Idea → Scanner Workflow | 6 | Critical |
| 9.4 Test Agent Coordination | 5 | Critical |
| 9.5 Performance Testing | 5 | Critical |
| 9.6 Load Testing | 4 | High |
| 9.7 Security Validation | 4 | High |
| 9.8 User Acceptance Testing | 6 | Critical |
| **TOTAL** | **44 hours** | |

### Completion Criteria
Sprint 9 is complete when:
- [ ] All three workflows validated end-to-end
- [ ] All agent coordination tested
- [ ] Performance benchmarks met
- [ ] Load testing successful
- [ ] Security validation passed
- [ ] UAT scenarios approved by Michael
- [ ] Test coverage > 85%
- [ ] Production readiness confirmed

### Dependencies
**Required Before Sprint 9**:
- All sprints completed (Sprints 0-8)
- All agents built and tested

**Enables Sprint 10**:
- Final production deployment
- Documentation completion
- Launch preparation

---

**Sprint 9 validates the entire system works as designed.**

**By completing Sprint 9, Renata V2 is proven ready for production.**

**Ready for Sprint 10: Production Polish.**
