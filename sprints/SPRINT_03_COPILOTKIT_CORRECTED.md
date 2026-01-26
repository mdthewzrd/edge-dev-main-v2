# 🤖 SPRINT 3: COPILOTKIT INTEGRATION (CORRECTED)
## Renata AI Assistant - Sidebar Integration

**Duration**: Weeks 3-4 (14 days)
**Objective**: Integrate CopilotKit-based Renata as sidebar chat, preserve all existing UI
**Dependencies**: Sprint 1 (Platform stable), Sprint 2 (Archon ready)
**Status**: ⏳ READY TO START AFTER SPRINT 2

---

## 📋 SPRINT OBJECTIVE

Integrate Renata V2 AI assistant into existing EdgeDev pages using CopilotKit v1.50, implemented as a **sidebar chat** that slides in from the right. All existing UI, functionality, and workflows remain 100% preserved.

---

## 🎯 DELIVERABLES

- [ ] CopilotKit v1.50 installed and configured
- [ ] RenataV2CopilotKit sidebar component created
- [ ] "Open Renata" button added to existing pages
- [ ] Sidebar integrated into `/scan` page (existing UI preserved)
- [ ] Sidebar integrated into `/backtest` page (existing UI preserved)
- [ ] Sidebar integrated into `/projects` page (existing UI preserved)
- [ ] Sidebar integrated into `/exec` page (existing UI preserved)
- [ ] All existing functionality tested and working
- [ ] AI agent actions registered and functional
- [ ] Archon context integrated

---

## 📊 SIDEBAR INTEGRATION DESIGN

### Visual Layout
```
┌─────────────────────────────────────────────────────────────────┐
│                    EDGE DEV /scan PAGE (PRESERVED)              │
│  ┌────────┐  ┌──────────────┐  ┌─────────────┐  [🧠 Renata]   │
│  │Symbol  │  │ Timeframes  │  │ Date Nav    │               │
│  └────────┘  └──────────────┘  └─────────────┘  <Brain Button> │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                   EdgeChart Component              │       │
│  │                   (PRESERVED AS-IS)                │       │
│  └──────────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                   Scanner Results                   │       │
│  │                   (PRESERVED AS-IS)                │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                          ↓ Click [🧠 Renata]
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR (slides in from right, 400px wide)                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ [← Close] Renata AI Assistant                              │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │  Chat Messages                                              │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │ [User] Help me build a backside B scanner         │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │ [AI] I can help with that! Let me analyze...      │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┤ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Quick Actions                                              │ │
│  │  [Generate Scanner] [Analyze Code] [Execute]         │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Input: [Type your message...]                    [Send] │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Sidebar States
1. **Closed** (default): Not visible, existing UI has full width
2. **Open**: Slides in from right, existing UI shrinks to accommodate
3. **Dismissable**: User can close with X button or click outside

---

## 📊 DETAILED TASK BREAKDOWN

### Task 3.1: Install CopilotKit Dependencies (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: None

```bash
cd projects/edge-dev-main
npm install @copilotkit/react-ui@latest @copilotkit/react-core@latest
npm install @copilotkit/runtime class-validator
```

**Subtasks**:
- [ ] Update package.json
- [ ] Run npm install
- [ ] Verify no version conflicts
- [ ] Document installed versions

**Acceptance**:
- CopilotKit packages installed
- No peer dependency warnings

---

### Task 3.2: Create CopilotKit Provider (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: Task 3.1

**Implementation** (preserve existing layout):
```typescript
// /src/app/layout.tsx
'use client';

import { CopilotKit } from '@copilotkit/react-core';
import { CopilotKitCSSProperties } from '@copilotkit/react-ui';
import React from 'react';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <title>Edge Dev - Renata V2</title>
        <CopilotKitCSSProperties />
      </head>
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

**Subtasks**:
- [ ] Add CopilotKit provider
- [ ] Add CSS properties
- [ ] Configure runtime URL
- [ ] Test app renders
- [ ] Verify no layout changes

**Acceptance**:
- App renders with provider
- No visual changes to existing layout
- No console errors

---

### Task 3.3: Create CopilotKit API Route (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: Task 3.1

```typescript
// /src/app/api/copilotkit/route.ts
import { CopilotRuntime } from '@copilotkit/runtime';
import { NextRequest } from 'next/server';

const copilotKit = new CopilotRuntime({
  apiKey: process.env.OPENROUTER_API_KEY,
  model: 'anthropic/claude-sonnet-4-5-20250514',
});

export async function POST(req: NextRequest) {
  const { messages } = await req.json();
  const response = await copilotKit.stream({ messages });

  return new Response(response.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

**Subtasks**:
- [ ] Create API route
- [ ] Configure runtime
- [ ] Test endpoint responds
- [ ] Validate streaming

**Acceptance**:
- API endpoint works
- Streaming functional

---

### Task 3.4: Create RenataV2CopilotKit Sidebar Component (8 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.1, 3.2, 3.3

**Component Structure**:
```typescript
// /src/components/renata/RenataV2Sidebar.tsx
'use client';

import React, { useState } from 'react';
import { useCopilotChat, useCopilotReadable, useCopilotAction } from '@copilotkit/react-core';
import { Brain, X, Send, Loader2, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface RenataSidebarProps {
  onScannerGenerated?: (scanner: any) => void;
  onExecutionRequested?: (executionId: string) => void;
  onCodeAnalyzed?: (analysis: any) => void;
}

export default function RenataV2Sidebar({
  onScannerGenerated,
  onExecutionRequested,
  onCodeAnalyzed
}: RenataSidebarProps) {
  const [isOpen, setIsOpen] = useState(false);

  // CopilotKit chat hook
  const {
    messages,
    appendMessage,
    setMessages,
    isLoading
  } = useCopilotChat();

  // Archon knowledge contexts
  const v31Standard = useCopilotReadable({
    description: 'V31 Gold Standard specification for scanner development',
    value: `V31 is a 3-stage grouped endpoint architecture...`
  });

  const linguaFramework = useCopilotReadable({
    description: 'Lingua trading framework for trend analysis',
    value: `Lingua defines the trend cycle as...`
  });

  // Agent actions
  useCopilotAction({
    name: 'generateScanner',
    description: 'Generate a V31-compliant scanner from user description',
    parameters: [
      { name: 'description', type: 'string', required: true, description: 'Strategy description' },
      { name: 'setupType', type: 'string', required: false, description: 'Setup type' }
    ],
    handler: async ({ description, setupType }) => {
      // Call Builder agent (to be implemented in Sprint 6)
      const scanner = await generateScannerAction({ description, setupType });
      if (onScannerGenerated) onScannerGenerated(scanner);
      return { success: true, scanner };
    }
  });

  useCopilotAction({
    name: 'executeScanner',
    description: 'Execute a scanner and return results',
    parameters: [
      { name: 'scannerCode', type: 'string', required: true },
      { name: 'scanDate', type: 'string', required: true }
    ],
    handler: async ({ scannerCode, scanDate }) => {
      const executionId = await executeScannerAction({ scannerCode, scanDate });
      if (onExecutionRequested) onExecutionRequested(executionId);
      return { success: true, executionId };
    }
  });

  // If closed, don't render content
  if (!isOpen) return null;

  return (
    <div className="renata-sidebar-overlay" onClick={() => setIsOpen(false)}>
      <div
        className="renata-sidebar"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="renata-sidebar-header">
          <div className="renata-title">
            <Brain className="brain-icon" />
            <h3>Renata AI Assistant</h3>
          </div>
          <button
            className="close-button"
            onClick={() => setIsOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        {/* Messages */}
        <div className="renata-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                {message.role === 'assistant' ? (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                ) : (
                  <p>{message.content}</p>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <Loader2 className="spinner" size={16} />
                <span>Renata is thinking...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="renata-input">
          <textarea
            value={currentInput}
            onChange={(e) => setCurrentInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                appendMessage(currentInput);
                setCurrentInput('');
              }
            }}
            placeholder="Ask Renata to help build your strategy..."
            rows={3}
            autoFocus
          />
          <button
            onClick={() => {
              appendMessage(currentInput);
              setCurrentInput('');
            }}
            disabled={isLoading || !currentInput.trim()}
            className="send-button"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
```

**Subtasks**:
- [ ] Create sidebar component structure
- [ ] Implement open/close state
- [ ] Implement useCopilotChat hook
- [ ] Add useCopilotReadable contexts
- [ ] Register generateScanner action
- [ ] Register executeScanner action
- [ ] Register analyzeCode action
- [ ] Register convertToV31 action
- [ ] Add sidebar styling (slide-in animation)
- [ ] Test sidebar opens/closes
- [ ] Test overlay click to close

**Files to Create**:
- `/src/components/renata/RenataV2Sidebar.tsx`
- `/src/components/renata/RenataV2Sidebar.module.css`

**Acceptance**:
- Sidebar component renders
- Slide-in animation works
- Chat interface functional
- Agent actions registered

---

### Task 3.5: Create "Open Renata" Button Component (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 3.4

**Button Component**:
```typescript
// /src/components/renata/OpenRenataButton.tsx
'use client';

import { Brain, X } from 'lucide-react';
import { useState } from 'react';
import RenataV2Sidebar from './RenataV2Sidebar';

export default function OpenRenataButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        className="open-renata-button"
        onClick={() => setIsOpen(true)}
        title="Open Renata AI Assistant"
      >
        <Brain className="brain-icon" size={20} />
        <span className="button-text">Renata AI</span>
      </button>

      {isOpen && (
        <RenataV2Sidebar
          isOpen={isOpen}
          onClose={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
```

**Styling** (button in existing UI, non-intrusive):
```css
.open-renata-button {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;

  display: flex;
  align-items: center;
  gap: 8px;

  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.open-renata-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

.brain-icon {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

**Subtasks**:
- [ ] Create button component
- [ ] Style as floating button
- [ ] Add pulse animation to brain icon
- [ ] Test button visibility
- [ ] Test button click opens sidebar
- [ ] Ensure button doesn't overlap important UI elements

**Files to Create**:
- `/src/components/renata/OpenRenataButton.tsx`

**Acceptance**:
- Button visible on all pages
- Non-intrusive to existing UI
- Click opens sidebar
- Animation subtle but noticeable

---

### Task 3.6: Integrate Sidebar into /scan Page (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.4, 3.5

**Integration** (preserve existing scan page):
```typescript
// /src/app/scan/page.tsx

// Near top of file, add import:
import OpenRenataButton from '@/components/renata/OpenRenataButton';

// In main component, add button (WITHOUT changing existing layout):
export default function ScanPage() {
  // ... existing state and logic ...

  return (
    <div className="scan-page-container">
      {/* EXISTING UI - PRESERVE COMPLETELY */}
      <div className="scan-controls">
        {/* Existing scan controls */}
      </div>

      <EdgeChart />

      {/* NEW: Add Renata button */}
      <OpenRenataButton />

      {/* Rest of existing scan page */}
      <ScannerResults />

      {/* ... rest of existing scan page ... */}
    </div>
  );
}
```

**Subtasks**:
- [ ] Import OpenRenataButton component
- [ ] Add button to scan page
- [ ] Position button (doesn't overlap elements)
- [ ] Test existing scan functionality unchanged
- [ ] Test Renata button opens sidebar
- [ ] Test existing chart display unchanged

**Acceptance**:
- Scan page looks identical to before
- All scan features work as before
- Renata button visible and functional
- Sidebar opens and closes properly

---

### Task 3.7: Integrate Sidebar into /backtest Page (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.4, 3.5

**Integration** (preserve existing backtest page):
```typescript
// /src/app/backtest/page.tsx

import OpenRenataButton from '@/components/renata/OpenRenataButton';

export default function BacktestPage() {
  // ... existing state and logic ...

  return (
    <div className="backtest-page-container">
      {/* EXISTING UI - PRESERVE COMPLETELY */}
      <div className="backtest-controls">
        {/* Existing backtest controls */}
      </div>

      <EdgeChart />

      {/* NEW: Add Renata button */}
      <OpenRenataButton />

      {/* Rest of existing backtest page */}
      <BacktestResults />

      {/* ... rest of existing backtest page ... */}
    </div>
  );
}
```

**Subtasks**:
- [ ] Import OpenRenataButton component
- [ ] Add button to backtest page
- [ ] Position button appropriately
- [ ] Test existing backtest functionality unchanged
- [ ] Test Renata button works
- [ ] Test existing chart display unchanged

**Acceptance**:
- Backtest page looks identical to before
- All backtest features work as before
- Renata button visible and functional

---

### Task 3.8: Integrate Sidebar into /projects Page (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: Tasks 3.4, 3.5

**Integration** (preserve existing projects page):
```typescript
// /src/app/projects/page.tsx

import OpenRenataButton from '@/components/renata/OpenRenataButton';

export default function ProjectsPage() {
  // ... existing state and logic ...

  return (
    <div className="projects-page-container">
      {/* EXISTING UI - PRESERVE COMPLETELY */}
      <div className="projects-header">
        {/* Existing project controls */}
      </div>

      <ProjectList />

      {/* NEW: Add Renata button */}
      <OpenRenataButton />

      {/* Rest of existing projects page */}
      <ProjectDetails />

      {/* ... rest of existing projects page ... */}
    </div>
  );
}
```

**Subtasks**:
- [ ] Import OpenRenataButton component
- [ ] Add button to projects page
- [ ] Test existing project management unchanged
- [ ] Test Renata button works
- [ ] Test existing UI unchanged

**Acceptance**:
- Projects page looks identical to before
- All project features work as before
- Renata button visible and functional

---

### Task 3.9: Integrate Sidebar into /exec Page (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: Tasks 3.4, 3.5

**Integration** (preserve existing exec page):
```typescript
// /src/app/exec/page.tsx

import OpenRenataButton from '@/components/renata/OpenRenataButton';

export default function ExecPage() {
  // ... existing state and logic ...

  return (
    <div className="exec-page-container">
      {/* EXISTING UI - PRESERVE COMPLETELY */}
      <div className="exec-controls">
        {/* Existing execution controls */}
      </div>

      <ExecutionChart />

      {/* NEW: Add Renata button */}
      <OpenRenataButton />

      {/* Rest of existing exec page */}
      <ExecutionStats />

      {/* ... rest of existing exec page ... */}
    </div>
  );
}
```

**Subtasks**:
- [ ] Import OpenRenataButton component
- [ ] Add button to exec page
- [ ] Test existing execution functionality unchanged
- [ ] Test Renata button works
- [ ] Test existing UI unchanged

**Acceptance**:
- Exec page looks identical to before
- All execution features work as before
- Renata button visible and functional

---

### Task 3.10: Comprehensive UI Testing (4 hours)
**Owner**: Michael Durante + CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.6-3.9

**Objective**: Validate existing UI completely preserved.

**Test Matrix**:

| Page | Feature | Test | Expected Result |
|------|---------|------|----------------|
| /scan | Chart display | ✅ | Chart loads and displays |
| /scan | Scanner selector | ✅ | Can select scanners |
| /scan | Results table | ✅ | Results display correctly |
| /scan | Date navigation | ✅ | Day offset works |
| /scan | **Renata button** | ✅ | Button visible |
| /scan | **Sidebar opens** | ✅ | Sidebar slides in |
| /backtest | Chart display | ✅ | Chart loads and displays |
| /backtest | Backtest controls | ✅ | Controls work |
| /backtest | Results display | ✅ | Results show correctly |
| /backtest | **Renata button** | ✅ | Button visible |
| /backtest | **Sidebar opens** | ✅ | Sidebar slides in |
| /projects | Project list | ✅ | Projects display |
| /projects | Project CRUD | ✅ | Can manage projects |
| /projects | **Renata button** | ✅ | Button visible |
| /projects | **Sidebar opens** | ✅ | Sidebar slides in |
| /exec | Execution chart | ✅ | Chart displays |
| /exec | Execution stats | ✅ | Stats show correctly |
| /exec | **Renata button** | ✅ | Button visible |
| /exec | **Sidebar opens** | ✅ | Sidebar slides in |

**Subtasks**:
- [ ] Test all /scan page features
- [ ] Test all /backtest page features
- [ ] Test all /projects page features
- [ ] Test all /exec page features
- [ ] Test Renata button on all pages
- [ ] Test sidebar opens on all pages
- [ ] Test sidebar closes properly
- [ ] Test overlay click closes sidebar
- [ ] Take screenshots before/after for comparison
- [ ] Document any visual differences

**Output**: `/Users/michaeldurante/ai dev/ce-hub/projects/edge-dev-main/RENATA_V2_2026/SPRINT_3_TEST_RESULTS.md`

**Acceptance**:
- All existing features working
- No visual regressions
- Sidebar integration works seamlessly
- Ready for agent action development

---

### Task 3.11: Implement Agent Action Handlers (6 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 3.4

**Actions to Implement** (temporary implementations, enhanced in later sprints):

**1. generateScanner** (calls existing formatter, enhanced in Sprint 6):
```typescript
async function generateScannerAction(params: {
  description: string;
  setupType?: string;
}): Promise<{ scanner: string; metadata: any }> {
  // TEMPORARY: Use existing code formatter
  const response = await fetch('/api/format/generate-from-description', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: params.description })
  });
  return response.json();
}
```

**2. executeScanner** (direct backend call, enhanced in Sprint 7):
```typescript
async function executeScannerAction(params: {
  scannerCode: string;
  scanDate: string;
}): Promise<{ executionId: string }> {
  const response = await fetch('http://localhost:8000/api/scan/execute', {
    method: 'POST',
    headers: { { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      scanner_code: params.scannerCode,
      scan_date: params.scanDate
    })
  });
  return response.json();
}
```

**3. analyzeCode** (existing analyzer, enhanced in Sprint 5):
```typescript
async function analyzeCodeAction(params: {
  code: string;
}): Promise<{ analysis: any }> {
  const response = await fetch('/api/format/analyze-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: params.code })
  });
  return response.json();
}
```

**4. convertToV31** (existing formatter, enhanced in Sprint 6):
```typescript
async function convertToV31Action(params: {
  code: string;
  sourceFormat?: string;
}): Promise<{ convertedCode: string }> {
  const response = await fetch('/api/format/code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code: params.code,
      target_format: 'v31'
    })
  });
  return response.json();
}
```

**Subtasks**:
- [ ] Create agentActions service file
- [ ] Implement generateScanner handler
- [ ] Implement executeScanner handler
- [ ] Implement analyzeCode handler
- [ ] Implement convertToV31 handler
- [ ] Add error handling
- [ ] Add TypeScript types
- [ ] Test all actions
- [ ] Document which actions are temporary

**Files to Create**:
- `/src/services/renata/agentActions.ts`

**Acceptance**:
- All actions functional
- Actions integrate with CopilotKit
- Temporary implementations marked for future enhancement

---

### Task 3.12: Load Archon Knowledge into Sidebar (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Sprint 2 (Archon ready), Task 3.4

**Implementation**:
```typescript
// In RenataV2Sidebar component

useEffect(() => {
  // Load V31 knowledge from Archon
  const loadV31Knowledge = async () => {
    const response = await fetch('http://localhost:8051/rag_search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'V31 Gold Standard overview',
        domain: 'v31_spec',
        limit: 1
      })
    });
    const data = await response.json();
    if (data.results && data.results.length > 0) {
      setV31Knowledge(data.results[0].content);
    }
  };

  // Load Lingua knowledge from Archon
  const loadLinguaKnowledge = async () => {
    const response = await fetch('http://localhost:8051/rag_search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'Lingua trading framework overview',
        domain: 'lingua_framework',
        limit: 1
      })
    });
    const data = await response.json();
    if (data.results && data.results.length > 0) {
      setLinguaKnowledge(data.results[0].content);
    }
  };

  loadV31Knowledge();
  loadLinguaKnowledge();
}, []);
```

**Subtasks**:
- [ ] Fetch V31 knowledge from Archon
- [ ] Fetch Lingua knowledge from Archon
- [ ] Make available via useCopilotReadable
- [ ] Test AI can access V31 in responses
- [ ] Test AI can access Lingua in responses
- [ ] Handle Archon connection errors gracefully

**Acceptance**:
- Archon knowledge loads into sidebar
- AI can reference V31 in chat
- AI can reference Lingua in chat
- Fallback if Archon unavailable

---

### Task 3.13: Test CopilotKit Chat Functionality (3 hours)
**Owner**: Michael Durante + CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.1-3.12

**Test Cases**:

**Test Case 1: Basic Chat**
1. Open /scan page
2. Click "Renata AI" button
3. Verify sidebar slides in from right
4. Type: "Hello Renata"
5. Verify response received
6. Verify response displays
7. Click X to close
8. Verify sidebar closes

**Test Case 2: Agent Action - generateScanner**
1. Open Renata sidebar
2. Type: "Generate a backside B scanner"
3. Verify AI requests parameters if needed
4. Provide parameters
5. Verify scanner generated
6. Verify code is V31 compliant
7. Verify can add scanner to results

**Test Case 3: Agent Action - executeScanner**
1. Generate or upload scanner
2. Request: "Execute this scanner"
3. Verify execution starts
4. Verify progress updates
5. Verify results displayed

**Test Case 4: Context Awareness**
1. Ask: "What is V31?"
2. Verify AI explains using Archon knowledge
3. Ask: "What is Lingua?"
4. Verify AI explains using Archon knowledge

**Test Case 5: UI Preservation**
1. Navigate to /scan
2. Verify chart works
3. Verify results table works
4. Open Renata sidebar
5. Verify chart still works behind sidebar
6. Close Renata sidebar
7. Verify chart still works

**Subtasks**:
- [ ] Test Case 1: Basic chat
- [ ] Test Case 2: generateScanner action
- [ ] Test Case 3: executeScanner action
- [ ] Test Case 4: Context awareness
- [ ] Test Case 5: UI preservation
- [ ] Document test results
- [ ] Fix any issues found
- [ ] Re-test until all pass

**Output**: Update `SPRINT_3_TEST_RESULTS.md`

**Acceptance**:
- All test cases pass
- Sidebar integration seamless
- Existing UI 100% functional
- Agent actions working
- Ready for specialized agents (Sprint 4-8)

---

## 📊 TIME ESTIMATE SUMMARY

| Task | Estimate | Owner |
|------|----------|-------|
| 3.1: Install dependencies | 2 hours | CE-Hub |
| 3.2: Create provider | 2 hours | CE-Hub |
| 3.3: Create API route | 2 hours | CE-Hub |
| 3.4: Create sidebar component | 8 hours | CE-Hub |
| 3.5: Create button component | 2 hours | CE-Hub |
| 3.6: Integrate into /scan | 2 hours | CE-Hub |
| 3.3: Integrate into /backtest | 2 hours | CE-Hub |
| 3.8: Integrate into /projects | 2 hours | CE-Hub |
| 3.9: Integrate into /exec | 2 hours | CE-Hub |
| 3.10: UI testing | 4 hours | Both |
| 3.11: Agent actions | 6 hours | CE-Hub |
| 3.12: Archon knowledge | 4 hours | CE-Hub |
| 3.13: Chat testing | 3 hours | Both |
| **TOTAL** | **43 hours (~6 days)** | |

**Sprint Buffer**: Add 8-12 hours for unknowns = ~7 days (1 week)

**Actual Duration**: Weeks 3-4 (14 days) allows for parallel work and buffer

---

## ✅ SPRINT VALIDATION GATE

Sprint 3 is complete when:
- [ ] CopilotKit installed and configured
- [ ] RenataV2Sidebar component created
- [ ] "Open Renata" button added to all pages
- [ ] Sidebar integrated into /scan (UI preserved)
- [ ] Sidebar integrated into /backtest (UI preserved)
- [ ] Sidebar integrated into /projects (UI preserved)
- [ ] Sidebar integrated into /exec (UI preserved)
- [ ] All existing functionality tested and working
- [ ] Agent actions registered and functional
- [ ] Archon knowledge integrated
- [ ] All test cases pass
- [ ] No breaking changes to current platform

**Final Validation**:
User opens /scan page → everything works as before → clicks "Renata AI" → sidebar slides in → chats with Renata → generates scanner → executes it → sees results → closes sidebar → everything still works.

---

## 🚨 RISKS & MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Sidebar overlaps important UI | Medium | Medium | Careful positioning, make dismissible |
| Performance degradation | Low | Medium | Monitor page load times |
| Existing functionality breaks | Low | High | Comprehensive testing, easy rollback |
| CopilotKit integration issues | Medium | High | Keep old component as fallback |

**Rollback Plan**:
If CopilotKit integration breaks existing UI, revert to RenataV2Chat with sidebar wrapper instead.

---

## 🎯 SUCCESS CRITERIA

Sprint 3 Success means:
- ✅ Existing EdgeDev UI 100% preserved
- ✅ All existing features work exactly as before
- ✅ Sidebar chat adds AI capabilities
- ✅ Non-intrusive integration (can close sidebar)
- ✅ Agent actions functional
- ✅ Archon knowledge available to AI
- ✅ Clean foundation for specialized agents (Sprints 4-8)

---

## 📝 NOTES

- **SIDEBAR APPROACH**: Non-intrusive, can be dismissed
- **UI PRESERVATION**: #1 priority - protect existing functionality
- **PROGRESSIVE ENHANCEMENT**: Agent actions will be enhanced in future sprints
- **TEST THOROUGHLY**: Validate existing UI after every change
- **FALLBACK READY**: Can rollback if needed

---

**Sprint 3 adds AI intelligence to your existing platform without breaking what works.**

**Sidebar approach ensures you can use Renata when needed, ignore it when not.**

**Your workflow, your UI, your control - enhanced with AI, not replaced.**
