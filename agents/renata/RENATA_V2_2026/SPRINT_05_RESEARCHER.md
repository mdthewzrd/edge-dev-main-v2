# 🔍 SPRINT 5: RESEARCHER AGENT
## Archon RAG Integration & Strategy Research

**Duration**: Weeks 5-6 (14 days)
**Objective**: Build intelligent research agent that leverages Archon knowledge base for pattern matching, strategy discovery, and market intelligence

**Success Criteria**:
- [ ] Researcher agent can search Archon RAG for similar strategies
- [ ] Pattern matching against V31 Gold Standard scanners
- [ ] Lingua framework integration for setup identification
- [ ] Market regime analysis and context awareness
- [ ] Parameter suggestion engine based on historical data
- [ ] CopilotKit integration for research actions

---

## 📋 DELIVERABLES

### Core Deliverables
- [ ] Researcher agent service with Archon RAG client
- [ ] Similar strategy search functionality
- [ ] Pattern matching engine for V31 compliance
- [ ] Market regime detection and analysis
- [ ] Parameter suggestion system
- [ ] Research report generation
- [ ] Integration with CopilotKit actions
- [ ] Comprehensive test suite

### Integration Points
- **Archon MCP**: `rag_search_knowledge_base()`, `rag_search_code_examples()`
- **CopilotKit**: `researchStrategy`, `findSimilarSetups`, `analyzeMarketRegime`
- **V31 Gold Standard**: Pattern validation and compliance checking
- **Lingua Framework**: Setup type identification and context

---

## 🎯 DETAILED TASKS

### Task 5.1: Create Researcher Agent Service (6 hours)

**Subtasks**:
1. Create `src/services/researcherAgent.ts` service structure
2. Implement Archon MCP RAG client wrapper
3. Create research state management
4. Build research result caching system
5. Implement search query optimization
6. Add error handling for RAG failures

**Code Example**:
```typescript
// src/services/researcherAgent.ts

import { ArchonMCPClient } from '@/archon/archonClient';

export interface ResearchQuery {
  query: string;
  domain?: 'scanner' | 'setup' | 'pattern' | 'indicator';
  timeframe?: string;
  marketCondition?: string;
}

export interface ResearchResult {
  relevantStrategies: StrategyMatch[];
  relevantPatterns: PatternMatch[];
  relevantSetups: SetupMatch[];
  marketContext: MarketContext;
  suggestedParameters: ParameterSuggestion[];
  confidence: number;
  sources: string[];
}

export class ResearcherAgent {
  private archon: ArchonMCPClient;
  private cache: Map<string, ResearchResult>;

  constructor() {
    this.archon = new ArchonMCPClient();
    this.cache = new Map();
  }

  async research(query: ResearchQuery): Promise<ResearchResult> {
    // Check cache first
    const cacheKey = this.generateCacheKey(query);
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    // Search Archon knowledge base
    const strategies = await this.searchStrategies(query);
    const patterns = await this.searchPatterns(query);
    const setups = await this.searchSetups(query);
    const marketContext = await this.analyzeMarketContext(query);

    const result: ResearchResult = {
      relevantStrategies: strategies,
      relevantPatterns: patterns,
      relevantSetups: setups,
      marketContext,
      suggestedParameters: [],
      confidence: this.calculateConfidence(strategies, patterns, setups),
      sources: this.extractSources(strategies, patterns, setups)
    };

    // Cache result
    this.cache.set(cacheKey, result);

    return result;
  }

  private async searchStrategies(query: ResearchQuery): Promise<StrategyMatch[]> {
    const ragQuery = this.buildRAGQuery(query, 'scanner');
    const results = await this.archon.ragSearchKnowledgeBase(ragQuery);

    return results
      .filter(r => r.metadata.type === 'scanner')
      .map(r => ({
        name: r.metadata.name,
        similarity: r.score,
        setupType: r.metadata.setupType,
        keyParameters: r.metadata.parameters,
        v31Compliant: r.metadata.v31Compliant === true,
        source: r.metadata.source
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 5);
  }

  // ... other methods
}
```

**Acceptance Criteria**:
- [ ] Researcher service created with all core methods
- [ ] Archon MCP integration working
- [ ] Caching reduces redundant queries by 80%+
- [ ] Error handling gracefully handles RAG failures
- [ ] All methods have unit tests

**Dependencies**:
- Archon MCP running and accessible (Sprint 2)
- V31 Gold Standard ingested (Sprint 2)
- Lingua framework ingested (Sprint 2)

**Risks**:
- **Risk**: Archon RAG performance slow
  - **Mitigation**: Implement caching, query optimization, pagination
- **Risk**: Poor relevance of search results
  - **Mitigation**: Iterative query refinement, relevance feedback loop

---

### Task 5.2: Implement Similar Strategy Search (5 hours)

**Subtasks**:
1. Build similarity scoring algorithm
2. Implement parameter-based matching
3. Create setup type detection
4. Build pattern recognition logic
5. Add V31 compliance filtering
6. Implement result ranking and relevance scoring

**Code Example**:
```typescript
// src/services/researcherAgent.ts

export interface StrategyMatch {
  name: string;
  similarity: number;
  setupType: string;
  keyParameters: Record<string, any>;
  v31Compliant: boolean;
  source: string;
  codeSnippet?: string;
}

async findSimilarStrategies(
  parameters: Record<string, any>,
  setupType?: string
): Promise<StrategyMatch[]> {
  // Build query from parameters
  const query = this.buildParameterQuery(parameters, setupType);

  // Search Archon for similar scanners
  const results = await this.archon.ragSearchCodeExamples(query);

  // Calculate similarity scores
  const scored = results.map(result => ({
    ...result,
    similarity: this.calculateSimilarity(parameters, result.metadata.parameters)
  }));

  // Filter by similarity threshold
  const similar = scored.filter(s => s.similarity >= 0.6);

  // Sort by similarity
  return similar
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 10);
}

private calculateSimilarity(
  params1: Record<string, any>,
  params2: Record<string, any>
): number {
  const keys1 = Object.keys(params1);
  const keys2 = Object.keys(params2);
  const allKeys = new Set([...keys1, ...keys2]);

  let similarity = 0;
  let matches = 0;

  allKeys.forEach(key => {
    const val1 = params1[key];
    const val2 = params2[key];

    if (val1 === undefined || val2 === undefined) {
      // One has parameter, other doesn't
      similarity += 0.3;
    } else if (val1 === val2) {
      // Exact match
      similarity += 1.0;
      matches++;
    } else if (typeof val1 === 'number' && typeof val2 === 'number') {
      // Numeric similarity
      const diff = Math.abs(val1 - val2) / Math.max(val1, val2);
      similarity += 1 - diff;
      matches++;
    } else {
      // Partial match for strings
      const str1 = String(val1).toLowerCase();
      const str2 = String(val2).toLowerCase();
      if (str1.includes(str2) || str2.includes(str1)) {
        similarity += 0.7;
        matches++;
      }
    }
  });

  return similarity / allKeys.size;
}
```

**Acceptance Criteria**:
- [ ] Can find similar strategies with 70%+ accuracy
- [ ] Similarity scoring algorithm validated
- [ ] Results ranked correctly by relevance
- [ ] V31 compliance filtering works
- [ ] Performance: Search completes in <3 seconds

**Dependencies**:
- Archon code examples ingested (Sprint 2)
- Researcher agent service created (Task 5.1)

**Risks**:
- **Risk**: Similarity algorithm produces poor matches
  - **Mitigation**: Iterative testing with real data, user feedback integration

---

### Task 5.3: Implement Pattern Matching Engine (6 hours)

**Subtasks**:
1. Build V31 pattern detection logic
2. Create Lingua setup pattern matching
3. Implement indicator pattern recognition
4. Add timeframe pattern analysis
5. Build market structure pattern detection
6. Create pattern confidence scoring

**Code Example**:
```typescript
// src/services/patternMatcher.ts

export interface PatternMatch {
  patternName: string;
  patternType: 'setup' | 'indicator' | 'market-structure' | 'timeframe';
  confidence: number;
  description: string;
  linguaReference?: string;
  v31Compliant: boolean;
  suggestedImplementation?: string;
}

export class PatternMatcher {
  private linguaPatterns: Map<string, LinguaPattern>;
  private v31Patterns: Map<string, V31Pattern>;

  constructor() {
    this.loadLinguaPatterns();
    this.loadV31Patterns();
  }

  async matchPatterns(
    scannerCode: string,
    parameters: Record<string, any>
  ): Promise<PatternMatch[]> {
    const matches: PatternMatch[] = [];

    // Match Lingua setup patterns
    const setupMatches = this.matchSetupPatterns(parameters);
    matches.push(...setupMatches);

    // Match V31 structural patterns
    const v31Matches = this.matchV31Patterns(scannerCode);
    matches.push(...v31Matches);

    // Match indicator patterns
    const indicatorMatches = this.matchIndicatorPatterns(scannerCode, parameters);
    matches.push(...indicatorMatches);

    // Sort by confidence
    return matches.sort((a, b) => b.confidence - a.confidence);
  }

  private matchSetupPatterns(parameters: Record<string, any>): PatternMatch[] {
    const matches: PatternMatch[] = [];

    // Detect OS D1 setup
    if (this.hasOversoldPattern(parameters)) {
      matches.push({
        patternName: 'OS D1',
        patternType: 'setup',
        confidence: 0.85,
        description: 'Oversold Daily setup - extreme deviation below lower cloud',
        linguaReference: 'Lingua lines 123-145',
        v31Compliant: true,
        suggestedImplementation: 'Use EMA cloud deviation bands, look for < -2.5 SD'
      });
    }

    // Detect G2G S1 setup
    if (this.hasGapToGapPattern(parameters)) {
      matches.push({
        patternName: 'G2G S1',
        patternType: 'setup',
        confidence: 0.82,
        description: 'Gap-to-Gap Stage 1 - gap up into resistance',
        linguaReference: 'Lingua lines 167-189',
        v31Compliant: true,
        suggestedImplementation: 'Identify gaps using overnight gap %, resistance at prior highs'
      });
    }

    // Detect SC DMR setup
    if (this.hasDemandRallyPattern(parameters)) {
      matches.push({
        patternName: 'SC DMR',
        patternType: 'setup',
        confidence: 0.88,
        description: 'Stage Change Demand Rally - strong move off bottom',
        linguaReference: 'Lingua lines 201-223',
        v31Compliant: true,
        suggestedImplementation: 'Detect strong volume rally off demand zone'
      });
    }

    // Detect SC MDR Swing setup
    if (this.hasSwingPattern(parameters)) {
      matches.push({
        patternName: 'SC MDR Swing',
        patternType: 'setup',
        confidence: 0.80,
        description: 'Stage Change Minor Demand Rally Swing - swing trading variant',
        linguaReference: 'Lingua lines 245-267',
        v31Compliant: true,
        suggestedImplementation: 'Similar to DMR but wider stops, longer holding period'
      });
    }

    return matches;
  }

  private matchV31Patterns(scannerCode: string): PatternMatch[] {
    const matches: PatternMatch[] = [];

    // Check for grouped endpoint pattern
    if (this.hasGroupedEndpointPattern(scannerCode)) {
      matches.push({
        patternName: 'V31 Grouped Endpoint',
        patternType: 'market-structure',
        confidence: 0.95,
        description: 'V31 Gold Standard 3-stage grouped endpoint architecture',
        v31Compliant: true,
        suggestedImplementation: 'Ensure: simple_features() → filter() → full_features() → detect()'
      });
    }

    // Check for per-ticker operations
    if (this.hasPerTickerPattern(scannerCode)) {
      matches.push({
        patternName: 'V31 Per-Ticker Operations',
        patternType: 'market-structure',
        confidence: 0.93,
        description: 'Per-ticker operations for correct historical buffer calculation',
        v31Compliant: true,
        suggestedImplementation: 'Use df.groupby("ticker") for all calculations'
      });
    }

    // Check for two-pass feature computation
    if (this.hasTwoPassPattern(scannerCode)) {
      matches.push({
        patternName: 'V31 Two-Pass Feature Computation',
        patternType: 'market-structure',
        confidence: 0.90,
        description: 'Two-pass approach: simple features first, then filter, then full features',
        v31Compliant: true,
        suggestedImplementation: 'Pass 1: Simple features → Pass 2: Filter → Pass 3: Full features'
      });
    }

    return matches;
  }

  private hasOversoldPattern(params: Record<string, any>): boolean {
    return (
      params.ema_cloud !== undefined ||
      params.deviation_band !== undefined ||
      params.oversold_threshold !== undefined
    );
  }

  // ... other pattern detection methods
}
```

**Acceptance Criteria**:
- [ ] Can detect all 4 systematized Lingua setups with 80%+ accuracy
- [ ] Can detect V31 structural patterns with 90%+ accuracy
- [ ] Pattern confidence scoring is reliable
- [ ] Suggested implementations are accurate
- [ ] Performance: Pattern matching completes in <2 seconds

**Dependencies**:
- Lingua framework ingested (Sprint 2)
- V31 Gold Standard ingested (Sprint 2)

**Risks**:
- **Risk**: False positive pattern detection
  - **Mitigation**: Confidence thresholding, manual validation dataset

---

### Task 5.4: Implement Market Regime Analysis (5 hours)

**Subtasks**:
1. Create regime detection algorithm
2. Implement trend cycle stage identification
3. Build volatility regime detection
4. Add market condition analysis
5. Create regime context suggestions
6. Implement regime change detection

**Code Example**:
```typescript
// src/services/marketRegimeAnalyzer.ts

export interface MarketRegime {
  trendStage: TrendStage;
  volatility: 'low' | 'medium' | 'high';
  marketCondition: 'bullish' | 'bearish' | 'sideways';
  confidence: number;
  timeframe: string;
  suggestedSetups: string[];
  avoidSetups: string[];
}

export type TrendStage =
  | 'consolidation'
  | 'breakout'
  | 'uptrend'
  | 'extreme-deviation'
  | 'euphoric-top'
  | 'trend-break'
  | 'backside'
  | 'backside-reverted';

export class MarketRegimeAnalyzer {
  async analyzeRegime(
    tickers: string[],
    timeframe: string = 'daily'
  ): Promise<MarketRegime> {
    // Fetch market data for regime analysis
    const marketData = await this.fetchMarketData(tickers, timeframe);

    // Detect trend stage
    const trendStage = this.detectTrendStage(marketData);

    // Detect volatility regime
    const volatility = this.detectVolatility(marketData);

    // Determine overall market condition
    const marketCondition = this.determineMarketCondition(marketData);

    // Calculate confidence
    const confidence = this.calculateConfidence(marketData);

    // Suggest setups based on regime
    const suggestedSetups = this.suggestSetups(trendStage, volatility, marketCondition);
    const avoidSetups = this.avoidSetups(trendStage, volatility, marketCondition);

    return {
      trendStage,
      volatility,
      marketCondition,
      confidence,
      timeframe,
      suggestedSetups,
      avoidSetups
    };
  }

  private detectTrendStage(marketData: MarketData[]): TrendStage {
    const latest = marketData[marketData.length - 1];
    const recent = marketData.slice(-20);

    // Calculate metrics
    const priceVsCloud = this.comparePriceToCloud(latest);
    const momentum = this.calculateMomentum(recent);
    const volume = this.analyzeVolume(recent);

    // Detect consolidation
    if (this.isConsolidating(recent)) {
      return 'consolidation';
    }

    // Detect breakout
    if (this.isBreakingOut(recent)) {
      return 'breakout';
    }

    // Detect uptrend
    if (priceVsCloud > 0 && momentum > 0) {
      if (this.isExtremeDeviation(recent)) {
        return 'extreme-deviation';
      }
      if (this.isEuphoricTop(recent)) {
        return 'euphoric-top';
      }
      return 'uptrend';
    }

    // Detect trend break
    if (this.isTrendBreaking(recent)) {
      return 'trend-break';
    }

    // Detect backside
    if (this.isBackside(recent)) {
      if (this.isBacksideReverted(recent)) {
        return 'backside-reverted';
      }
      return 'backside';
    }

    return 'consolidation';
  }

  private suggestSetups(
    trendStage: TrendStage,
    volatility: string,
    marketCondition: string
  ): string[] {
    const setups: string[] = [];

    // Trend-specific setup suggestions
    switch (trendStage) {
      case 'consolidation':
        setups.push('OS D1', 'G2G S1');
        break;
      case 'breakout':
        setups.push('SC DMR', 'SC MDR Swing');
        break;
      case 'uptrend':
        setups.push('SC DMR', 'Pullback Entries');
        break;
      case 'extreme-deviation':
        setups.push('OS D1', 'SC MDR Swing');
        break;
      case 'trend-break':
        setups.push('Backside B', 'Short Setups');
        break;
      case 'backside':
        setups.push('Backside B', 'OS D1 (long side)');
        break;
    }

    // Volatility adjustments
    if (volatility === 'high') {
      // Avoid wide-stop setups in high volatility
      return setups.filter(s => !s.includes('Swing'));
    }

    return setups;
  }

  // ... other detection methods
}
```

**Acceptance Criteria**:
- [ ] Can detect all 8 Lingua trend stages with 75%+ accuracy
- [ ] Volatility regime detection is reliable
- [ ] Setup suggestions are contextually appropriate
- [ ] Regime change detection works in real-time
- [ ] Performance: Regime analysis completes in <2 seconds

**Dependencies**:
- Lingua framework ingested (Sprint 2)
- Market data API available

**Risks**:
- **Risk**: Regime detection accuracy insufficient
  - **Mitigation**: Machine learning model training, backtesting against historical regimes

---

### Task 5.5: Implement Parameter Suggestion Engine (5 hours)

**Subtasks**:
1. Build parameter recommendation algorithm
2. Create historical parameter analysis
3. Implement setup-specific parameter suggestions
4. Add market condition adjustments
5. Create parameter optimization hints
6. Build parameter validation system

**Code Example**:
```typescript
// src/services/parameterSuggester.ts

export interface ParameterSuggestion {
  parameter: string;
  suggestedValue: any;
  confidence: number;
  reasoning: string;
  basedOn: string[];
  alternatives?: ParameterAlternative[];
}

export interface ParameterAlternative {
  value: any;
  useCase: string;
  tradeoffs: string;
}

export class ParameterSuggester {
  private researcher: ResearcherAgent;

  constructor() {
    this.researcher = new ResearcherAgent();
  }

  async suggestParameters(
    setupType: string,
    marketContext: MarketRegime,
    userConstraints?: Record<string, any>
  ): Promise<ParameterSuggestion[]> {
    const suggestions: ParameterSuggestion[] = [];

    // Research similar strategies
    const similarStrategies = await this.researcher.findSimilarStrategies(
      { setupType },
      setupType
    );

    // Extract common parameters
    const commonParams = this.extractCommonParameters(similarStrategies);

    // Generate suggestions for each parameter
    for (const [param, value] of Object.entries(commonParams)) {
      const suggestion = await this.generateSuggestion(
        param,
        value,
        setupType,
        marketContext,
        similarStrategies
      );
      suggestions.push(suggestion);
    }

    // Adjust for market conditions
    const adjusted = this.adjustForMarketConditions(suggestions, marketContext);

    // Apply user constraints
    const filtered = this.applyConstraints(adjusted, userConstraints);

    return filtered;
  }

  private async generateSuggestion(
    parameter: string,
    commonValue: any,
    setupType: string,
    marketContext: MarketRegime,
    similarStrategies: StrategyMatch[]
  ): Promise<ParameterSuggestion> {
    // Analyze historical performance
    const historical = await this.analyzeHistoricalPerformance(
      parameter,
      commonValue,
      setupType
    );

    // Calculate confidence based on historical success
    const confidence = this.calculateConfidence(historical);

    // Generate reasoning
    const reasoning = this.generateReasoning(
      parameter,
      commonValue,
      historical,
      marketContext
    );

    // Generate alternatives
    const alternatives = this.generateAlternatives(
      parameter,
      commonValue,
      setupType,
      marketContext
    );

    return {
      parameter,
      suggestedValue: commonValue,
      confidence,
      reasoning,
      basedOn: similarStrategies.map(s => s.name),
      alternatives
    };
  }

  private adjustForMarketConditions(
    suggestions: ParameterSuggestion[],
    marketContext: MarketRegime
  ): ParameterSuggestion[] {
    return suggestions.map(s => {
      let adjusted = { ...s };

      // Adjust stop-loss based on volatility
      if (s.parameter === 'stop_loss' || s.parameter === 'stopLoss') {
        if (marketContext.volatility === 'high') {
          adjusted.suggestedValue = s.suggestedValue * 1.5;
          adjusted.reasoning += ' | Increased for high volatility';
        } else if (marketContext.volatility === 'low') {
          adjusted.suggestedValue = s.suggestedValue * 0.8;
          adjusted.reasoning += ' | Decreased for low volatility';
        }
      }

      // Adjust position size based on market condition
      if (s.parameter === 'position_size' || s.parameter === 'positionSize') {
        if (marketContext.marketCondition === 'bearish') {
          adjusted.suggestedValue = s.suggestedValue * 0.7;
          adjusted.reasoning += ' | Reduced for bearish market';
        }
      }

      // Adjust lookback period based on trend stage
      if (s.parameter === 'lookback' || s.parameter === 'lookbackPeriod') {
        if (marketContext.trendStage === 'consolidation') {
          adjusted.suggestedValue = Math.min(s.suggestedValue * 1.2, 60);
          adjusted.reasoning += ' | Increased for consolidation';
        }
      }

      return adjusted;
    });
  }

  private generateAlternatives(
    parameter: string,
    currentValue: any,
    setupType: string,
    marketContext: MarketRegime
  ): ParameterAlternative[] {
    const alternatives: ParameterAlternative[] = [];

    if (typeof currentValue === 'number') {
      // Conservative alternative
      alternatives.push({
        value: currentValue * 0.8,
        useCase: 'Conservative approach',
        tradeoffs: 'Fewer signals, higher quality'
      });

      // Aggressive alternative
      alternatives.push({
        value: currentValue * 1.2,
        useCase: 'Aggressive approach',
        tradeoffs: 'More signals, lower quality'
      });
    }

    if (parameter.includes('threshold') || parameter.includes('filter')) {
      // Strict alternative
      alternatives.push({
        value: currentValue * 1.3,
        useCase: 'Strict filtering',
        tradeoffs: 'Fewer false positives, may miss opportunities'
      });

      // Loose alternative
      alternatives.push({
        value: currentValue * 0.7,
        useCase: 'Loose filtering',
        tradeoffs: 'More signals, more false positives'
      });
    }

    return alternatives;
  }

  // ... other methods
}
```

**Acceptance Criteria**:
- [ ] Can suggest parameters for all 4 systematized setups
- [ ] Suggestions are based on historical data
- [ ] Market condition adjustments are sensible
- [ ] Alternatives provide useful options
- [ ] Confidence scoring is accurate
- [ ] Performance: Suggestion generation completes in <3 seconds

**Dependencies**:
- Researcher agent service (Task 5.1)
- Similar strategy search (Task 5.2)
- Market regime analyzer (Task 5.4)

**Risks**:
- **Risk**: Poor parameter suggestions leading to bad scanners
  - **Mitigation**: Extensive backtesting, user feedback loop, manual override

---

### Task 5.6: Implement Research Report Generation (4 hours)

**Subtasks**:
1. Create report template structure
2. Build research finding synthesis
3. Implement markdown report generation
4. Add code example inclusion
5. Create visual recommendation display
6. Build report export functionality

**Code Example**:
```typescript
// src/services/researchReportGenerator.ts

export interface ResearchReport {
  title: string;
  summary: string;
  similarStrategies: StrategySummary[];
  matchedPatterns: PatternSummary[];
  marketContext: MarketContextSummary;
  parameterSuggestions: ParameterSummary[];
  recommendedApproach: string;
  nextSteps: string[];
  confidence: number;
  generatedAt: Date;
}

export class ResearchReportGenerator {
  async generateReport(
    query: ResearchQuery,
    results: ResearchResult
  ): Promise<ResearchReport> {
    return {
      title: this.generateTitle(query),
      summary: this.generateSummary(results),
      similarStrategies: this.summarizeStrategies(results.relevantStrategies),
      matchedPatterns: this.summarizePatterns(results.relevantPatterns),
      marketContext: this.summarizeMarketContext(results.marketContext),
      parameterSuggestions: this.summarizeParameters(results.suggestedParameters),
      recommendedApproach: this.generateRecommendation(results),
      nextSteps: this.generateNextSteps(results),
      confidence: results.confidence,
      generatedAt: new Date()
    };
  }

  private generateSummary(results: ResearchResult): string {
    const parts: string[] = [];

    // Similar strategies summary
    if (results.relevantStrategies.length > 0) {
      parts.push(
        `Found ${results.relevantStrategies.length} similar strategies, ` +
        `most similar being ${results.relevantStrategies[0].name} ` +
        `(${Math.round(results.relevantStrategies[0].similarity * 100)}% match).`
      );
    }

    // Pattern matches summary
    if (results.relevantPatterns.length > 0) {
      const patterns = results.relevantPatterns.map(p => p.patternName).join(', ');
      parts.push(`Detected patterns: ${patterns}.`);
    }

    // Market context summary
    if (results.marketContext) {
      parts.push(
        `Current market regime: ${results.marketContext.trendStage}, ` +
        `${results.marketContext.volatility} volatility, ` +
        `${results.marketContext.marketCondition} market.`
      );
    }

    return parts.join(' ');
  }

  private generateRecommendation(results: ResearchResult): string {
    const recommendations: string[] = [];

    // Based on similar strategies
    if (results.relevantStrategies.length > 0) {
      const topStrategy = results.relevantStrategies[0];
      if (topStrategy.similarity > 0.8) {
        recommendations.push(
          `High similarity to ${topStrategy.name} found. ` +
          `Consider using this as a template and modifying parameters.`
        );
      }
    }

    // Based on patterns
    if (results.relevantPatterns.length > 0) {
      const v31Patterns = results.relevantPatterns.filter(p => p.v31Compliant);
      if (v31Patterns.length > 0) {
        recommendations.push(
          `Detected V31-compliant patterns. Ensure your implementation follows ` +
          `V31 Gold Standard architecture.`
        );
      }
    }

    // Based on market context
    if (results.marketContext) {
      if (results.marketContext.suggestedSetups.length > 0) {
        recommendations.push(
          `Current market conditions favor: ` +
          results.marketContext.suggestedSetups.join(', ')
        );
      }
    }

    return recommendations.join(' ') || 'No specific recommendations based on research.';
  }

  private generateNextSteps(results: ResearchResult): string[] {
    const steps: string[] = [];

    // If similar strategies found
    if (results.relevantStrategies.length > 0) {
      steps.push('Review similar strategies for implementation patterns');
      steps.push('Compare parameters with top matches');
    }

    // If patterns found
    if (results.relevantPatterns.length > 0) {
      steps.push('Review pattern match details and suggested implementations');
      steps.push('Ensure V31 compliance if patterns indicate');
    }

    // If parameter suggestions available
    if (results.suggestedParameters.length > 0) {
      steps.push('Review suggested parameters with confidence scores');
      steps.push('Adjust parameters based on market conditions');
    }

    // Always include
    steps.push('Build initial scanner based on research findings');
    steps.push('Test on A+ examples before full market scan');
    steps.push('Run backtest to validate performance');

    return steps;
  }

  async toMarkdown(report: ResearchReport): Promise<string> {
    const lines: string[] = [];

    lines.push(`# ${report.title}\n`);
    lines.push(`*Generated: ${report.generatedAt.toISOString()}*\n`);
    lines.push(`**Confidence**: ${Math.round(report.confidence * 100)}%\n`);

    lines.push('## Summary\n');
    lines.push(`${report.summary}\n`);

    lines.push('## Similar Strategies\n');
    report.similarStrategies.forEach((s, i) => {
      lines.push(`${i + 1}. **${s.name}** (${Math.round(s.similarity * 100)}% match)`);
      lines.push(`   - Setup: ${s.setupType}`);
      lines.push(`   - V31 Compliant: ${s.v31Compliant ? '✅' : '❌'}`);
      if (s.keyParameters) {
        lines.push(`   - Parameters: \`${JSON.stringify(s.keyParameters)}\``);
      }
      lines.push('');
    });

    lines.push('## Matched Patterns\n');
    report.matchedPatterns.forEach((p, i) => {
      lines.push(`${i + 1}. **${p.patternName}** (${Math.round(p.confidence * 100)}% confidence)`);
      lines.push(`   - Type: ${p.patternType}`);
      lines.push(`   - Description: ${p.description}`);
      if (p.suggestedImplementation) {
        lines.push(`   - Implementation: ${p.suggestedImplementation}`);
      }
      lines.push('');
    });

    lines.push('## Market Context\n');
    lines.push(`- **Trend Stage**: ${report.marketContext.trendStage}`);
    lines.push(`- **Volatility**: ${report.marketContext.volatility}`);
    lines.push(`- **Market Condition**: ${report.marketContext.marketCondition}`);
    if (report.marketContext.suggestedSetups.length > 0) {
      lines.push(`- **Suggested Setups**: ${report.marketContext.suggestedSetups.join(', ')}`);
    }
    lines.push('');

    lines.push('## Parameter Suggestions\n');
    report.parameterSuggestions.forEach((p, i) => {
      lines.push(`${i + 1}. **${p.parameter}**`);
      lines.push(`   - Suggested Value: \`${p.suggestedValue}\``);
      lines.push(`   - Confidence: ${Math.round(p.confidence * 100)}%`);
      lines.push(`   - Reasoning: ${p.reasoning}`);
      if (p.alternatives && p.alternatives.length > 0) {
        lines.push(`   - Alternatives:`);
        p.alternatives.forEach(alt => {
          lines.push(`     - \`${alt.value}\`: ${alt.useCase} (${alt.tradeoffs})`);
        });
      }
      lines.push('');
    });

    lines.push('## Recommended Approach\n');
    lines.push(`${report.recommendedApproach}\n`);

    lines.push('## Next Steps\n');
    report.nextSteps.forEach((step, i) => {
      lines.push(`${i + 1}. ${step}`);
    });
    lines.push('');

    return lines.join('\n');
  }
}
```

**Acceptance Criteria**:
- [ ] Research reports include all relevant findings
- [ ] Markdown generation is clean and readable
- [ ] Recommendations are actionable
- [ ] Next steps are logical and complete
- [ ] Confidence scores are prominently displayed
- [ ] Performance: Report generation completes in <1 second

**Dependencies**:
- All previous tasks in Sprint 5

**Risks**:
- **Risk**: Reports too verbose or overwhelming
  - **Mitigation**: Progressive disclosure, summary + details view

---

### Task 5.7: Integrate with CopilotKit Actions (4 hours)

**Subtasks**:
1. Define CopilotKit action schemas
2. Implement action handlers
3. Create action result formatting
4. Add error handling for actions
5. Test all research actions
6. Document action usage

**Code Example**:
```typescript
// src/components/renataV2CopilotKit.tsx

import { CopilotKit } from '@copilotkit/react-core';
import { CopilotSidebar } from './CopilotSidebar';

export function RenataV2CopilotKit() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <ResearchActions />
      <CopilotSidebar />
    </CopilotKit>
  );
}

function ResearchActions() {
  return (
    <>
      <Action
        name="researchStrategy"
        description="Research similar strategies and patterns for a trading setup"
        parameters={[
          {
            name: "setupType",
            type: "string",
            description: "Type of setup (e.g., OS D1, G2G S1, SC DMR, Backside B)",
            required: true
          },
          {
            name: "parameters",
            type: "object",
            description: "Current parameters for the setup",
            required: false
          }
        ]}
        handler={async (args) => {
          const researcher = new ResearcherAgent();
          const results = await researcher.research({
            query: args.setupType,
            domain: 'scanner',
            ...args.parameters
          });

          const reportGen = new ResearchReportGenerator();
          const report = await reportGen.generateReport(
            { query: args.setupType, ...args.parameters },
            results
          );

          return {
            summary: report.summary,
            similarStrategies: report.similarStrategies,
            matchedPatterns: report.matchedPatterns,
            recommendedApproach: report.recommendedApproach,
            confidence: report.confidence
          };
        }}
      />

      <Action
        name="findSimilarSetups"
        description="Find similar existing setups based on parameters"
        parameters={[
          {
            name: "parameters",
            type: "object",
            description: "Parameters to match against",
            required: true
          },
          {
            name: "setupType",
            type: "string",
            description: "Optional setup type filter",
            required: false
          }
        ]}
        handler={async (args) => {
          const researcher = new ResearcherAgent();
          const similar = await researcher.findSimilarStrategies(
            args.parameters,
            args.setupType
          );

          return {
            count: similar.length,
            strategies: similar.map(s => ({
              name: s.name,
              similarity: Math.round(s.similarity * 100) + '%',
              setupType: s.setupType,
              v31Compliant: s.v31Compliant,
              parameters: s.keyParameters
            }))
          };
        }}
      />

      <Action
        name="analyzeMarketRegime"
        description="Analyze current market regime and suggest appropriate setups"
        parameters={[
          {
            name: "tickers",
            type: "array",
            description: "List of tickers to analyze",
            required: true
          },
          {
            name: "timeframe",
            type: "string",
            description: "Timeframe for analysis (default: daily)",
            required: false
          }
        ]}
        handler={async (args) => {
          const analyzer = new MarketRegimeAnalyzer();
          const regime = await analyzer.analyzeRegime(
            args.tickers,
            args.timeframe || 'daily'
          );

          return {
            trendStage: regime.trendStage,
            volatility: regime.volatility,
            marketCondition: regime.marketCondition,
            confidence: Math.round(regime.confidence * 100) + '%',
            suggestedSetups: regime.suggestedSetups,
            avoidSetups: regime.avoidSetups,
            timeframe: regime.timeframe
          };
        }}
      />

      <Action
        name="suggestParameters"
        description="Suggest optimal parameters for a setup based on research and market conditions"
        parameters={[
          {
            name: "setupType",
            type: "string",
            description: "Type of setup",
            required: true
          },
          {
            name: "marketRegime",
            type: "object",
            description: "Current market regime context",
            required: false
          },
          {
            name: "constraints",
            type: "object",
            description: "User constraints on parameters",
            required: false
          }
        ]}
        handler={async (args) => {
          const suggester = new ParameterSuggester();
          const suggestions = await suggester.suggestParameters(
            args.setupType,
            args.marketRegime || {},
            args.constraints
          );

          return {
            count: suggestions.length,
            suggestions: suggestions.map(s => ({
              parameter: s.parameter,
              suggestedValue: s.suggestedValue,
              confidence: Math.round(s.confidence * 100) + '%',
              reasoning: s.reasoning,
              basedOn: s.basedOn,
              alternatives: s.alternatives
            }))
          };
        }}
      />
    </>
  );
}
```

**Acceptance Criteria**:
- [ ] All research actions defined and working
- [ ] Actions return properly formatted results
- [ ] Error handling gracefully handles failures
- [ ] Actions integrate with chat context
- [ ] Performance: Actions complete in <5 seconds

**Dependencies**:
- CopilotKit installed (Sprint 3)
- All researcher components built (Tasks 5.1-5.6)

**Risks**:
- **Risk**: Action timeout or failure
  - **Mitigation**: Async processing with status updates, timeout handling

---

### Task 5.8: Testing & Validation (4 hours)

**Subtasks**:
1. Create unit tests for researcher agent
2. Create integration tests for RAG searches
3. Create tests for pattern matching
4. Create tests for regime analysis
5. Create tests for parameter suggestions
6. Create end-to-end tests for CopilotKit actions
7. Manual validation with real data
8. Performance testing

**Code Example**:
```typescript
// src/services/__tests__/researcherAgent.test.ts

import { ResearcherAgent, ResearchQuery } from '../researcherAgent';

describe('ResearcherAgent', () => {
  let researcher: ResearcherAgent;

  beforeEach(() => {
    researcher = new ResearcherAgent();
  });

  describe('research', () => {
    it('should find similar strategies for OS D1 setup', async () => {
      const query: ResearchQuery = {
        query: 'OS D1 oversold daily setup',
        domain: 'scanner',
        timeframe: 'daily'
      };

      const result = await researcher.research(query);

      expect(result.relevantStrategies.length).toBeGreaterThan(0);
      expect(result.confidence).toBeGreaterThan(0.5);
      expect(result.sources.length).toBeGreaterThan(0);
    });

    it('should match V31 patterns in scanner code', async () => {
      const scannerCode = `
        def simple_features(df):
          # EMA cloud calculation
          df['ema_20'] = df['close'].ewm(span=20).mean()
          df['ema_50'] = df['close'].ewm(span=50).mean()

        def filter(df):
          return df[df['volume'] > 1000000]

        def full_features(df):
          # Full feature computation

        def detect(df):
          # Detection logic
      `;

      const patterns = await researcher.matchPatterns(scannerCode, {});

      const v31Pattern = patterns.find(p => p.patternName.includes('V31'));
      expect(v31Pattern).toBeDefined();
      expect(v31Pattern?.v31Compliant).toBe(true);
    });

    it('should detect market regime correctly', async () => {
      const regime = await researcher.analyzeMarketRegime(['AAPL', 'MSFT'], 'daily');

      expect(regime.trendStage).toBeDefined();
      expect(regime.volatility).toBeDefined();
      expect(regime.marketCondition).toBeDefined();
      expect(regime.suggestedSetups.length).toBeGreaterThan(0);
    });

    it('should suggest parameters based on similar strategies', async () => {
      const suggestions = await researcher.suggestParameters(
        'OS D1',
        { trendStage: 'uptrend', volatility: 'medium' }
      );

      expect(suggestions.length).toBeGreaterThan(0);
      suggestions.forEach(s => {
        expect(s.parameter).toBeDefined();
        expect(s.suggestedValue).toBeDefined();
        expect(s.confidence).toBeGreaterThan(0);
        expect(s.reasoning).toBeDefined();
      });
    });
  });

  describe('findSimilarStrategies', () => {
    it('should find strategies with similar parameters', async () => {
      const parameters = {
        ema_short: 20,
        ema_long: 50,
        deviation_threshold: 2.5
      };

      const similar = await researcher.findSimilarStrategies(parameters, 'OS D1');

      expect(similar.length).toBeGreaterThan(0);
      expect(similar[0].similarity).toBeGreaterThan(0.5);
    });
  });
});
```

**Acceptance Criteria**:
- [ ] Unit tests achieve 80%+ code coverage
- [ ] Integration tests validate Archon RAG searches
- [ ] Pattern matching tests include all 4 systematized setups
- [ ] Regime analysis tests include all 8 trend stages
- [ ] Parameter suggestion tests validate accuracy
- [ ] CopilotKit action tests validate end-to-end flows
- [ ] Performance tests confirm all operations complete in <5 seconds
- [ ] Manual validation with real A+ examples successful

**Dependencies**:
- All researcher components built (Tasks 5.1-5.7)
- Test infrastructure setup (Sprint 1)

**Risks**:
- **Risk**: Test coverage insufficient
  - **Mitigation**: Target 80% coverage, manual validation of edge cases

---

## 📊 SPRINT 5 SUMMARY

### Time Investment
| Task | Hours | Priority |
|------|-------|----------|
| 5.1 Create Researcher Agent Service | 6 | Critical |
| 5.2 Implement Similar Strategy Search | 5 | Critical |
| 5.3 Implement Pattern Matching Engine | 6 | Critical |
| 5.4 Implement Market Regime Analysis | 5 | High |
| 5.5 Implement Parameter Suggestion Engine | 5 | High |
| 5.6 Implement Research Report Generation | 4 | Medium |
| 5.7 Integrate with CopilotKit Actions | 4 | Critical |
| 5.8 Testing & Validation | 4 | Critical |
| **TOTAL** | **39 hours** | |

### Completion Criteria
Sprint 5 is complete when:
- [ ] Researcher agent can search Archon for similar strategies
- [ ] Pattern matching detects all 4 systematized Lingua setups
- [ ] Market regime analysis identifies all 8 trend stages
- [ ] Parameter suggestions are accurate and context-aware
- [ ] Research reports are comprehensive and actionable
- [ ] All CopilotKit actions working in chat interface
- [ ] Test coverage 80%+, all tests passing
- [ ] Manual validation successful with real examples

### Dependencies
**Required Before Sprint 5**:
- Sprint 2: Archon MCP running with V31 and Lingua ingested
- Sprint 3: CopilotKit installed and configured

**Enables Sprint 6**:
- Builder Agent will use researcher findings for code generation
- Parameter suggestions will guide scanner construction
- Pattern matching will validate V31 compliance

### Risk Mitigation
**High-Risk Items**:
1. **Archon RAG performance** → Caching, query optimization, pagination
2. **Pattern matching accuracy** → Manual validation dataset, confidence thresholding
3. **Parameter suggestion quality** → Extensive backtesting, user feedback loop

**Contingency Plans**:
- If RAG too slow → Implement caching with 24-hour TTL
- If patterns inaccurate → Manual pattern library as fallback
- If suggestions poor → Conservative defaults with user override

---

## 🎯 NEXT STEPS

**After Sprint 5 Complete**:
1. Begin Sprint 6: Builder Agent (code generation)
2. Use researcher insights for intelligent code construction
3. Implement V31-compliant scanner generation
4. Build A+ mold to scanner conversion workflow

**Integration Points**:
- Researcher → Builder: Pattern and parameter insights guide code generation
- Researcher → Analyst: Historical research informs backtest analysis
- Researcher → Planner: Similar strategies provide implementation templates

---

**Sprint 5 creates the research and intelligence foundation for all AI agent workflows.**

**By completing Sprint 5, Renata will have deep domain knowledge retrieval and pattern recognition capabilities.**

**Ready to build Builder Agent in Sprint 6.**
