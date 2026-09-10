# NearCast AI Architecture

NearCast's AI layer has two primary responsibilities:

1. Recommend relevant existing groups to users.
2. Help a group plan and manage activities through an AI agent.

The recommendation system is based mainly on embeddings and vector similarity. The activity planner is an agentic workflow built with LangChain and LangGraph.

---

# 1. AI Feature Overview

The AI functionality is divided into two independent systems.

```text
NearCast AI
│
├── Group Recommendation Engine
│   ├── Normal Recommendation
│   └── Query Recommendation
│
└── AI Activity / Team Planner
    └── LangGraph Agent
```

The recommendation engine answers:

> Which existing groups are relevant to this user?

The activity planner answers:

> Given this group and its members, how can we plan this activity/team?

---

# 2. Group Recommendation Engine

NearCast recommends already-existing groups rather than recommending activities as the final result.

Activities are still important because an activity belongs to a group and its embedding can provide an additional semantic signal when identifying relevant groups.

There are two recommendation modes:

- Normal Recommendation
- Query Recommendation

---

## 2.1 Normal Recommendation

Normal recommendations are generated automatically from information already associated with the user.

Relevant information includes:

- User interests
- User preferences
- Relevant profile information

This information is converted into text and then into an embedding.

```text
User Interests
      +
User Preferences
      +
Relevant Profile Information
      ↓
Profile Text
      ↓
Embedding Model
      ↓
User Embedding
      ↓
Vector Similarity Search
      ↓
Relevant Groups
      ↓
Ranking
      ↓
Recommended Groups
```

Example:

```text
Interests:
- Cricket
- Football
- Hiking

Preferences:
- Small groups
- Outdoor activities
- Within 10 km
```

The system creates a semantic representation of this information and compares it with existing group representations.

The resulting groups can appear on the user's dashboard.

---

# 3. Query Recommendation

The second recommendation mode starts with an explicit query from the user.

Example:

```text
"I like cricket and want to play this weekend."
```

The query is first converted into an embedding.

```text
User Query
    ↓
Embedding Model
    ↓
Query Embedding
    ↓
Vector Search
    │
    ├── User Embeddings
    ├── Activity Embeddings
    └── Group Embeddings
    ↓
Relevant Candidates
    ↓
Map Activity Matches → Their Groups
    ↓
Rank Groups
    ↓
Recommended Groups
```

The final result shown to the user is always a group.

---

# 4. Why Activity Embeddings Participate in Query Recommendation

An activity can sometimes describe a group's purpose better than the group's own description.

Example:

```text
Group:
"Weekend Sports Group"
```

The group's description may be relatively generic.

Its activity might be:

```text
"Sunday competitive cricket tournament
for intermediate players."
```

If the user searches:

```text
"I want competitive cricket."
```

the activity embedding may be highly similar to the query.

That activity can therefore help identify its associated group.

Conceptually:

```text
                    Query
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       User        Activity      Group
     Embedding     Embedding    Embedding
          │           │           │
          └───────────┼───────────┘
                      ↓
               Candidate Groups
                      ↓
                Final Ranking
                      ↓
              Recommended Groups
```

---

# 5. Embedding Models

NearCast uses three domain-specific embedding models:

```text
UserEmbedding
ActivityEmbedding
GroupEmbedding
```

The generic `Embedding` model is unnecessary because each domain already has its own embedding model.

The embeddings use:

```text
384 dimensions
```

and are stored using pgvector.

---

## 5.1 User Embedding

`UserEmbedding` represents the semantic profile of a user.

Its source can be constructed from:

```text
Interests
+
Preferences
+
Relevant Profile Information
```

Example:

```text
Interested in cricket, football and hiking.
Prefers outdoor activities and small groups.
```

That text is passed through the embedding model and stored as the user's vector representation.

---

## 5.2 Activity Embedding

`ActivityEmbedding` represents the semantic meaning of an activity.

Potential input includes:

```text
Activity Title
+
Activity Description
+
Activity Type
+
Other Relevant Activity Information
```

Example:

```text
Title:
Sunday Cricket Tournament

Description:
Competitive cricket match for intermediate players.
```

The resulting representation is stored as a 384-dimensional vector.

---

## 5.3 Group Embedding

`GroupEmbedding` represents the semantic meaning of an existing group.

It can be created from:

```text
Group Name
+
Group Description
+
Other Relevant Group Information
```

Example:

```text
Name:
Weekend Cricket Community

Description:
A local community for people who enjoy playing
competitive cricket on weekends.
```

This information is converted into the group's embedding.

---

# 6. Vector Search

PostgreSQL and pgvector provide the vector-search layer.

The general recommendation process is:

```text
User / Query Embedding
        ↓
      pgvector
        ↓
Compare with stored vectors
        ↓
Similarity Scores
        ↓
Candidate Selection
        ↓
Ranking
        ↓
Recommended Groups
```

Cosine similarity can be used to measure semantic similarity between vectors.

---

# 7. Recommendation Pipeline

The recommendation engine does not need to be an LLM agent.

It can remain a deterministic backend pipeline:

```text
Recommendation Request
        ↓
Generate Embedding
        ↓
Perform Vector Search
        ↓
Retrieve Candidates
        ↓
Calculate / Combine Scores
        ↓
Rank Groups
        ↓
Return Groups
```

Other signals can later participate in ranking, including:

- Geographic distance
- User interests
- User preferences
- Group relevance
- Activity relevance
- User interaction history
- Group activity
- Availability

These ranking operations should primarily remain application logic rather than being delegated to an LLM.

---

# 8. Dashboard

The AI recommendation system feeds the user dashboard.

A simplified dashboard can contain:

```text
User Dashboard
│
├── Recommended Groups
│
├── Nearby Broadcasts
│
└── Gamification
```

Recommended Groups come from the recommendation engine.

Nearby Broadcasts come from the normal NearCast broadcast/location system.

Gamification is an application feature and does not need an LLM.

AI can eventually use participation and gamification-related signals as additional recommendation inputs.

---

# 9. Broadcasts and Activities

Broadcasts are primarily part of NearCast's normal application workflow rather than an AI feature.

A typical flow is:

```text
User wants to organize something
        ↓
Create Activity
        ↓
Create Broadcast
        ↓
Broadcast reaches nearby users
        ↓
Nearby users see it
        ↓
User requests to join
        ↓
User joins the relevant group/activity
```

The activity is stored in the activity domain.

Nearby delivery is primarily handled through:

```text
PostgreSQL
+
PostGIS
+
Application Logic
```

AI is therefore not required for basic nearby-broadcast delivery.

---

# 10. AI Activity / Team Planner

The second major AI capability is an AI-powered activity and team management planner.

It is accessed from inside a group.

Example:

```text
Cricket Group

15 Members

[ Plan Activity with AI ]
```

When the planner starts, the agent receives the relevant information about the group and its members.

---

# 11. Planner Context

The planner can work with information such as:

```text
Group
├── Name
├── Description
│
└── Members
    ├── User
    │   ├── Name
    │   ├── Interests
    │   └── Preferences
    │
    ├── User
    │   ├── Name
    │   ├── Interests
    │   └── Preferences
    │
    └── ...
```

It can additionally receive activity-specific requirements and constraints.

Example:

```text
Activity:
Cricket Match

Members:
15

Requirements:
- Team balance
- Player preferences
- Player availability
- Role suitability
```

---

# 12. Example: Cricket Team Planning

Imagine that a cricket group contains 15 members.

The AI can use the available information about those members to propose roles.

Example:

```text
Team A

Openers:
- Rahul
- User 2

Middle Order:
- User 3
- User 4

All-Rounders:
- Vishesh
- User 6

Bowlers:
- Aman
- User 8

Substitutes:
- User 9
- User 10
```

The actual assignments depend on the information available about each member and the constraints supplied to the planner.

Potential factors include:

- Member interests
- Member preferences
- Availability
- Activity requirements
- Team balance
- Admin instructions

---

# 13. Why LangGraph Fits the Planner

The planner is more complex than a simple LLM call.

It is not:

```text
Prompt
  ↓
LLM
  ↓
Response
```

Instead, the workflow may need to:

1. Retrieve group information
2. Retrieve group members
3. Retrieve member interests
4. Retrieve member preferences
5. Build the planner state
6. Generate a plan
7. Validate the plan
8. Ask the admin for approval
9. Receive admin instructions
10. Modify the plan
11. Re-plan
12. Finalize the result

This type of stateful, branching and iterative workflow is where LangGraph becomes useful.

---

# 14. LangGraph Concepts Used in NearCast

| LangGraph Concept | NearCast Application |
|---|---|
| LangGraph | Orchestrates the activity/team planning workflow |
| Chain vs Graph | Shows why the planner needs branching and iterative execution |
| State | Stores the current planning context |
| `TypedDict` | Defines the planner state |
| Message State | Holds planner conversation messages |
| `add_messages` | Adds messages to message state |
| Nodes | Individual planner operations |
| Node Functions | Implementation of each node |
| Edges | Connect workflow steps |
| `START` | Entry point of the graph |
| `END` | Exit point of the graph |
| Conditional Edges | Choose the next step based on state |
| Routing Functions | Determine workflow routing |
| Loops | Allow the planner to re-plan |
| Agent → Tool → Agent | Retrieve application information dynamically |
| Tools | Expose application functionality to the agent |
| `ToolNode` | Executes LangGraph tools |
| `bind_tools()` | Makes tools available to the LLM |
| LLM Tool Calling | Lets the LLM request application data |
| ReAct-style Agent Loop | Reason → Tool → Result → Continue |
| Multiple Tool Calls | Retrieve multiple kinds of information |
| RAG as a Tool | Retrieve relevant information when required |
| Web Search as a Tool | Optional; not part of the core planner |
| Calculator as a Tool | Optional; use when required |
| Memory | Preserve planner context |
| `thread_id` | Identifies a planner conversation |
| Checkpointing | Persists graph state |
| MongoDB Checkpointer | Possible checkpoint backend |
| Conversation Isolation | Keeps planner sessions separate |
| Human-in-the-Loop | Gives the admin control |
| `interrupt()` | Pauses execution for human input |
| `Command(resume=...)` | Resumes execution after human input |
| Streaming | Sends results progressively |
| `graph.astream()` | Streams graph execution |
| `stream_mode="messages"` | Streams AI messages |
| FastAPI Streaming | Delivers planner output to React |

---

# 15. Planner State

The graph needs a state containing the information required throughout the planning process.

Conceptually:

```text
PlannerState

├── group information
├── members
├── member interests
├── member preferences
├── activity requirements
├── current plan
├── validation result
├── admin instruction
└── messages
```

The exact `TypedDict` definition will be decided during implementation.

---

# 16. Planner Nodes

The workflow can be divided into separate nodes.

A possible structure is:

```text
load_group
      ↓
load_members
      ↓
load_interests_preferences
      ↓
build_context
      ↓
generate_plan
      ↓
validate_plan
      ↓
human_review
      ↓
finalize_plan
```

Each node should have one clear responsibility.

---

# 17. Edges and Routing

The nodes are connected through edges.

A basic flow could look like:

```text
START
  ↓
load_group
  ↓
load_members
  ↓
build_context
  ↓
generate_plan
  ↓
validate_plan
  ↓
human_review
  ↓
finalize_plan
  ↓
END
```

Conditional edges are used when the next step depends on the current state.

Example:

```text
validate_plan
       ↓
   Is it valid?
      /   \
    Yes    No
    ↓       ↓
Human     Re-plan
Review      │
   ↑        │
   └────────┘
```

A routing function determines which branch should execute.

---

# 18. Re-planning Loop

The planner should be able to regenerate a plan when the current result is invalid or unsuitable.

Example:

```text
Generate Plan
      ↓
Validate
      ↓
Invalid
      ↓
Generate Again
      ↓
Validate
      ↓
Valid
      ↓
Human Review
```

This loop is one of the reasons a graph is more appropriate than a simple sequential chain.

---

# 19. Agent Tools

The planner should access NearCast data through tools rather than directly manipulating the database.

Possible tools include:

```text
get_group_details()
get_group_members()
get_user_interests()
get_user_preferences()
get_activity_details()
```

These tools can internally communicate with the NearCast backend and database.

The agent receives the returned information and uses it during planning.

---

# 20. Agent → Tool → Agent

A typical planner interaction can follow:

```text
Agent
  ↓
Tool Call
  ↓
ToolNode
  ↓
Tool Result
  ↓
Agent
  ↓
Another Tool Call
  ↓
Tool Result
  ↓
Agent
  ↓
Final Plan
```

Example:

```text
User:
Plan a cricket activity for this group.

Agent:
I need the group members.

        ↓

get_group_members()

        ↓

Members returned.

        ↓

Agent:
I need their preferences.

        ↓

get_user_preferences()

        ↓

Preferences returned.

        ↓

Agent:
Generate the team plan.
```

---

# 21. Tool Binding

Tools can be attached to the LLM using:

```text
bind_tools()
```

This allows the model to determine when application data is needed.

Conceptually:

```text
LLM
 ↓
Determine required information
 ↓
Tool Call
 ↓
Tool Execution
 ↓
Tool Result
 ↓
LLM continues
```

---

# 22. ReAct-Style Planning

The planner can follow a ReAct-style agent loop:

```text
Reason
  ↓
Select Tool
  ↓
Execute Tool
  ↓
Receive Result
  ↓
Reason Again
  ↓
Select Another Tool
  ↓
...
  ↓
Generate Final Plan
```

This allows the agent to dynamically determine what information it needs before producing the plan.

---

# 23. Multiple Tool Calls

A planner may require several pieces of application data before it can generate a good result.

For example:

```text
get_group_members()
        +
get_user_interests()
        +
get_user_preferences()
        +
get_activity_details()
```

The agent can make multiple tool calls before generating the final plan.

---

# 24. RAG

RAG can be made available as a tool when retrieval of relevant information is useful.

```text
Agent
  ↓
RAG Tool
  ↓
Retrieve Relevant Information
  ↓
Agent
```

RAG is not required for every planner request.

It should be introduced when it provides a real benefit to the planner.

---

# 25. Web Search and Calculator

Web search and calculator are useful LangGraph learning concepts, but neither is a core requirement of the initial NearCast planner.

They should only be introduced when an actual NearCast use case requires them.

The planner should primarily work with NearCast's own application data.

---

# 26. Human-in-the-Loop

The group admin remains the final decision-maker.

Suppose the AI produces:

```text
AI Generated Plan

Rahul → Opener
Aman → Bowler
Vishesh → All-Rounder
```

The admin can accept the plan or provide a correction.

Example:

```text
"Move Rahul to middle order."
```

The planner then uses the current state together with that instruction:

```text
Current Plan
      +
Admin Instruction
      ↓
Update State
      ↓
Re-plan
      ↓
Updated Plan
      ↓
Human Review
```

This creates an iterative planning process rather than a single AI response.

---

# 27. `interrupt()`

LangGraph's `interrupt()` can pause graph execution while waiting for human input.

Example:

```text
Generate Plan
      ↓
Validate Plan
      ↓
interrupt()
      ↓
Admin Review
```

The planning workflow can then continue after the administrator responds.

---

# 28. `Command(resume=...)`

Once the administrator provides an instruction, the graph can resume with that information.

Example:

```text
Admin:
"Move Rahul to middle order."
```

Conceptually:

```text
Previous State
      +
Admin Instruction
      ↓
Command(resume=...)
      ↓
Continue Graph
```

---

# 29. Memory

Memory becomes important when the administrator modifies the same plan multiple times.

Example:

```text
Admin:
Move Rahul to middle order.

AI:
Updated plan.

Admin:
Make Aman captain.

AI:
Updated plan.

Admin:
Remove Raj from the team.
```

The planner needs the previous context so that each new instruction applies to the existing planning session.

---

# 30. `thread_id`

Each planner session can have its own `thread_id`.

Example:

```text
thread_id = group_123_planner_456
```

This allows a particular planning conversation to maintain its own state.

Example:

```text
Group A
 ├── Planner Session 1
 │    └── thread_id: X
 │
 └── Planner Session 2
      └── thread_id: Y
```

---

# 31. Checkpointing

Checkpointing allows graph state to be persisted.

This is particularly useful when the planner pauses for human approval.

```text
Generate Plan
      ↓
Checkpoint
      ↓
Human Review
      ↓
Resume Application
      ↓
Load Previous State
      ↓
Continue Planning
```

A MongoDB checkpointer can be explored for LangGraph checkpoint persistence.

This checkpointing storage is separate from the primary NearCast PostgreSQL database.

---

# 32. Conversation Isolation

`thread_id` also prevents different planning sessions from sharing state accidentally.

Example:

```text
Group A
 └── Cricket Planning
      └── thread_id: cricket_001

Group B
 └── Football Planning
      └── thread_id: football_001
```

Each planning session maintains its own context.

---

# 33. Streaming

The planner should eventually stream AI output to the React frontend.

Architecture:

```text
React
  ↓
FastAPI
  ↓
LangGraph
  ↓
graph.astream()
  ↓
Streaming Response
  ↓
React UI
```

This avoids making the user wait for the entire AI workflow before receiving output.

---

# 34. `graph.astream()`

LangGraph provides asynchronous graph streaming through:

```text
graph.astream()
```

This can be used by the FastAPI layer to stream graph execution/results.

---

# 35. `stream_mode="messages"`

For message-level streaming, NearCast can use:

```text
stream_mode="messages"
```

This allows AI message chunks to be delivered progressively.

---

# 36. FastAPI AI Streaming

The eventual request flow is:

```text
React
   ↓
HTTP Request
   ↓
FastAPI
   ↓
LangGraph
   ↓
Agent
   ↓
Tools
   ↓
LLM
   ↓
graph.astream()
   ↓
FastAPI Streaming Response
   ↓
React
```

The user can therefore see the planner's output as it is produced.

---

# 37. AIInteraction

`AIInteraction` represents communication between a user and the AI system.

It is particularly relevant to conversational features such as the activity/team planner.

Conceptually:

```text
User
  ↓
AI Request
  ↓
AIInteraction
  ↓
AI Processing
  ↓
AI Response
```

It can support:

- Conversation history
- AI usage tracking
- Debugging
- AI interaction analysis
- Planner conversations

The exact database fields will be finalized when the AI models are designed.

---

# 38. Recommendation Model

`Recommendation` represents a recommendation generated for a user.

For NearCast, the final recommendation target is a Group.

```text
User
  ↓
Recommendation Engine
  ↓
Recommendation
  ↓
Recommended Group
```

The primary recommendation modes are:

```text
normal
query
```

### Normal

```text
User Interests
      +
User Preferences
      ↓
User Embedding
      ↓
Similarity Search
      ↓
Candidate Groups
      ↓
Recommended Groups
```

### Query

```text
User Query
      ↓
Query Embedding
      ↓
Search
      │
      ├── User Embeddings
      ├── Activity Embeddings
      └── Group Embeddings
      ↓
Candidate Groups
      ↓
Recommended Groups
```

---

# 39. Interaction vs Recommendation

These two concepts should remain separate.

An interaction describes what the user did.

Examples:

```text
Viewed
Clicked
Saved
Joined
Shared
```

A recommendation describes what the recommendation engine showed.

```text
User
  ↓
Recommended Group
```

Together they form a feedback relationship:

```text
Recommendation
      ↓
User sees Group
      ↓
User interacts
      ↓
Interaction
      ↓
Future Recommendation Signal
```

This can eventually help make recommendations more personalized.

---

# 40. Recommendation Feedback Loop

The longer-term recommendation architecture can evolve into:

```text
User
 ↓
Interests + Preferences
 ↓
User Embedding
 ↓
Recommended Groups
 ↓
User sees recommendation
 ↓
User Interaction
 ↓
Interaction Data
 ↓
Future Recommendation Signals
 ↓
Improved Recommendations
```

The interaction data therefore becomes another potential input for future recommendation improvements.

---

# 41. AI Data and Responsibility Boundaries

NearCast should keep AI responsibilities separate from normal backend responsibilities.

| Requirement | Main Technology |
|---|---|
| User authentication | FastAPI + PostgreSQL |
| Group management | FastAPI + PostgreSQL |
| Activity management | FastAPI + PostgreSQL |
| Nearby users/groups | PostGIS |
| Broadcast delivery | PostGIS + Application Logic |
| Group membership | PostgreSQL |
| Chat | WebSockets + Redis |
| Gamification | Application Logic + PostgreSQL |
| User embeddings | Embedding Model + pgvector |
| Activity embeddings | Embedding Model + pgvector |
| Group embeddings | Embedding Model + pgvector |
| Normal recommendations | Embeddings + pgvector + Ranking |
| Query recommendations | Query Embedding + Vector Search + Ranking |
| Activity/team planning | LangChain + LangGraph + LLM |
| Agent tools | LangGraph Tools |
| Human approval | LangGraph Human-in-the-Loop |
| Planner memory | LangGraph Memory / Checkpointing |
| Planner streaming | LangGraph + FastAPI |

---

# 42. What Is Not Part of the Initial AI Scope

The initial AI implementation will not:

- Recommend activities independently as the final target
- Replace the group administrator
- Automatically finalize a team without human approval
- Use an LLM to calculate basic geographic distances
- Use an LLM for ordinary CRUD operations
- Require web search for recommendations
- Use a generic embedding table
- Give the AI unrestricted direct database access

The intended separation is:

```text
AI
↓
Understands, searches semantically, reasons and plans

Application
↓
Provides business logic and controlled tools

PostgreSQL
↓
Stores application data

PostGIS
↓
Handles geographic operations

pgvector
↓
Handles semantic vector similarity

Human Admin
↓
Maintains final control over AI-generated plans
```

---

# 43. Final AI Architecture

```text
                         NEARCAST AI
                              │
              ┌───────────────┴────────────────┐
              │                                │
              ▼                                ▼
     GROUP RECOMMENDATION              AI ACTIVITY PLANNER
              │                                │
       ┌──────┴──────┐                     LangGraph
       │             │                         │
       ▼             ▼                         ▼
    Normal         Query                    Agent
       │             │                         │
       │             │                  ┌──────┼──────┐
       │             │                  │      │      │
       │             │                State  Tools  Memory
       │             │                  │      │      │
       │             │                Nodes ToolNode Checkpoint
       │             │                  │      │
       │             │              Conditional │
       │             │                Edges     │
       │             │                  │       │
       │             │            Human-in-Loop │
       │             │                  │       │
       │             │                  ▼       │
       │             │             Final Plan   │
       │             │
       └──────┬──────┘
              │
              ▼
         Embeddings
              │
       ┌──────┼──────────┐
       ▼      ▼          ▼
      User  Activity    Group
   Embedding Embedding Embedding
       │      │          │
       └──────┼──────────┘
              ▼
           pgvector
              │
              ▼
       Candidate Groups
              │
              ▼
      Recommended Groups
```

---

# 44. Technology Stack

```text
                         NearCast AI
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ▼                                 ▼
       Recommendation                    Activity Planner
             │                                 │
             │                              LangChain
             │                                 │
             │                              LangGraph
             │                                 │
             │                    ┌────────────┼────────────┐
             │                    │            │            │
             │                  State        Tools        Memory
             │                    │            │            │
             │                  Nodes       ToolNode   Checkpointing
             │                    │            │            │
             │                  Edges     Tool Calling  thread_id
             │                    │            │
             │             Conditional     Agent Loop
             │                Edges
             │                    │
             │             Human-in-Loop
             │
             ▼
         Embeddings
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
     User  Activity Group
   Embedding Embedding Embedding
       │     │     │
       └─────┼─────┘
             ▼
          pgvector
             │
             ▼
      Recommended Groups
```

---

# 45. Core NearCast AI Features

The actual product-level AI features are:

1. Normal Group Recommendation
2. Query-Based Group Recommendation
3. AI Activity / Team Planner
4. Human-Controlled AI Planning

---

# 46. LangGraph Learning Concepts Applied to the Project

The LangGraph concepts that will have practical use in NearCast are:

1. LangGraph
2. Chain vs Graph
3. State
4. `TypedDict`
5. Message State
6. `add_messages`
7. Nodes
8. Node Functions
9. Edges
10. `START`
11. `END`
12. Conditional Edges
13. Routing Functions
14. Loops
15. Tools
16. `ToolNode`
17. `bind_tools()`
18. LLM Tool Calling
19. ReAct-style Agent Loop
20. Multiple Tool Calls
21. RAG as a Tool
22. Memory
23. `thread_id`
24. Checkpointing
25. MongoDB Checkpointer
26. Conversation Isolation
27. Human-in-the-Loop
28. `interrupt()`
29. `Command(resume=...)`
30. Streaming
31. `graph.astream()`
32. `stream_mode="messages"`
33. FastAPI Agent Streaming

---

# 47. Development Roadmap

The AI implementation should be developed progressively.

```text
Embedding Foundation
        ↓
User / Activity / Group Embeddings
        ↓
Normal Group Recommendation
        ↓
Query-Based Group Recommendation
        ↓
Recommendation API
        ↓
LangChain Tools
        ↓
LangGraph Activity Planner
        ↓
State + Nodes + Edges
        ↓
Agent + Tool Calling
        ↓
Conditional Edges + Loops
        ↓
Memory + thread_id + Checkpointing
        ↓
Human-in-the-Loop
        ↓
Streaming through FastAPI
        ↓
React AI UI
        ↓
Testing + Evaluation
```

---

# 48. Final Goal

NearCast's AI layer demonstrates two distinct AI approaches.

## Semantic Recommendation

```text
Embeddings
+
pgvector
+
Vector Similarity
+
Ranking
```

This system finds relevant existing groups using the user's profile or an explicit query.

## Agentic Activity Planning

```text
LLM
+
LangChain
+
LangGraph
+
State
+
Nodes
+
Edges
+
Tools
+
Tool Calling
+
Memory
+
Checkpointing
+
Human-in-the-Loop
+
Streaming
```

This system uses group and member information to generate activity/team plans and allows the group administrator to review, modify, and approve the AI's proposal.

The overall design therefore keeps the responsibilities clear:

```text
Recommendation System
        ↓
Find relevant existing groups

AI Planner
        ↓
Plan activities/teams for a selected group

Human Admin
        ↓
Approve or modify the AI plan
```
