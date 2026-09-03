# Activity Models

This folder contains models related to activities, participants, locations, AI embeddings, and saved activities.

## Models

### 1. Activity

**Table:** `activities`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique activity ID |
| `group_id` | UUID | Reference to Group |
| `title` | String | Activity name |
| `description` | Text | Activity description |
| `starts_at` | DateTime | Activity start time |
| `ends_at` | DateTime | Activity end time |
| `is_public` | Boolean | Public/private activity |
| `is_active` | Boolean | Activity status |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** `Group 1:N Activity`

**Stores:** The actual activity/event created in NearCast.

---

### 2. ActivityParticipant

**Table:** `activity_participants`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique participant record |
| `activity_id` | UUID | Reference to Activity |
| `user_id` | UUID | Reference to User |
| `status` | String | Participation status |
| `joined_at` | DateTime | When user joined |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:**
- `Activity 1:N ActivityParticipant`
- `User 1:N ActivityParticipant`

**Stores:** Users who participate in an activity.

---

### 3. ActivityEmbedding

**Table:** `activity_embeddings`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique embedding ID |
| `activity_id` | UUID | Reference to Activity |
| `embedding` | Vector(384) | Activity's semantic vector |
| `model_name` | String | Embedding model used |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** `Activity 1:1 ActivityEmbedding`

**Stores:** AI/vector representation of the activity generated from relevant activity information such as title and description.

---

### 4. ActivityLocation

**Table:** `activity_locations`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique location record |
| `activity_id` | UUID | Reference to Activity |
| `location` | Geography | Geographic point |
| `name` | String | Location name |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** `Activity 1:N ActivityLocation`

**Stores:** Geographic location information associated with an activity.

---

### 5. SavedActivity

**Table:** `saved_activities`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique saved record |
| `user_id` | UUID | Reference to User |
| `activity_id` | UUID | Reference to Activity |
| `saved_at` | DateTime | When activity was saved |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:**
- `User 1:N SavedActivity`
- `Activity 1:N SavedActivity`

**Stores:** Activities that users have saved/bookmarked for later.

---

## Relationship Summary

| Relationship | Mapping | Purpose |
|---|---|---|
| Group → Activity | 1:N | A group can organize multiple activities |
| Activity → ActivityParticipant | 1:N | An activity can have multiple participants |
| User → ActivityParticipant | 1:N | A user can participate in multiple activities |
| Activity → ActivityEmbedding | 1:1 | One AI embedding per activity |
| Activity → ActivityLocation | 1:N | An activity can have location records |
| User → SavedActivity | 1:N | A user can save multiple activities |
| Activity → SavedActivity | 1:N | An activity can be saved by multiple users |

## Important Distinction

| Model | Meaning |
|---|---|
| `ActivityParticipant` | User joined/participates in the activity |
| `SavedActivity` | User saved/bookmarked the activity |
| `UserActivityInteraction` | User interacted with the activity, e.g. viewed, clicked, saved, joined |