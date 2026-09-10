# NearCast Database Models

This document describes the database models used by NearCast.

The models are organized by domain:

- User
- Group
- Activity
- Chat
- AI
- Common

---

# 1. User

Folder:

`server/app/models/user/`

The User domain stores information about users, their interests, preferences, locations, embeddings, and interactions.

## Models

### User

Stores basic user account information.

| Field | Description |
|---|---|
| id | Unique user ID |
| username | User's username |
| email | User's email |
| password_hash | Hashed password |
| is_active | Whether the account is active |
| created_at | Account creation time |
| updated_at | Last update time |

### Interest

Stores available interests.

| Field | Description |
|---|---|
| id | Unique interest ID |
| name | Interest name |
| created_at | Creation time |
| updated_at | Last update time |

Examples:

- Cricket
- Football
- Music
- Photography
- Gaming

### UserInterest

Connects users with their interests.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| interest_id | Interest ID |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → UserInterest ← Interest`

One user can have many interests.

One interest can belong to many users.

---

### UserPreference

Stores user activity and recommendation preferences.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| max_distance_km | Maximum preferred distance |
| preferred_group_size | Preferred group size |
| preferred_activity_type | Preferred activity type |
| notifications_enabled | Notification setting |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → UserPreference`

One user has one preference record.

---

### UserLocation

Stores the user's location.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| location | Geographic location |
| is_current | Whether this is the current location |
| recorded_at | Time when location was recorded |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → UserLocation`

One user can have multiple location records.

---

### UserEmbedding

Stores the AI embedding generated for a user.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| source_text | Text used to create embedding |
| embedding | Vector representation |
| model_name | Embedding model used |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → UserEmbedding`

One user has one current embedding.

Used by the recommendation agent.

---

### UserActivityInteraction

Stores how a user interacts with activities.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| activity_id | Activity ID |
| interaction_type | Type of interaction |
| occurred_at | Interaction time |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → UserActivityInteraction ← Activity`

---

### UserGroupInteraction

Stores how a user interacts with groups.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| group_id | Group ID |
| interaction_type | Type of interaction |
| occurred_at | Interaction time |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → UserGroupInteraction ← Group`

---

# 2. Group

Folder:

`server/app/models/group/`

The Group domain stores groups, members, locations, embeddings, and group broadcasts.

## Models

### Group

Stores a NearCast group.

| Field | Description |
|---|---|
| id | Unique group ID |
| name | Group name |
| description | Group description |
| is_private | Whether the group is private |
| is_active | Whether the group is active |
| created_at | Creation time |
| updated_at | Last update time |

Example:

`Sunday Cricket Group`

---

### GroupMember

Connects users with groups.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| group_id | Group ID |
| role | Member role |
| joined_at | Join time |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → GroupMember ← Group`

This is a many-to-many relationship.

A user can join many groups.

A group can have many users.

Group members automatically get access to the group's chat.

---

### GroupLocation

Stores the group's location.

| Field | Description |
|---|---|
| id | Unique ID |
| group_id | Group ID |
| location | Geographic location |
| name | Location name |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Group → GroupLocation`

One group has one main location.

---

### GroupEmbedding

Stores the AI embedding for a group.

| Field | Description |
|---|---|
| id | Unique ID |
| group_id | Group ID |
| embedding | Vector representation |
| model_name | Embedding model used |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Group → GroupEmbedding`

One group has one embedding.

Used by the recommendation agent.

---

### Broadcast

Stores announcements sent by a group.

| Field | Description |
|---|---|
| id | Unique broadcast ID |
| group_id | Group ID |
| title | Broadcast title |
| message | Broadcast message |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Group → Broadcast`

---

# 3. Activity

Folder:

`server/app/models/activity/`

The Activity domain stores activities created by groups and information about participation, locations, embeddings, and saved activities.

## Models

### Activity

Stores an activity created by a group.

| Field | Description |
|---|---|
| id | Unique activity ID |
| group_id | Group ID |
| title | Activity title |
| description | Activity description |
| starts_at | Start time |
| ends_at | End time |
| is_public | Whether activity is public |
| is_active | Whether activity is active |
| created_at | Creation time |
| updated_at | Last update time |

Example:

`Sunday Cricket Match`

Relationship:

`Group → Activity`

One group can create many activities.

---

### ActivityParticipant

Connects users with activities.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| activity_id | Activity ID |
| status | Participation status |
| joined_at | Join time |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → ActivityParticipant ← Activity`

This is a many-to-many relationship.

---

### ActivityLocation

Stores locations for an activity.

| Field | Description |
|---|---|
| id | Unique ID |
| activity_id | Activity ID |
| location | Geographic location |
| name | Location name |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Activity → ActivityLocation`

One activity can have one or more locations.

---

### ActivityEmbedding

Stores the AI embedding for an activity.

| Field | Description |
|---|---|
| id | Unique ID |
| activity_id | Activity ID |
| embedding | Vector representation |
| model_name | Embedding model used |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Activity → ActivityEmbedding`

One activity has one embedding.

Used by the query recommendation flow.

---

### SavedActivity

Stores activities saved by users.

| Field | Description |
|---|---|
| id | Unique ID |
| user_id | User ID |
| activity_id | Activity ID |
| saved_at | Save time |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → SavedActivity ← Activity`

---

# 4. Chat

Folder:

`server/app/models/chat/`

The Chat domain stores group messages and polls.

Group members automatically have access to the group's chat.

## Models

### Chat

Stores a group's chat.

| Field | Description |
|---|---|
| id | Unique chat ID |
| group_id | Group ID |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Group → Chat`

---

### Message

Stores messages sent in a chat.

| Field | Description |
|---|---|
| id | Unique message ID |
| chat_id | Chat ID |
| user_id | Sender ID |
| content | Message content |
| created_at | Creation time |
| updated_at | Last update time |

Relationships:

`Chat → Message`

`User → Message`

---

### Poll

Stores polls created inside a chat.

| Field | Description |
|---|---|
| id | Unique poll ID |
| chat_id | Chat ID |
| creator_id | User who created poll |
| question | Poll question |
| is_multiple_choice | Whether multiple options can be selected |
| is_closed | Whether poll is closed |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Chat → Poll`

---

### PollOption

Stores options belonging to a poll.

| Field | Description |
|---|---|
| id | Unique option ID |
| poll_id | Poll ID |
| option_text | Option text |
| position | Display order |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`Poll → PollOption`

---

### PollVote

Stores user votes on poll options.

| Field | Description |
|---|---|
| id | Unique vote ID |
| poll_id | Poll ID |
| option_id | Selected option |
| user_id | User who voted |
| voted_at | Vote time |
| created_at | Creation time |
| updated_at | Last update time |

Relationships:

`Poll → PollVote`

`PollOption → PollVote`

`User → PollVote`

---

# 5. AI

Folder:

`server/app/models/ai/`

The AI domain stores AI interactions and generated recommendations.

## Models

### AIInteraction

Stores conversations/interactions between a user and an AI agent.

| Field | Description |
|---|---|
| id | Unique interaction ID |
| user_id | User ID |
| type | Type of AI interaction |
| input | User input |
| output | AI output |
| created_at | Creation time |
| updated_at | Last update time |

Examples:

- activity planning
- recommendation query
- team planning

Relationship:

`User → AIInteraction`

---

### Recommendation

Stores recommendations generated for users.

| Field | Description |
|---|---|
| id | Unique recommendation ID |
| user_id | User ID |
| group_id | Recommended group |
| recommendation_type | Recommendation type |
| score | Recommendation score |
| status | Recommendation status |
| recommended_at | Recommendation time |
| created_at | Creation time |
| updated_at | Last update time |

Recommendation types:

- normal
- query

The final recommendation target is always a Group.

Relationship:

`User → Recommendation ← Group`

---

# 6. Common

Folder:

`server/app/models/common/`

Common models contain functionality shared across multiple domains.

## Models

### JoinRequest

Stores requests to join groups.

| Field | Description |
|---|---|
| id | Unique request ID |
| user_id | User ID |
| group_id | Group ID |
| status | Request status |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → JoinRequest ← Group`

---

### Location

Location is not a normal database table.

It provides reusable geographic location fields for:

- UserLocation
- GroupLocation
- ActivityLocation

The location is stored using PostGIS.

---

### Notification

Stores notifications sent to users.

| Field | Description |
|---|---|
| id | Unique notification ID |
| user_id | User ID |
| title | Notification title |
| message | Notification message |
| type | Notification type |
| is_read | Whether notification was read |
| created_at | Creation time |
| updated_at | Last update time |

Relationship:

`User → Notification`

---

# Overall Relationships

```text
User
 │
 ├── UserInterest ── Interest
 ├── UserPreference
 ├── UserLocation
 ├── UserEmbedding
 ├── UserActivityInteraction ── Activity
 ├── UserGroupInteraction ── Group
 ├── GroupMember ── Group
 ├── ActivityParticipant ── Activity
 ├── SavedActivity ── Activity
 ├── AIInteraction
 ├── Recommendation ── Group
 ├── JoinRequest ── Group
 ├── Notification
 └── PollVote ── Poll ── PollOption

Group
 │
 ├── GroupMember
 ├── GroupLocation
 ├── GroupEmbedding
 ├── Broadcast
 ├── Activity
 └── Chat

Activity
 │
 ├── ActivityParticipant
 ├── ActivityLocation
 ├── ActivityEmbedding
 └── SavedActivity

Chat
 │
 ├── Message
 └── Poll
      │
      ├── PollOption
      └── PollVote
```

# AI Data Flow

```text
User
 │
 ├── Interests
 ├── Preferences
 └── UserEmbedding
          │
          ▼
   Recommendation Agent
          │
          ▼
     GroupEmbedding
          │
          ▼
   Recommended Groups
```

For natural-language search:

```text
User Query
    │
    ▼
Query Embedding
    │
    ├── UserEmbedding
    ├── ActivityEmbedding
    └── GroupEmbedding
            │
            ▼
      Matching Groups
            │
            ▼
      Recommendations
```

For activity planning:

```text
User
  │
  ▼
Group
  │
  ├── Members
  ├── Interests
  ├── Preferences
  └── Activities
          │
          ▼
   Planner Agent
          │
          ▼
   Activity / Team Plan
```

# Important Design Rules

1. `User` stores account information.
2. `Group` stores communities.
3. `GroupMember` is the main User ↔ Group relationship.
4. `Activity` belongs to a Group.
5. `ActivityParticipant` is the main User ↔ Activity relationship.
6. `Chat` belongs to a Group.
7. Group members automatically get access to the Group chat.
8. `UserEmbedding`, `GroupEmbedding`, and `ActivityEmbedding` store AI vectors.
9. The recommendation agent ultimately recommends existing Groups.
10. AI agents access application data through tools/services rather than directly accessing the database.
11. PostGIS is used for geographic location data.
12. pgvector is used for embeddings.
13. Additional domains such as gamification, payments, analytics, and moderation can be added later.
