# 🎯 RENATA V2 SCOPE CORRECTION V2
## Hybrid Approach + Visual Design Clone + Project Integration

**Date**: January 24, 2026
**Based On**: User feedback after platform analysis
**Status**: FINAL REQUIREMENTS - Ready for planning updates

---

## ✅ YOUR REQUIREMENTS (CONFIRMED)

### 1. Integration Approach
**DECISION**: ✅ **HYBRID (Option C)**
- `/plan` page: Dedicated Renata workspace for deep planning and building
- Sidebar on `/scan` and `/backtest`: Quick AI access while working
- User's choice where to work based on their current needs

### 2. Visual Design
**DECISION**: ✅ **CLONE TRADERRA AI JOURNAL UI**
- Source: `/ai dev/ce-hub/projects/traderra/frontend/` (port 6565)
- Component: `StandaloneRenataChat` + `RenataSidebar`
- Design: Fixed sidebar, 480px wide, slides in from right
- Colors: Dark theme (#111111 background), purple/pink gradients

### 3. Workflow Requirements
**DECISION**: ✅ **PLAN → BUILD → TEST → EXECUTE**
- Primary workflow: Brainstorm and plan → Build → Test → Execute
- Secondary workflow: Brainstorm → Move (quick iterations)
- Flexibility: User chooses where to work based on task

### 4. Cross-Page Integration
**DECISION**: ✅ **PROJECTS TIED ACROSS ALL PAGES**
- Projects on `/plan` page linked to `/scan` and `/backtest` projects
- Chats tied to projects for knowledge organization
- Can do complete workflow from any page (user's choice)

### 5. Layout Requirements
**DECISION**: ✅ **LEFT SIDEBAR = PROJECTS**
- Left sidebar: Always shows projects list
- Renata: Has dropdown for chat history
- No separate Renata sidebar - integrated with projects

### 6. Execution Locations
**CONFIRMED**: ✅ **UI TAILORED TO EACH TYPE**
- `/scan` page: For scans (scan-specific UI components)
- `/backtest` page: For backtests (backtest-specific UI)
- Each page has optimized UI for its purpose

---

## 📊 VISUAL DESIGN TO CLONE

### From Traderra AI Journal (Port 6565)

**File**: `/ai dev/ce-hub/projects/traderra/frontend/src/components/chat/standalone-renata-chat.tsx`

### Key Design Elements:

#### 1. Header Section
```typescript
<div className="flex items-center justify-between p-4 border-b border-border">
  <div className="flex items-center gap-2">
    <Brain className="w-5 h-5 text-purple-400" />
    <span className="font-medium text-studio-text">Renata AI</span>
  </div>
  <div className="flex items-center gap-2">
    {/* Mode Selector */}
    <select className="text-xs bg-studio-surface border border-border rounded px-2 py-1">
      <option>Renata</option>
      <option>Analyst</option>
      <option>Coach</option>
      <option>Mentor</option>
    </select>

    {/* AG-UI Toggle */}
    <button className="text-xs px-2 py-1 rounded border">
      🔧 AG-UI
    </button>

    {/* Reset Button */}
    <button>
      <RotateCcw className="w-4 h-4" />
    </button>

    {/* Sparkles Icon */}
    <Sparkles className="w-4 h-4 text-yellow-400" />
  </div>
</div>
```

#### 2. Messages Area
```typescript
<div className="flex-1 overflow-y-auto p-4 space-y-4">
  {/* Messages with gradient avatar */}
  <div className="flex gap-3">
    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500">
      <Brain className="w-4 h-4 text-white" />
    </div>
    <div className="max-w-[80%] p-3 rounded-lg bg-studio-accent/50">
      <p>{message.content}</p>
    </div>
  </div>
</div>
```

#### 3. Input Area
```typescript
<div className="p-4 border-t border-border">
  <div className="flex gap-2">
    <input
      placeholder="Chat with Renata..."
      className="flex-1 px-3 py-2 bg-studio-surface border border-border rounded-md"
    />
    <button className="px-4 py-2 bg-primary rounded-md">
      <Send className="w-4 h-4" />
    </button>
  </div>
</div>
```

#### 4. Sidebar Container
```typescript
<div style={{
  position: 'fixed',
  top: '64px',
  right: '0',
  bottom: '0',
  width: '480px',
  backgroundColor: '#111111',
  borderLeft: '1px solid #1a1a1a',
  zIndex: 99999,
  overflow: 'auto'
}}>
  <StandaloneRenataChat />
</div>
```

---

## 🎯 REVISED PAGE STRUCTURE

### NEW: `/plan` Page (Dedicated Workspace)

```
┌─────────────────────────────────────────────────────────────────┐
│  /plan - RENATA WORKSPACE                                       │
│  ┌──────────────────────┬─────────────────────────────────────┐   │
│  │ LEFT: Projects       │ MAIN: Renata Chat + Projects      │   │
│  │ ┌────────────────┐   │                                     │   │
│  │ │ Project 1       │   │  ┌─────────────────────────────────┐ │   │
│  │ │ Project 2       │   │  │ RENATA CHAT (FULL WIDTH)       │ │   │
│  │ │ Project 3       │   │  │                                 │ │   │
│  │ │                │   │  │ User: I want to build...         │ │   │
│  │ │ [+ New Project] │   │  │                                 │ │   │
│  │ └────────────────┘   │  │ Renata: Let me help...           │ │   │
│  │                      │   │  │ [Planning Agent] [Researcher]    │ │   │
│  │  Chat History:       │   │  │ [Builder Agent]                 │ │   │
│  │  [▼ Dropdown]        │   │  │                                 │ │   │
│  │                      │   │  │ Scanner ready!                    │ │   │
│  │                      │   │  │ [→ Send to /scan]               │ │   │
│  │                      │   │  │ [→ Send to /backtest]           │ │   │
│  │                      │   │  └─────────────────────────────────┘ │   │
│  └──────────────────────┘   │                                     │   │
│                              └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### REVISED: `/scan` Page (Add Quick Renata Access)

```
┌─────────────────────────────────────────────────────────────────┐
│  /scan - MARKET SCANNER                                         │
│  ┌──────────────────────┬─────────────────────────────────┐     │
│  │ LEFT: Projects       │ MAIN: Chart + Results            │     │
│  │ ┌────────────────┐   │                                  │     │
│  │ │ Project 1       │   │  EdgeChart                      │     │
│  │ │ Project 2       │   │  Scanner Results                │     │
│  │ │ Project 3       │   │                                  │     │
│  │ │                │   │  [Execute Scanner]               │     │
│  │ └────────────────┘   │                                  │     │
│  │                      │   │  [🧠 Renata] ← NEW BUTTON       │     │
│  │  Chat History:       │   │  (opens sidebar for quick help)   │     │
│  │  [▼ Dropdown]        │   │                                  │     │
│  └──────────────────────┴─────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ↓ Click [🧠 Renata]
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR slides in (480px from right)                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ [← Close] Renata AI                                        │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Chat with Renata (quick help while scanning)               │  │
│  │ Can do full workflow: plan → build → test → execute        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### REVISED: `/backtest` Page (Add Quick Renata Access)

```
┌─────────────────────────────────────────────────────────────────┐
│  /backtest - BACKTEST ENGINE                                      │
│  ┌──────────────────────┬─────────────────────────────────┐     │
│  │ LEFT: Backtests      │ MAIN: Chart + Results            │     │
│  │ ┌────────────────┐   │                                  │     │
│  │ │ Backtest 1      │   │  EdgeChart                      │     │
│  │ │ Backtest 2      │   │  Results Panel                  │     │
│  │ │ Backtest 3      │   │                                  │     │
│  │ │                │   │  [View Results]                 │     │
│  │ └────────────────┘   │                                  │     │
│  │                      │   │  [🧠 Renata] ← NEW BUTTON       │     │
│  │  Chat History:       │   │  (opens sidebar for quick help)   │     │
│  │  [▼ Dropdown]        │   │                                  │     │
│  └──────────────────────┴─────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ↓ Click [🧠 Renata]
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR slides in (480px from right)                              │
│  │ Same Renata chat as /scan page                             │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 KEY INTEGRATION REQUIREMENTS

### 1. Project-Chat Tying System

**Requirement**: Chats tied to projects for knowledge organization

**Data Structure**:
```typescript
interface Project {
  id: string;
  name: string;
  type: 'scan' | 'backtest' | 'idea';
  status: 'planning' | 'building' | 'testing' | 'ready';

  // Chat history tied to project
  conversations: ChatConversation[];
  activeConversationId: string;

  // Scanner/Backtest specific
  scannerCode?: string;
  parameters?: Record<string, any>;

  // Metadata
  createdAt: Date;
  updatedAt: Date;
  tags: string[];
}

interface ChatConversation {
  id: string;
  projectId: string; // ← TIED TO PROJECT
  name: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
```

**Behavior**:
- When you create a new project on `/plan`, it creates a project with a new conversation
- When you open a project on `/scan` or `/backtest`, it loads the project's conversation
- Chat history dropdown shows conversations for current project
- Switching projects switches conversations

### 2. Cross-Page Project Sync

**Requirement**: Projects on `/plan` linked to `/scan` and `/backtest`

**Implementation**:
- Shared project storage (localStorage or database)
- Projects have `type: 'scan'` | 'backtest' | 'idea'`
- `/plan` shows all projects
- `/scan` shows only scan projects
- `/backtest` shows only backtest projects
- Changes sync across pages instantly

### 3. Chat History Dropdown

**Requirement**: Renata has dropdown for chat history

**UI Design**:
```
┌─────────────────────────────────────────────┐
│ [🧠 Renata AI] [Chat History ▼] [Settings]     │
├─────────────────────────────────────────────┤
│ Chat History Dropdown:                           │
│ ┌───────────────────────────────────────┐   │
│ │ Current Conversation                     │   │
│ │ ├─ Backside B Scanner (5 messages)    │   │
│ │ ├─ IPO Setup (12 messages)             │   │
│ │ └─ Gap Continuation (8 messages)        │   │
│ │                                           │   │
│ │ [+ New Conversation]                    │   │
│ └───────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 📋 WORKFLOW SCENARIOS

### Scenario 1: New Scanner Idea (Full Planning Flow)

**User Action**: Go to `/plan` page
```
1. /plan page loads
2. Left sidebar shows projects list
3. Click [+ New Project] → Creates "Backside B Gap Scanner"
4. Renata chat opens with new conversation tied to project
5. Chat: "I want to build a backside B scanner for gap ups..."
6. Renata agents:
   - Planning Agent: Breaks down the idea
   - Researcher Agent: Finds similar setups
   - Builder Agent: Generates V31 code
7. Scanner ready in chat
8. Click [→ Send to /scan]
9. Page redirects to /scan with scanner loaded
10. Execute scanner on /scan page
```

### Scenario 2: Quick Help While Scanning

**User Action**: Already on `/scan` page, needs help
```
1. On /scan page, viewing results
2. Click [🧠 Renata] button (top-right)
3. Sidebar slides in from right (480px wide)
4. Chat: "Help me optimize these parameters..."
5. Renata provides suggestions
6. Close sidebar, back to scanning
7. Results updated based on suggestions
```

### Scenario 3: Continue Previous Project

**User Action**: Want to continue working on a project
```
1. Go to /plan page
2. Left sidebar shows projects
3. Click "Backside B Gap Scanner" project
4. Project loads with:
   - Previous chat conversation
   - Current scanner code
   - Parameters saved
   - Status: "building"
5. Continue chatting with Renata to refine
```

### Scenario 4: Cross-Page Workflow

**User Action**: Start on /plan, move to /scan
```
1. /plan: Plan and build scanner
2. [→ Send to /scan]
3. /scan: Scanner loaded automatically
4. Execute scanner
5. Need to refine → Click [🧠 Renata]
6. Sidebar opens, chat with Renata
7. Renata helps optimize parameters
8. Re-execute with new parameters
```

---

## 🎨 DESIGN SYSTEM TO CLONE

### Colors (From Traderra AI Journal)

```css
:root {
  --studio-bg: #0a0a0a;
  --studio-surface: #111111;
  --studio-accent: #1a1a1a;
  --studio-text: #fafafa;
  --studio-muted: #a1a1aa;
  --border: rgba(212, 175, 55, 0.2);
  --primary: #3b82f6;
  --primary-foreground: #ffffff;
}

/* Renata-specific */
--renata-purple: #A855F7;
--renata-pink: #EC4899;
--renata-gradient: linear-gradient(135deg, #A855F7 0%, #EC4899 100%);
```

### Components to Clone

1. **StandaloneRenataChat**: Full chat component
2. **RenataSidebar**: Fixed positioning, 480px wide
3. **ChatHistorySidebar**: Conversation history dropdown
4. **Header Controls**: Mode selector, AG-UI toggle, reset button

---

## 🚨 SPRINT 3 CHANGES

### Remove Tasks
- ~~Task 3.8: Integrate into `/projects` page~~ (You don't use it)
- ~~Task 3.9: Integrate into `/exec` page~~ (You don't use it)

### New Tasks

**Task 3.5: Create `/plan` Page** (8 hours)
- Create dedicated Renata workspace page
- Left sidebar: Projects list (same component as /scan)
- Main area: Full-width Renata chat (no sidebar)
- Header: Page title, new project button
- Chat history dropdown
- "Send to /scan" and "Send to /backtest" actions

**Task 3.6: Create Project-Chat Tying System** (4 hours)
- Shared project storage across pages
- Project type filtering (scan vs backtest vs idea)
- Conversation-project linking
- Cross-page synchronization

**Task 3.7: Clone Traderra Renata UI** (4 hours)
- Copy StandaloneRenataChat component
- Copy RenataSidebar container
- Adapt to EdgeDev color scheme
- Maintain visual consistency

**Task 3.8: Integrate Sidebar into `/scan`** (2 hours)
- Add [🧠 Renata] button to /scan header
- Wire up to same RenataSidebar component
- Test toggle functionality

**Task 3.9: Integrate Sidebar into `/backtest`** (2 hours)
- Add [🧠 Renata] button to /backtest header
- Wire up to same RenataSidebar component
- Test toggle functionality

---

## ✅ ACCEPTANCE CRITERIA

### /plan Page
- [ ] Left sidebar shows all projects
- [ ] Clicking project loads its conversation
- [ ] New project button creates project + conversation
- [ ] Full-width Renata chat (no sidebar on this page)
- [ ] Chat history dropdown shows conversations
- [ ] "Send to /scan" redirects with scanner
- [ ] "Send to /backtest" redirects with backtest

### /scan Page
- [ ] Left sidebar shows scan projects only
- [ ] [🧠 Renata] button in header
- [ ] Clicking button opens Renata sidebar
- [ ] Sidebar shows current project's conversation
- [ ] Can do full workflow from sidebar
- [ ] Existing UI preserved (chart, results)

### /backtest Page
- [ ] Left sidebar shows backtest projects only
- [ ] [🧠 Renata] button in header
- [ ] Clicking button opens Renata sidebar
- [ ] Sidebar shows current project's conversation
- [ ] Can do full workflow from sidebar
- [ ] Existing UI preserved (chart, results)

### Cross-Page Integration
- [ ] Projects sync across /plan, /scan, /backtest
- [ ] Conversations tied to projects
- [ ] Chat history shows project-specific conversations
- [ ] Switching projects switches conversations

---

## 📊 UPDATED TIMELINE

### Sprint 3 (Revised)
**Duration**: 2 weeks (was 35 hours, now 38 hours)

Tasks:
1. Install CopilotKit (2h)
2. Create provider (2h)
3. Create API route (2h)
4. **Create /plan page** (8h) ← NEW
5. **Clone Traderra Renata UI** (4h) ← NEW
6. **Create project-chat tying system** (4h) ← NEW
7. Integrate sidebar into /scan (2h)
8. Integrate sidebar into /backtest (2h)
9. Comprehensive UI testing (4h)
10. Agent action handlers (6h)
11. Load Archon knowledge (4h)
12. Chat functionality testing (3h)

**Total**: 43 hours (~6 days)

---

## 🎯 SUCCESS CRITERIA

### You Can:
- ✅ Go to `/plan` for dedicated workspace
- ✅ Plan, build, and test strategies with Renata
- ✅ Send results to /scan or /backtest for execution
- ✅ Go to /scan or /backtest directly
- ✅ Click [🧠 Renata] for quick AI help
- ✅ Do complete workflow from any page
- ✅ Projects sync across all pages
- ✅ Chats tied to projects for organization

### Visual Design:
- ✅ Looks like Traderra AI Journal (port 6565)
- ✅ Clean, professional interface
- ✅ Purple/pink gradient avatars
- ✅ Dark theme (#111111 background)
- ✅ 480px sidebar when open

### Organization:
- ✅ Left sidebar always shows projects
- ✅ Chat history dropdown for navigation
- ✅ Project-chat linking for knowledge
- ✅ Type-filtered projects (scan vs backtest)

---

**This is your complete, final requirement specification.**

**Ready to update all planning documents and begin Sprint 0 setup.**

**Does this capture everything you want? Any changes needed?**
