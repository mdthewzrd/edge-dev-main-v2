# ⚡ SPRINT 7: EXECUTOR AGENT
## Backend Integration & Real-Time Execution

**Duration**: Weeks 7-8 (14 days)
**Objective**: Build intelligent execution agent that integrates with FastAPI backend, manages scanner executions, provides real-time progress tracking, and handles result collection

**Success Criteria**:
- [ ] Executor agent can deploy scanners to FastAPI backend
- [ ] Real-time progress tracking via WebSocket
- [ ] Scanner execution on single tickers and full market
- [ ] Result collection and formatting
- [ ] Error handling and recovery
- [ ] CopilotKit integration for executor actions

---

## 📋 DELIVERABLES

### Core Deliverables
- [ ] Executor agent service with backend integration
- [ ] WebSocket progress tracking system
- [ ] Scanner deployment manager
- [ ] Execution result collector
- [ ] Error handler and recovery system
- [ ] A+ example testing workflow
- [ ] Full market scan workflow
- [ ] Integration with CopilotKit actions

### Integration Points
- **FastAPI Backend** (port 8000): Scanner upload, execution, status check, result retrieval
- **WebSocket**: Real-time progress updates, execution status
- **Archon MCP**: Execution history, result storage
- **Builder Agent** (Sprint 6): Generated scanner deployment
- **Analyst Agent** (Sprint 8): Result analysis

---

## 🎯 DETAILED TASKS

### Task 7.1: Create Executor Agent Service (5 hours)

**Subtasks**:
1. Create `src/services/executorAgent.ts` service structure
2. Implement FastAPI backend client
3. Create execution state management
4. Build execution queue system
5. Implement execution tracking
6. Add error handling and retry logic

**Code Example**:
```typescript
// src/services/executorAgent.ts

import { ArchonMCPClient } from '@/archon/archonClient';

const BACKEND_URL = 'http://localhost:8000';

export interface ExecutionRequest {
  scannerCode: string;
  scannerName: string;
  tickers?: string[];
  dateRange?: DateRange;
  executionType: 'test' | 'scan' | 'backtest';
  aPlusNames?: string[];
}

export interface ExecutionResult {
  executionId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  currentStep: string;
  results?: ScanResult[];
  error?: string;
  startTime: Date;
  endTime?: Date;
}

export interface ScanResult {
  ticker: string;
  date: string;
  signal: boolean;
  parameters: Record<string, any>;
  indicators: Record<string, number>;
}

export class ExecutorAgent {
  private archon: ArchonMCPClient;
  private executionQueue: Map<string, ExecutionRequest>;
  private activeExecutions: Map<string, ExecutionResult>;

  constructor() {
    this.archon = new ArchonMCPClient();
    this.executionQueue = new Map();
    this.activeExecutions = new Map();
  }

  async execute(request: ExecutionRequest): Promise<ExecutionResult> {
    // Generate execution ID
    const executionId = this.generateExecutionId(request);

    // Create execution result
    const result: ExecutionResult = {
      executionId,
      status: 'pending',
      progress: 0,
      currentStep: 'Initializing',
      startTime: new Date()
    };

    // Store in active executions
    this.activeExecutions.set(executionId, result);

    try {
      // Step 1: Deploy scanner to backend
      result.currentStep = 'Deploying scanner to backend';
      result.progress = 10;
      await this.deployScanner(request.scannerCode, request.scannerName);

      // Step 2: Start execution
      result.currentStep = 'Starting execution';
      result.progress = 20;
      result.status = 'running';

      if (request.executionType === 'test' && request.aPlusNames) {
        // Test on A+ names only
        await this.executeOnAPlusNames(executionId, request);
      } else if (request.executionType === 'scan') {
        // Full market scan
        await this.executeFullScan(executionId, request);
      } else if (request.executionType === 'backtest') {
        // Backtest execution
        await this.executeBacktest(executionId, request);
      }

      // Step 3: Collect results
      result.currentStep = 'Collecting results';
      result.progress = 90;
      result.results = await this.collectResults(executionId);

      // Complete
      result.status = 'completed';
      result.progress = 100;
      result.currentStep = 'Completed';
      result.endTime = new Date();

      // Store results in Archon
      await this.storeResultsInArchon(executionId, result);

    } catch (error) {
      result.status = 'failed';
      result.error = error instanceof Error ? error.message : String(error);
      result.currentStep = 'Failed';
      result.endTime = new Date();
    }

    // Remove from active executions
    this.activeExecutions.delete(executionId);

    return result;
  }

  async getExecutionStatus(executionId: string): Promise<ExecutionResult | null> {
    return this.activeExecutions.get(executionId) || null;
  }

  private async deployScanner(scannerCode: string, scannerName: string): Promise<void> {
    const response = await fetch(`${BACKEND_URL}/upload_scanner`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_name: scannerName,
        scanner_code: scannerCode
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to deploy scanner: ${response.statusText}`);
    }
  }

  private async executeOnAPlusNames(
    executionId: string,
    request: ExecutionRequest
  ): Promise<void> {
    const result = this.activeExecutions.get(executionId)!;

    // Execute on each A+ name
    const tickers = request.aPlusNames!;
    const total = tickers.length;

    for (let i = 0; i < tickers.length; i++) {
      const ticker = tickers[i];
      result.currentStep = `Testing on ${ticker} (${i + 1}/${total})`;
      result.progress = 20 + ((i / total) * 60);

      await this.executeSingleTicker(executionId, request.scannerName, ticker, request.dateRange);

      // Update result
      const tickerResult = await this.getTickerResult(executionId, ticker);
      if (tickerResult && !result.results) {
        result.results = [];
      }
      if (tickerResult) {
        result.results!.push(tickerResult);
      }
    }
  }

  private async executeFullScan(
    executionId: string,
    request: ExecutionRequest
  ): Promise<void> {
    const result = this.activeExecutions.get(executionId)!;

    result.currentStep = 'Fetching market universe';
    result.progress = 30;

    // Get market universe
    const tickers = request.tickers || await this.getMarketUniverse();

    result.currentStep = `Scanning ${tickers.length} tickers`;
    result.progress = 40;

    // Start scan execution
    const response = await fetch(`${BACKEND_URL}/scan/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_name: request.scannerName,
        tickers: tickers,
        date_range: request.dateRange
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to start scan: ${response.statusText}`);
    }

    // Wait for completion
    await this.waitForCompletion(executionId, request.scannerName);
  }

  private async executeBacktest(
    executionId: string,
    request: ExecutionRequest
  ): Promise<void> {
    const result = this.activeExecutions.get(executionId)!;

    result.currentStep = 'Starting backtest';
    result.progress = 30;

    // Start backtest execution
    const response = await fetch(`${BACKEND_URL}/backtest/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_name: request.scannerName,
        tickers: request.tickers,
        date_range: request.dateRange
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to start backtest: ${response.statusText}`);
    }

    // Wait for completion
    await this.waitForCompletion(executionId, request.scannerName);
  }

  private async executeSingleTicker(
    executionId: string,
    scannerName: string,
    ticker: string,
    dateRange?: DateRange
  ): Promise<void> {
    const response = await fetch(`${BACKEND_URL}/scan/single`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_name: scannerName,
        ticker: ticker,
        date_range: dateRange
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to execute on ${ticker}: ${response.statusText}`);
    }
  }

  private async waitForCompletion(
    executionId: string,
    scannerName: string
  ): Promise<void> {
    const result = this.activeExecutions.get(executionId)!;
    let completed = false;
    let progress = 40;

    while (!completed) {
      // Check status
      const response = await fetch(
        `${BACKEND_URL}/scan/status?scanner_name=${encodeURIComponent(scannerName)}`
      );

      if (!response.ok) {
        throw new Error('Failed to check execution status');
      }

      const status = await response.json();

      // Update progress
      if (status.progress) {
        result.progress = 40 + (status.progress * 0.5); // 40-90%
        result.currentStep = status.step || 'Processing';
      }

      // Check if completed
      if (status.status === 'completed' || status.status === 'failed') {
        completed = true;
      } else {
        // Wait before checking again
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }

  private async collectResults(executionId: string): Promise<ScanResult[]> {
    const result = this.activeExecutions.get(executionId)!;

    const response = await fetch(
      `${BACKEND_URL}/scan/results?execution_id=${executionId}`
    );

    if (!response.ok) {
      throw new Error('Failed to collect results');
    }

    return await response.json();
  }

  private async getTickerResult(
    executionId: string,
    ticker: string
  ): Promise<ScanResult | null> {
    const response = await fetch(
      `${BACKEND_URL}/scan/result?execution_id=${executionId}&ticker=${ticker}`
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  }

  private async getMarketUniverse(): Promise<string[]> {
    // Fetch from market universe service
    const response = await fetch(`${BACKEND_URL}/market/universe`);

    if (!response.ok) {
      throw new Error('Failed to fetch market universe');
    }

    return await response.json();
  }

  private async storeResultsInArchon(
    executionId: string,
    result: ExecutionResult
  ): Promise<void> {
    // Store execution record in Archon
    await this.archon.manageTask({
      task_id: executionId,
      status: result.status === 'completed' ? 'completed' : 'failed',
      result: JSON.stringify(result),
      metadata: {
        scanner_name: result.results?.[0]?.ticker || 'unknown',
        execution_type: 'scan',
        timestamp: result.startTime.toISOString()
      }
    });
  }

  private generateExecutionId(request: ExecutionRequest): string {
    return `exec_${Date.now()}_${request.scannerName.replace(/\s+/g, '_')}`;
  }
}
```

**Acceptance Criteria**:
- [ ] Executor service created with all core methods
- [ ] Can deploy scanners to FastAPI backend
- [ ] Can execute on single tickers
- [ ] Can execute full market scans
- [ ] Can execute backtests
- [ ] Error handling works
- [ ] All methods have unit tests

**Dependencies**:
- FastAPI backend running (port 8000)
- Archon MCP running (Sprint 2)

**Risks**:
- **Risk**: Backend API changes break integration
  - **Mitigation**: Versioned API contracts, backward compatibility

---

### Task 7.2: Implement WebSocket Progress Tracking (5 hours)

**Subtasks**:
1. Create WebSocket client
2. Implement real-time progress updates
3. Build progress state management
4. Create progress UI components
5. Add error recovery for WebSocket drops
6. Implement progress aggregation

**Code Example**:
```typescript
// src/services/websocketProgressTracker.ts

export interface ProgressUpdate {
  executionId: string;
  progress: number;
  step: string;
  ticker?: string;
  message?: string;
  timestamp: Date;
}

export class WebSocketProgressTracker {
  private ws: WebSocket | null = null;
  private progressListeners: Map<string, (update: ProgressUpdate) => void>;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;

  constructor() {
    this.progressListeners = new Map();
  }

  connect(executionId: string): void {
    const wsUrl = `ws://localhost:8000/ws/progress/${executionId}`;

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log(`WebSocket connected for execution ${executionId}`);
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const update: ProgressUpdate = JSON.parse(event.data);
      this.notifyListeners(executionId, update);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed, attempting to reconnect...');
      this.reconnect(executionId);
    };
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  subscribe(
    executionId: string,
    callback: (update: ProgressUpdate) => void
  ): () => void {
    this.progressListeners.set(executionId, callback);

    // Return unsubscribe function
    return () => {
      this.progressListeners.delete(executionId);
    };
  }

  private notifyListeners(executionId: string, update: ProgressUpdate): void {
    const listener = this.progressListeners.get(executionId);
    if (listener) {
      listener(update);
    }
  }

  private reconnect(executionId: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

      setTimeout(() => {
        console.log(`Reconnecting to WebSocket (attempt ${this.reconnectAttempts})...`);
        this.connect(executionId);
      }, delay);
    } else {
      console.error('Max reconnect attempts reached');
    }
  }
}

// React hook for progress tracking
export function useExecutionProgress(executionId: string) {
  const [progress, setProgress] = useState(0);
  const [step, setStep] = useState('');
  const [ticker, setTicker] = useState<string | undefined>();
  const [message, setMessage] = useState<string | undefined>();

  useEffect(() => {
    const tracker = new WebSocketProgressTracker();

    tracker.connect(executionId);

    const unsubscribe = tracker.subscribe(executionId, (update) => {
      setProgress(update.progress);
      setStep(update.step);
      setTicker(update.ticker);
      setMessage(update.message);
    });

    return () => {
      unsubscribe();
      tracker.disconnect();
    };
  }, [executionId]);

  return { progress, step, ticker, message };
}

// Progress UI component
export function ExecutionProgress({ executionId }: { executionId: string }) {
  const { progress, step, ticker, message } = useExecutionProgress(executionId);

  return (
    <div className="execution-progress">
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="progress-details">
        <span className="progress-percent">{Math.round(progress)}%</span>
        <span className="progress-step">{step}</span>
        {ticker && <span className="progress-ticker">{ticker}</span>}
        {message && <span className="progress-message">{message}</span>}
      </div>
    </div>
  );
}
```

**Acceptance Criteria**:
- [ ] WebSocket client connects successfully
- [ ] Real-time progress updates work
- [ ] Progress UI displays correctly
- [ ] Automatic reconnection on WebSocket drop
- [ ] Performance: Updates received within 100ms

**Dependencies**:
- FastAPI backend with WebSocket support
- Executor agent service (Task 7.1)

**Risks**:
- **Risk**: WebSocket connection unstable
  - **Mitigation**: Automatic reconnection, fallback to polling

---

### Task 7.3: Implement Scanner Deployment Manager (4 hours)

**Subtasks**:
1. Build scanner upload API client
2. Create scanner validation before upload
3. Implement scanner versioning
4. Add scanner update/delete operations
5. Create scanner listing endpoint
6. Build deployment status tracking

**Code Example**:
```typescript
// src/services/scannerDeploymentManager.ts

export interface ScannerDeployment {
  scannerId: string;
  scannerName: string;
  version: number;
  deployedAt: Date;
  status: 'active' | 'inactive' | 'error';
  validationResults: ValidationResult[];
}

export class ScannerDeploymentManager {
  private backendUrl: string;

  constructor() {
    this.backendUrl = 'http://localhost:8000';
  }

  async deploy(
    scannerCode: string,
    scannerName: string,
    validate: boolean = true
  ): Promise<ScannerDeployment> {
    // Validate scanner if requested
    let validationResults: ValidationResult[] = [];
    if (validate) {
      const validator = new V31Validator();
      validationResults = await validator.validate(scannerCode);

      const criticalIssues = validationResults.filter(r => r.severity === 'critical');
      if (criticalIssues.length > 0) {
        throw new Error(
          `Scanner has ${criticalIssues.length} critical issues that must be resolved`
        );
      }
    }

    // Deploy to backend
    const response = await fetch(`${this.backendUrl}/upload_scanner`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_name: scannerName,
        scanner_code: scannerCode,
        validation_results: validationResults
      })
    });

    if (!response.ok) {
      throw new Error(`Deployment failed: ${response.statusText}`);
    }

    const result = await response.json();

    return {
      scannerId: result.scanner_id,
      scannerName: scannerName,
      version: result.version,
      deployedAt: new Date(),
      status: 'active',
      validationResults
    };
  }

  async update(
    scannerId: string,
    scannerCode: string
  ): Promise<ScannerDeployment> {
    const response = await fetch(`${this.backendUrl}/scanner/${scannerId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_code: scannerCode
      })
    });

    if (!response.ok) {
      throw new Error(`Update failed: ${response.statusText}`);
    }

    return await response.json();
  }

  async delete(scannerId: string): Promise<void> {
    const response = await fetch(`${this.backendUrl}/scanner/${scannerId}`, {
      method: 'DELETE'
    });

    if (!response.ok) {
      throw new Error(`Delete failed: ${response.statusText}`);
    }
  }

  async list(): Promise<ScannerDeployment[]> {
    const response = await fetch(`${this.backendUrl}/scanners`);

    if (!response.ok) {
      throw new Error('Failed to list scanners');
    }

    return await response.json();
  }

  async get(scannerId: string): Promise<ScannerDeployment> {
    const response = await fetch(`${this.backendUrl}/scanner/${scannerId}`);

    if (!response.ok) {
      throw new Error('Failed to get scanner');
    }

    return await response.json();
  }

  async validate(scannerCode: string): Promise<ValidationResult[]> {
    const response = await fetch(`${this.backendUrl}/validate_scanner`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scanner_code: scannerCode
      })
    });

    if (!response.ok) {
      throw new Error('Validation failed');
    }

    return await response.json();
  }
}
```

**Acceptance Criteria**:
- [ ] Can deploy scanners to backend
- [ ] Can update existing scanners
- [ ] Can delete scanners
- [ ] Can list all deployed scanners
- [ ] Validation works before deployment
- [ ] Performance: Deployment completes in <5 seconds

**Dependencies**:
- FastAPI backend upload endpoint
- V31 validator (Sprint 6)

**Risks**:
- **Risk**: Deployment failures corrupt system
  - **Mitigation**: Validation before deploy, versioning, rollback capability

---

### Task 7.4: Implement Execution Result Collector (4 hours)

**Subtasks**:
1. Create result fetching API client
2. Build result parsing and formatting
3. Implement result aggregation
4. Create result export functionality
5. Add result visualization data preparation
6. Build result storage in Archon

**Code Example**:
```typescript
// src/services/resultCollector.ts

export interface CollectedResults {
  executionId: string;
  scannerName: string;
  executionType: 'test' | 'scan' | 'backtest';
  totalSignals: number;
  uniqueTickers: number;
  results: ScanResult[];
  summary: ResultSummary;
  exportFormats: ExportFormats;
}

export interface ResultSummary {
  totalSignals: number;
  signalsByTicker: Map<string, number>;
  signalsByDate: Map<string, number>;
  topPerformers: string[];
  avgSignalQuality: number;
}

export interface ExportFormats {
  json: string;
  csv: string;
  markdown: string;
}

export class ResultCollector {
  private backendUrl: string;
  private archon: ArchonMCPClient;

  constructor() {
    this.backendUrl = 'http://localhost:8000';
    this.archon = new ArchonMCPClient();
  }

  async collect(executionId: string): Promise<CollectedResults> {
    // Fetch raw results
    const rawResults = await this.fetchResults(executionId);

    // Parse results
    const results = this.parseResults(rawResults);

    // Generate summary
    const summary = this.generateSummary(results);

    // Generate export formats
    const exportFormats = this.generateExports(results, summary);

    // Get execution metadata
    const metadata = await this.getExecutionMetadata(executionId);

    const collected: CollectedResults = {
      executionId,
      scannerName: metadata.scannerName,
      executionType: metadata.executionType,
      totalSignals: results.length,
      uniqueTickers: summary.signalsByTicker.size,
      results,
      summary,
      exportFormats
    };

    // Store in Archon
    await this.storeInArchon(executionId, collected);

    return collected;
  }

  private async fetchResults(executionId: string): Promise<any> {
    const response = await fetch(
      `${this.backendUrl}/results/${executionId}`
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch results: ${response.statusText}`);
    }

    return await response.json();
  }

  private parseResults(raw: any): ScanResult[] {
    return raw.map((r: any) => ({
      ticker: r.ticker,
      date: r.date,
      signal: r.signal,
      parameters: r.parameters || {},
      indicators: r.indicators || {}
    }));
  }

  private generateSummary(results: ScanResult[]): ResultSummary {
    // Total signals
    const totalSignals = results.length;

    // Signals by ticker
    const signalsByTicker = new Map<string, number>();
    results.forEach(r => {
      const count = signalsByTicker.get(r.ticker) || 0;
      signalsByTicker.set(r.ticker, count + 1);
    });

    // Signals by date
    const signalsByDate = new Map<string, number>();
    results.forEach(r => {
      const count = signalsByDate.get(r.date) || 0;
      signalsByDate.set(r.date, count + 1);
    });

    // Top performers (tickers with most signals)
    const topPerformers = Array.from(signalsByTicker.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([ticker]) => ticker);

    // Average signal quality (if available)
    const avgSignalQuality = results.reduce((sum, r) => {
      // Assuming quality is calculated from indicators
      const quality = this.calculateSignalQuality(r);
      return sum + quality;
    }, 0) / results.length;

    return {
      totalSignals,
      signalsByTicker,
      signalsByDate,
      topPerformers,
      avgSignalQuality
    };
  }

  private calculateSignalQuality(result: ScanResult): number {
    // Simple quality metric based on indicator strength
    let quality = 0.5;

    if (result.indicators.rsi !== undefined) {
      // RSI < 30 is good for OS, > 70 is good for overbought
      if (result.indicators.rsi < 30 || result.indicators.rsi > 70) {
        quality += 0.2;
      }
    }

    if (result.indicators.volume !== undefined) {
      // High volume is good
      quality += 0.2;
    }

    return Math.min(quality, 1.0);
  }

  private generateExports(
    results: ScanResult[],
    summary: ResultSummary
  ): ExportFormats {
    // JSON export
    const json = JSON.stringify({ results, summary }, null, 2);

    // CSV export
    const csv = this.generateCSV(results);

    // Markdown export
    const markdown = this.generateMarkdown(results, summary);

    return { json, csv, markdown };
  }

  private generateCSV(results: ScanResult[]): string {
    const headers = ['ticker', 'date', 'signal', ...Object.keys(results[0]?.parameters || {})];
    const rows = results.map(r => [
      r.ticker,
      r.date,
      String(r.signal),
      ...Object.values(r.parameters).map(v => String(v))
    ]);

    return [headers, ...rows].map(row => row.join(',')).join('\n');
  }

  private generateMarkdown(
    results: ScanResult[],
    summary: ResultSummary
  ): string {
    const lines: string[] = [];

    lines.push('# Scan Results\n');
    lines.push(`## Summary`);
    lines.push(`- Total Signals: ${summary.totalSignals}`);
    lines.push(`- Unique Tickers: ${summary.signalsByTicker.size}`);
    lines.push(`- Average Quality: ${(summary.avgSignalQuality * 100).toFixed(1)}%\n`);

    lines.push(`## Top Performers`);
    summary.topPerformers.forEach((ticker, i) => {
      const count = summary.signalsByTicker.get(ticker) || 0;
      lines.push(`${i + 1}. ${ticker}: ${count} signals`);
    });

    lines.push(`\n## All Signals`);
    lines.push(`| Ticker | Date | Signal |`);
    lines.push(`|--------|------|--------|`);
    results.forEach(r => {
      lines.push(`| ${r.ticker} | ${r.date} | ${r.signal ? '✓' : '✗'} |`);
    });

    return lines.join('\n');
  }

  private async getExecutionMetadata(executionId: string): Promise<any> {
    const response = await fetch(
      `${this.backendUrl}/execution/${executionId}/metadata`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch execution metadata');
    }

    return await response.json();
  }

  private async storeInArchon(
    executionId: string,
    collected: CollectedResults
  ): Promise<void> {
    await this.archon.manageTask({
      task_id: executionId,
      status: 'completed',
      result: collected.exportFormats.json,
      metadata: {
        scanner_name: collected.scannerName,
        execution_type: collected.executionType,
        total_signals: collected.totalSignals,
        unique_tickers: collected.uniqueTickers
      }
    });
  }
}
```

**Acceptance Criteria**:
- [ ] Can collect results from backend
- [ ] Results parsed and formatted correctly
- [ ] Summary statistics accurate
- [ ] Export formats work (JSON, CSV, Markdown)
- [ ] Results stored in Archon
- [ ] Performance: Collection completes in <5 seconds

**Dependencies**:
- FastAPI backend results endpoint
- Archon MCP (Sprint 2)

**Risks**:
- **Risk**: Large result sets cause memory issues
  - **Mitigation**: Pagination, streaming, lazy loading

---

### Task 7.5: Implement Error Handler and Recovery (3 hours)

**Subtasks**:
1. Create error classification system
2. Build error detection logic
3. Implement retry strategies
4. Create error reporting
5. Build recovery workflows
6. Add error logging to Archon

**Code Example**:
```typescript
// src/services/errorHandler.ts

export enum ErrorSeverity {
  Low = 'low',
  Medium = 'medium',
  High = 'high',
  Critical = 'critical'
}

export enum ErrorType {
  Network = 'network',
  Backend = 'backend',
  Validation = 'validation',
  Execution = 'execution',
  Timeout = 'timeout'
}

export interface ExecutionError {
  errorId: string;
  executionId: string;
  type: ErrorType;
  severity: ErrorSeverity;
  message: string;
  stack?: string;
  timestamp: Date;
  retryable: boolean;
  retryCount?: number;
  maxRetries?: number;
}

export class ErrorHandler {
  private archon: ArchonMCPClient;
  private retryStrategies: Map<ErrorType, RetryStrategy>;

  constructor() {
    this.archon = new ArchonMCPClient();
    this.initializeRetryStrategies();
  }

  async handleError(error: ExecutionError): Promise<ErrorHandlingResult> {
    // Log error
    await this.logError(error);

    // Determine if retryable
    if (error.retryable && (error.retryCount || 0) < (error.maxRetries || 3)) {
      // Attempt recovery
      return await this.attemptRecovery(error);
    } else {
      // No recovery possible
      return {
        action: 'fail',
        message: 'Error cannot be recovered from',
        error
      };
    }
  }

  private async attemptRecovery(error: ExecutionError): Promise<ErrorHandlingResult> {
    const strategy = this.retryStrategies.get(error.type);

    if (!strategy) {
      return {
        action: 'fail',
        message: 'No retry strategy for this error type',
        error
      };
    }

    // Increment retry count
    error.retryCount = (error.retryCount || 0) + 1;

    // Apply retry strategy
    const result = await strategy.execute(error);

    // Log recovery attempt
    await this.logRecoveryAttempt(error, result);

    return result;
  }

  private initializeRetryStrategies(): void {
    // Network errors: retry with exponential backoff
    this.retryStrategies.set(ErrorType.Network, {
      maxRetries: 5,
      backoffMs: 1000,
      backoffMultiplier: 2,
      execute: async (error) => {
        const delay = 1000 * Math.pow(2, error.retryCount || 0);
        await new Promise(resolve => setTimeout(resolve, delay));

        return {
          action: 'retry',
          message: `Retrying after ${delay}ms`,
          error
        };
      }
    });

    // Backend errors: don't retry (server-side issue)
    this.retryStrategies.set(ErrorType.Backend, {
      maxRetries: 0,
      execute: async (error) => ({
        action: 'fail',
        message: 'Backend error cannot be retried',
        error
      })
    });

    // Validation errors: don't retry (code issue)
    this.retryStrategies.set(ErrorType.Validation, {
      maxRetries: 0,
      execute: async (error) => ({
        action: 'fail',
        message: 'Validation error requires code fix',
        error
      })
    });

    // Execution errors: retry once (may be transient)
    this.retryStrategies.set(ErrorType.Execution, {
      maxRetries: 1,
      execute: async (error) => ({
        action: 'retry',
        message: 'Retrying execution',
        error
      })
    });

    // Timeout errors: retry with longer timeout
    this.retryStrategies.set(ErrorType.Timeout, {
      maxRetries: 3,
      execute: async (error) => {
        return {
          action: 'retry',
          message: 'Retrying with extended timeout',
          error
        };
      }
    });
  }

  private async logError(error: ExecutionError): Promise<void> {
    // Store error in Archon
    await this.archon.manageTask({
      task_id: error.errorId,
      status: 'failed',
      result: error.message,
      metadata: {
        error_type: error.type,
        severity: error.severity,
        timestamp: error.timestamp.toISOString()
      }
    });

    // Log to console
    console.error(`[${error.severity.toUpperCase()}] ${error.type}: ${error.message}`);
  }

  private async logRecoveryAttempt(
    error: ExecutionError,
    result: ErrorHandlingResult
  ): Promise<void> {
    console.log(`Recovery attempt ${error.retryCount}/${error.maxRetries}: ${result.message}`);
  }
}
```

**Acceptance Criteria**:
- [ ] All error types classified
- [ ] Retry strategies defined
- [ ] Error logging works
- [ ] Recovery attempts successful
- [ ] All errors stored in Archon

**Dependencies**:
- Archon MCP (Sprint 2)
- Executor agent service (Task 7.1)

**Risks**:
- **Risk**: Infinite retry loops
  - **Mitigation**: Max retry limits, exponential backoff

---

### Task 7.6: Implement A+ Example Testing Workflow (4 hours)

**Subtasks**:
1. Create A+ testing workflow manager
2. Implement test on single A+ name
3. Build test on all A+ names workflow
4. Create A+ result validation
5. Implement A+ result comparison
6. Build A+ testing report

**Code Example**:
```typescript
// src/services/aPlusTestingWorkflow.ts

export interface APlusTestRequest {
  scannerName: string;
  scannerCode: string;
  aPlusNames: string[];
  dateRange: DateRange;
  expectedSignals?: Map<string, boolean>; // Expected signals for each name
}

export interface APlusTestResult {
  scannerName: string;
  totalTested: number;
  signalsFound: number;
  expectedHits: number;
  unexpectedSignals: string[];
  missedSignals: string[];
  accuracy: number;
  results: Map<string, APlusTickerResult>;
}

export interface APlusTickerResult {
  ticker: string;
  signalFound: boolean;
  expected: boolean;
  match: boolean;
  signalDate?: string;
  signalQuality?: number;
}

export class APlusTestingWorkflow {
  private executor: ExecutorAgent;
  private resultCollector: ResultCollector;

  constructor() {
    this.executor = new ExecutorAgent();
    this.resultCollector = new ResultCollector();
  }

  async testOnAPlusNames(request: APlusTestRequest): Promise<APlusTestResult> {
    // Deploy scanner
    await this.deployScanner(request.scannerCode, request.scannerName);

    // Execute on A+ names
    const executionResult = await this.executor.execute({
      scannerCode: request.scannerCode,
      scannerName: request.scannerName,
      executionType: 'test',
      aPlusNames: request.aPlusNames,
      dateRange: request.dateRange
    });

    // Collect results
    const collected = await this.resultCollector.collect(executionResult.executionId);

    // Analyze results
    const analysis = this.analyzeAPlusResults(
      collected,
      request.expectedSignals
    );

    return analysis;
  }

  private async deployScanner(scannerCode: string, scannerName: string): Promise<void> {
    const manager = new ScannerDeploymentManager();
    await manager.deploy(scannerCode, scannerName);
  }

  private analyzeAPlusResults(
    collected: CollectedResults,
    expected?: Map<string, boolean>
  ): APlusTestResult {
    const results = new Map<string, APlusTickerResult>();
    const signalsFound: string[] = [];
    const unexpectedSignals: string[] = [];
    const missedSignals: string[] = [];
    let expectedHits = 0;

    // Analyze each ticker
    collected.results.forEach(result => {
      const tickerResult: APlusTickerResult = {
        ticker: result.ticker,
        signalFound: result.signal,
        expected: expected?.get(result.ticker) || false,
        match: false
      };

      if (result.signal) {
        signalsFound.push(result.ticker);

        if (expected?.get(result.ticker)) {
          tickerResult.match = true;
          expectedHits++;
        } else {
          unexpectedSignals.push(result.ticker);
        }
      } else {
        if (expected?.get(result.ticker)) {
          missedSignals.push(result.ticker);
        }
      }

      results.set(result.ticker, tickerResult);
    });

    // Calculate accuracy
    const accuracy = expectedHits / (expected?.size || 1);

    return {
      scannerName: collected.scannerName,
      totalTested: collected.uniqueTickers,
      signalsFound: signalsFound.length,
      expectedHits,
      unexpectedSignals,
      missedSignals,
      accuracy,
      results
    };
  }

  generateTestReport(result: APlusTestResult): string {
    const lines: string[] = [];

    lines.push('# A+ Example Test Report\n');
    lines.push(`## Scanner: ${result.scannerName}\n`);
    lines.push('## Summary');
    lines.push(`- Total Tested: ${result.totalTested}`);
    lines.push(`- Signals Found: ${result.signalsFound}`);
    lines.push(`- Expected Hits: ${result.expectedHits}`);
    lines.push(`- Accuracy: ${(result.accuracy * 100).toFixed(1)}%\n`);

    if (result.unexpectedSignals.length > 0) {
      lines.push('## Unexpected Signals');
      result.unexpectedSignals.forEach(ticker => {
        lines.push(`- ${ticker}`);
      });
      lines.push('');
    }

    if (result.missedSignals.length > 0) {
      lines.push('## Missed Signals');
      result.missedSignals.forEach(ticker => {
        lines.push(`- ${ticker}`);
      });
      lines.push('');
    }

    lines.push('## Detailed Results');
    result.results.forEach((tickerResult, ticker) => {
      lines.push(`### ${ticker}`);
      lines.push(`- Signal Found: ${tickerResult.signalFound ? 'Yes' : 'No'}`);
      lines.push(`- Expected: ${tickerResult.expected ? 'Yes' : 'No'}`);
      lines.push(`- Match: ${tickerResult.match ? '✓' : '✗'}`);
      if (tickerResult.signalDate) {
        lines.push(`- Signal Date: ${tickerResult.signalDate}`);
      }
      if (tickerResult.signalQuality) {
        lines.push(`- Signal Quality: ${(tickerResult.signalQuality * 100).toFixed(1)}%`);
      }
      lines.push('');
    });

    return lines.join('\n');
  }
}
```

**Acceptance Criteria**:
- [ ] Can test scanners on A+ names
- [ ] Results analyzed correctly
- [ ] Accuracy calculation accurate
- [ ] Report generation works
- [ ] Unexpected and missed signals identified

**Dependencies**:
- Executor agent (Task 7.1)
- Result collector (Task 7.4)

**Risks**:
- **Risk**: A+ names produce no signals
  - **Mitigation**: Parameter adjustment, manual review

---

### Task 7.7: Integrate with CopilotKit Actions (4 hours)

**Subtasks**:
1. Define CopilotKit action schemas
2. Implement action handlers
3. Create action result formatting
4. Add error handling
5. Test all executor actions

**Code Example**:
```typescript
// src/components/renataV2CopilotKit.tsx

<Action
  name="testScannerOnAPlus"
  description="Test a scanner on A+ example names"
  parameters={[
    {
      name: "scannerCode",
      type: "string",
      description: "Scanner code to test",
      required: true
    },
    {
      name: "scannerName",
      type: "string",
      description: "Name of the scanner",
      required: true
    },
    {
      name: "aPlusNames",
      type: "array",
      description: "A+ example ticker symbols",
      required: true
    },
    {
      name: "dateRange",
      type: "object",
      description: "Date range for testing",
      required: false
    }
  ]}
  handler={async (args) => {
    const workflow = new APlusTestingWorkflow();
    const result = await workflow.testOnAPlusNames({
      scannerCode: args.scannerCode,
      scannerName: args.scannerName,
      aPlusNames: args.aPlusNames,
      dateRange: args.dateRange || { start: '2024-01-01', end: '2024-12-31' }
    });

    return {
      scannerName: result.scannerName,
      totalTested: result.totalTested,
      signalsFound: result.signalsFound,
      expectedHits: result.expectedHits,
      accuracy: Math.round(result.accuracy * 100) + '%',
      unexpectedSignals: result.unexpectedSignals,
      missedSignals: result.missedSignals,
      report: workflow.generateTestReport(result)
    };
  }}
/>

<Action
  name="runMarketScan"
  description="Run a scanner on the full market"
  parameters={[
    {
      name: "scannerCode",
      type: "string",
      description: "Scanner code to run",
      required: true
    },
    {
      name: "scannerName",
      type: "string",
      description: "Name of the scanner",
      required: true
    },
    {
      name: "tickers",
      type: "array",
      description: "Tickers to scan (optional, defaults to market universe)",
      required: false
    },
    {
      name: "dateRange",
      type: "object",
      description: "Date range for scanning",
      required: false
    }
  ]}
  handler={async (args) => {
    const executor = new ExecutorAgent();
    const result = await executor.execute({
      scannerCode: args.scannerCode,
      scannerName: args.scannerName,
      executionType: 'scan',
      tickers: args.tickers,
      dateRange: args.dateRange || { start: '2024-01-01', end: '2024-12-31' }
    });

    return {
      executionId: result.executionId,
      status: result.status,
      progress: Math.round(result.progress) + '%',
      currentStep: result.currentStep,
      resultCount: result.results?.length || 0,
      completed: result.status === 'completed'
    };
  }}
/>

<Action
  name="getScanResults"
  description="Get results from a completed scan"
  parameters={[
    {
      name: "executionId",
      type: "string",
      description: "Execution ID from scan",
      required: true
    }
  ]}
  handler={async (args) => {
    const collector = new ResultCollector();
    const collected = await collector.collect(args.executionId);

    return {
      executionId: collected.executionId,
      scannerName: collected.scannerName,
      totalSignals: collected.totalSignals,
      uniqueTickers: collected.uniqueTickers,
      summary: collected.summary,
      results: collected.results.slice(0, 100), // First 100 results
      exportFormats: collected.exportFormats
    };
  }}
/>
```

**Acceptance Criteria**:
- [ ] All executor actions defined and working
- [ ] Actions return properly formatted results
- [ ] Error handling works
- [ ] Performance: Actions complete in expected timeframes

**Dependencies**:
- CopilotKit installed (Sprint 3)
- All executor components built (Tasks 7.1-7.6)

**Risks**:
- **Risk**: Long-running executions timeout
  - **Mitigation**: Async execution, status polling

---

### Task 7.8: Testing & Validation (4 hours)

**Subtasks**:
1. Create unit tests for executor agent
2. Create tests for WebSocket progress tracking
3. Create tests for deployment manager
4. Create tests for result collector
5. Create tests for error handler
6. Create tests for A+ testing workflow
7. Integration tests with FastAPI backend
8. Performance testing

**Acceptance Criteria**:
- [ ] Unit tests achieve 80%+ coverage
- [ ] WebSocket integration tests pass
- [ ] Backend integration tests pass
- [ ] Error handling tests validate retry logic
- [ ] A+ testing workflow validated
- [ ] Performance: All operations complete in specified times

**Dependencies**:
- All executor components built (Tasks 7.1-7.7)

**Risks**:
- **Risk**: Integration tests flaky
  - **Mitigation**: Mock backend responses, retry logic

---

## 📊 SPRINT 7 SUMMARY

### Time Investment
| Task | Hours | Priority |
|------|-------|----------|
| 7.1 Create Executor Agent Service | 5 | Critical |
| 7.2 Implement WebSocket Progress Tracking | 5 | Critical |
| 7.3 Implement Scanner Deployment Manager | 4 | High |
| 7.4 Implement Execution Result Collector | 4 | High |
| 7.5 Implement Error Handler and Recovery | 3 | High |
| 7.6 Implement A+ Example Testing Workflow | 4 | Critical |
| 7.7 Integrate with CopilotKit Actions | 4 | Critical |
| 7.8 Testing & Validation | 4 | Critical |
| **TOTAL** | **33 hours** | |

### Completion Criteria
Sprint 7 is complete when:
- [ ] Executor agent can deploy and execute scanners
- [ ] WebSocket progress tracking works in real-time
- [ ] Scanner deployment manager works
- [ ] Results collected and formatted correctly
- [ ] Error handling and recovery works
- [ ] A+ testing workflow validated
- [ ] All CopilotKit actions working
- [ ] Test coverage 80%+, all tests passing

### Dependencies
**Required Before Sprint 7**:
- Sprint 2: Archon MCP running
- Sprint 3: CopilotKit installed
- Sprint 6: Builder agent available

**Enables Sprint 8**:
- Analyst will analyze execution results
- Backtest analysis workflow
- Performance optimization

---

**Sprint 7 creates the execution engine that runs scanners and collects results.**

**By completing Sprint 7, Renata can execute scanners and provide real-time progress.**

**Ready to build Analyst Agent in Sprint 8.**
