# User Models

This folder contains models related to users, their interests, preferences,
locations, AI embeddings, and interactions.

## Models

### 1. User

**Table:** `users`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique user ID |
| `username` | String | User's username |
| `email` | String | User's email |
| `password_hash` | String | Hashed password |
| `is_active` | Boolean | User account status |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** Base entity for all user-related models.

**Stores:** Basic user/account information.

---

### 2. Interest

**Table:** `interests`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique interest ID |
| `name` | String | Interest name |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** Many-to-Many with `User` through `UserInterest`.

**Stores:** Available interests such as Cricket, Hiking, Football, etc.

---

### 3. UserInterest

**Table:** `user_interests`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique record ID |
| `user_id` | UUID | Reference to User |
| `interest_id` | UUID | Reference to Interest |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** Junction table for `User ↔ Interest`.

**Stores:** Which interests belong to which users.

---

### 4. UserPreference

**Table:** `user_preferences`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique preference ID |
| `user_id` | UUID | Reference to User |
| `max_distance_km` | Float | Maximum discovery distance |
| `preferred_group_size` | Integer | Preferred group size |
| `preferred_activity_type` | String | Preferred activity type |
| `notifications_enabled` | Boolean | Notification preference |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** One-to-One with `User`.

**Stores:** User's discovery and activity preferences.

---

### 5. UserLocation

**Table:** `user_locations`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique location record ID |
| `user_id` | UUID | Reference to User |
| `location` | Geography | User's geographic location |
| `is_current` | Boolean | Whether this is the current location |
| `recorded_at` | DateTime | When location was recorded |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** One-to-Many with `User`.

**Stores:** User's current and historical locations.

---

### 6. UserEmbedding

**Table:** `user_embeddings`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique embedding ID |
| `user_id` | UUID | Reference to User |
| `source_text` | Text | User information converted into embedding input |
| `embedding` | Vector(384) | User's semantic vector |
| `model_name` | String | Embedding model used |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** One-to-One with `User`.

**Stores:** AI representation of the user's interests, preferences, and other relevant profile information.

---

### 7. UserActivityInteraction

**Table:** `user_activity_interactions`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique interaction ID |
| `user_id` | UUID | Reference to User |
| `activity_id` | UUID | Reference to Activity |
| `interaction_type` | String | Type of interaction |
| `occurred_at` | DateTime | When interaction occurred |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** One-to-Many with `User`.

**Stores:** User behavior toward activities such as viewed, clicked, saved, or joined.

---

### 8. UserGroupInteraction

**Table:** `user_group_interactions`

| Field | Type | Purpose |
|---|---|---|
| `id` | UUID | Unique interaction ID |
| `user_id` | UUID | Reference to User |
| `group_id` | UUID | Reference to Group |
| `interaction_type` | String | Type of interaction |
| `occurred_at` | DateTime | When interaction occurred |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

**Mapping:** One-to-Many with `User`.

**Stores:** User behavior toward groups such as viewed, clicked, joined, or left.

---

## Relationship Summary

| Model | Mapping |
|---|---|
| User ↔ Interest | Many-to-Many |
| User ↔ UserInterest | One-to-Many |
| User ↔ UserPreference | One-to-One |
| User ↔ UserLocation | One-to-Many |
| User ↔ UserEmbedding | One-to-One |
| User ↔ UserActivityInteraction | One-to-Many |
| User ↔ UserGroupInteraction | One-to-Many |