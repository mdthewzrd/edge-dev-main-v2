# 📊 SPRINT 8: ANALYST AGENT
## Backtest Analysis & Strategy Optimization

**Duration**: Weeks 8-9 (14 days)
**Objective**: Build intelligent analysis agent that evaluates backtest results, performs IS/OOS validation, runs Monte Carlo simulations, analyzes market regimes, and optimizes parameters

**Success Criteria**:
- [ ] Analyst agent can analyze backtest results
- [ ] IS/OOS validation implemented
- [ ] Monte Carlo simulation working
- [ ] Market regime analysis functional
- [ ] Parameter optimization produces improvements
- [ ] CopilotKit integration for analyst actions

---

## 📋 DELIVERABLES

### Core Deliverables
- [ ] Analyst agent service with analysis capabilities
- [ ] Backtest result analyzer
- [ ] IS/OOS validation system
- [ ] Monte Carlo simulation engine
- [ ] Market regime analyzer
- [ ] Parameter optimizer
- [ ] Performance report generator
- [ ] Integration with CopilotKit actions

### Integration Points
- **Archon MCP**: Historical backtest storage, result retrieval, parameter tracking
- **Executor Agent** (Sprint 7): Backtest execution, result collection
- **Researcher Agent** (Sprint 5): Market context, regime analysis
- **Builder Agent** (Sprint 6): Parameter adjustment, scanner regeneration

---

## 🎯 DETAILED TASKS

### Task 8.1: Create Analyst Agent Service (5 hours)

**Subtasks**:
1. Create `src/services/analystAgent.ts` service structure
2. Implement analysis state management
3. Build result retrieval from Archon
4. Create metric calculation engine
5. Implement comparison logic
6. Add analysis result storage

**Code Example**:
```typescript
// src/services/analystAgent.ts

import { ArchonMCPClient } from '@/archon/archonClient';

export interface AnalysisRequest {
  backtestId: string;
  comparisonIds?: string[];
  analysisType: 'performance' | 'is-oos' | 'monte-carlo' | 'regime' | 'optimization';
  parameters?: AnalysisParameters;
}

export interface AnalysisResult {
  analysisId: string;
  backtestId: string;
  analysisType: string;
  metrics: PerformanceMetrics;
  insights: Insight[];
  recommendations: Recommendation[];
  generatedAt: Date;
}

export interface PerformanceMetrics {
  totalReturn: number;
  annualizedReturn: number;
  sharpeRatio: number;
  sortinoRatio: number;
  maxDrawdown: number;
  winRate: number;
  profitFactor: number;
  avgTrade: number;
  avgWin: number;
  avgLoss: number;
  largestWin: number;
  largestLoss: number;
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  expectancy: number;
  calmarRatio: number;
  omegaRatio: number;
}

export interface Insight {
  category: 'strength' | 'weakness' | 'opportunity' | 'risk';
  title: string;
  description: string;
  evidence: string[];
  impact: 'high' | 'medium' | 'low';
}

export interface Recommendation {
  type: 'parameter' | 'filter' | 'execution' | 'risk-management';
  priority: 'high' | 'medium' | 'low';
  action: string;
  expectedImprovement: string;
  implementation: string;
}

export class AnalystAgent {
  private archon: ArchonMCPClient;
  private executor: ExecutorAgent;

  constructor() {
    this.archon = new ArchonMCPClient();
    this.executor = new ExecutorAgent();
  }

  async analyze(request: AnalysisRequest): Promise<AnalysisResult> {
    let result: AnalysisResult;

    switch (request.analysisType) {
      case 'performance':
        result = await this.analyzePerformance(request);
        break;

      case 'is-oos':
        result = await this.analyzeISOOS(request);
        break;

      case 'monte-carlo':
        result = await this.runMonteCarlo(request);
        break;

      case 'regime':
        result = await this.analyzeRegime(request);
        break;

      case 'optimization':
        result = await this.optimizeParameters(request);
        break;

      default:
        throw new Error(`Unknown analysis type: ${request.analysisType}`);
    }

    // Store analysis in Archon
    await this.storeAnalysis(result);

    return result;
  }

  private async analyzePerformance(request: AnalysisRequest): Promise<AnalysisResult> {
    // Fetch backtest results
    const backtest = await this.fetchBacktest(request.backtestId);

    // Calculate metrics
    const metrics = this.calculateMetrics(backtest);

    // Generate insights
    const insights = this.generateInsights(metrics, backtest);

    // Generate recommendations
    const recommendations = this.generateRecommendations(metrics, insights);

    return {
      analysisId: this.generateAnalysisId(request),
      backtestId: request.backtestId,
      analysisType: 'performance',
      metrics,
      insights,
      recommendations,
      generatedAt: new Date()
    };
  }

  private calculateMetrics(backtest: BacktestResult): PerformanceMetrics {
    const trades = backtest.trades;

    // Basic calculations
    const totalReturn = trades.reduce((sum, t) => sum + t.pnl, 0);
    const winningTrades = trades.filter(t => t.pnl > 0);
    const losingTrades = trades.filter(t => t.pnl <= 0);
    const winRate = winningTrades.length / trades.length;
    const avgWin = winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length;
    const avgLoss = losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length;
    const avgTrade = totalReturn / trades.length;
    const profitFactor = Math.abs(winningTrades.reduce((sum, t) => sum + t.pnl, 0) /
                                 losingTrades.reduce((sum, t) => sum + t.pnl, 0));
    const expectancy = (avgWin * winRate) + (avgLoss * (1 - winRate));

    // Advanced calculations
    const returns = this.calculateReturns(trades);
    const sharpeRatio = this.calculateSharpeRatio(returns);
    const sortinoRatio = this.calculateSortinoRatio(returns);
    const maxDrawdown = this.calculateMaxDrawdown(returns);
    const calmarRatio = this.calculateCalmarRatio(returns, maxDrawdown);
    const omegaRatio = this.calculateOmegaRatio(returns);

    return {
      totalReturn,
      annualizedReturn: this.annualizeReturn(totalReturn, backtest.period),
      sharpeRatio,
      sortinoRatio,
      maxDrawdown,
      winRate,
      profitFactor,
      avgTrade,
      avgWin,
      avgLoss,
      largestWin: Math.max(...winningTrades.map(t => t.pnl)),
      largestLoss: Math.min(...losingTrades.map(t => t.pnl)),
      totalTrades: trades.length,
      winningTrades: winningTrades.length,
      losingTrades: losingTrades.length,
      expectancy,
      calmarRatio,
      omegaRatio
    };
  }

  private calculateReturns(trades: Trade[]): number[] {
    const returns: number[] = [];
    let cumulative = 0;

    trades.forEach(trade => {
      cumulative += trade.pnl;
      returns.push(cumulative);
    });

    return returns;
  }

  private calculateSharpeRatio(returns: number[]): number {
    if (returns.length < 2) return 0;

    const mean = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);

    return stdDev === 0 ? 0 : (mean / stdDev) * Math.sqrt(252); // Annualized
  }

  private calculateSortinoRatio(returns: number[]): number {
    if (returns.length < 2) return 0;

    const mean = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const downsideVariance = returns.reduce((sum, r) => {
      return sum + (r < mean ? Math.pow(r - mean, 2) : 0);
    }, 0) / returns.length;
    const downsideDev = Math.sqrt(downsideVariance);

    return downsideDev === 0 ? 0 : (mean / downsideDev) * Math.sqrt(252);
  }

  private calculateMaxDrawdown(returns: number[]): number {
    let maxDrawdown = 0;
    let peak = returns[0];

    for (let i = 1; i < returns.length; i++) {
      if (returns[i] > peak) {
        peak = returns[i];
      }
      const drawdown = (peak - returns[i]) / peak;
      if (drawdown > maxDrawdown) {
        maxDrawdown = drawdown;
      }
    }

    return maxDrawdown;
  }

  private calculateCalmarRatio(returns: number[], maxDrawdown: number): number {
    const totalReturn = returns[returns.length - 1];
    const annualizedReturn = this.annualizeReturn(totalReturn, { years: 1 });
    return maxDrawdown === 0 ? 0 : annualizedReturn / maxDrawdown;
  }

  private calculateOmegaRatio(returns: number[], threshold: number = 0): number {
    const gains = returns.filter(r => r > threshold).reduce((sum, r) => sum + (r - threshold), 0);
    const losses = Math.abs(returns.filter(r => r < threshold).reduce((sum, r) => sum + (r - threshold), 0));

    return losses === 0 ? 0 : gains / losses;
  }

  private annualizeReturn(totalReturn: number, period: { years: number }): number {
    return Math.pow(1 + totalReturn, 1 / period.years) - 1;
  }

  private generateInsights(
    metrics: PerformanceMetrics,
    backtest: BacktestResult
  ): Insight[] {
    const insights: Insight[] = [];

    // Analyze win rate
    if (metrics.winRate > 0.6) {
      insights.push({
        category: 'strength',
        title: 'High Win Rate',
        description: `Win rate of ${(metrics.winRate * 100).toFixed(1)}% is excellent.`,
        evidence: [`Win rate: ${(metrics.winRate * 100).toFixed(1)}%`],
        impact: 'high'
      });
    } else if (metrics.winRate < 0.4) {
      insights.push({
        category: 'weakness',
        title: 'Low Win Rate',
        description: `Win rate of ${(metrics.winRate * 100).toFixed(1)}% may need improvement.`,
        evidence: [`Win rate: ${(metrics.winRate * 100).toFixed(1)}%`],
        impact: 'high'
      });
    }

    // Analyze profit factor
    if (metrics.profitFactor > 2.0) {
      insights.push({
        category: 'strength',
        title: 'Strong Profit Factor',
        description: `Profit factor of ${metrics.profitFactor.toFixed(2)} indicates good risk/reward.`,
        evidence: [`Profit factor: ${metrics.profitFactor.toFixed(2)}`],
        impact: 'high'
      });
    }

    // Analyze drawdown
    if (metrics.maxDrawdown > 0.3) {
      insights.push({
        category: 'risk',
        title: 'High Maximum Drawdown',
        description: `Maximum drawdown of ${(metrics.maxDrawdown * 100).toFixed(1)}% is concerning.`,
        evidence: [`Max drawdown: ${(metrics.maxDrawdown * 100).toFixed(1)}%`],
        impact: 'high'
      });
    }

    // Analyze Sharpe ratio
    if (metrics.sharpeRatio > 2.0) {
      insights.push({
        category: 'strength',
        title: 'Excellent Risk-Adjusted Returns',
        description: `Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)} is excellent.`,
        evidence: [`Sharpe ratio: ${metrics.sharpeRatio.toFixed(2)}`],
        impact: 'high'
      });
    } else if (metrics.sharpeRatio < 1.0) {
      insights.push({
        category: 'weakness',
        title: 'Low Risk-Adjusted Returns',
        description: `Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)} is below optimal.`,
        evidence: [`Sharpe ratio: ${metrics.sharpeRatio.toFixed(2)}`],
        impact: 'medium'
      });
    }

    return insights;
  }

  private generateRecommendations(
    metrics: PerformanceMetrics,
    insights: Insight[]
  ): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // Based on insights
    insights.forEach(insight => {
      if (insight.category === 'risk') {
        recommendations.push({
          type: 'risk-management',
          priority: insight.impact === 'high' ? 'high' : 'medium',
          action: `Address: ${insight.title}`,
          expectedImprovement: 'Reduced drawdown, improved risk-adjusted returns',
          implementation: 'Consider adding stop-loss, position sizing, or filters'
        });
      }
    });

    // Specific recommendations based on metrics
    if (metrics.maxDrawdown > 0.25) {
      recommendations.push({
        type: 'risk-management',
        priority: 'high',
        action: 'Implement position sizing',
        expectedImprovement: 'Reduce maximum drawdown by 30-50%',
        implementation: 'Use volatility-based or Kelly criterion position sizing'
      });
    }

    if (metrics.winRate < 0.45) {
      recommendations.push({
        type: 'filter',
        priority: 'high',
        action: 'Add entry filters',
        expectedImprovement: 'Improve win rate by 5-10%',
        implementation: 'Add volume, trend, or momentum confirmation filters'
      });
    }

    if (metrics.profitFactor < 1.5) {
      recommendations.push({
        type: 'execution',
        priority: 'medium',
        action: 'Optimize exit strategy',
        expectedImprovement: 'Improve profit factor to 2.0+',
        implementation: 'Consider trailing stops, profit targets, or time-based exits'
      });
    }

    return recommendations;
  }

  private async fetchBacktest(backtestId: string): Promise<BacktestResult> {
    // Fetch from Archon or backend
    const response = await fetch(`http://localhost:8000/backtest/${backtestId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch backtest');
    }
    return await response.json();
  }

  private async storeAnalysis(analysis: AnalysisResult): Promise<void> {
    await this.archon.manageTask({
      task_id: analysis.analysisId,
      status: 'completed',
      result: JSON.stringify(analysis),
      metadata: {
        backtest_id: analysis.backtestId,
        analysis_type: analysis.analysisType,
        timestamp: analysis.generatedAt.toISOString()
      }
    });
  }

  private generateAnalysisId(request: AnalysisRequest): string {
    return `analysis_${Date.now()}_${request.analysisType}`;
  }

  // ... other analysis methods (ISOOS, Monte Carlo, Regime, Optimization)
}
```

**Acceptance Criteria**:
- [ ] Analyst service created with all core methods
- [ ] All performance metrics calculated correctly
- [ ] Insights generated make sense
- [ ] Recommendations are actionable
- [ ] All methods have unit tests

**Dependencies**:
- Archon MCP (Sprint 2)
- Executor Agent (Sprint 7)

**Risks**:
- **Risk**: Metric calculation errors
  - **Mitigation**: Extensive validation against known results

---

### Task 8.2: Implement IS/OOS Validation (6 hours)

**Subtasks**:
1. Create IS/OOS splitter
2. Implement in-sample analysis
3. Implement out-of-sample analysis
4. Build overfitting detector
5. Create IS/OOS comparison report
6. Generate overfitting recommendations

**Code Example**:
```typescript
// src/services/isoosValidator.ts

export interface ISOOSRequest {
  backtestId: string;
  inSamplePeriod: DateRange;
  outOfSamplePeriod: DateRange;
  minTrades?: number;
}

export interface ISOOSResult {
  backtestId: string;
  inSample: PerformanceMetrics;
  outOfSample: PerformanceMetrics;
  comparison: ISOOSComparison;
  overfittingScore: number;
  overfitting: boolean;
  insights: ISOOSInsight[];
}

export interface ISOOSComparison {
  returnDecay: number;
  sharpeDecay: number;
  winRateDecay: number;
  drawdownIncrease: number;
  overallDegradation: number;
}

export interface ISOOSInsight {
  metric: string;
  inSampleValue: number;
  outOfSampleValue: number;
  degradation: number;
  acceptable: boolean;
  concern: string;
}

export class ISOOSValidator {
  private executor: ExecutorAgent;
  private analyst: AnalystAgent;

  constructor() {
    this.executor = new ExecutorAgent();
    this.analyst = new AnalystAgent();
  }

  async validate(request: ISOOSRequest): Promise<ISOOSResult> {
    // Fetch backtest results
    const backtest = await this.fetchBacktest(request.backtestId);

    // Split into IS and OOS periods
    const inSampleTrades = this.filterTradesByPeriod(
      backtest.trades,
      request.inSamplePeriod
    );
    const outOfSampleTrades = this.filterTradesByPeriod(
      backtest.trades,
      request.outOfSamplePeriod
    );

    // Check minimum trades
    if (request.minTrades && outOfSampleTrades.length < request.minTrades) {
      throw new Error(
        `Insufficient OOS trades: ${outOfSampleTrades.length} < ${request.minTrades}`
      );
    }

    // Calculate metrics for each period
    const inSampleMetrics = this.calculateMetrics(inSampleTrades, request.inSamplePeriod);
    const outOfSampleMetrics = this.calculateMetrics(outOfSampleTrades, request.outOfSamplePeriod);

    // Compare performance
    const comparison = this.comparePerformance(inSampleMetrics, outOfSampleMetrics);

    // Calculate overfitting score
    const overfittingScore = this.calculateOverfittingScore(comparison);

    // Generate insights
    const insights = this.generateInsights(inSampleMetrics, outOfSampleMetrics, comparison);

    return {
      backtestId: request.backtestId,
      inSample: inSampleMetrics,
      outOfSample: outOfSampleMetrics,
      comparison,
      overfittingScore,
      overfitting: overfittingScore > 0.5,
      insights
    };
  }

  private filterTradesByPeriod(trades: Trade[], period: DateRange): Trade[] {
    const start = new Date(period.start);
    const end = new Date(period.end);

    return trades.filter(trade => {
      const tradeDate = new Date(trade.date);
      return tradeDate >= start && tradeDate <= end;
    });
  }

  private calculateMetrics(trades: Trade[], period: DateRange): PerformanceMetrics {
    // Reuse analyst agent's metric calculation
    const backtest = {
      trades,
      period: { years: this.calculateYears(period) }
    };

    return this.analyst['calculateMetrics'](backtest);
  }

  private calculateYears(period: DateRange): number {
    const start = new Date(period.start);
    const end = new Date(period.end);
    return (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24 * 365);
  }

  private comparePerformance(
    is: PerformanceMetrics,
    oos: PerformanceMetrics
  ): ISOOSComparison {
    const returnDecay = (is.annualizedReturn - oos.annualizedReturn) / is.annualizedReturn;
    const sharpeDecay = (is.sharpeRatio - oos.sharpeRatio) / is.sharpeRatio;
    const winRateDecay = (is.winRate - oos.winRate) / is.winRate;
    const drawdownIncrease = (oos.maxDrawdown - is.maxDrawdown) / is.maxDrawdown;

    const overallDegradation = (
      returnDecay +
      sharpeDecay +
      winRateDecay +
      drawdownIncrease
    ) / 4;

    return {
      returnDecay,
      sharpeDecay,
      winRateDecay,
      drawdownIncrease,
      overallDegradation
    };
  }

  private calculateOverfittingScore(comparison: ISOOSComparison): number {
    // Score ranges from 0 (no overfitting) to 1 (severe overfitting)
    let score = 0;

    // Return decay > 30% is concerning
    score += Math.max(0, (comparison.returnDecay - 0.3) / 0.7);

    // Sharpe decay > 40% is concerning
    score += Math.max(0, (comparison.sharpeDecay - 0.4) / 0.6);

    // Win rate decay > 20% is concerning
    score += Math.max(0, (comparison.winRateDecay - 0.2) / 0.8);

    // Drawdown increase > 50% is concerning
    score += Math.max(0, (comparison.drawdownIncrease - 0.5) / 0.5);

    return Math.min(score / 4, 1);
  }

  private generateInsights(
    is: PerformanceMetrics,
    oos: PerformanceMetrics,
    comparison: ISOOSComparison
  ): ISOOSInsight[] {
    const insights: ISOOSInsight[] = [];

    // Return insight
    insights.push({
      metric: 'Annualized Return',
      inSampleValue: is.annualizedReturn,
      outOfSampleValue: oos.annualizedReturn,
      degradation: comparison.returnDecay,
      acceptable: comparison.returnDecay < 0.3,
      concern: comparison.returnDecay > 0.3
        ? 'Significant return decay indicates potential overfitting'
        : 'Return decay within acceptable range'
    });

    // Sharpe ratio insight
    insights.push({
      metric: 'Sharpe Ratio',
      inSampleValue: is.sharpeRatio,
      outOfSampleValue: oos.sharpeRatio,
      degradation: comparison.sharpeDecay,
      acceptable: comparison.sharpeDecay < 0.4,
      concern: comparison.sharpeDecay > 0.4
        ? 'Sharpe ratio decay suggests strategy may not generalize'
        : 'Sharpe ratio degradation acceptable'
    });

    // Win rate insight
    insights.push({
      metric: 'Win Rate',
      inSampleValue: is.winRate,
      outOfSampleValue: oos.winRate,
      degradation: comparison.winRateDecay,
      acceptable: comparison.winRateDecay < 0.2,
      concern: comparison.winRateDecay > 0.2
        ? 'Win rate decay indicates possible overfitting'
        : 'Win rate stable across periods'
    });

    // Drawdown insight
    insights.push({
      metric: 'Max Drawdown',
      inSampleValue: is.maxDrawdown,
      outOfSampleValue: oos.maxDrawdown,
      degradation: comparison.drawdownIncrease,
      acceptable: comparison.drawdownIncrease < 0.5,
      concern: comparison.drawdownIncrease > 0.5
        ? 'Drawdown significantly higher in OOS - risk management concern'
        : 'Drawdown consistent across periods'
    });

    return insights;
  }

  private async fetchBacktest(backtestId: string): Promise<any> {
    const response = await fetch(`http://localhost:8000/backtest/${backtestId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch backtest');
    }
    return await response.json();
  }
}
```

**Acceptance Criteria**:
- [ ] Can split backtest into IS/OOS periods
- [ ] Metrics calculated for both periods
- [ ] Overfitting detection accurate
- [ ] Insights generated correctly
- [ ] Performance: Validation completes in <5 seconds

**Dependencies**:
- Analyst agent service (Task 8.1)
- Executor agent (Sprint 7)

**Risks**:
- **Risk**: Insufficient OOS data
  - **Mitigation**: Minimum trade requirements, period validation

---

### Task 8.3: Implement Monte Carlo Simulation (6 hours)

**Subtasks**:
1. Create Monte Carlo simulation engine
2. Implement trade shuffling
3. Build resampling methods
4. Create confidence interval calculator
5. Generate distribution analysis
6. Build Monte Carlo report

**Code Example**:
```typescript
// src/services/monteCarloSimulator.ts

export interface MonteCarloRequest {
  backtestId: string;
  simulations: number;
  confidenceLevel: number; // 0.95 for 95% confidence
  method: 'shuffle' | 'resample' | 'bootstrap';
}

export interface MonteCarloResult {
  backtestId: string;
  simulations: number;
  method: string;
  originalMetrics: PerformanceMetrics;
  simulatedMetrics: SimulationMetrics;
  confidenceIntervals: ConfidenceIntervals;
  distribution: DistributionAnalysis;
  probabilityOfProfit: number;
  riskOfRuin: number;
}

export interface SimulationMetrics {
  mean: PerformanceMetrics;
  median: PerformanceMetrics;
  percentile5: PerformanceMetrics;
  percentile95: PerformanceMetrics;
  stdDev: number;
}

export interface ConfidenceIntervals {
  return: [number, number]; // [lower, upper]
  sharpe: [number, number];
  maxDrawdown: [number, number];
  winRate: [number, number];
}

export interface DistributionAnalysis {
  returnDistribution: number[];
  drawdownDistribution: number[];
  sharpeDistribution: number[];
}

export class MonteCarloSimulator {
  private analyst: AnalystAgent;

  constructor() {
    this.analyst = new AnalystAgent();
  }

  async simulate(request: MonteCarloRequest): Promise<MonteCarloResult> {
    // Fetch original backtest
    const backtest = await this.fetchBacktest(request.backtestId);
    const originalMetrics = this.analyst['calculateMetrics'](backtest);

    // Run simulations
    const simulatedMetrics = await this.runSimulations(
      backtest.trades,
      request.simulations,
      request.method
    );

    // Calculate confidence intervals
    const confidenceIntervals = this.calculateConfidenceIntervals(
      simulatedMetrics,
      request.confidenceLevel
    );

    // Analyze distributions
    const distribution = this.analyzeDistributions(simulatedMetrics);

    // Calculate probability metrics
    const probabilityOfProfit = this.calculateProbabilityOfProfit(simulatedMetrics);
    const riskOfRuin = this.calculateRiskOfRuin(simulatedMetrics);

    return {
      backtestId: request.backtestId,
      simulations: request.simulations,
      method: request.method,
      originalMetrics,
      simulatedMetrics,
      confidenceIntervals,
      distribution,
      probabilityOfProfit,
      riskOfRuin
    };
  }

  private async runSimulations(
    trades: Trade[],
    numSimulations: number,
    method: string
  ): Promise<SimulationMetrics> {
    const results: PerformanceMetrics[] = [];

    for (let i = 0; i < numSimulations; i++) {
      let simulatedTrades: Trade[];

      switch (method) {
        case 'shuffle':
          simulatedTrades = this.shuffleTrades(trades);
          break;
        case 'resample':
          simulatedTrades = this.resampleTrades(trades);
          break;
        case 'bootstrap':
          simulatedTrades = this.bootstrapTrades(trades);
          break;
        default:
          throw new Error(`Unknown simulation method: ${method}`);
      }

      const metrics = this.analyst['calculateMetrics']({ trades: simulatedTrades });
      results.push(metrics);
    }

    return this.aggregateResults(results);
  }

  private shuffleTrades(trades: Trade[]): Trade[] {
    // Fisher-Yates shuffle
    const shuffled = [...trades];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }

  private resampleTrades(trades: Trade[]): Trade[] {
    // Resample with replacement
    const resampled: Trade[] = [];
    for (let i = 0; i < trades.length; i++) {
      const randomIndex = Math.floor(Math.random() * trades.length);
      resampled.push(trades[randomIndex]);
    }
    return resampled;
  }

  private bootstrapTrades(trades: Trade[]): Trade[] {
    // Bootstrap: resample blocks to preserve some time series properties
    const blockSize = Math.max(5, Math.floor(trades.length / 50));
    const bootstrapped: Trade[] = [];

    while (bootstrapped.length < trades.length) {
      const startIndex = Math.floor(Math.random() * (trades.length - blockSize));
      const block = trades.slice(startIndex, startIndex + blockSize);
      bootstrapped.push(...block);
    }

    return bootstrapped.slice(0, trades.length);
  }

  private aggregateResults(results: PerformanceMetrics[]): SimulationMetrics {
    const mean = this.calculateMeanMetrics(results);
    const median = this.calculateMedianMetrics(results);
    const percentile5 = this.calculatePercentileMetrics(results, 5);
    const percentile95 = this.calculatePercentileMetrics(results, 95);

    const returns = results.map(r => r.totalReturn);
    const stdDev = this.calculateStdDev(returns);

    return {
      mean,
      median,
      percentile5,
      percentile95,
      stdDev
    };
  }

  private calculateMeanMetrics(results: PerformanceMetrics[]): PerformanceMetrics {
    const n = results.length;

    return {
      totalReturn: results.reduce((sum, r) => sum + r.totalReturn, 0) / n,
      annualizedReturn: results.reduce((sum, r) => sum + r.annualizedReturn, 0) / n,
      sharpeRatio: results.reduce((sum, r) => sum + r.sharpeRatio, 0) / n,
      sortinoRatio: results.reduce((sum, r) => sum + r.sortinoRatio, 0) / n,
      maxDrawdown: results.reduce((sum, r) => sum + r.maxDrawdown, 0) / n,
      winRate: results.reduce((sum, r) => sum + r.winRate, 0) / n,
      profitFactor: results.reduce((sum, r) => sum + r.profitFactor, 0) / n,
      avgTrade: results.reduce((sum, r) => sum + r.avgTrade, 0) / n,
      avgWin: results.reduce((sum, r) => sum + r.avgWin, 0) / n,
      avgLoss: results.reduce((sum, r) => sum + r.avgLoss, 0) / n,
      largestWin: results.reduce((sum, r) => sum + r.largestWin, 0) / n,
      largestLoss: results.reduce((sum, r) => sum + r.largestLoss, 0) / n,
      totalTrades: results.reduce((sum, r) => sum + r.totalTrades, 0) / n,
      winningTrades: results.reduce((sum, r) => sum + r.winningTrades, 0) / n,
      losingTrades: results.reduce((sum, r) => sum + r.losingTrades, 0) / n,
      expectancy: results.reduce((sum, r) => sum + r.expectancy, 0) / n,
      calmarRatio: results.reduce((sum, r) => sum + r.calmarRatio, 0) / n,
      omegaRatio: results.reduce((sum, r) => sum + r.omegaRatio, 0) / n
    };
  }

  private calculateMedianMetrics(results: PerformanceMetrics[]): PerformanceMetrics {
    const sorted = [...results].sort((a, b) => a.totalReturn - b.totalReturn);
    const mid = Math.floor(sorted.length / 2);

    return sorted.length % 2 === 0
      ? this.meanMetrics(sorted[mid - 1], sorted[mid])
      : sorted[mid];
  }

  private meanMetrics(a: PerformanceMetrics, b: PerformanceMetrics): PerformanceMetrics {
    return {
      totalReturn: (a.totalReturn + b.totalReturn) / 2,
      annualizedReturn: (a.annualizedReturn + b.annualizedReturn) / 2,
      sharpeRatio: (a.sharpeRatio + b.sharpeRatio) / 2,
      sortinoRatio: (a.sortinoRatio + b.sortinoRatio) / 2,
      maxDrawdown: (a.maxDrawdown + b.maxDrawdown) / 2,
      winRate: (a.winRate + b.winRate) / 2,
      profitFactor: (a.profitFactor + b.profitFactor) / 2,
      avgTrade: (a.avgTrade + b.avgTrade) / 2,
      avgWin: (a.avgWin + b.avgWin) / 2,
      avgLoss: (a.avgLoss + b.avgLoss) / 2,
      largestWin: (a.largestWin + b.largestWin) / 2,
      largestLoss: (a.largestLoss + b.largestLoss) / 2,
      totalTrades: (a.totalTrades + b.totalTrades) / 2,
      winningTrades: (a.winningTrades + b.winningTrades) / 2,
      losingTrades: (a.losingTrades + b.losingTrades) / 2,
      expectancy: (a.expectancy + b.expectancy) / 2,
      calmarRatio: (a.calmarRatio + b.calmarRatio) / 2,
      omegaRatio: (a.omegaRatio + b.omegaRatio) / 2
    };
  }

  private calculatePercentileMetrics(
    results: PerformanceMetrics[],
    percentile: number
  ): PerformanceMetrics {
    const sorted = [...results].sort((a, b) => a.totalReturn - b.totalReturn);
    const index = Math.floor((percentile / 100) * sorted.length);
    return sorted[index];
  }

  private calculateStdDev(values: number[]): number {
    const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
    const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length;
    return Math.sqrt(variance);
  }

  private calculateConfidenceIntervals(
    simulated: SimulationMetrics,
    confidenceLevel: number
  ): ConfidenceIntervals {
    const alpha = 1 - confidenceLevel;

    return {
      return: [simulated.percentile5.totalReturn, simulated.percentile95.totalReturn],
      sharpe: [simulated.percentile5.sharpeRatio, simulated.percentile95.sharpeRatio],
      maxDrawdown: [simulated.percentile5.maxDrawdown, simulated.percentile95.maxDrawdown],
      winRate: [simulated.percentile5.winRate, simulated.percentile95.winRate]
    };
  }

  private analyzeDistributions(simulated: SimulationMetrics): DistributionAnalysis {
    // Extract distribution data from simulation results
    return {
      returnDistribution: [], // Would be populated during simulation
      drawdownDistribution: [],
      sharpeDistribution: []
    };
  }

  private calculateProbabilityOfProfit(simulated: SimulationMetrics): number {
    // Percentage of simulations with positive return
    // This is a simplified calculation
    return simulated.mean.totalReturn > 0 ? 0.95 : 0.5;
  }

  private calculateRiskOfRuin(simulated: SimulationMetrics): number {
    // Percentage of simulations with drawdown > 50%
    return simulated.percentile95.maxDrawdown > 0.5 ? 0.1 : 0.01;
  }

  private async fetchBacktest(backtestId: string): Promise<any> {
    const response = await fetch(`http://localhost:8000/backtest/${backtestId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch backtest');
    }
    return await response.json();
  }
}
```

**Acceptance Criteria**:
- [ ] Can run 1000+ simulations
- [ ] All shuffle methods work
- [ ] Confidence intervals calculated correctly
- [ ] Distribution analysis provides insights
- [ ] Performance: 1000 simulations complete in <30 seconds

**Dependencies**:
- Analyst agent service (Task 8.1)

**Risks**:
- **Risk**: Simulation takes too long
  - **Mitigation**: Parallel processing, optimized algorithms

---

### Task 8.4: Implement Market Regime Analyzer (4 hours)

**Subtasks**:
1. Create regime detection for backtest periods
2. Implement regime-specific performance analysis
3. Build regime comparison
4. Create regime transition analysis
5. Generate regime recommendations

**Code Example**:
```typescript
// src/services/regimeAnalyzer.ts

export interface RegimeAnalysisRequest {
  backtestId: string;
}

export interface RegimeAnalysisResult {
  backtestId: string;
  regimes: RegimePerformance[];
  bestRegime: string;
  worstRegime: string;
  regimeTransitions: RegimeTransition[];
  recommendations: RegimeRecommendation[];
}

export interface RegimePerformance {
  regime: string;
  trades: number;
  totalReturn: number;
  winRate: number;
  sharpeRatio: number;
  maxDrawdown: number;
  characteristics: string[];
}

export interface RegimeTransition {
  from: string;
  to: string;
  performanceAfter: string;
  tradesAfterTransition: number;
}

export interface RegimeRecommendation {
  regime: string;
  action: 'avoid' | 'favor' | 'neutral';
  reason: string;
  adjustment: string;
}

export class RegimeAnalyzer {
  private researcher: ResearcherAgent;

  constructor() {
    this.researcher = new ResearcherAgent();
  }

  async analyze(request: RegimeAnalysisRequest): Promise<RegimeAnalysisResult> {
    // Fetch backtest with market data
    const backtest = await this.fetchBacktestWithMarketData(request.backtestId);

    // Detect regime for each trade
    const tradesWithRegimes = await this.annotateTradesWithRegimes(backtest.trades);

    // Group by regime
    const regimes = this.groupByRegime(tradesWithRegimes);

    // Calculate performance for each regime
    const regimePerformance = this.calculateRegimePerformance(regimes);

    // Identify best and worst regimes
    const bestRegime = this.findBestRegime(regimePerformance);
    const worstRegime = this.findWorstRegime(regimePerformance);

    // Analyze regime transitions
    const regimeTransitions = this.analyzeRegimeTransitions(tradesWithRegimes);

    // Generate recommendations
    const recommendations = this.generateRegimeRecommendations(regimePerformance);

    return {
      backtestId: request.backtestId,
      regimes: regimePerformance,
      bestRegime,
      worstRegime,
      regimeTransitions,
      recommendations
    };
  }

  private async annotateTradesWithRegimes(trades: Trade[]): Promise<TradeWithRegime[]> {
    const tradesWithRegimes: TradeWithRegime[] = [];

    for (const trade of trades) {
      // Get market regime at trade time
      const regime = await this.getRegimeAtDate(trade.date, trade.ticker);

      tradesWithRegimes.push({
        ...trade,
        regime: regime.trendStage
      });
    }

    return tradesWithRegimes;
  }

  private async getRegimeAtDate(date: string, ticker: string): Promise<MarketRegime> {
    // Use researcher agent's regime analysis
    const analyzer = new MarketRegimeAnalyzer();
    return await analyzer.analyzeRegime([ticker], 'daily');
  }

  private groupByRegime(trades: TradeWithRegime[]): Map<string, Trade[]> {
    const grouped = new Map<string, Trade[]>();

    trades.forEach(trade => {
      const regime = trade.regime || 'unknown';
      if (!grouped.has(regime)) {
        grouped.set(regime, []);
      }
      grouped.get(regime)!.push(trade);
    });

    return grouped;
  }

  private calculateRegimePerformance(grouped: Map<string, Trade[]>): RegimePerformance[] {
    const performances: RegimePerformance[] = [];

    grouped.forEach((trades, regime) => {
      const totalReturn = trades.reduce((sum, t) => sum + t.pnl, 0);
      const winningTrades = trades.filter(t => t.pnl > 0);
      const winRate = winningTrades.length / trades.length;

      const returns = this.calculateReturns(trades);
      const sharpeRatio = this.calculateSharpeRatio(returns);
      const maxDrawdown = this.calculateMaxDrawdown(returns);

      const characteristics = this.getRegimeCharacteristics(regime);

      performances.push({
        regime,
        trades: trades.length,
        totalReturn,
        winRate,
        sharpeRatio,
        maxDrawdown,
        characteristics
      });
    });

    return performances;
  }

  private getRegimeCharacteristics(regime: string): string[] {
    const characteristics: Record<string, string[]> = {
      'uptrend': ['Strong momentum', 'Higher highs', 'Bullish'],
      'downtrend': ['Weak momentum', 'Lower lows', 'Bearish'],
      'consolidation': ['Sideways', 'Range-bound', 'Neutral'],
      'breakout': ['High volatility', 'Trend initiation'],
      'extreme-deviation': ['Overextended', 'Potential reversal']
    };

    return characteristics[regime] || ['Unknown regime'];
  }

  private findBestRegime(performances: RegimePerformance[]): string {
    return performances.reduce((best, p) =>
      p.sharpeRatio > best.sharpeRatio ? p : best
    ).regime;
  }

  private findWorstRegime(performances: RegimePerformance[]): string {
    return performances.reduce((worst, p) =>
      p.sharpeRatio < worst.sharpeRatio ? p : worst
    ).regime;
  }

  private analyzeRegimeTransitions(trades: TradeWithRegime[]): RegimeTransition[] {
    const transitions: RegimeTransition[] = [];

    // Find regime changes
    for (let i = 1; i < trades.length; i++) {
      const prevTrade = trades[i - 1];
      const currTrade = trades[i];

      if (prevTrade.regime !== currTrade.regime) {
        // Look at performance after transition
        const subsequentTrades = trades.slice(i, i + 10);
        const avgReturn = subsequentTrades.reduce((sum, t) => sum + t.pnl, 0) / subsequentTrades.length;

        transitions.push({
          from: prevTrade.regime!,
          to: currTrade.regime!,
          performanceAfter: avgReturn > 0 ? 'positive' : 'negative',
          tradesAfterTransition: subsequentTrades.length
        });
      }
    }

    return transitions;
  }

  private generateRegimeRecommendations(performances: RegimePerformance[]): RegimeRecommendation[] {
    const recommendations: RegimeRecommendation[] = [];

    const avgSharpe = performances.reduce((sum, p) => sum + p.sharpeRatio, 0) / performances.length;

    performances.forEach(p => {
      let action: 'avoid' | 'favor' | 'neutral';
      let reason: string;
      let adjustment: string;

      if (p.sharpeRatio > avgSharpe * 1.5) {
        action = 'favor';
        reason = `Strong performance in ${p.regime} (Sharpe: ${p.sharpeRatio.toFixed(2)})`;
        adjustment = 'Increase position sizes during this regime';
      } else if (p.sharpeRatio < avgSharpe * 0.5) {
        action = 'avoid';
        reason = `Poor performance in ${p.regime} (Sharpe: ${p.sharpeRatio.toFixed(2)})`;
        adjustment = 'Reduce position sizes or avoid trading during this regime';
      } else {
        action = 'neutral';
        reason = `Average performance in ${p.regime} (Sharpe: ${p.sharpeRatio.toFixed(2)})`;
        adjustment = 'Maintain normal position sizes';
      }

      recommendations.push({
        regime: p.regime,
        action,
        reason,
        adjustment
      });
    });

    return recommendations;
  }

  private calculateReturns(trades: Trade[]): number[] {
    const returns: number[] = [];
    let cumulative = 0;

    trades.forEach(trade => {
      cumulative += trade.pnl;
      returns.push(cumulative);
    });

    return returns;
  }

  private calculateSharpeRatio(returns: number[]): number {
    if (returns.length < 2) return 0;

    const mean = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);

    return stdDev === 0 ? 0 : (mean / stdDev) * Math.sqrt(252);
  }

  private calculateMaxDrawdown(returns: number[]): number {
    let maxDrawdown = 0;
    let peak = returns[0];

    for (let i = 1; i < returns.length; i++) {
      if (returns[i] > peak) {
        peak = returns[i];
      }
      const drawdown = (peak - returns[i]) / peak;
      if (drawdown > maxDrawdown) {
        maxDrawdown = drawdown;
      }
    }

    return maxDrawdown;
  }

  private async fetchBacktestWithMarketData(backtestId: string): Promise<any> {
    const response = await fetch(`http://localhost:8000/backtest/${backtestId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch backtest');
    }
    return await response.json();
  }
}

interface TradeWithRegime extends Trade {
  regime?: string;
}
```

**Acceptance Criteria**:
- [ ] Can detect regimes for backtest periods
- [ ] Regime-specific performance calculated
- [ ] Recommendations are sensible
- [ ] Transition analysis provides insights

**Dependencies**:
- Researcher Agent (Sprint 5) - Market regime analysis
- Analyst agent service (Task 8.1)

**Risks**:
- **Risk**: Regime detection inaccurate
  - **Mitigation**: Use multiple detection methods, manual validation

---

### Task 8.5: Implement Parameter Optimizer (5 hours)

**Subtasks**:
1. Create optimization strategy (grid search, random search, Bayesian)
2. Implement objective function (Sharpe, profit factor, etc.)
3. Build optimization engine
4. Implement parameter constraints
5. Create optimization report
6. Generate optimized scanner code

**Code Example**:
```typescript
// src/services/parameterOptimizer.ts

export interface OptimizationRequest {
  backtestId: string;
  scannerCode: string;
  scannerName: string;
  parameters: ParameterRange[];
  objective: 'sharpe' | 'profit-factor' | 'return' | 'custom';
  optimizationMethod: 'grid' | 'random' | 'bayesian';
  maxIterations: number;
  constraints?: OptimizationConstraint[];
}

export interface ParameterRange {
  name: string;
  min: number;
  max: number;
  step?: number;
}

export interface OptimizationConstraint {
  type: 'max-drawdown' | 'min-trades' | 'win-rate';
  value: number;
}

export interface OptimizationResult {
  scannerName: string;
  bestParameters: Record<string, number>;
  bestMetrics: PerformanceMetrics;
  objectiveValue: number;
  iterations: number;
  optimizationCurve: OptimizationPoint[];
  convergence: boolean;
  improved: boolean;
  improvement: string;
  optimizedCode: string;
}

export interface OptimizationPoint {
  iteration: number;
  parameters: Record<string, number>;
  objectiveValue: number;
  metrics: PerformanceMetrics;
}

export class ParameterOptimizer {
  private executor: ExecutorAgent;
  private analyst: AnalystAgent;
  private builder: BuilderAgent;

  constructor() {
    this.executor = new ExecutorAgent();
    this.analyst = new AnalystAgent();
    this.builder = new BuilderAgent();
  }

  async optimize(request: OptimizationRequest): Promise<OptimizationResult> {
    const optimizationCurve: OptimizationPoint[] = [];
    let bestParameters: Record<string, number> = {};
    let bestMetrics: PerformanceMetrics | null = null;
    let bestObjectiveValue = -Infinity;

    // Generate parameter combinations based on method
    const combinations = this.generateParameterCombinations(request);

    // Limit iterations
    const iterations = Math.min(combinations.length, request.maxIterations);

    for (let i = 0; i < iterations; i++) {
      const parameters = combinations[i];

      // Generate optimized scanner code
      const scannerCode = this.updateParameters(request.scannerCode, parameters);

      try {
        // Execute backtest
        const execution = await this.executor.execute({
          scannerCode,
          scannerName: `${request.scannerName}_opt_${i}`,
          executionType: 'backtest'
        });

        // Collect results
        const collected = await this.executor['resultCollector'].collect(execution.executionId);

        // Calculate metrics
        const backtest = { trades: collected.results, period: { years: 1 } };
        const metrics = this.analyst['calculateMetrics'](backtest);

        // Check constraints
        if (this.satisfiesConstraints(metrics, request.constraints)) {
          // Calculate objective value
          const objectiveValue = this.calculateObjective(metrics, request.objective);

          // Update best if improved
          if (objectiveValue > bestObjectiveValue) {
            bestObjectiveValue = objectiveValue;
            bestParameters = parameters;
            bestMetrics = metrics;
          }

          // Track optimization curve
          optimizationCurve.push({
            iteration: i,
            parameters,
            objectiveValue,
            metrics
          });
        }
      } catch (error) {
        console.error(`Optimization iteration ${i} failed:`, error);
      }
    }

    // Check convergence
    const convergence = this.checkConvergence(optimizationCurve);

    // Calculate improvement
    const originalBacktest = await this.fetchBacktest(request.backtestId);
    const originalMetrics = this.analyst['calculateMetrics'](originalBacktest);
    const improved = bestMetrics !== null && this.isImproved(bestMetrics, originalMetrics, request.objective);
    const improvement = this.calculateImprovement(bestMetrics || originalMetrics, originalMetrics, request.objective);

    // Generate optimized scanner code
    const optimizedCode = bestMetrics
      ? this.updateParameters(request.scannerCode, bestParameters)
      : request.scannerCode;

    return {
      scannerName: request.scannerName,
      bestParameters,
      bestMetrics: bestMetrics || originalMetrics,
      objectiveValue: bestObjectiveValue,
      iterations,
      optimizationCurve,
      convergence,
      improved,
      improvement,
      optimizedCode
    };
  }

  private generateParameterCombinations(request: OptimizationRequest): Record<string, number>[] {
    const combinations: Record<string, number>[] = [];

    switch (request.optimizationMethod) {
      case 'grid':
        return this.gridSearch(request.parameters);
      case 'random':
        return this.randomSearch(request.parameters, request.maxIterations);
      case 'bayesian':
        return this.bayesianOptimization(request.parameters, request.maxIterations);
      default:
        throw new Error(`Unknown optimization method: ${request.optimizationMethod}`);
    }
  }

  private gridSearch(parameters: ParameterRange[]): Record<string, number>[] {
    const combinations: Record<string, number>[] = [];

    // Generate all combinations
    const generate = (index: number, current: Record<string, number>) => {
      if (index >= parameters.length) {
        combinations.push({ ...current });
        return;
      }

      const param = parameters[index];
      const step = param.step || 1;
      const values: number[] = [];

      for (let v = param.min; v <= param.max; v += step) {
        values.push(v);
      }

      values.forEach(value => {
        current[param.name] = value;
        generate(index + 1, current);
      });
    };

    generate(0, {});

    return combinations;
  }

  private randomSearch(parameters: ParameterRange[], iterations: number): Record<string, number>[] {
    const combinations: Record<string, number>[] = [];

    for (let i = 0; i < iterations; i++) {
      const combination: Record<string, number> = {};

      parameters.forEach(param => {
        const range = param.max - param.min;
        const random = Math.random() * range + param.min;
        combination[param.name] = Math.round(random / (param.step || 1)) * (param.step || 1);
      });

      combinations.push(combination);
    }

    return combinations;
  }

  private bayesianOptimization(
    parameters: ParameterRange[],
    iterations: number
  ): Record<string, number>[] {
    // Simplified Bayesian optimization
    // Real implementation would use Gaussian Processes
    const combinations: Record<string, number>[] = [];

    // Start with random initial samples
    const initialSamples = Math.min(10, iterations);
    combinations.push(...this.randomSearch(parameters, initialSamples));

    // Would then use acquisition function to select next samples
    // For now, just use random search
    const remaining = iterations - initialSamples;
    if (remaining > 0) {
      combinations.push(...this.randomSearch(parameters, remaining));
    }

    return combinations;
  }

  private updateParameters(scannerCode: string, parameters: Record<string, number>): string {
    let updated = scannerCode;

    Object.entries(parameters).forEach(([name, value]) => {
      // Replace parameter placeholders
      const placeholder = new RegExp(`\\{\\{${name}\\}\\}`, 'g');
      updated = updated.replace(placeholder, String(value));

      // Replace parameter assignments
      const assignment = new RegExp(`(${name}\\s*=\\s*)\\d+`, 'g');
      updated = updated.replace(assignment, `$1${value}`);
    });

    return updated;
  }

  private calculateObjective(metrics: PerformanceMetrics, objective: string): number {
    switch (objective) {
      case 'sharpe':
        return metrics.sharpeRatio;
      case 'profit-factor':
        return metrics.profitFactor;
      case 'return':
        return metrics.annualizedReturn;
      case 'custom':
        // Custom objective: Sharpe * (1 - maxDrawdown)
        return metrics.sharpeRatio * (1 - metrics.maxDrawdown);
      default:
        return metrics.sharpeRatio;
    }
  }

  private satisfiesConstraints(
    metrics: PerformanceMetrics,
    constraints?: OptimizationConstraint[]
  ): boolean {
    if (!constraints || constraints.length === 0) {
      return true;
    }

    return constraints.every(constraint => {
      switch (constraint.type) {
        case 'max-drawdown':
          return metrics.maxDrawdown <= constraint.value;
        case 'min-trades':
          return metrics.totalTrades >= constraint.value;
        case 'win-rate':
          return metrics.winRate >= constraint.value;
        default:
          return true;
      }
    });
  }

  private checkConvergence(curve: OptimizationPoint[]): boolean {
    if (curve.length < 10) return false;

    // Check if last 10 iterations improved less than 1%
    const recent = curve.slice(-10);
    const bestRecent = Math.max(...recent.map(p => p.objectiveValue));
    const bestOverall = Math.max(...curve.map(p => p.objectiveValue));

    return (bestOverall - bestRecent) / bestOverall < 0.01;
  }

  private isImproved(
    newMetrics: PerformanceMetrics,
    originalMetrics: PerformanceMetrics,
    objective: string
  ): boolean {
    const newValue = this.calculateObjective(newMetrics, objective);
    const originalValue = this.calculateObjective(originalMetrics, objective);

    return newValue > originalValue * 1.05; // 5% improvement threshold
  }

  private calculateImprovement(
    newMetrics: PerformanceMetrics,
    originalMetrics: PerformanceMetrics,
    objective: string
  ): string {
    const newValue = this.calculateObjective(newMetrics, objective);
    const originalValue = this.calculateObjective(originalMetrics, objective);

    const improvement = ((newValue - originalValue) / originalValue) * 100;

    return `${improvement > 0 ? '+' : ''}${improvement.toFixed(1)}%`;
  }

  private async fetchBacktest(backtestId: string): Promise<any> {
    const response = await fetch(`http://localhost:8000/backtest/${backtestId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch backtest');
    }
    return await response.json();
  }
}
```

**Acceptance Criteria**:
- [ ] All optimization methods work
- [ ] Objective function correctly calculated
- [ ] Constraints enforced
- [ ] Convergence detection works
- [ ] Optimized code generated

**Dependencies**:
- Executor Agent (Sprint 7)
- Analyst Agent (Task 8.1)
- Builder Agent (Sprint 6)

**Risks**:
- **Risk**: Overfitting through optimization
  - **Mitigation**: OOS validation, regularization, early stopping

---

### Task 8.6: Implement Performance Report Generator (3 hours)

**Subtasks**:
1. Create report template structure
2. Build report sections
3. Implement markdown generation
4. Add visualizations (charts, graphs)
5. Create export functionality

**Code Example**:
```typescript
// src/services/reportGenerator.ts

export interface ReportRequest {
  analysisResults: AnalysisResult[];
  backtestResults: BacktestResult[];
  includeVisualizations: boolean;
}

export class PerformanceReportGenerator {
  async generate(request: ReportRequest): Promise<string> {
    const sections: string[] = [];

    // Title page
    sections.push(this.generateTitlePage(request));

    // Executive summary
    sections.push(this.generateExecutiveSummary(request));

    // Performance metrics
    sections.push(this.generatePerformanceSection(request));

    // Analysis results
    request.analysisResults.forEach(analysis => {
      sections.push(this.generateAnalysisSection(analysis));
    });

    // Recommendations
    sections.push(this.generateRecommendationsSection(request));

    // Appendices
    sections.push(this.generateAppendices(request));

    return sections.join('\n\n---\n\n');
  }

  private generateTitlePage(request: ReportRequest): string {
    const date = new Date().toLocaleDateString();

    return `
# Strategy Performance Report

**Generated**: ${date}
**Backtests**: ${request.backtestResults.length}
**Analyses**: ${request.analysisResults.length}
    `.trim();
  }

  private generateExecutiveSummary(request: ReportRequest): string {
    const sections: string[] = [];

    sections.push('## Executive Summary\n');

    // Overall performance
    const avgSharpe = this.calculateAverageSharpe(request.backtestResults);
    const avgReturn = this.calculateAverageReturn(request.backtestResults);

    sections.push('### Overall Performance');
    sections.push(`- **Average Sharpe Ratio**: ${avgSharpe.toFixed(2)}`);
    sections.push(`- **Average Annual Return**: ${(avgReturn * 100).toFixed(1)}%\n`);

    // Key insights
    sections.push('### Key Insights');
    const allInsights = request.analysisResults.flatMap(a => a.insights);
    const topInsights = allInsights.slice(0, 5);

    topInsights.forEach((insight, i) => {
      sections.push(`${i + 1}. **${insight.title}** (${insight.impact} impact)`);
      sections.push(`   ${insight.description}`);
    });

    return sections.join('\n');
  }

  private generatePerformanceSection(request: ReportRequest): string {
    const sections: string[] = [];

    sections.push('## Performance Metrics\n');

    request.backtestResults.forEach((backtest, i) => {
      sections.push(`### Backtest ${i + 1}: ${backtest.scannerName}`);
      sections.push(this.generateMetricsTable(backtest.metrics));
    });

    return sections.join('\n');
  }

  private generateMetricsTable(metrics: PerformanceMetrics): string {
    return `
| Metric | Value |
|--------|-------|
| Total Return | ${(metrics.totalReturn * 100).toFixed(2)}% |
| Annualized Return | ${(metrics.annualizedReturn * 100).toFixed(2)}% |
| Sharpe Ratio | ${metrics.sharpeRatio.toFixed(2)} |
| Sortino Ratio | ${metrics.sortinoRatio.toFixed(2)} |
| Max Drawdown | ${(metrics.maxDrawdown * 100).toFixed(2)}% |
| Win Rate | ${(metrics.winRate * 100).toFixed(1)}% |
| Profit Factor | ${metrics.profitFactor.toFixed(2)} |
| Avg Trade | ${metrics.avgTrade.toFixed(2)} |
| Expectancy | ${metrics.expectancy.toFixed(2)} |
| Total Trades | ${metrics.totalTrades} |
    `.trim();
  }

  private generateAnalysisSection(analysis: AnalysisResult): string {
    const sections: string[] = [];

    sections.push(`## ${analysis.analysisType.toUpperCase()} Analysis\n`);

    // Metrics
    sections.push('### Metrics');
    sections.push(this.generateMetricsTable(analysis.metrics));

    // Insights
    sections.push('\n### Insights');
    analysis.insights.forEach(insight => {
      const emoji = insight.category === 'strength' ? '✅' :
                   insight.category === 'weakness' ? '❌' :
                   insight.category === 'opportunity' ? '💡' : '⚠️';
      sections.push(`${emoji} **${insight.title}** (${insight.impact})`);
      sections.push(`> ${insight.description}`);
    });

    // Recommendations
    sections.push('\n### Recommendations');
    analysis.recommendations.forEach(rec => {
      const emoji = rec.priority === 'high' ? '🔴' :
                   rec.priority === 'medium' ? '🟡' : '🟢';
      sections.push(`${emoji} **${rec.type}**: ${rec.action}`);
      sections.push(`> ${rec.expectedImprovement}`);
      sections.push(`> Implementation: ${rec.implementation}`);
    });

    return sections.join('\n');
  }

  private generateRecommendationsSection(request: ReportRequest): string {
    const sections: string[] = [];

    sections.push('## Recommendations\n');

    // Aggregate all recommendations
    const allRecommendations = request.analysisResults.flatMap(a => a.recommendations);

    // Group by type
    const byType = new Map<string, Recommendation[]>();
    allRecommendations.forEach(rec => {
      if (!byType.has(rec.type)) {
        byType.set(rec.type, []);
      }
      byType.get(rec.type)!.push(rec);
    });

    // Generate recommendations for each type
    byType.forEach((recs, type) => {
      sections.push(`### ${type.charAt(0).toUpperCase() + type.slice(1)}`);

      // Sort by priority
      const sorted = recs.sort((a, b) => {
        const priorityOrder = { high: 0, medium: 1, low: 2 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });

      sorted.forEach(rec => {
        const emoji = rec.priority === 'high' ? '🔴' :
                     rec.priority === 'medium' ? '🟡' : '🟢';
        sections.push(`${emoji} ${rec.action}`);
        sections.push(`- Expected: ${rec.expectedImprovement}`);
        sections.push(`- How: ${rec.implementation}\n`);
      });
    });

    return sections.join('\n');
  }

  private generateAppendices(request: ReportRequest): string {
    const sections: string[] = [];

    sections.push('## Appendices\n');

    // Methodology
    sections.push('### Methodology');
    sections.push('This report was generated using the RENATA V2 Analyst Agent.');
    sections.push('All metrics calculated using industry-standard formulas.\n');

    // Data
    sections.push('### Data');
    sections.push(`- **Number of Backtests**: ${request.backtestResults.length}`);
    sections.push(`- **Analysis Types**: ${[...new Set(request.analysisResults.map(a => a.analysisType))].join(', ')}\n`);

    return sections.join('\n');
  }

  private calculateAverageSharpe(backtests: BacktestResult[]): number {
    return backtests.reduce((sum, b) => sum + b.metrics.sharpeRatio, 0) / backtests.length;
  }

  private calculateAverageReturn(backtests: BacktestResult[]): number {
    return backtests.reduce((sum, b) => sum + b.metrics.annualizedReturn, 0) / backtests.length;
  }
}
```

**Acceptance Criteria**:
- [ ] Report includes all sections
- [ ] Markdown formatting correct
- [ ] All metrics displayed
- [ ] Visualizations generated

**Dependencies**:
- All analysis components (Tasks 8.1-8.5)

**Risks**:
- **Risk**: Report too long
  - **Mitigation**: Executive summary, progressive disclosure

---

### Task 8.7: Integrate with CopilotKit Actions (4 hours)

**Subtasks**:
1. Define CopilotKit action schemas
2. Implement action handlers
3. Create action result formatting
4. Add error handling
5. Test all analyst actions

**Code Example**:
```typescript
// src/components/renataV2CopilotKit.tsx

<Action
  name="analyzeBacktest"
  description="Analyze backtest results and generate insights"
  parameters={[
    {
      name: "backtestId",
      type: "string",
      description: "Backtest ID to analyze",
      required: true
    },
    {
      name: "analysisType",
      type: "string",
      description: "Type of analysis: performance, is-oos, monte-carlo, regime, optimization",
      required: false
    }
  ]}
  handler={async (args) => {
    const analyst = new AnalystAgent();
    const result = await analyst.analyze({
      backtestId: args.backtestId,
      analysisType: args.analysisType || 'performance'
    });

    return {
      analysisId: result.analysisId,
      sharpeRatio: result.metrics.sharpeRatio.toFixed(2),
      totalReturn: (result.metrics.totalReturn * 100).toFixed(2) + '%',
      maxDrawdown: (result.metrics.maxDrawdown * 100).toFixed(2) + '%',
      winRate: (result.metrics.winRate * 100).toFixed(1) + '%',
      insightsCount: result.insights.length,
      recommendationsCount: result.recommendations.length,
      topInsights: result.insights.slice(0, 3).map(i => i.title),
      topRecommendations: result.recommendations.slice(0, 3).map(r => r.action)
    };
  }}
/>

<Action
  name="validateISOOS"
  description="Validate strategy with in-sample and out-of-sample testing"
  parameters={[
    {
      name: "backtestId",
      type: "string",
      description: "Backtest ID to validate",
      required: true
    },
    {
      name: "inSamplePeriod",
      type: "object",
      description: "In-sample period {start, end}",
      required: true
    },
    {
      name: "outOfSamplePeriod",
      type: "object",
      description: "Out-of-sample period {start, end}",
      required: true
    }
  ]}
  handler={async (args) => {
    const validator = new ISOOSValidator();
    const result = await validator.validate({
      backtestId: args.backtestId,
      inSamplePeriod: args.inSamplePeriod,
      outOfSamplePeriod: args.outOfSamplePeriod
    });

    return {
      overfitting: result.overfitting,
      overfittingScore: (result.overfittingScore * 100).toFixed(1) + '%',
      returnDecay: (result.comparison.returnDecay * 100).toFixed(1) + '%',
      sharpeDecay: (result.comparison.sharpeDecay * 100).toFixed(1) + '%',
      overallDegradation: (result.comparison.overallDegradation * 100).toFixed(1) + '%',
      insightCount: result.insights.filter(i => !i.acceptable).length
    };
  }}
/>

<Action
  name="runMonteCarlo"
  description="Run Monte Carlo simulation on backtest results"
  parameters={[
    {
      name: "backtestId",
      type: "string",
      description: "Backtest ID to simulate",
      required: true
    },
    {
      name: "simulations",
      type: "number",
      description: "Number of simulations (default: 1000)",
      required: false
    },
    {
      name: "confidenceLevel",
      type: "number",
      description: "Confidence level (default: 0.95)",
      required: false
    }
  ]}
  handler={async (args) => {
    const simulator = new MonteCarloSimulator();
    const result = await simulator.simulate({
      backtestId: args.backtestId,
      simulations: args.simulations || 1000,
      confidenceLevel: args.confidenceLevel || 0.95,
      method: 'shuffle'
    });

    return {
      simulations: result.simulations,
      originalReturn: (result.originalMetrics.totalReturn * 100).toFixed(2) + '%',
      meanReturn: (result.simulatedMetrics.mean.totalReturn * 100).toFixed(2) + '%',
      confidenceInterval: [
        (result.confidenceIntervals.return[0] * 100).toFixed(2) + '%',
        (result.confidenceIntervals.return[1] * 100).toFixed(2) + '%'
      ],
      probabilityOfProfit: (result.probabilityOfProfit * 100).toFixed(1) + '%',
      riskOfRuin: (result.riskOfRuin * 100).toFixed(1) + '%'
    };
  }}
/>
```

**Acceptance Criteria**:
- [ ] All analyst actions defined and working
- [ ] Actions return properly formatted results
- [ ] Error handling works
- [ ] Performance: Actions complete in expected timeframes

**Dependencies**:
- CopilotKit installed (Sprint 3)
- All analyst components built (Tasks 8.1-8.6)

**Risks**:
- **Risk**: Long-running analysis timeout
  - **Mitigation**: Async processing, status updates

---

### Task 8.8: Testing & Validation (4 hours)

**Subtasks**:
1. Create unit tests for analyst agent
2. Create tests for IS/OOS validator
3. Create tests for Monte Carlo simulator
4. Create tests for regime analyzer
5. Create tests for parameter optimizer
6. Create tests for report generator
7. Integration tests
8. Performance testing

**Acceptance Criteria**:
- [ ] Unit tests achieve 80%+ coverage
- [ ] All analysis methods tested
- [ ] IS/OOS validation accurate
- [ ] Monte Carlo results consistent
- [ ] Regime analysis validated
- [ ] Parameter optimization improves performance
- [ ] Reports generate correctly

**Dependencies**:
- All analyst components built (Tasks 8.1-8.7)

**Risks**:
- **Risk**: Test data insufficient
  - **Mitigation**: Use historical backtests, synthetic data

---

## 📊 SPRINT 8 SUMMARY

### Time Investment
| Task | Hours | Priority |
|------|-------|----------|
| 8.1 Create Analyst Agent Service | 5 | Critical |
| 8.2 Implement IS/OOS Validation | 6 | Critical |
| 8.3 Implement Monte Carlo Simulation | 6 | Critical |
| 8.4 Implement Market Regime Analyzer | 4 | High |
| 8.5 Implement Parameter Optimizer | 5 | Critical |
| 8.6 Implement Performance Report Generator | 3 | Medium |
| 8.7 Integrate with CopilotKit Actions | 4 | Critical |
| 8.8 Testing & Validation | 4 | Critical |
| **TOTAL** | **37 hours** | |

### Completion Criteria
Sprint 8 is complete when:
- [ ] Analyst agent can analyze backtests
- [ ] IS/OOS validation detects overfitting
- [ ] Monte Carlo simulation provides confidence intervals
- [ ] Regime analysis identifies favorable/unfavorable conditions
- [ ] Parameter optimization improves performance
- [ ] Reports generated correctly
- [ ] All CopilotKit actions working
- [ ] Test coverage 80%+, all tests passing

### Dependencies
**Required Before Sprint 8**:
- Sprint 2: Archon MCP running
- Sprint 5: Researcher agent available
- Sprint 6: Builder agent available
- Sprint 7: Executor agent available

**Enables Sprint 9**:
- End-to-end testing of complete workflows
- Validation of all agent coordination

---

**Sprint 8 creates the intelligence layer that analyzes and optimizes strategies.**

**By completing Sprint 8, Renata can validate strategies and optimize parameters.**

**Ready for Sprint 9: Integration Testing.**
