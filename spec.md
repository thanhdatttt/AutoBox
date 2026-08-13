# Autobox — AI Business Process Automation Agent

## 1. Project Overview

**Project name:** Autobox

**Project type:** AI Agent for Business Process Automation

**Current domain:** Education

**Primary goal:**
Build an AI Agent system capable of understanding natural-language requests and executing business workflows through controlled tools.

Autobox is designed as a **general-purpose business process automation agent**, but the first implementation focuses only on the **Education domain**.

The architecture must allow additional domains and workflows to be added later without rewriting the core Agent system.

---

# 2. Vision

Traditional business applications require users to manually navigate multiple screens:

```text
Login
  ↓
Find module
  ↓
Find class
  ↓
Find student
  ↓
Select operation
  ↓
Enter data
  ↓
Submit
```

Autobox aims to replace this interaction model with:

```text
User
  ↓
Natural Language
  ↓
AI Agent
  ↓
Understand Intent
  ↓
Select Workflow
  ↓
Execute Tools
  ↓
Business System / Database
  ↓
Result
  ↓
Natural Language Response
```

Example:

```text
Teacher:

"Cho tôi danh sách sinh viên vắng hôm nay."

                    ↓

                Autobox Agent

                    ↓

          Understand the request

                    ↓

          Resolve "hôm nay"

                    ↓

          Find attendance data

                    ↓

             Query database

                    ↓

              Analyze result

                    ↓

"Hiện có 3 sinh viên vắng hôm nay:
Nguyễn Văn A, Trần Văn B và Lê Văn C."
```

The Agent is therefore not simply a chatbot.

It is a **workflow execution system controlled through natural language**.

---

# 3. Core Concept

Autobox consists of three major concepts:

```text
Agent
Workflow
Tool
```

## Agent

The Agent understands user requests and determines what should happen.

## Workflow

A Workflow represents a business process.

For example:

```text
Record Attendance
```

could be:

```text
Identify Student
      ↓
Resolve Date
      ↓
Validate Attendance
      ↓
Record Attendance
      ↓
Confirm Result
```

## Tool

A Tool is a controlled capability that the Agent can execute.

Examples:

```text
get_students()
get_attendance()
record_attendance()
get_schedule()
create_assignment()
```

The Agent should never directly manipulate infrastructure.

---

# 4. Project Scope

## Current Scope

The first version focuses exclusively on:

> **Education business-process automation**

The initial target user is:

> **Teacher / Instructor**

The first implementation should automate common classroom-management workflows.

### Initial education workflows

```text
Student Management
Attendance Management
Class Schedule Management
Assignment Management
Basic Class Information
```

The implementation should start with the smallest useful subset and expand incrementally.

---

# 5. Future Scope

Autobox should eventually support multiple domains.

Possible future domains:

```text
Education
    ├── Classroom
    ├── Attendance
    ├── Assignments
    └── Scheduling

Human Resources
    ├── Leave Management
    ├── Employee Information
    └── Recruitment

Customer Support
    ├── Ticket Management
    ├── Customer Information
    └── Issue Resolution

Sales
    ├── Customer Management
    ├── Order Management
    └── Sales Reporting
```

These domains are **future extensions**, not part of the current implementation.

The architecture must therefore avoid education-specific logic inside the core Agent infrastructure.

---

# 6. Architectural Principle

The most important architectural rule is:

> **Separate the Agent Core from Domain Logic.**

Incorrect:

```text
Agent
 ├── Student logic
 ├── Attendance logic
 ├── Schedule logic
 └── Education-specific rules
```

Preferred:

```text
                    Autobox
                       │
             ┌─────────┴─────────┐
             │                   │
        Agent Core          Domain Modules
             │                   │
             │          ┌────────┴────────┐
             │          │                 │
             │      Education          Future
             │          │              Domains
             │          │
             │      Workflows
             │          │
             │        Tools
             │          │
             └──────────┴───────────────┐
                                        │
                                  Infrastructure
```

The Agent Core should not know that a tool belongs specifically to education.

It should work with capabilities exposed by domain modules.

---

# 7. High-Level Architecture

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    API Layer     │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │      Autobox Agent       │
                    │                         │
                    │ Intent Understanding    │
                    │ Tool Selection          │
                    │ Workflow Execution       │
                    │ Response Generation      │
                    └───────────┬─────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Workflow Engine  │
                       └────────┬─────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
        Education Tools    Future Domain     Other Tools
               │             Tools
               ▼
        ┌──────────────┐
        │   Services   │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ Repositories │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  PostgreSQL  │
        └──────────────┘
```

---

# 8. Agent Core

The Agent Core is domain-independent.

Its responsibilities are:

1. Receive a user request.
2. Understand the user's intent.
3. Determine the required workflow.
4. Select appropriate tools.
5. Execute tools.
6. Process tool results.
7. Handle multi-step operations.
8. Produce a final response.
9. Ask for clarification when necessary.
10. Avoid hallucinating unavailable information.

The Agent Core must **not** contain:

```text
Student
Attendance
Classroom
Assignment
Teacher-specific business rules
```

Those belong to domain modules.

---

# 9. LLM Layer

The project should use an LLM through a provider abstraction.

Initial provider:

```text
Ollama Cloud
```

The application should not tightly couple the Agent implementation to a specific model.

Conceptually:

```text
Agent
  ↓
LLM Provider Interface
  ↓
Ollama Cloud
```

Configuration:

```env
OLLAMA_API_KEY=
OLLAMA_MODEL=
```

The model name must be configurable.

---

# 10. Agent Framework

The initial implementation uses:

```text
OpenAI Agents SDK
```

The framework provides capabilities such as:

* Agent definition
* Tool calling
* Runner/execution
* Model integration
* Agent orchestration

The project should keep domain logic outside the framework-specific layer wherever practical.

---

# 11. Domain Architecture

Each business domain should be implemented as an independent module.

Current:

```text
domains/
└── education/
```

Future:

```text
domains/
├── education/
├── hr/
├── customer_support/
└── sales/
```

A domain should contain:

```text
Domain
 ├── workflows
 ├── tools
 ├── services
 ├── repositories
 ├── models
 └── domain rules
```

---

# 12. Education Domain

The Education domain is the first implementation.

Structure:

```text
education/
├── workflows/
├── tools/
├── services/
├── repositories/
├── models/
└── rules/
```

The Education domain should expose capabilities to the Agent Core without requiring the Agent Core to understand education-specific implementation details.

---

# 13. Education Workflows

The initial workflows are:

## 13.1 Student Management

Examples:

```text
"Cho tôi danh sách sinh viên."

"Thông tin của Nguyễn Văn A?"

"Tìm sinh viên có mã SV001."
```

Possible tools:

```text
get_students()
get_student()
search_students()
```

---

## 13.2 Attendance Management

Examples:

```text
"Ai vắng hôm nay?"

"Nguyễn Văn A đã đi học tuần này bao nhiêu buổi?"

"Ghi nhận Nguyễn Văn A có mặt hôm nay."
```

Possible tools:

```text
get_attendance()
get_student_attendance()
record_attendance()
update_attendance()
```

---

## 13.3 Schedule Management

Examples:

```text
"Ngày mai tôi có lịch gì?"

"Lịch học tuần này của lớp là gì?"

"Khi nào có tiết CSC13112?"
```

Possible tools:

```text
get_schedule()
get_class_schedule()
```

---

## 13.4 Assignment Management

Potential future workflow:

```text
"Tạo bài tập về OOP, hạn nộp thứ sáu."

"Cho tôi danh sách bài tập tuần này."

"Bài tập nào chưa có điểm?"
```

Possible tools:

```text
create_assignment()
get_assignments()
update_assignment()
```

This workflow can be implemented after the core education workflows are stable.

---

# 14. Workflow Model

A workflow is a reusable business process.

Example:

```text
Record Attendance
```

```text
User Request
     ↓
Identify Student
     ↓
Resolve Date
     ↓
Determine Attendance Status
     ↓
Validate Request
     ↓
Record Attendance
     ↓
Return Confirmation
```

The workflow may involve multiple tools.

The Agent should be capable of handling:

```text
Single-step workflows
Multi-step workflows
Conditional workflows
Workflows requiring clarification
```

---

# 15. Tool Architecture

Tools are the controlled interface between the Agent and the application.

Example:

```text
Agent
  ↓
record_attendance()
  ↓
AttendanceService
  ↓
AttendanceRepository
  ↓
PostgreSQL
```

The LLM should never directly access:

```text
Database
Filesystem
Shell
External APIs
```

unless an explicit, validated tool provides such access.

---

# 16. Tool Categories

Tools should be classified as:

### Read Tools

```text
get_students
get_student
get_attendance
get_schedule
get_assignments
```

### Write Tools

```text
record_attendance
update_attendance
create_assignment
update_assignment
```

Write tools require stronger validation than read tools.

---

# 17. Tool Design Requirements

Every tool should have:

* Unique name.
* Clear description.
* Typed parameters.
* Input validation.
* Predictable output.
* Error handling.
* No hidden side effects.

Example:

```python
@function_tool
def get_students(classroom_id: int):
    """Return students belonging to a classroom."""
```

The tool should delegate business logic:

```text
Tool
 ↓
Service
 ↓
Repository
```

The tool itself should remain thin.

---

# 18. Natural Language Date Resolution

Many business workflows contain temporal expressions.

Examples:

```text
hôm nay
ngày mai
hôm qua
tuần này
tuần sau
tháng này
```

The system should provide a reusable date-resolution component.

Architecture:

```text
User Request
      ↓
Agent
      ↓
Date Resolver
      ↓
Normalized Date / Date Range
      ↓
Workflow
```

Example:

```text
"hôm nay"
      ↓
2026-08-13
```

```text
"tuần này"
      ↓
start_date + end_date
```

Date resolution should be deterministic whenever possible.

It must use a configurable timezone:

```env
APP_TIMEZONE=Asia/Ho_Chi_Minh
```

The Date Resolver should be reusable by future domains.

For example:

```text
Education → attendance today
HR        → employees on leave today
Sales     → orders this week
```

---

# 19. Business Logic Layer

Business logic must not be implemented inside prompts.

Incorrect:

```text
Prompt:
"If student is absent then..."
```

Preferred:

```text
AttendanceService
    ↓
Business Rule
    ↓
Result
```

The LLM is responsible for language understanding and orchestration.

The application is responsible for deterministic business rules.

---

# 20. Data Architecture

The first version uses PostgreSQL.

Education domain entities initially include:

```text
Classroom
Student
ClassroomStudent
Attendance
Schedule
```

Future:

```text
Assignment
Submission
Grade
Teacher
Course
```

The database schema should be designed so future education workflows can be added without major restructuring.

---

# 21. Database Access

The Agent must never generate arbitrary SQL.

Incorrect:

```text
User
 ↓
LLM
 ↓
Generated SQL
 ↓
PostgreSQL
```

Correct:

```text
User
 ↓
Agent
 ↓
Tool
 ↓
Service
 ↓
Repository
 ↓
PostgreSQL
```

This provides:

* Security
* Validation
* Testability
* Maintainability
* Predictable behavior

---

# 22. Repository Structure

The initial repository should approximately follow:

```text
Autobox/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── agent/
│   │   ├── workflow/
│   │   ├── tools/
│   │   ├── llm/
│   │   └── date_resolver/
│   │
│   ├── domains/
│   │   │
│   │   └── education/
│   │       ├── workflows/
│   │       ├── tools/
│   │       ├── services/
│   │       ├── repositories/
│   │       ├── models/
│   │       └── rules/
│   │
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── config/
│   │   └── logging/
│   │
│   └── api/
│       └── ...
│
├── tests/
│   ├── core/
│   └── domains/
│       └── education/
│
├── docker/
├── docker-compose.yml
├── .env.example
├── pyproject.toml
└── README.md
```

This structure is intentionally designed around **domain separation**.

---

# 23. Configuration

Environment-dependent configuration must be externalized.

Example:

```env
OLLAMA_API_KEY=
OLLAMA_MODEL=

DATABASE_URL=

APP_TIMEZONE=Asia/Ho_Chi_Minh
```

Never commit:

```text
.env
API keys
Database credentials
Tokens
Secrets
```

---

# 24. Safety and Reliability

Autobox must prioritize correctness over appearing intelligent.

## No hallucinated business data

If the database contains no result:

```text
Do not invent one.
```

Instead:

```text
"Không tìm thấy dữ liệu phù hợp."
```

## No guessing critical parameters

Example:

```text
Teacher:
"Điểm danh Nguyễn Văn A."
```

The system should not assume:

```text
present
```

or:

```text
absent
```

It should ask:

```text
"Bạn muốn ghi nhận Nguyễn Văn A có mặt hay vắng?"
```

## No uncontrolled writes

All write operations must go through validated tools.

---

# 25. Agent Interaction Model

The basic Agent loop is:

```text
User Request
     ↓
Understand Intent
     ↓
Determine Workflow
     ↓
Select Tool
     ↓
Execute Tool
     ↓
Observe Result
     ↓
Continue / Ask / Finish
     ↓
Final Response
```

For a multi-step workflow:

```text
User
 ↓
Agent
 ↓
Identify student
 ↓
Resolve date
 ↓
Validate
 ↓
Execute operation
 ↓
Return result
```

---

# 26. Example End-to-End Flow

User:

```text
"Nguyễn Văn A nghỉ bao nhiêu buổi tuần này?"
```

System:

```text
                User
                 │
                 ▼
            Agent Core
                 │
                 ▼
        Identify Workflow
                 │
                 ▼
     Student Attendance Workflow
                 │
          ┌──────┴──────┐
          ▼             ▼
    Find Student   Resolve Date
          │             │
          └──────┬──────┘
                 ▼
       get_student_attendance()
                 │
                 ▼
             PostgreSQL
                 │
                 ▼
          Attendance Data
                 │
                 ▼
               Agent
                 │
                 ▼
          Natural Response
```

---

# 27. Error Handling

The system must handle:

```text
Database unavailable
Student not found
Classroom not found
No attendance data
Invalid date
Invalid tool arguments
Ambiguous request
LLM failure
Tool failure
```

The Agent must never hide failures by fabricating data.

Example:

```text
Database unavailable
       ↓
Agent
       ↓
"Hiện tại tôi không thể truy cập dữ liệu lớp học. Vui lòng thử lại sau."
```

---

# 28. Observability

During development, it should be possible to inspect:

```text
User Request
     ↓
Detected Workflow
     ↓
Tool Calls
     ↓
Tool Arguments
     ↓
Tool Results
     ↓
Final Response
```

Logs must not expose:

```text
API keys
Passwords
Database credentials
Unnecessary sensitive information
```

---

# 29. Testing Strategy

Testing should happen at multiple levels.

## Unit Tests

Test:

```text
Date Resolver
Business Rules
Services
Repositories
```

## Tool Tests

Test:

```text
Valid inputs
Invalid inputs
Missing data
Database failures
```

## Workflow Tests

Test complete business workflows.

Example:

```text
record attendance
```

## Agent Tests

Test natural-language requests:

```text
"Cho tôi danh sách sinh viên."

"Ai vắng hôm nay?"

"Ngày mai có lịch gì?"

"Nguyễn Văn A nghỉ bao nhiêu buổi tuần này?"
```

The purpose is to verify that the Agent selects and executes the correct capabilities.

---

# 30. Development Strategy

The project must be built incrementally.

Do not attempt to implement every workflow immediately.

## Phase 0 — Project Foundation

Build:

```text
Repository
Configuration
Logging
Basic application entry point
Dependency management
```

---

## Phase 1 — Agent Core

Build:

```text
Agents SDK
LLM provider
Ollama Cloud integration
Basic Agent
```

Goal:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Answer
```

---

## Phase 2 — Tool System

Build:

```text
Tool abstraction
Tool registration
Tool execution
Tool validation
```

Implement one simple tool first.

Example:

```text
get_students()
```

---

## Phase 3 — Database Infrastructure

Build:

```text
PostgreSQL
Docker
Database connection
Models
Repositories
Seed data
```

Goal:

```text
Tool
 ↓
Service
 ↓
Repository
 ↓
PostgreSQL
```

---

## Phase 4 — Education Domain

Implement the first domain:

```text
Education
```

Start with:

```text
Student Management
```

Then:

```text
Attendance
```

Then:

```text
Schedule
```

Then:

```text
Assignment
```

---

## Phase 5 — Natural Date Resolution

Build reusable:

```text
DateResolver
```

Support:

```text
hôm nay
ngày mai
hôm qua
tuần này
tuần sau
tháng này
```

---

## Phase 6 — Workflow Orchestration

Support multi-step workflows.

Example:

```text
Find Student
     ↓
Resolve Date
     ↓
Query Attendance
     ↓
Analyze
     ↓
Respond
```

---

## Phase 7 — Write Operations

Implement controlled mutations:

```text
record_attendance
update_attendance
create_assignment
```

Add strong validation and ambiguity handling.

---

## Phase 8 — Education MVP

The Education Agent should support:

```text
Student Management
Attendance Management
Schedule Management
Basic Assignment Management
Natural Date Expressions
Multi-step Workflows
```

---

# 31. Extensibility Requirement

Adding a new domain should not require rewriting the Agent Core.

For example, after Education is complete:

```text
domains/
├── education/
└── hr/
```

The HR domain could expose:

```text
get_employee()
get_leave_requests()
create_leave_request()
```

The Agent Core should be able to work with these capabilities through the same architecture.

The goal is:

```text
                    Autobox Core
                        │
          ┌─────────────┼─────────────┐
          │             │             │
      Education        HR       Customer Support
          │             │             │
       Tools          Tools         Tools
          │             │             │
       Services       Services      Services
          │             │             │
       Database       Database      External API
```

---

# 32. Domain Plugin Principle

A domain should be treated as a collection of capabilities.

Conceptually:

```python
EducationDomain.register()
```

could register:

```text
Student Tools
Attendance Tools
Schedule Tools
Assignment Tools
```

Later:

```python
HRDomain.register()
```

could register:

```text
Employee Tools
Leave Tools
Recruitment Tools
```

The Agent Core should not need to know the internal implementation of these domains.

---

# 33. What Autobox Is Not

Autobox is not:

```text
❌ A generic chatbot
❌ An LLM wrapper
❌ A system where the LLM directly queries SQL
❌ A collection of hard-coded prompts
❌ A single-purpose classroom chatbot
```

Autobox is:

```text
✅ An AI Agent
✅ A business-process automation system
✅ A tool-based workflow executor
✅ A domain-extensible architecture
✅ A natural-language interface for business operations
```

---

# 34. Definition of Done — Foundation

The foundation is complete when:

* [ ] Project runs locally.
* [ ] Configuration is externalized.
* [ ] Ollama Cloud connection works.
* [ ] Agent can process natural-language input.
* [ ] Agent can call tools.
* [ ] Tool architecture is separated from Agent Core.
* [ ] PostgreSQL runs through Docker.
* [ ] Database access is separated from Agent logic.
* [ ] Date Resolver exists as a reusable component.
* [ ] Education is implemented as a domain module.
* [ ] At least one complete education workflow works end-to-end.
* [ ] Tests exist for core business logic.
* [ ] No secrets are committed.

---

# 35. Definition of Done — Education MVP

The Education MVP is complete when the Agent can reliably perform:

```text
Student queries
        +
Attendance queries
        +
Schedule queries
        +
Basic assignment operations
        +
Natural date resolution
        +
Multi-step workflows
        +
Validated write operations
```

Example:

```text
Teacher
  ↓
"Nguyễn Văn A nghỉ bao nhiêu buổi tuần này?"
  ↓
Autobox Agent
  ↓
Education Workflow
  ↓
Date Resolver
  ↓
Attendance Tool
  ↓
PostgreSQL
  ↓
Result
  ↓
Natural Language Response
```

---

# 36. Engineering Principles

## Principle 1 — Agent is an orchestrator

The Agent coordinates actions.

It should not contain all business logic.

## Principle 2 — Domain logic belongs to domains

Education logic belongs in:

```text
domains/education/
```

not:

```text
core/agent/
```

## Principle 3 — Deterministic logic belongs in code

Examples:

```text
Date calculation
Validation
Business rules
Database queries
Authorization
```

should not depend solely on the LLM.

## Principle 4 — LLM selects capabilities

The LLM determines:

```text
"What does the user want?"
"What capability should I use?"
```

The application determines:

```text
"How is that operation safely executed?"
```

## Principle 5 — Database is the source of truth

The Agent must never invent business data.

## Principle 6 — Small workflows first

Build one reliable workflow before adding another.

## Principle 7 — Domain independence

The Agent Core must remain independent from Education.

## Principle 8 — Extensibility over premature complexity

The architecture should be extensible, but the implementation should remain simple until complexity is actually required.

---

# 37. First Implementation Target

The project should **start completely from scratch**.

The first implementation target is:

```text
                    Autobox
                      │
                      ▼
                Agent Core
                      │
                      ▼
                 Ollama Cloud
                      │
                      ▼
                 Tool System
                      │
                      ▼
              Education Domain
                      │
                      ▼
              Student Workflow
                      │
                      ▼
                PostgreSQL
```

The first complete workflow should be:

```text
"Cho tôi danh sách sinh viên."
```

Expected execution:

```text
User
 ↓
Agent
 ↓
Understand intent
 ↓
Select get_students()
 ↓
Education Service
 ↓
PostgreSQL
 ↓
Student data
 ↓
Agent
 ↓
Final response
```

Once this workflow is reliable, the project should proceed incrementally to:

```text
Attendance
     ↓
Natural Date Resolution
     ↓
Schedule
     ↓
Assignments
     ↓
Multi-step Workflows
     ↓
Write Operations
```

Only after the Education domain is stable should the architecture be extended to additional business domains.

---

# 38. Guideline for AI Coding Agents

When an AI coding agent works on this project, it must:

1. Read this specification before implementing features.
2. Inspect the existing code before making changes.
3. Start from the current milestone.
4. Avoid implementing future milestones prematurely.
5. Keep Agent Core domain-independent.
6. Keep Education-specific logic inside the Education domain.
7. Never let the LLM execute arbitrary SQL.
8. Use tools for external operations.
9. Keep tools thin and business logic in services.
10. Keep database access in repositories/infrastructure.
11. Prefer deterministic application logic over prompt-based business rules.
12. Add tests for new functionality.
13. Avoid unnecessary dependencies.
14. Do not expose secrets.
15. Do not silently change architecture.
16. Preserve existing working functionality.
17. Make small, reviewable changes.
18. When a requirement is ambiguous, identify the ambiguity instead of inventing behavior.
19. Update documentation when architecture or behavior changes.
20. Implement the simplest correct solution before introducing additional abstraction.

---

# 39. Current Priority

The project should currently be implemented in this exact order:

```text
01. Project Foundation
        ↓
02. Agent Core
        ↓
03. Ollama Cloud Integration
        ↓
04. Tool Calling
        ↓
05. PostgreSQL Infrastructure
        ↓
06. Education Domain
        ↓
07. Student Workflow
        ↓
08. Attendance Workflow
        ↓
09. Natural Date Resolver
        ↓
10. Schedule Workflow
        ↓
11. Assignment Workflow
        ↓
12. Multi-step Workflow
        ↓
13. Write Operations
        ↓
14. Education MVP
        ↓
15. Additional Domains
```

The immediate objective is **not to build a sophisticated autonomous AI system**.

The immediate objective is to establish a clean foundation where:

```text
Natural Language
       ↓
AI Agent
       ↓
Business Workflow
       ↓
Controlled Tools
       ↓
Real Data / External Systems
       ↓
Business Result
```

works reliably for the **Education domain**, while keeping the core architecture reusable for future business domains.
