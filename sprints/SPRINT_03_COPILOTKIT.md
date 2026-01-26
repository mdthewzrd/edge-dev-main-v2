# 🤖 SPRINT 3: COPILOTKIT FOUNDATION
## Renata Multi-Agent System Rebuild

**Duration**: Weeks 3-4 (14 days)
**Objective**: Rebuild Renata with CopilotKit v1.50, install AG-UI protocol
**Dependencies**: Sprint 1 (Platform stable), Sprint 2 (Archon ready)
**Status**: ⏳ READY TO START AFTER SPRINT 2

---

## 📋 SPRINT OBJECTIVE

Replace the existing RenataV2Chat component with a production-grade CopilotKit v1.50 implementation. This rebuild provides:
- Clean AG-UI protocol compliance
- Better agent state management
- Improved message history
- Standardized agent actions
- Future-proof architecture

This is a **complete rebuild** of the Renata interface, not an enhancement.

---

## 🎯 DELIVERABLES

- [ ] CopilotKit v1.50 installed and configured
- [ ] AG-UI protocol integrated
- [ ] New Renata chat interface built
- [ ] Multi-agent actions registered
- [ ] Message history management
- [ ] Archon integration points created
- [ ] Old RenataV2Chat deprecated

---

## 📊 DETAILED TASK BREAKDOWN

### Task 3.1: Install CopilotKit Dependencies (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: None

**Commands**:
```bash
cd projects/edge-dev-main

# Install CopilotKit packages
npm install @copilotkit/react-ui@latest @copilotkit/react-core@latest
npm install @copilotkit/runtime class-validator

# Install required peer dependencies
npm install react@^18.2.0
npm install @types/react@^18.2.0
```

**Subtasks**:
- [ ] Update package.json with CopilotKit packages
- [ ] Run npm install
- [ ] Verify no version conflicts
- [ ] Check for peer dependency warnings
- [ ] Document versions installed

**Acceptance Criteria**:
- CopilotKit packages installed without errors
- No version conflicts
- All peer dependencies satisfied

---

### Task 3.2: Create CopilotKit Provider (3 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: Task 3.1

**Objective**:
Wrap the EdgeDev app with CopilotKit provider for agent functionality.

**Implementation**:
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
- [ ] Update layout.tsx with CopilotKit provider
- [ ] Add CopilotKitCSSProperties
- [ ] Configure runtime URL
- [ ] Test app still renders
- [ ] Verify no console errors

**Files to Modify**:
- `/src/app/layout.tsx`

**Acceptance Criteria**:
- CopilotKit wraps entire app
- App renders without errors
- Provider configuration correct

---

### Task 3.3: Create CopilotKit API Route (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: CRITICAL
**Dependencies**: Task 3.1

**Objective**:
Create Next.js API route that acts as CopilotKit runtime.

**Implementation**:
```typescript
// /src/app/api/copilotkit/route.ts
import { CopilotRuntime } from '@copilotkit/runtime';
import { NextRequest } from 'next/server';

const copilotKit = new CopilotRuntime({
  // Your API keys for AI model
  apiKey: process.env.OPENROUTER_API_KEY,

  // Configure model
  model: 'anthropic/claude-sonnet-4-5-20250514',

  // Or use OpenRouter for model access
  // endpoint: 'https://openrouter.ai/api/v1'
});

export async function POST(req: NextRequest) {
  const { messages } = await req.json();

  const response = await copilotKit.stream({
    messages,
  });

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
- [ ] Create /api/copilotkit/route.ts
- [ ] Configure CopilotKit runtime
- [ ] Add API key configuration
- [ ] Configure model (Claude Sonnet via OpenRouter)
- [ ] Test endpoint responds
- [ ] Validate streaming works

**Files to Create**:
- `/src/app/api/copilotkit/route.ts`

**Acceptance Criteria**:
- API endpoint responds to POST requests
- Streaming responses work
- No CORS errors
- API keys properly configured

---

### Task 3.4: Create Unified Renata Component (6 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.1, 3.2, 3.3

**Objective**:
Build new Renata chat interface using CopilotKit hooks, replacing RenataV2Chat.

**Architecture**:
```typescript
// /src/components/renata/RenataV2CopilotKit.tsx
'use client';

import React, { useState } from 'react';
import { useCopilotChat, useCopilotReadable, useCopilotAction } from '@copilotkit/react-core';
import { Brain, Send, Upload, Loader2 } from 'lucide-react';

interface RenataV2Props {
  onScannerGenerated?: (scanner: any) => void;
  onExecutionRequested?: (scannerId: string) => void;
}

export default function RenataV2CopilotKit({
  onScannerGenerated,
  onExecutionRequested
}: RenataV2Props) {
  // CopilotKit chat interface
  const {
    messages,
    appendMessage,
    setMessages,
    isLoading
  } = useCopilotChat();

  // Register context for AI to read
  const v31Standard = useCopilotReadable({
    description: 'V31 Gold Standard specification for scanner development',
    value: 'V31 is a 3-stage grouped endpoint architecture...'
  });

  const linguaFramework = useCopilotReadable({
    description: 'Lingua trading framework for trend analysis',
    value: 'Lingua defines the trend cycle as...'
  });

  // Register actions for AI to call
  useCopilotAction({
    name: 'generateScanner',
    description: 'Generate a V31-compliant scanner from user description',
    parameters: [
      {
        name: 'description',
        type: 'string',
        description: 'Natural language description of the strategy',
        required: true
      },
      {
        name: 'setupType',
        type: 'string',
        description: 'Type of setup (e.g., backside_b, lc_d2, etc.)',
        required: false
      }
    ],
    handler: async ({ description, setupType }) => {
      // Call Builder agent
      const scanner = await callBuilderAgent({ description, setupType });

      if (onScannerGenerated) {
        onScannerGenerated(scanner);
      }

      return {
        success: true,
        scanner
      };
    }
  });

  useCopilotAction({
    name: 'executeScanner',
    description: 'Execute a scanner and return results',
    parameters: [
      {
        name: 'scannerCode',
        type: 'string',
        description: 'V31 scanner Python code',
        required: true
      },
      {
        name: 'scanDate',
        type: 'string',
        description: 'Scan date (YYYY-MM-DD)',
        required: true
      }
    ],
    handler: async ({ scannerCode, scanDate }) => {
      // Call Executor agent
      const executionId = await callExecutorAgent({ scannerCode, scanDate });

      if (onExecutionRequested) {
        onExecutionRequested(executionId);
      }

      return {
        success: true,
        executionId
      };
    }
  });

  return (
    <div className="renata-v2-container">
      <div className="renata-header">
        <Brain className="brain-icon" />
        <h2>Renata V2 - AI Trading Assistant</h2>
      </div>

      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="loading-indicator">
            <Loader2 className="spinner" />
            <span>Renata is thinking...</span>
          </div>
        )}
      </div>

      <div className="input-container">
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
          placeholder="Describe your strategy or upload code..."
          rows={3}
        />

        <button
          onClick={() => {
            appendMessage(currentInput);
            setCurrentInput('');
          }}
          disabled={isLoading || !currentInput.trim()}
        >
          <Send className="send-icon" />
        </button>
      </div>
    </div>
  );
}
```

**Subtasks**:
- [ ] Create component structure
- [ ] Implement useCopilotChat hook
- [ ] Add useCopilotReadable contexts (V31, Lingua)
- [ ] Register generateScanner action
- [ ] Register executeScanner action
- [ ] Add analyzeCode action
- [ ] Add convertToV31 action
- [ ] Add optimizeParameters action
- [ ] Style component (match existing design)
- [ ] Test chat interface
- [ ] Test agent actions

**Files to Create**:
- `/src/components/renata/RenataV2CopilotKit.tsx`
- `/src/components/renata/RenataV2CopilotKit.module.css`

**Acceptance Criteria**:
- Component renders without errors
- Chat interface functional
- Messages display correctly
- Agent actions registered
- Can send and receive messages

---

### Task 3.5: Implement Agent Action Handlers (8 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 3.4

**Objective**:
Create handler functions for all agent actions. These will call the backend services (to be built in future sprints).

**Actions to Implement**:

**1. generateScanner Action**
```typescript
// /src/services/renata/agentActions.ts
export async function generateScannerAction(params: {
  description: string;
  setupType?: string;
}): Promise<{ scanner: string; metadata: any }> {
  // TEMPORARY: Call existing code formatter
  // In Sprint 6, this will call Builder Agent

  const response = await fetch('/api/format/generate-from-description', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      description: params.description,
      setup_type: params.setupType
    })
  });

  if (!response.ok) {
    throw new Error('Scanner generation failed');
  }

  return response.json();
}
```

**2. executeScanner Action**
```typescript
export async function executeScannerAction(params: {
  scannerCode: string;
  scanDate: string;
}): Promise<{ executionId: string }> {
  // TEMPORARY: Direct backend call
  // In Sprint 7, this will call Executor Agent

  const response = await fetch('http://localhost:8000/api/scan/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      scanner_code: params.scannerCode,
      scan_date: params.scanDate
    })
  });

  if (!response.ok) {
    throw new Error('Scanner execution failed');
  }

  return response.json();
}
```

**3. analyzeCode Action**
```typescript
export async function analyzeCodeAction(params: {
  code: string;
}): Promise<{ analysis: any; v31Compliant: boolean }> {
  // TEMPORARY: Use existing validator
  // In Sprint 5, this will use Archon RAG

  const response = await fetch('/api/format/analyze-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: params.code })
  });

  return response.json();
}
```

**4. convertToV31 Action**
```typescript
export async function convertToV31Action(params: {
  code: string;
  sourceFormat?: string;
}): Promise<{ convertedCode: string; changes: string[] }> {
  // TEMPORARY: Use existing formatter
  // In Sprint 6, this will call Builder Agent with V31 validation

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

**5. optimizeParameters Action**
```typescript
export async function optimizeParametersAction(params: {
  scannerCode: string;
  results: any[];
}): Promise<{ optimizations: any[] }> {
  // TEMPORARY: Return placeholder
  // In Sprint 8, this will call Analyst Agent

  // Will be implemented in Sprint 8
  return {
    optimizations: [
      {
        parameter: 'gap_over_atr',
        current_value: 0.75,
        suggested_value: 0.80,
        reason: 'Improves signal quality'
      }
    ]
  };
}
```

**Subtasks**:
- [ ] Create agentActions.ts service file
- [ ] Implement generateScanner handler
- [ ] Implement executeScanner handler
- [ ] Implement analyzeCode handler
- [ ] Implement convertToV31 handler
- [ ] Implement optimizeParameters handler
- [ ] Add error handling
- [ ] Add TypeScript types
- [ ] Test all actions
- [ ] Document action signatures

**Files to Create**:
- `/src/services/renata/agentActions.ts`
- `/src/services/renata/types.ts`

**Acceptance Criteria**:
- All actions implemented
- TypeScript types complete
- Error handling working
- Actions can be called from CopilotKit
- Test actions return expected responses

---

### Task 3.6: Integrate Archon Context Providers (4 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Sprint 2 (Archon ready), Task 3.4

**Objective**:
Make Archon knowledge available to AI agents through CopilotKit readable contexts.

**Implementation**:
```typescript
// /src/components/renata/RenataV2CopilotKit.tsx (enhanced)

export default function RenataV2CopilotKit(props: RenataV2Props) {
  // Fetch knowledge from Archon
  const [v31Knowledge, setV31Knowledge] = useState('');
  const [linguaKnowledge, setLinguaKnowledge] = useState('');
  const [strategies, setStrategies] = useState([]);

  useEffect(() => {
    // Load V31 knowledge from Archon
    fetch('http://localhost:8051/rag_search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'V31 Gold Standard overview',
        domain: 'v31_spec',
        limit: 1
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.results && data.results.length > 0) {
          setV31Knowledge(data.results[0].content);
        }
      });

    // Load Lingua knowledge from Archon
    fetch('http://localhost:8051/rag_search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'Lingua trading framework overview',
        domain: 'lingua_framework',
        limit: 1
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.results && data.results.length > 0) {
          setLinguaKnowledge(data.results[0].content);
        }
      });
  }, []);

  // Make knowledge available to AI
  const v31Context = useCopilotReadable({
    description: 'V31 Gold Standard - Complete specification for scanner development',
    value: v31Knowledge
  });

  const linguaContext = useCopilotReadable({
    description: 'Lingua Trading Framework - Michael Durante trend analysis system',
    value: linguaKnowledge
  });

  const strategiesContext = useCopilotReadable({
    description: 'Existing systematized strategies - 4 working implementations',
    value: JSON.stringify(strategies)
  });

  // ... rest of component
}
```

**Subtasks**:
- [ ] Add Archon knowledge fetching
- [ ] Create useCopilotReadable contexts
- [ ] Implement V31 knowledge provider
- [ ] Implement Lingua knowledge provider
- [ ] Implement strategies knowledge provider
- [ ] Test knowledge availability in chat
- [ ] Validate AI can access contexts

**Acceptance Criteria**:
- Archon knowledge fetched on component mount
- Knowledge available through useCopilotReadable
- AI can reference V31 in responses
- AI can reference Lingua in responses
- AI can reference existing strategies

---

### Task 3.7: Create Chat History Management (3 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: MEDIUM
**Dependencies**: Task 3.4

**Objective**:
Implement conversation history storage and retrieval for improved AI interactions.

**Implementation**:
```typescript
// /src/utils/renataChatHistory.ts (enhanced for CopilotKit)

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatConversation {
  id: string;
  name: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

const STORAGE_KEY = 'renata_v2_conversations';

export function saveConversation(
  conversationId: string,
  messages: ChatMessage[]
): void {
  const conversations = loadAllConversations();

  const existingIndex = conversations.findIndex(c => c.id === conversationId);

  if (existingIndex >= 0) {
    conversations[existingIndex] = {
      ...conversations[existingIndex],
      messages,
      updatedAt: new Date()
    };
  } else {
    conversations.push({
      id: conversationId,
      name: generateConversationName(messages),
      messages,
      createdAt: new Date(),
      updatedAt: new Date()
    });
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
}

export function loadConversation(conversationId: string): ChatConversation | null {
  const conversations = loadAllConversations();
  return conversations.find(c => c.id === conversationId) || null;
}

export function loadAllConversations(): ChatConversation[] {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? JSON.parse(stored) : [];
}

function generateConversationName(messages: ChatMessage[]): string {
  const firstUserMessage = messages.find(m => m.role === 'user');
  if (firstUserMessage) {
    const content = firstUserMessage.content;
    return content.slice(0, 50) + (content.length > 50 ? '...' : '');
  }
  return `New Conversation ${new Date().toLocaleDateString()}`;
}
```

**Integration with CopilotKit**:
```typescript
// In RenataV2CopilotKit component
const [currentConversationId, setCurrentConversationId] = useState<string>();

// Load conversation on mount
useEffect(() => {
  const conversation = loadConversation(currentConversationId);
  if (conversation) {
    setMessages(conversation.messages);
  }
}, [currentConversationId]);

// Save messages on change
useEffect(() => {
  if (currentConversationId && messages.length > 0) {
    saveConversation(currentConversationId, messages);
  }
}, [messages, currentConversationId]);
```

**Subtasks**:
- [ ] Enhance chat history utilities
- [ ] Add conversation ID generation
- [ ] Integrate with CopilotKit messages
- [ ] Add conversation switching
- [ ] Add new conversation button
- [ ] Add conversation naming
- [ ] Test history persistence

**Acceptance Criteria**:
- Conversations persist across page refreshes
- Can switch between conversations
- Can create new conversations
- Conversations have meaningful names
- History doesn't grow unbounded (limit to 50 messages)

---

### Task 3.8: Replace RenataV2Chat in Pages (2 hours)
**Owner**: CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Task 3.4

**Objective**:
Replace old RenataV2Chat component with new RenataV2CopilotKit in all pages.

**Pages to Update**:
- `/src/app/scan/page.tsx`
- `/src/app/backtest/page.tsx`
- `/src/app/exec/page.tsx`
- `/src/app/projects/page.tsx`

**Implementation** (per page):
```typescript
// OLD:
import RenataV2Chat from '@/components/renata/RenataV2Chat';

// NEW:
import RenataV2CopilotKit from '@/components/renata/RenataV2CopilotKit';

// In component:
<RenataV2CopilotKit
  onScannerGenerated={(scanner) => {
    // Handle generated scanner
    setGeneratedScanner(scanner);
  }}
  onExecutionRequested={(executionId) => {
    // Handle execution request
    setExecutionId(executionId);
  }}
/>
```

**Subtasks**:
- [ ] Update /scan/page.tsx
- [ ] Update /backtest/page.tsx
- [ ] Update /exec/page.tsx
- [ ] Update /projects/page.tsx
- [ ] Test each page
- [ ] Verify no console errors
- [ ] Verify chat interface works

**Acceptance Criteria**:
- All pages use new component
- Old component deprecated
- Chat interface functional on all pages
- No breaking changes to existing functionality

---

### Task 3.9: Deprecate Old RenataV2Chat (1 hour)
**Owner**: CE-Hub Orchestrator
**Priority**: LOW
**Dependencies**: Task 3.8

**Objective**:
Mark old RenataV2Chat as deprecated and document migration.

**Actions**:
```typescript
// /src/components/renata/RenataV2Chat.tsx (add deprecation notice)

/**
 * @deprecated Use RenataV2CopilotKit instead
 *
 * This component is deprecated and will be removed in Sprint 5.
 * Please migrate to RenataV2CopilotKit for continued support.
 *
 * Migration guide:
 * 1. Import RenataV2CopilotKit from '@/components/renata/RenataV2CopilotKit'
 * 2. Replace <RenataV2Chat /> with <RenataV2CopilotKit />
 * 3. Remove any custom props not supported by new component
 *
 * @see RenataV2CopilotKit
 */
export default function RenataV2Chat({ /* ... */ }) {
  console.warn('RenataV2Chat is deprecated. Use RenataV2CopilotKit instead.');

  // ... existing code
}
```

**Subtasks**:
- [ ] Add deprecation notice to RenataV2Chat
- [ ] Create migration documentation
- [ ] Add TODO comment for removal in Sprint 5
- [ ] Document breaking changes
- [ ] Update component exports

**Output**: `/Users/michaeldurante/ai dev/ce-hub/projects/edge-dev-main/RENATA_V2_2026/MIGRATION_GUIDE.md`

**Acceptance Criteria**:
- Deprecation notice visible
- Migration guide created
- Removal scheduled for Sprint 5

---

### Task 3.10: Test CopilotKit Integration (4 hours)
**Owner**: Michael Durante + CE-Hub Orchestrator
**Priority**: HIGH
**Dependencies**: Tasks 3.1-3.9

**Objective**:
Comprehensive testing of new CopilotKit-based Renata interface.

**Test Cases**:

**Test Case 1: Basic Chat**
1. Open /scan page
2. Type message in chat: "Hello Renata"
3. Verify response received
4. Verify response displayed
5. Verify no console errors

**Test Case 2: Agent Action - generateScanner**
1. Type: "Generate a backside B scanner"
2. Verify AI requests parameters
3. Provide parameters
4. Verify scanner generated
5. Verify code is V31 compliant

**Test Case 3: Agent Action - executeScanner**
1. Upload or generate scanner
2. Request execution
3. Verify execution starts
4. Verify progress updates
5. Verify results displayed

**Test Case 4: Context Awareness**
1. Ask: "What is V31?"
2. Verify AI explains V31 using Archon knowledge
3. Ask: "What is Lingua?"
4. Verify AI explains Lingua framework

**Test Case 5: Chat History**
1. Have conversation
2. Refresh page
3. Verify conversation restored
4. Create new conversation
5. Verify can switch between conversations

**Test Case 6: Error Handling**
1. Send malformed request
2. Verify graceful error message
3. Verify no crash
4. Verify can continue chatting

**Subtasks**:
- [ ] Test Case 1: Basic chat
- [ ] Test Case 2: generateScanner action
- [ ] Test Case 3: executeScanner action
- [ ] Test Case 4: Context awareness
- [ ] Test Case 5: Chat history
- [ ] Test Case 6: Error handling
- [ ] Document test results
- [ ] Fix any critical issues
- [ ] Re-test until all pass

**Output**: `/Users/michaeldurante/ai dev/ce-hub/projects/edge-dev-main/RENATA_V2_2026/SPRINT_3_TEST_RESULTS.md`

**Acceptance Criteria**:
- All test cases pass
- No critical bugs
- Chat interface stable
- Agent actions working
- Ready to proceed to Sprint 4

---

## 📊 TIME ESTIMATE SUMMARY

| Task | Estimate | Owner |
|------|----------|-------|
| 3.1: Install dependencies | 2 hours | CE-Hub |
| 3.2: Create provider | 3 hours | CE-Hub |
| 3.3: Create API route | 2 hours | CE-Hub |
| 3.4: Create component | 6 hours | CE-Hub |
| 3.5: Agent handlers | 8 hours | CE-Hub |
| 3.6: Archon contexts | 4 hours | CE-Hub |
| 3.7: Chat history | 3 hours | CE-Hub |
| 3.8: Replace in pages | 2 hours | CE-Hub |
| 3.9: Deprecate old | 1 hour | CE-Hub |
| 3.10: Test integration | 4 hours | Both |
| **TOTAL** | **35 hours (~5 days)** | |

**Sprint Buffer**: Add 7-14 hours for unknowns = ~7 days (1 week) total

**Actual Duration**: Weeks 3-4 (14 days) allows for parallel work and buffer

---

## ✅ SPRINT VALIDATION GATE

Sprint 3 is complete when:
- [ ] CopilotKit installed and configured
- [ ] New Renata interface built and functional
- [ ] All agent actions registered and working
- [ ] Chat history management working
- [ ] Archon contexts integrated
- [ ] Old component deprecated
- [ ] All test cases pass
- [ ] No critical bugs remaining

**Final Validation**:
User can chat with Renata, request scanner generation, receive V31-compliant code, execute it, and see results - all through the new CopilotKit interface.

---

## 🚨 RISKS & MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| CopilotKit integration issues | Medium | High | Keep old component as fallback, gradual rollout |
| Agent actions don't work | Medium | High | Test each action independently before integrating |
| Performance degradation | Low | Medium | Monitor response times, optimize queries |
| Context not available | Low | Medium | Test Archon integration thoroughly |

**Rollback Plan**:
If CopilotKit rebuild fails, revert to RenataV2Chat and extend with enhancements instead of rebuilding.

---

## 🎯 SUCCESS CRITERIA

Sprint 3 Success means:
- ✅ Production-grade CopilotKit interface
- ✅ All basic agent actions working
- ✅ Archon knowledge available to AI
- ✅ Chat history persists
- ✅ Clean architecture for future agent development
- ✅ Ready to build specialized agents (Sprints 4-8)

---

## 📝 NOTES

- **This is a complete rebuild, not an enhancement**
- **Focus on clean architecture over features**
- **Agent actions will be enhanced in future sprints**
- **Temporary implementations will be replaced with real agents**
- **Test thoroughly before deprecating old component**

---

**Sprint 3 rebuilds Renata on a modern foundation.**

**CopilotKit provides the architecture for sophisticated AI agents.**

**Let's build this right.**
