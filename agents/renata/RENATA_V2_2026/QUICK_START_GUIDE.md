# 🚀 Quick Start: GitHub Projects Setup

## Step-by-Step Guide

### Step 1: Create GitHub Project Board (2 minutes)

1. Open: https://github.com/mdthewzrd/renata-v2/projects
2. Click **"New project"** button
3. Select **"Board"** (Kanban style)
4. Name: **RENATA V2 Build**
5. Under "Repository":
   - Click **"Select repository"**
   - Select **renata-v2** (already linked)
6. Click **"Create project"**

✅ **You now have a project board linked to your repo!**

---

### Step 2: Add Columns (1 minute)

Your board should have:
- **Backlog** (default)
- **Todo** (default - rename to "In Progress")
- **Done** (default - rename to "Review")

**To rename columns:**
- Click column header → Click ⚙️ → Edit title

**Add missing columns:**
- Click **"+"** at the end of columns
- Add: **"Review"** column

**Final columns should be:**
```
Backlog → In Progress → Review → Done
```

---

### Step 3: Create Issues (Automated - 1 minute)

**Option A: Run the script (RECOMMENDED)**
```bash
cd "/Users/michaeldurante/ai dev/ce-hub/projects/edge-dev-main/RENATA_V2_2026"
./create_issues.sh
```

This creates all 8 Sprint 0 issues automatically! ✅

**Option B: Create manually via web**
- Go to: https://github.com/mdthewzrd/ce-hub/issues/new
- Copy from PROJECT_TRACKING.md
- Create each issue manually

---

### Step 4: Add Issues to Project Board (2 minutes)

Once issues are created:

1. Go to your project: https://github.com/mdthewzrd/ce-hub/projects
2. Click **"Add items"** button (top right)
3. Select **"Existing issues"**
4. Check all the Sprint 0 issues you just created
5. Click **"Add selected issues"**

✅ **All issues now in your Backlog column!**

---

### Step 5: Create Milestone (1 minute)

1. Go to: https://github.com/mdthewzrd/renata-v2/milestones
2. Click **"New milestone"**
3. Title: **Sprint 0**
4. Due date: **January 27, 2026**
5. Description: **Pre-Flight & Planning**
6. Click **"Create milestone"**

---

### Step 6: Organize Your Board (2 minutes)

Drag issues to appropriate columns:
- **Task 0.1** → Done (already complete)
- **Task 0.2** → In Progress (current task)
- **Tasks 0.3-0.10** → Backlog

---

## 📊 Your Board Should Look Like:

```
┌─────────────────┬──────────────┬────────┬──────────┐
│   BACKLOG       │ IN PROGRESS  │ REVIEW │   DONE   │
├─────────────────┼──────────────┼────────┼──────────┤
│ Task 0.3        │ Task 0.2     │        │ Task 0.1 │
│ Task 0.4        │              │        │          │
│ Task 0.5        │              │        │          │
│ Task 0.6        │              │        │          │
│ Task 0.7        │              │        │          │
│ Task 0.8        │              │        │          │
│ Task 0.9        │              │        │          │
│ Task 0.10       │              │        │          │
└─────────────────┴──────────────┴────────┴──────────┘
```

---

## ✅ Setup Complete!

Now you can:
- ✅ Track all Sprint 0 tasks
- ✅ See progress at a glance
- ✅ Drag tasks between columns
- ✅ Add labels and assignees
- ✅ View progress on timeline

---

## 🎯 Next Steps

1. ✅ Complete Task 0.2 (Project Tracking) - YOU ARE HERE
2. ⏳ Move to Task 0.3 (Acceptance Criteria Template)
3. ⏳ Continue through Sprint 0 tasks

**Total setup time**: ~10 minutes

---

**Need help?** Check PROJECT_TRACKING.md for full documentation
