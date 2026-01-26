# 🔨 SPRINT 6: BUILDER AGENT
## V31 Code Generation & Scanner Construction

**Duration**: Weeks 6-7 (14 days)
**Objective**: Build intelligent code generation agent that transforms ideas, A+ examples, and non-V31 code into production-ready V31 scanners

**Success Criteria**:
- [ ] Builder agent can generate V31-compliant scanner code from ideas
- [ ] Can transform non-V31 scanners to V31 Gold Standard
- [ ] Can convert A+ molds into functional scanners
- [ ] All generated code passes V31 validation
- [ ] Code quality meets production standards
- [ ] CopilotKit integration for builder actions

---

## 📋 DELIVERABLES

### Core Deliverables
- [ ] Builder agent service with code generation capabilities
- [ ] Idea → Scanner generator
- [ ] Non-V31 → V31 transformer
- [ ] A+ mold → Scanner converter
- [ ] V31 validation system
- [ ] Template library expansion
- [ ] Integration with CopilotKit actions
- [ ] Comprehensive test suite

### Integration Points
- **Archon MCP**: Template retrieval, pattern examples, code samples
- **Researcher Agent**: Parameter insights, similar strategies, pattern matching
- **V31 Gold Standard**: Compliance validation, architecture enforcement
- **FastAPI Backend**: Generated scanner deployment, execution validation

---

## 🎯 DETAILED TASKS

### Task 6.1: Create Builder Agent Service (6 hours)

**Subtasks**:
1. Create `src/services/builderAgent.ts` service structure
2. Implement code generation state management
3. Build template retrieval system
4. Create code quality validator
5. Implement V31 compliance checker
6. Add error handling for generation failures

**Code Example**:
```typescript
// src/services/builderAgent.ts

import { ArchonMCPClient } from '@/archon/archonClient';
import { V31Validator } from './v31Validator';
import { TemplateLibrary } from './templateLibrary';

export interface BuildRequest {
  type: 'idea' | 'mold' | 'transform';
  input: IdeaInput | MoldInput | TransformInput;
  setupType?: string;
  constraints?: BuildConstraints;
}

export interface BuildResult {
  scannerCode: string;
  scannerName: string;
  v31Compliant: boolean;
  validationResults: ValidationResult[];
  qualityScore: number;
  warnings: string[];
  suggestedTests: string[];
}

export class BuilderAgent {
  private archon: ArchonMCPClient;
  private validator: V31Validator;
  private templates: TemplateLibrary;

  constructor() {
    this.archon = new ArchonMCPClient();
    this.validator = new V31Validator();
    this.templates = new TemplateLibrary();
  }

  async build(request: BuildRequest): Promise<BuildResult> {
    let scannerCode: string;

    switch (request.type) {
      case 'idea':
        scannerCode = await this.buildFromIdea(
          request.input as IdeaInput,
          request.setupType,
          request.constraints
        );
        break;

      case 'mold':
        scannerCode = await this.buildFromMold(
          request.input as MoldInput,
          request.setupType,
          request.constraints
        );
        break;

      case 'transform':
        scannerCode = await this.transformToV31(
          request.input as TransformInput,
          request.constraints
        );
        break;

      default:
        throw new Error(`Unknown build type: ${(request as any).type}`);
    }

    // Validate V31 compliance
    const validationResults = await this.validator.validate(scannerCode);

    // Calculate quality score
    const qualityScore = this.calculateQualityScore(scannerCode, validationResults);

    // Generate warnings
    const warnings = this.generateWarnings(validationResults);

    // Suggest tests
    const suggestedTests = this.suggestTests(scannerCode, request.setupType);

    return {
      scannerCode,
      scannerName: this.generateScannerName(request),
      v31Compliant: validationResults.every(v => v.compliant),
      validationResults,
      qualityScore,
      warnings,
      suggestedTests
    };
  }

  private async buildFromIdea(
    idea: IdeaInput,
    setupType: string | undefined,
    constraints: BuildConstraints | undefined
  ): Promise<string> {
    // Research similar strategies
    const researcher = new ResearcherAgent();
    const research = await researcher.research({
      query: idea.description,
      domain: 'scanner',
      setupType
    });

    // Get appropriate template
    const template = await this.templates.getTemplate(setupType || 'generic');

    // Extract parameters from idea
    const parameters = await this.extractParameters(idea, research);

    // Generate scanner code
    const scannerCode = this.generateScannerCode(
      template,
      parameters,
      research,
      constraints
    );

    return scannerCode;
  }

  private async buildFromMold(
    mold: MoldInput,
    setupType: string | undefined,
    constraints: BuildConstraints | undefined
  ): Promise<string> {
    // Parse A+ breakdown
    const breakdown = this.parseBreakdown(mold.breakdown);

    // Extract parameters from breakdown
    const parameters = this.extractMoldParameters(breakdown);

    // Get mold-specific template
    const template = await this.templates.getMoldTemplate(mold.setupName);

    // Generate scanner code
    const scannerCode = this.generateScannerFromMold(
      template,
      parameters,
      breakdown,
      constraints
    );

    return scannerCode;
  }

  private async transformToV31(
    input: TransformInput,
    constraints: BuildConstraints | undefined
  ): Promise<string> {
    // Analyze existing code
    const analysis = this.analyzeExistingCode(input.existingCode);

    // Identify V31 violations
    const violations = await this.validator.identifyViolations(input.existingCode);

    // Get V31 template
    const template = await this.templates.getV31Template();

    // Transform code to V31
    const transformedCode = this.transformCode(
      input.existingCode,
      template,
      violations,
      analysis
    );

    return transformedCode;
  }

  // ... other methods
}
```

**Acceptance Criteria**:
- [ ] Builder service created with all core methods
- [ ] Can handle all three build types (idea, mold, transform)
- [ ] V31 validation integrated
- [ ] Error handling gracefully handles failures
- [ ] All methods have unit tests

**Dependencies**:
- Archon MCP running (Sprint 2)
- V31 Gold Standard ingested (Sprint 2)
- Researcher agent available (Sprint 5)

**Risks**:
- **Risk**: Code generation produces unusable code
  - **Mitigation**: Extensive template library, validation, testing

---

### Task 6.2: Implement Idea → Scanner Generator (8 hours)

**Subtasks**:
1. Build natural language parser for ideas
2. Create parameter extraction from descriptions
3. Implement setup type detection
4. Build code generation from templates
5. Add researcher insights integration
6. Create code refinement and optimization

**Code Example**:
```typescript
// src/services/ideaToScannerGenerator.ts

export interface IdeaInput {
  description: string;
  examples?: string[];
  requirements?: string[];
  marketConditions?: string[];
}

export interface ParsedIdea {
  coreConcept: string;
  setupType: string;
  parameters: Record<string, any>;
  indicators: string[];
  logic: LogicBlock[];
  filters: Filter[];
  entryConditions: string[];
  exitConditions: string[];
}

export class IdeaToScannerGenerator {
  private researcher: ResearcherAgent;
  private templates: TemplateLibrary;

  constructor() {
    this.researcher = new ResearcherAgent();
    this.templates = new TemplateLibrary();
  }

  async generateFromIdea(idea: IdeaInput): Promise<string> {
    // Step 1: Parse idea into structured format
    const parsed = await this.parseIdea(idea);

    // Step 2: Research similar strategies
    const research = await this.researcher.research({
      query: parsed.coreConcept,
      domain: 'scanner',
      setupType: parsed.setupType
    });

    // Step 3: Get appropriate template
    const template = await this.templates.getTemplate(parsed.setupType);

    // Step 4: Enhance parameters with research insights
    const enhancedParams = await this.enhanceParameters(
      parsed.parameters,
      research
    );

    // Step 5: Generate scanner code
    const scannerCode = this.generateScannerCode(
      template,
      parsed,
      enhancedParams,
      research
    );

    // Step 6: Validate and refine
    const refinedCode = await this.validateAndRefine(scannerCode, parsed);

    return refinedCode;
  }

  private async parseIdea(idea: IdeaInput): Promise<ParsedIdea> {
    // Analyze description to extract core concept
    const coreConcept = this.extractCoreConcept(idea.description);

    // Detect setup type
    const setupType = this.detectSetupType(idea.description);

    // Extract parameters using NLP
    const parameters = await this.extractParameters(idea.description);

    // Identify required indicators
    const indicators = this.identifyIndicators(idea.description);

    // Build logic blocks
    const logic = this.buildLogicBlocks(idea.description, parameters);

    // Extract filters
    const filters = this.extractFilters(idea.description);

    // Extract entry/exit conditions
    const entryConditions = this.extractEntryConditions(idea.description);
    const exitConditions = this.extractExitConditions(idea.description);

    return {
      coreConcept,
      setupType,
      parameters,
      indicators,
      logic,
      filters,
      entryConditions,
      exitConditions
    };
  }

  private extractCoreConcept(description: string): string {
    // Use AI/LLM to extract core concept
    // For now, use keyword extraction
    const keywords = description
      .toLowerCase()
      .split(' ')
      .filter(word => word.length > 4)
      .slice(0, 5);

    return keywords.join(' ');
  }

  private detectSetupType(description: string): string {
    const desc = description.toLowerCase();

    // Check for known setup types
    if (desc.includes('oversold') || desc.includes('os d1')) {
      return 'OS D1';
    }
    if (desc.includes('gap') || desc.includes('g2g')) {
      return 'G2G S1';
    }
    if (desc.includes('demand rally') || desc.includes('dmr')) {
      return 'SC DMR';
    }
    if (desc.includes('backside')) {
      return 'Backside B';
    }

    // Default to generic
    return 'Generic';
  }

  private async extractParameters(description: string): Promise<Record<string, any>> {
    const params: Record<string, any> = {};

    // Extract numeric parameters
    const numberPattern = /(\w+)\s*[:=]\s*(\d+(?:\.\d+)?)/g;
    let match;
    while ((match = numberPattern.exec(description)) !== null) {
      const [, key, value] = match;
      params[key] = parseFloat(value);
    }

    // Extract EMA periods
    const emaPattern = /ema\s*(\d+)/gi;
    const emas: number[] = [];
    while ((match = emaPattern.exec(description)) !== null) {
      emas.push(parseInt(match[1]));
    }
    if (emas.length > 0) {
      params.ema_periods = emas;
    }

    // Extract threshold values
    const thresholdPattern = /threshold\s*(?:of\s*)?[-+]?\d*\.?\d+/gi;
    const thresholds: number[] = [];
    while ((match = thresholdPattern.exec(description)) !== null) {
      const num = parseFloat(match[0].replace(/\D/g, ''));
      if (!isNaN(num)) {
        thresholds.push(num);
      }
    }
    if (thresholds.length > 0) {
      params.threshold = thresholds[0];
    }

    return params;
  }

  private identifyIndicators(description: string): string[] {
    const indicators: string[] = [];
    const desc = description.toLowerCase();

    const indicatorPatterns = {
      'EMA Cloud': /ema\s*cloud|cloud\s*ema|ema\s*\d+.*ema\s*\d+/i,
      'Deviation Bands': /deviation|std\s*dev|sigma|band/i,
      'Volume': /volume|vol/i,
      'RSI': /rsi/i,
      'MACD': /macd/i,
      'ATR': /atr/i,
      'Gap': /gap/i
    };

    for (const [indicator, pattern] of Object.entries(indicatorPatterns)) {
      if (pattern.test(desc)) {
        indicators.push(indicator);
      }
    }

    return indicators;
  }

  private buildLogicBlocks(
    description: string,
    parameters: Record<string, any>
  ): LogicBlock[] {
    const blocks: LogicBlock[] = [];

    // Build EMA cloud logic
    if (parameters.ema_periods && parameters.ema_periods.length >= 2) {
      blocks.push({
        type: 'indicator',
        name: 'EMA Cloud',
        code: this.generateEMACloudCode(parameters.ema_periods)
      });
    }

    // Build deviation logic
    if (description.toLowerCase().includes('deviation')) {
      blocks.push({
        type: 'indicator',
        name: 'Deviation Bands',
        code: this.generateDeviationCode(parameters)
      });
    }

    // Build filter logic
    if (description.toLowerCase().includes('filter')) {
      blocks.push({
        type: 'filter',
        name: 'Volume Filter',
        code: this.generateVolumeFilterCode(parameters)
      });
    }

    return blocks;
  }

  private generateScannerCode(
    template: ScannerTemplate,
    parsed: ParsedIdea,
    parameters: Record<string, any>,
    research: ResearchResult
  ): string {
    let code = template.code;

    // Replace template placeholders
    code = code.replace(/\{\{SETUP_NAME\}\}/g, parsed.setupType.replace(/\s+/g, '_'));
    code = code.replace(/\{\{DESCRIPTION\}\}/g, parsed.coreConcept);

    // Add indicators
    const indicatorCode = this.generateIndicatorCode(parsed.indicators, parameters);
    code = code.replace(/\{\{INDICATORS\}\}/g, indicatorCode);

    // Add logic blocks
    const logicCode = parsed.logic.map(block => block.code).join('\n');
    code = code.replace(/\{\{LOGIC\}\}/g, logicCode);

    // Add filters
    const filterCode = this.generateFilterCode(parsed.filters);
    code = code.replace(/\{\{FILTERS\}\}/g, filterCode);

    // Add entry/exit conditions
    const entryCode = this.generateConditionCode(parsed.entryConditions);
    const exitCode = this.generateConditionCode(parsed.exitConditions);
    code = code.replace(/\{\{ENTRY_CONDITIONS\}\}/g, entryCode);
    code = code.replace(/\{\{EXIT_CONDITIONS\}\}/g, exitCode);

    return code;
  }

  private async validateAndRefine(
    scannerCode: string,
    parsed: ParsedIdea
  ): Promise<string> {
    // Validate V31 compliance
    const validator = new V31Validator();
    const validation = await validator.validate(scannerCode);

    // Fix any critical issues
    let refinedCode = scannerCode;
    for (const issue of validation) {
      if (issue.severity === 'critical' && issue.fix) {
        refinedCode = refinedCode.replace(issue.pattern, issue.fix);
      }
    }

    return refinedCode;
  }

  // ... helper methods
}
```

**Acceptance Criteria**:
- [ ] Can parse natural language ideas into structured format
- [ ] Setup type detection 80%+ accurate
- [ ] Parameter extraction captures key values
- [ ] Generated code compiles and runs
- [ ] Generated code passes basic V31 validation
- [ ] Performance: Generation completes in <10 seconds

**Dependencies**:
- Researcher agent (Sprint 5)
- Template library (Task 6.5)

**Risks**:
- **Risk**: NLP parsing insufficient for complex ideas
  - **Mitigation**: Interactive clarification, template fallbacks

---

### Task 6.3: Implement Non-V31 → V31 Transformer (7 hours)

**Subtasks**:
1. Build code analyzer for existing scanners
2. Create V31 violation detector
3. Implement grouped endpoint transformation
4. Add per-ticker operation transformation
5. Create two-pass feature computation transformation
6. Build smart filter implementation

**Code Example**:
```typescript
// src/services/v31Transformer.ts

export interface TransformInput {
  existingCode: string;
  scannerName: string;
  preserveLogic?: boolean;
}

export interface TransformResult {
  transformedCode: string;
  changes: TransformChange[];
  v31Compliant: boolean;
  warnings: string[];
}

export interface TransformChange {
  type: 'architecture' | 'structure' | 'logic' | 'optimization';
  description: string;
  lineNumber: number;
  original: string;
  transformed: string;
}

export class V31Transformer {
  private validator: V31Validator;

  constructor() {
    this.validator = new V31Validator();
  }

  async transformToV31(input: TransformInput): Promise<TransformResult> {
    const changes: TransformChange[] = [];
    let transformedCode = input.existingCode;

    // Step 1: Detect V31 violations
    const violations = await this.validator.identifyViolations(input.existingCode);

    // Step 2: Transform to grouped endpoint architecture
    if (violations.some(v => v.type === 'grouped-endpoint')) {
      const result = this.transformToGroupedEndpoint(transformedCode);
      transformedCode = result.code;
      changes.push(...result.changes);
    }

    // Step 3: Transform to per-ticker operations
    if (violations.some(v => v.type === 'per-ticker')) {
      const result = this.transformToPerTicker(transformedCode);
      transformedCode = result.code;
      changes.push(...result.changes);
    }

    // Step 4: Transform to two-pass feature computation
    if (violations.some(v => v.type === 'two-pass')) {
      const result = this.transformToTwoPass(transformedCode);
      transformedCode = result.code;
      changes.push(...result.changes);
    }

    // Step 5: Add smart filters
    if (violations.some(v => v.type === 'smart-filter')) {
      const result = this.addSmartFilters(transformedCode);
      transformedCode = result.code;
      changes.push(...result.changes);
    }

    // Step 6: Validate transformed code
    const validation = await this.validator.validate(transformedCode);
    const v31Compliant = validation.every(v => v.compliant);

    // Generate warnings
    const warnings = this.generateWarnings(validation, changes);

    return {
      transformedCode,
      changes,
      v31Compliant,
      warnings
    };
  }

  private transformToGroupedEndpoint(code: string): TransformResult {
    const changes: TransformChange[] = = [];
    let transformedCode = code;

    // Detect existing structure
    const hasFunction = (name: string) =>
      new RegExp(`def\\s+${name}\\s*\\(`).test(code);

    // If already has functions, try to transform
    if (hasFunction('simple_features') || hasFunction('full_features')) {
      // May already be partially V31, check structure
      const violations = this.analyzeGroupedEndpointStructure(code);

      if (violations.length > 0) {
        // Transform to proper grouped endpoint
        transformedCode = this.restructureToGroupedEndpoint(code, violations);
        changes.push({
          type: 'architecture',
          description: 'Restructured to V31 grouped endpoint architecture',
          lineNumber: 1,
          original: code.substring(0, 100) + '...',
          transformed: transformedCode.substring(0, 100) + '...'
        });
      }
    } else {
      // Transform from single-function to grouped endpoint
      transformedCode = this.convertToGroupedEndpoint(code);
      changes.push({
        type: 'architecture',
        description: 'Converted single-function scanner to V31 grouped endpoint',
        lineNumber: 1,
        original: code.substring(0, 100) + '...',
        transformed: transformedCode.substring(0, 100) + '...'
      });
    }

    return { code: transformedCode, changes };
  }

  private convertToGroupedEndpoint(code: string): string {
    // Extract the main logic from existing code
    const logicMatch = code.match(/def\s+(?:scan|detect|run)\s*\([^)]*\)\s*:\s*\n((?:\s+.*\n)+)/);
    const mainLogic = logicMatch ? logicMatch[1] : '';

    // Build V31 structure
    const v31Template = `
def simple_features(df):
    """
    Stage 1: Calculate simple features before filtering.
    These features are used for filtering decisions.
    """
    # Extract existing logic and move here
    ${this.extractSimpleFeaturesCode(code)}

    return df

def filter(df):
    """
    Stage 2: Filter dataframe based on simple features.
    Preserves historical data for accurate indicator calculations.
    """
    # Apply filters
    filtered = df[
        # Add filter conditions
    ].copy()

    return filtered

def full_features(df):
    """
    Stage 3: Calculate full/compute-intensive features after filtering.
    Only processes tickers that passed the filter.
    """
    # Extract remaining logic
    ${this.extractFullFeaturesCode(code)}

    return df

def detect(df):
    """
    Stage 4: Detect signals based on all calculated features.
    Returns dataframe with signals only.
    """
    signals = df[
        # Add signal detection logic
        ${mainLogic}
    ].copy()

    return signals

def grouped_endpoint_scanner(data):
    """
    V31 Gold Standard: Grouped endpoint scanner architecture.
    Processes each ticker independently to avoid lookahead bias.
    """
    all_signals = []

    for ticker, group in data.groupby('ticker'):
        # Stage 1: Simple features
        with_features = simple_features(group)

        # Stage 2: Filter
        filtered = filter(with_features)

        # Don't process if no data after filter
        if filtered.empty:
            continue

        # Stage 3: Full features
        with_full_features = full_features(filtered)

        # Stage 4: Detect signals
        signals = detect(with_full_features)

        if not signals.empty:
            all_signals.append(signals)

    # Combine all signals
    if all_signals:
        return pd.concat(all_signals)
    else:
        return pd.DataFrame()
`;

    return v31Template.trim();
  }

  private transformToPerTicker(code: string): TransformResult {
    const changes: TransformChange[] = [];
    let transformedCode = code;

    // Check if operations are already per-ticker
    const hasGroupby = /groupby\s*\(\s*['"]ticker['"]/.test(code);

    if (!hasGroupby) {
      // Wrap operations in groupby
      transformedCode = this.wrapInGroupby(code);

      changes.push({
        type: 'structure',
        description: 'Wrapped operations in per-ticker groupby',
        lineNumber: 1,
        original: code.substring(0, 100) + '...',
        transformed: transformedCode.substring(0, 100) + '...'
      });
    }

    return { code: transformedCode, changes };
  }

  private wrapInGroupby(code: string): string {
    // Find operations that need per-ticker grouping
    const operations = [
      /rolling\s*\(/g,
      /ewm\s*\(/g,
      /shift\s*\(/g,
      /diff\s*\(/g,
      /pct_change\s*\(/g
    ];

    let wrappedCode = code;

    // Wrap main function in groupby loop
    const mainFunctionMatch = wrappedCode.match(
      /def\s+(?:scan|detect|run)\s*\([^)]*\)\s*:\s*\n((?:\s+.*\n)+)/
    );

    if (mainFunctionMatch) {
      const functionBody = mainFunctionMatch[1];
      const indentedBody = functionBody.split('\n').map(line => '    ' + line).join('\n');

      const wrappedFunction = `
def scan_with_per_ticker_operations(data):
    """
    Per-ticker operations to ensure correct historical buffer calculation.
    """
    all_signals = []

    for ticker, group in data.groupby('ticker'):
        # Process each ticker independently
${indentedBody}

        if not signals.empty:
            all_signals.append(signals)

    # Combine results
    if all_signals:
        return pd.concat(all_signals)
    else:
        return pd.DataFrame()
`;

      wrappedCode = wrappedCode.replace(mainFunctionMatch[0], wrappedFunction);
    }

    return wrappedCode;
  }

  private transformToTwoPass(code: string): TransformResult {
    const changes: TransformChange[] = [];
    let transformedCode = code;

    // Detect if already two-pass
    const hasSimpleFeatures = /def\s+simple_features/.test(code);
    const hasFullFeatures = /def\s+full_features/.test(code);

    if (!hasSimpleFeatures || !hasFullFeatures) {
      // Separate simple and complex operations
      transformedCode = this.separateSimpleAndComplexFeatures(code);

      changes.push({
        type: 'architecture',
        description: 'Separated simple and complex features into two-pass approach',
        lineNumber: 1,
        original: code.substring(0, 100) + '...',
        transformed: transformedCode.substring(0, 100) + '...'
      });
    }

    return { code: transformedCode, changes };
  }

  private separateSimpleAndComplexFeatures(code: string): string {
    // Identify simple operations (EMA, SMA, basic math)
    const simpleOps = [
      ['ema', 'ewm'],
      ['sma', 'rolling'],
      ['basic_math', ['+', '-', '*', '/']]
    ];

    // Identify complex operations (rank, percentile, complex indicators)
    const complexOps = [
      'rank',
      'percentile',
      'quantile',
      'bollinger',  // Requires std
      'rsi',        // Requires gain/loss
      'macd'        // Requires multiple EMAs
    ];

    // Parse code and separate operations
    // This is simplified - real implementation would use AST parsing

    return code; // Placeholder
  }

  private addSmartFilters(code: string): TransformResult {
    const changes: TransformChange[] = [];
    let transformedCode = code;

    // Check if smart filter function exists
    const hasSmartFilter = /def\s+(?:filter|smart_filter)\s*\(/.test(code);

    if (!hasSmartFilter) {
      // Add smart filter before signal detection
      const smartFilterCode = `
def filter(df):
    """
    Smart filter: Preserves historical data for accurate indicator calculations.
    Only filters for display purposes, not for computation.
    """
    # Start with all data
    filtered = df.copy()

    # Apply display filters
    # Example: Only show recent data
    # filtered = filtered[filtered['date'] >= RECENT_CUTOFF]

    # IMPORTANT: Keep historical data for indicator calculations
    # Do NOT filter before computing rolling/ewm features

    return filtered
`;

      // Insert before detect function
      const detectMatch = transformedCode.match(/def\s+detect\s*\(/);
      if (detectMatch) {
        const insertIndex = detectMatch.index;
        transformedCode =
          transformedCode.slice(0, insertIndex) +
          smartFilterCode +
          '\n' +
          transformedCode.slice(insertIndex);

        changes.push({
          type: 'structure',
          description: 'Added smart filter function',
          lineNumber: insertIndex,
          original: '',
          transformed: smartFilterCode.trim()
        });
      }
    }

    return { code: transformedCode, changes };
  }

  // ... helper methods
}
```

**Acceptance Criteria**:
- [ ] Can detect all V31 violations accurately
- [ ] Transformation produces V31-compliant code
- [ ] Transformed code preserves original logic
- [ ] Transformed code passes validation
- [ ] Performance: Transformation completes in <15 seconds

**Dependencies**:
- V31 validator (Task 6.4)
- V31 Gold Standard ingested (Sprint 2)

**Risks**:
- **Risk**: Transformation breaks scanner logic
  - **Mitigation**: Comprehensive testing, side-by-side comparison

---

### Task 6.4: Implement V31 Validation System (5 hours)

**Subtasks**:
1. Create V31 compliance checker
2. Build violation detector
3. Implement architecture validator
4. Create code quality analyzer
5. Build test generator
6. Add validation reporting

**Code Example**:
```typescript
// src/services/v31Validator.ts

export interface ValidationResult {
  compliant: boolean;
  category: 'architecture' | 'structure' | 'quality' | 'performance';
  type: string;
  severity: 'critical' | 'major' | 'minor' | 'info';
  message: string;
  lineNumber?: number;
  pattern?: RegExp;
  fix?: string;
}

export class V31Validator {
  private v31Spec: V31Specification;

  constructor() {
    this.loadV31Specification();
  }

  async validate(scannerCode: string): Promise<ValidationResult[]> {
    const results: ValidationResult[] = [];

    // Validate grouped endpoint architecture
    results.push(...this.validateGroupedEndpoint(scannerCode));

    // Validate per-ticker operations
    results.push(...this.validatePerTickerOperations(scannerCode));

    // Validate two-pass feature computation
    results.push(...this.validateTwoPassComputation(scannerCode));

    // Validate smart filters
    results.push(...this.validateSmartFilters(scannerCode));

    // Validate code quality
    results.push(...this.validateCodeQuality(scannerCode));

    return results;
  }

  async identifyViolations(scannerCode: string): Promise<ValidationResult[]> {
    const allResults = await this.validate(scannerCode);

    // Return only violations
    return allResults.filter(r => !r.compliant);
  }

  private validateGroupedEndpoint(code: string): ValidationResult[] {
    const results: ValidationResult[] = [];

    // Check for simple_features function
    const hasSimpleFeatures = /def\s+simple_features\s*\(/.test(code);
    if (!hasSimpleFeatures) {
      results.push({
        compliant: false,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'critical',
        message: 'Missing simple_features() function - required for V31 compliance',
        pattern: /def\s+simple_features\s*\(/,
        fix: 'def simple_features(df):\n    # Stage 1: Calculate simple features\n    return df'
      });
    } else {
      results.push({
        compliant: true,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'info',
        message: 'simple_features() function found'
      });
    }

    // Check for filter function
    const hasFilter = /def\s+filter\s*\(/.test(code);
    if (!hasFilter) {
      results.push({
        compliant: false,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'critical',
        message: 'Missing filter() function - required for V31 smart filtering',
        pattern: /def\s+filter\s*\(/,
        fix: 'def filter(df):\n    # Stage 2: Filter dataframe\n    return df'
      });
    } else {
      results.push({
        compliant: true,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'info',
        message: 'filter() function found'
      });
    }

    // Check for full_features function
    const hasFullFeatures = /def\s+full_features\s*\(/.test(code);
    if (!hasFullFeatures) {
      results.push({
        compliant: false,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'critical',
        message: 'Missing full_features() function - required for V31 compliance',
        pattern: /def\s+full_features\s*\(/,
        fix: 'def full_features(df):\n    # Stage 3: Calculate full features\n    return df'
      });
    } else {
      results.push({
        compliant: true,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'info',
        message: 'full_features() function found'
      });
    }

    // Check for detect function
    const hasDetect = /def\s+detect\s*\(/.test(code);
    if (!hasDetect) {
      results.push({
        compliant: false,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'critical',
        message: 'Missing detect() function - required for V31 signal detection',
        pattern: /def\s+detect\s*\(/,
        fix: 'def detect(df):\n    # Stage 4: Detect signals\n    return df'
      });
    } else {
      results.push({
        compliant: true,
        category: 'architecture',
        type: 'grouped-endpoint',
        severity: 'info',
        message: 'detect() function found'
      });
    }

    return results;
  }

  private validatePerTickerOperations(code: string): ValidationResult[] {
    const results: ValidationResult[] = [];

    // Check for groupby('ticker')
    const hasGroupby = /groupby\s*\(\s*['"]ticker['"]/.test(code);
    if (!hasGroupby) {
      results.push({
        compliant: false,
        category: 'structure',
        type: 'per-ticker',
        severity: 'critical',
        message: 'Missing groupby("ticker") - required for per-ticker operations',
        pattern: /groupby\s*\(\s*['"]ticker['"]/
      });
    } else {
      results.push({
        compliant: true,
        category: 'structure',
        type: 'per-ticker',
        severity: 'info',
        message: 'Per-ticker groupby found'
      });
    }

    // Check for operations before groupby (anti-pattern)
    const lines = code.split('\n');
    lines.forEach((line, index) => {
      const hasRollingBeforeGroupby =
        /rolling\s*\(/.test(line) && !hasGroupby;
      const hasEwmBeforeGroupby =
        /ewm\s*\(/.test(line) && !hasGroupby;

      if (hasRollingBeforeGroupby || hasEwmBeforeGroupby) {
        results.push({
          compliant: false,
          category: 'structure',
          type: 'per-ticker',
          severity: 'major',
          message: 'Rolling/EWM operation found outside per-ticker groupby',
          lineNumber: index + 1,
          pattern: /rolling\s*\(|ewm\s*\(/
        });
      }
    });

    return results;
  }

  private validateTwoPassComputation(code: string): ValidationResult[] {
    const results: ValidationResult[] = [];

    // Check for simple_features before full_features
    const simpleFeaturesMatch = code.match(/def\s+simple_features\s*\(/);
    const fullFeaturesMatch = code.match(/def\s+full_features\s*\(/);

    if (simpleFeaturesMatch && fullFeaturesMatch) {
      const simpleIndex = simpleFeaturesMatch.index;
      const fullIndex = fullFeaturesMatch.index;

      if (simpleIndex < fullIndex) {
        results.push({
          compliant: true,
          category: 'architecture',
          type: 'two-pass',
          severity: 'info',
          message: 'Two-pass feature computation: simple_features before full_features'
        });
      } else {
        results.push({
          compliant: false,
          category: 'architecture',
          type: 'two-pass',
          severity: 'major',
          message: 'full_features should come after simple_features in two-pass approach'
        });
      }
    }

    // Check for complex operations in simple_features
    if (simpleFeaturesMatch) {
      const simpleFeaturesEnd = this.findFunctionEnd(code, simpleFeaturesMatch.index);
      const simpleFeaturesCode = code.substring(simpleFeaturesMatch.index, simpleFeaturesEnd);

      const complexOps = ['rank', 'percentile', 'quantile'];
      complexOps.forEach(op => {
        if (new RegExp(op, 'i').test(simpleFeaturesCode)) {
          results.push({
            compliant: false,
            category: 'architecture',
            type: 'two-pass',
            severity: 'minor',
            message: `Complex operation (${op}) found in simple_features - consider moving to full_features`
          });
        }
      });
    }

    return results;
  }

  private validateSmartFilters(code: string): ValidationResult[] {
    const results: ValidationResult[] = [];

    // Check for filter before compute operations (anti-pattern)
    const lines = code.split('\n');
    let filterFound = false;
    let computeAfterFilter = false;

    lines.forEach((line, index) => {
      if (/def\s+filter\s*\(/.test(line)) {
        filterFound = true;
      }
      if (filterFound && /rolling\s*\(|ewm\s*\(/.test(line)) {
        computeAfterFilter = true;
        results.push({
          compliant: false,
          category: 'structure',
          type: 'smart-filter',
          severity: 'critical',
          message: 'Compute operation found after filter - breaks smart filter pattern',
          lineNumber: index + 1
        });
      }
    });

    if (!filterFound) {
      results.push({
        compliant: false,
        category: 'structure',
        type: 'smart-filter',
        severity: 'major',
        message: 'No filter function found - smart filtering not implemented'
      });
    } else if (!computeAfterFilter) {
      results.push({
        compliant: true,
        category: 'structure',
        type: 'smart-filter',
        severity: 'info',
        message: 'Smart filter pattern correctly implemented'
      });
    }

    return results;
  }

  private validateCodeQuality(code: string): ValidationResult[] {
    const results: ValidationResult[] = [];

    // Check for docstrings
    const functions = code.match(/def\s+\w+\s*\(/g) || [];
    const docstrings = code.match(/"""[\s\S]*?"""/g) || [];

    if (docstrings.length < functions.length) {
      results.push({
        compliant: false,
        category: 'quality',
        type: 'documentation',
        severity: 'minor',
        message: 'Missing docstrings - add docstrings to all functions'
      });
    }

    // Check for type hints
    const hasTypeHints = /def\s+\w+\s*\([^)]*\):\s*->/.test(code);
    if (!hasTypeHints) {
      results.push({
        compliant: false,
        category: 'quality',
        type: 'type-hints',
        severity: 'info',
        message: 'No type hints found - consider adding for better code quality'
      });
    }

    // Check for hardcoded values
    const hardcodedNumbers = code.match(/\b\d{2,}\b/g);
    if (hardcodedNumbers && hardcodedNumbers.length > 5) {
      results.push({
        compliant: false,
        category: 'quality',
        type: 'hardcoding',
        severity: 'minor',
        message: 'Multiple hardcoded values found - consider using named constants',
        lineNumber: undefined
      });
    }

    return results;
  }

  private findFunctionEnd(code: string, startIndex: number): number {
    const lines = code.substring(startIndex).split('\n');
    let indentLevel = 0;
    let endIndex = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const indent = line.search(/\S/);

      if (i === 0) {
        indentLevel = indent;
      } else if (indent <= indentLevel && line.trim().length > 0) {
        endIndex = startIndex + lines.slice(0, i).join('\n').length;
        break;
      }
    }

    return endIndex || code.length;
  }

  private loadV31Specification() {
    // Load V31 Gold Standard from Archon
    // This would be loaded from the ingested specification
    this.v31Spec = {
      groupedEndpoint: {
        simple_features: true,
        filter: true,
        full_features: true,
        detect: true
      },
      perTicker: true,
      twoPass: true,
      smartFilter: true
    };
  }
}
```

**Acceptance Criteria**:
- [ ] Can detect all V31 architecture violations
- [ ] Can detect all V31 structure violations
- [ ] Validation is accurate with minimal false positives
- [ ] Provides actionable fix suggestions
- [ ] Performance: Validation completes in <3 seconds

**Dependencies**:
- V31 Gold Standard ingested (Sprint 2)

**Risks**:
- **Risk**: False positives in validation
  - **Mitigation**: Tuning with real scanner code, manual review

---

### Task 6.5: Build Template Library (4 hours)

**Subtasks**:
1. Create template structure
2. Build setup-specific templates (OS D1, G2G S1, SC DMR, Backside B)
3. Create generic scanner template
4. Add V31 template
5. Implement template retrieval system
6. Create template customization system

**Code Example**:
```typescript
// src/services/templateLibrary.ts

export interface ScannerTemplate {
  name: string;
  setupType: string;
  category: 'setup' | 'generic' | 'v31';
  code: string;
  parameters: TemplateParameter[];
  description: string;
  indicators: string[];
}

export interface TemplateParameter {
  name: string;
  type: 'number' | 'string' | 'boolean' | 'array';
  default: any;
  description: string;
  required: boolean;
  validation?: (value: any) => boolean;
}

export class TemplateLibrary {
  private templates: Map<string, ScannerTemplate>;

  constructor() {
    this.templates = new Map();
    this.loadTemplates();
  }

  async getTemplate(setupType: string): Promise<ScannerTemplate> {
    // Try to get setup-specific template
    const template = this.templates.get(setupType.toLowerCase());

    if (template) {
      return template;
    }

    // Fall back to generic template
    return this.templates.get('generic')!;
  }

  async getMoldTemplate(setupName: string): Promise<ScannerTemplate> {
    // Similar setup types map to same templates
    const setupTypeMap: Record<string, string> = {
      'OS D1': 'os_d1',
      'G2G S1': 'g2g_s1',
      'SC DMR': 'sc_dmr',
      'Backside B': 'backside_b'
    };

    const templateKey = setupTypeMap[setupName] || 'generic';
    return this.templates.get(templateKey) || this.templates.get('generic')!;
  }

  async getV31Template(): Promise<ScannerTemplate> {
    return this.templates.get('v31')!;
  }

  private loadTemplates() {
    // OS D1 Template
    this.templates.set('os_d1', {
      name: 'OS D1 Scanner',
      setupType: 'OS D1',
      category: 'setup',
      code: `
def simple_features(df):
    """
    Stage 1: Calculate simple features for OS D1 setup.
    Oversold Daily - extreme deviation below lower EMA cloud.
    """
    # EMA Cloud
    df['ema_20'] = df['close'].ewm(span={{ema_short}}).mean()
    df['ema_50'] = df['close'].ewm(span={{ema_long}}).mean()
    df['cloud_mid'] = (df['ema_20'] + df['ema_50']) / 2

    # Deviation bands
    df['deviation'] = (df['close'] - df['cloud_mid']) / df['cloud_mid']

    return df

def filter(df):
    """
    Stage 2: Filter for potential OS D1 candidates.
    """
    # Filter for extreme deviation
    filtered = df[
        (df['deviation'] < -{{deviation_threshold}}) &
        (df['volume'] > {{min_volume}})
    ].copy()

    return filtered

def full_features(df):
    """
    Stage 3: Calculate full features for filtered candidates.
    """
    # Additional confirmation indicators
    df['rsi'] = calculate_rsi(df['close'], period=14)
    df['volume_ratio'] = df['volume'] / df['volume'].rolling(50).mean()

    return df

def detect(df):
    """
    Stage 4: Detect OS D1 signals.
    """
    signals = df[
        (df['deviation'] < -{{deviation_threshold}}) &
        (df['rsi'] < {{rsi_threshold}}) &
        (df['volume_ratio'] > {{volume_ratio_threshold}})
    ].copy()

    return signals

def grouped_endpoint_scanner(data):
    """
    OS D1 Scanner - V31 Gold Standard Compliant.
    """
    all_signals = []

    for ticker, group in data.groupby('ticker'):
        # Stage 1: Simple features
        with_simple = simple_features(group)

        # Stage 2: Filter
        filtered = filter(with_simple)

        if filtered.empty:
            continue

        # Stage 3: Full features
        with_full = full_features(filtered)

        # Stage 4: Detect
        signals = detect(with_full)

        if not signals.empty:
            all_signals.append(signals)

    if all_signals:
        return pd.concat(all_signals)
    else:
        return pd.DataFrame()
      `.trim(),
      parameters: [
        {
          name: 'ema_short',
          type: 'number',
          default: 20,
          description: 'Short EMA period',
          required: true,
          validation: (v) => v > 0 && v < 100
        },
        {
          name: 'ema_long',
          type: 'number',
          default: 50,
          description: 'Long EMA period',
          required: true,
          validation: (v) => v > 0 && v < 200
        },
        {
          name: 'deviation_threshold',
          type: 'number',
          default: 2.5,
          description: 'Deviation threshold (negative)',
          required: true
        },
        {
          name: 'min_volume',
          type: 'number',
          default: 1000000,
          description: 'Minimum volume',
          required: true
        },
        {
          name: 'rsi_threshold',
          type: 'number',
          default: 30,
          description: 'RSI threshold',
          required: true
        },
        {
          name: 'volume_ratio_threshold',
          type: 'number',
          default: 1.5,
          description: 'Volume ratio threshold',
          required: true
        }
      ],
      description: 'Oversold Daily setup - detects extreme deviation below lower EMA cloud',
      indicators: ['EMA Cloud', 'Deviation Bands', 'RSI', 'Volume']
    });

    // G2G S1 Template
    this.templates.set('g2g_s1', {
      name: 'G2G S1 Scanner',
      setupType: 'G2G S1',
      category: 'setup',
      code: `
# Similar structure for G2G S1...
      `.trim(),
      parameters: [
        // G2G S1 specific parameters
      ],
      description: 'Gap-to-Gap Stage 1 setup',
      indicators: ['Gap Detection', 'Resistance Levels', 'Volume']
    });

    // SC DMR Template
    this.templates.set('sc_dmr', {
      name: 'SC DMR Scanner',
      setupType: 'SC DMR',
      category: 'setup',
      code: `
# Similar structure for SC DMR...
      `.trim(),
      parameters: [
        // SC DMR specific parameters
      ],
      description: 'Stage Change Demand Rally setup',
      indicators: ['Demand Zones', 'Volume', 'Momentum']
    });

    // Backside B Template
    this.templates.set('backside_b', {
      name: 'Backside B Scanner',
      setupType: 'Backside B',
      category: 'setup',
      code: `
# Similar structure for Backside B...
      `.trim(),
      parameters: [
        // Backside B specific parameters
      ],
      description: 'Backside B setup',
      indicators: ['Trend Break', 'Supply Zones', 'Momentum']
    });

    // Generic Template
    this.templates.set('generic', {
      name: 'Generic Scanner Template',
      setupType: 'Generic',
      category: 'generic',
      code: `
# Generic V31-compliant template...
      `.trim(),
      parameters: [],
      description: 'Generic V31-compliant scanner template',
      indicators: []
    });

    // V31 Template
    this.templates.set('v31', {
      name: 'V31 Gold Standard Template',
      setupType: 'V31',
      category: 'v31',
      code: `
# Pure V31 structure template...
      `.trim(),
      parameters: [],
      description: 'V31 Gold Standard architecture template',
      indicators: []
    });
  }
}
```

**Acceptance Criteria**:
- [ ] Templates exist for all 4 systematized setups
- [ ] Generic template available for custom setups
- [ ] V31 template for transformations
- [ ] All templates are V31-compliant
- [ ] Template retrieval is fast (<100ms)

**Dependencies**:
- V31 Gold Standard ingested (Sprint 2)

**Risks**:
- **Risk**: Template quality insufficient
  - **Mitigation**: Iterative improvement, user feedback

---

### Task 6.6: Implement A+ Mold → Scanner Converter (6 hours)

**Subtasks**:
1. Build A+ breakdown parser
2. Create parameter extraction from breakdown
3. Implement mold-specific code generation
4. Add pattern detection from mold
5. Create validation against A+ examples
6. Build testing on A+ names workflow

**Code Example**:
```typescript
// src/services/moldToScannerConverter.ts

export interface MoldInput {
  setupName: string;
  breakdown: string;
  aPlusNames: string[];
  parameters?: Record<string, any>;
}

export interface ParsedBreakdown {
  setupType: string;
  entryConditions: Condition[];
  exitConditions: Condition[];
  indicators: IndicatorConfig[];
  parameters: Record<string, any>;
  stopLoss?: number;
  takeProfit?: number;
  positionSize?: number;
}

export class MoldToScannerConverter {
  private templates: TemplateLibrary;
  private researcher: ResearcherAgent;

  constructor() {
    this.templates = new TemplateLibrary();
    this.researcher = new ResearcherAgent();
  }

  async convert(mold: MoldInput): Promise<string> {
    // Step 1: Parse A+ breakdown
    const parsed = this.parseBreakdown(mold.breakdown);

    // Step 2: Extract parameters
    const parameters = {
      ...parsed.parameters,
      ...mold.parameters
    };

    // Step 3: Research similar setups
    const research = await this.researcher.research({
      query: mold.setupName,
      domain: 'scanner',
      setupType: parsed.setupType
    });

    // Step 4: Get mold-specific template
    const template = await this.templates.getMoldTemplate(mold.setupName);

    // Step 5: Generate scanner code
    const scannerCode = this.generateFromMold(
      template,
      parsed,
      parameters,
      research
    );

    // Step 6: Validate against A+ names
    const validated = await this.validateAgainstAPlusNames(
      scannerCode,
      mold.aPlusNames
    );

    return validated;
  }

  private parseBreakdown(breakdown: string): ParsedBreakdown {
    const parsed: ParsedBreakdown = {
      setupType: '',
      entryConditions: [],
      exitConditions: [],
      indicators: [],
      parameters: {}
    };

    // Detect setup type
    const setupTypes = ['OS D1', 'G2G S1', 'SC DMR', 'Backside B'];
    for (const type of setupTypes) {
      if (breakdown.toLowerCase().includes(type.toLowerCase())) {
        parsed.setupType = type;
        break;
      }
    }

    // Extract entry conditions
    const entryMatch = breakdown.match(/entry\s*[:\s]*(.*?)(?=exit|stop|take|$)/is);
    if (entryMatch) {
      parsed.entryConditions = this.parseConditions(entryMatch[1]);
    }

    // Extract exit conditions
    const exitMatch = breakdown.match(/exit\s*[:\s]*(.*?)(?=stop|take|$)/is);
    if (exitMatch) {
      parsed.exitConditions = this.parseConditions(exitMatch[1]);
    }

    // Extract stop loss
    const stopMatch = breakdown.match(/stop\s*[:\s]*[-+]?\d*\.?\d+/i);
    if (stopMatch) {
      parsed.stopLoss = parseFloat(stopMatch[0].replace(/\D/g, ''));
    }

    // Extract take profit
    const takeMatch = breakdown.match(/take\s*[:\s]*[-+]?\d*\.?\d+/i);
    if (takeMatch) {
      parsed.takeProfit = parseFloat(takeMatch[0].replace(/\D/g, ''));
    }

    // Extract indicators
    parsed.indicators = this.extractIndicators(breakdown);

    // Extract parameters
    parsed.parameters = this.extractMoldParameters(breakdown);

    return parsed;
  }

  private parseConditions(text: string): Condition[] {
    const conditions: Condition[] = [];

    // Split by common delimiters
    const parts = text.split(/,|and|;|\n/);

    parts.forEach(part => {
      const condition = part.trim();
      if (condition.length > 0) {
        conditions.push({
          description: condition,
          type: this.inferConditionType(condition)
        });
      }
    });

    return conditions;
  }

  private inferConditionType(condition: string): string {
    const cond = condition.toLowerCase();

    if (cond.includes('cross') || cond.includes('above') || cond.includes('below')) {
      return 'crossover';
    }
    if (cond.includes('volume')) {
      return 'volume';
    }
    if (cond.includes('rsi') || cond.includes('macd')) {
      return 'indicator';
    }
    if (cond.includes('close') || cond.includes('price')) {
      return 'price';
    }

    return 'generic';
  }

  private extractIndicators(breakdown: string): IndicatorConfig[] {
    const indicators: IndicatorConfig[] = [];

    const indicatorPatterns = {
      'EMA Cloud': /ema\s*cloud|cloud\s*ema/i,
      'Deviation Bands': /deviation|std\s*dev|sigma/i,
      'Volume': /volume/i,
      'RSI': /rsi/i,
      'MACD': /macd/i,
      'ATR': /atr/i
    };

    for (const [indicator, pattern] of Object.entries(indicatorPatterns)) {
      if (pattern.test(breakdown)) {
        indicators.push({
          name: indicator,
          parameters: this.extractIndicatorParams(indicator, breakdown)
        });
      }
    }

    return indicators;
  }

  private extractMoldParameters(breakdown: string): Record<string, any> {
    const params: Record<string, any> = {};

    // Extract numeric parameters
    const patterns = {
      ema_short: /ema\s*(\d+)/i,
      ema_long: /ema\s*(\d+).*?ema\s*(\d+)/i,
      deviation: /deviation\s*(?:of\s*)?([-+]?\d*\.?\d+)/i,
      threshold: /threshold\s*(?:of\s*)?([-+]?\d*\.?\d+)/i
    };

    for (const [key, pattern] of Object.entries(patterns)) {
      const match = breakdown.match(pattern);
      if (match) {
        if (key === 'ema_long' && match[2]) {
          params[key] = parseInt(match[2]);
        } else if (match[1]) {
          params[key] = parseFloat(match[1]);
        }
      }
    }

    return params;
  }

  private generateFromMold(
    template: ScannerTemplate,
    parsed: ParsedBreakdown,
    parameters: Record<string, any>,
    research: ResearchResult
  ): string {
    let code = template.code;

    // Replace parameter placeholders
    for (const [key, value] of Object.entries(parameters)) {
      const placeholder = `{{${key}}}`;
      code = code.replace(new RegExp(placeholder, 'g'), String(value));
    }

    // Add entry conditions
    const entryCode = this.generateConditionCode(parsed.entryConditions);
    code = code.replace(/\{\{ENTRY_CONDITIONS\}\}/g, entryCode);

    // Add exit conditions
    const exitCode = this.generateConditionCode(parsed.exitConditions);
    code = code.replace(/\{\{EXIT_CONDITIONS\}\}/g, exitCode);

    // Add stop loss / take profit
    if (parsed.stopLoss) {
      code = code.replace(/\{\{STOP_LOSS\}\}/g, String(parsed.stopLoss));
    }
    if (parsed.takeProfit) {
      code = code.replace(/\{\{TAKE_PROFIT\}\}/g, String(parsed.takeProfit));
    }

    return code;
  }

  private async validateAgainstAPlusNames(
    scannerCode: string,
    aPlusNames: string[]
  ): Promise<string> {
    // This would deploy the scanner and test it on A+ names
    // For now, just return the code
    // In Sprint 7, Executor will handle actual testing

    return scannerCode;
  }

  // ... helper methods
}
```

**Acceptance Criteria**:
- [ ] Can parse A+ breakdowns accurately
- [ ] Extracts parameters from breakdown
- [ ] Generates functional scanner code
- [ ] Generated code tests successfully on A+ names
- [ ] Performance: Conversion completes in <10 seconds

**Dependencies**:
- Template library (Task 6.5)
- Researcher agent (Sprint 5)

**Risks**:
- **Risk**: Breakdown parsing inaccurate
  - **Mitigation**: Interactive clarification, manual review

---

### Task 6.7: Integrate with CopilotKit Actions (4 hours)

**Subtasks**:
1. Define CopilotKit action schemas
2. Implement action handlers
3. Create action result formatting
4. Add error handling
5. Test all builder actions

**Code Example**:
```typescript
// src/components/renataV2CopilotKit.tsx

<Action
  name="generateScannerFromIdea"
  description="Generate a V31-compliant scanner from a natural language idea"
  parameters={[
    {
      name: "idea",
      type: "string",
      description: "Description of the scanner idea",
      required: true
    },
    {
      name: "setupType",
      type: "string",
      description: "Optional setup type (OS D1, G2G S1, SC DMR, Backside B)",
      required: false
    }
  ]}
  handler={async (args) => {
    const builder = new BuilderAgent();
    const result = await builder.build({
      type: 'idea',
      input: { description: args.idea },
      setupType: args.setupType
    });

    return {
      scannerName: result.scannerName,
      v31Compliant: result.v31Compliant,
      qualityScore: Math.round(result.qualityScore * 100) + '%',
      warnings: result.warnings,
      suggestedTests: result.suggestedTests,
      code: result.scannerCode
    };
  }}
/>

<Action
  name="transformToV31"
  description="Transform an existing non-V31 scanner to V31 Gold Standard compliance"
  parameters={[
    {
      name: "code",
      type: "string",
      description: "Existing scanner code to transform",
      required: true
    },
    {
      name: "scannerName",
      type: "string",
      description: "Name of the scanner",
      required: true
    }
  ]}
  handler={async (args) => {
    const transformer = new V31Transformer();
    const result = await transformer.transformToV31({
      existingCode: args.code,
      scannerName: args.scannerName
    });

    return {
      transformedCode: result.transformedCode,
      v31Compliant: result.v31Compliant,
      changeCount: result.changes.length,
      changes: result.changes.map(c => ({
        type: c.type,
        description: c.description
      })),
      warnings: result.warnings
    };
  }}
/>

<Action
  name="buildFromMold"
  description="Build a scanner from an A+ example mold"
  parameters={[
    {
      name: "setupName",
      type: "string",
      description: "Name of the setup (e.g., OS D1, G2G S1)",
      required: true
    },
    {
      name: "breakdown",
      type: "string",
      description: "A+ example breakdown",
      required: true
    },
    {
      name: "aPlusNames",
      type: "array",
      description: "A+ example ticker symbols",
      required: true
    }
  ]}
  handler={async (args) => {
    const converter = new MoldToScannerConverter();
    const scannerCode = await converter.convert({
      setupName: args.setupName,
      breakdown: args.breakdown,
      aPlusNames: args.aPlusNames
    });

    return {
      scannerCode,
      setupName: args.setupName,
      readyForTesting: true
    };
  }}
/>
```

**Acceptance Criteria**:
- [ ] All builder actions defined and working
- [ ] Actions return properly formatted results
- [ ] Error handling works
- [ ] Performance: Actions complete in <15 seconds

**Dependencies**:
- CopilotKit installed (Sprint 3)
- All builder components built (Tasks 6.1-6.6)

**Risks**:
- **Risk**: Code generation timeout
  - **Mitigation**: Streaming generation, progress updates

---

### Task 6.8: Testing & Validation (5 hours)

**Subtasks**:
1. Create unit tests for builder agent
2. Create tests for idea → scanner generator
3. Create tests for V31 transformer
4. Create tests for validator
5. Create tests for template library
6. Create tests for mold converter
7. Manual validation with real examples
8. Performance testing

**Acceptance Criteria**:
- [ ] Unit tests achieve 80%+ coverage
- [ ] Generated code compiles and runs
- [ ] V31 validation accuracy 95%+
- [ ] All templates validated
- [ ] Performance: All operations complete in specified times
- [ ] Manual validation successful with real A+ examples

**Dependencies**:
- All builder components built (Tasks 6.1-6.7)

**Risks**:
- **Risk**: Test coverage insufficient
  - **Mitigation**: Target 80% coverage, manual validation

---

## 📊 SPRINT 6 SUMMARY

### Time Investment
| Task | Hours | Priority |
|------|-------|----------|
| 6.1 Create Builder Agent Service | 6 | Critical |
| 6.2 Implement Idea → Scanner Generator | 8 | Critical |
| 6.3 Implement Non-V31 → V31 Transformer | 7 | Critical |
| 6.4 Implement V31 Validation System | 5 | Critical |
| 6.5 Build Template Library | 4 | High |
| 6.6 Implement A+ Mold → Scanner Converter | 6 | Critical |
| 6.7 Integrate with CopilotKit Actions | 4 | Critical |
| 6.8 Testing & Validation | 5 | Critical |
| **TOTAL** | **45 hours** | |

### Completion Criteria
Sprint 6 is complete when:
- [ ] Builder agent can generate scanners from ideas
- [ ] V31 transformer produces compliant code
- [ ] A+ mold converter works
- [ ] All generated code passes V31 validation
- [ ] All CopilotKit actions working
- [ ] Test coverage 80%+, all tests passing
- [ ] Manual validation successful

### Dependencies
**Required Before Sprint 6**:
- Sprint 2: V31 Gold Standard ingested
- Sprint 3: CopilotKit installed
- Sprint 5: Researcher agent available

**Enables Sprint 7**:
- Executor will deploy generated scanners
- Test generated scanners on A+ examples
- Run backtests on generated scanners

---

**Sprint 6 creates the code generation engine that transforms ideas into production scanners.**

**By completing Sprint 6, Renata can build V31-compliant scanners from any input.**

**Ready to build Executor Agent in Sprint 7.**
