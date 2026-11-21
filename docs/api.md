# Section 4: API Contract Specification (`/api/v1/...`)

All endpoints are versioned under `/api/v1` and follow strict REST principles, standard HTTP status codes, and unified JSON envelopes.

---

## 1. Authentication & Security Standard

1. **JWT Verification**: Every protected route requires the header:
   ```
   Authorization: Bearer <supabase_access_token>
   ```
   The backend verifies the token using the Supabase JWT Secret (`SUPABASE_JWT_SECRET`) or Supabase Public Key JWKS.
2. **Identity Derivation**: `user_id` is strictly extracted from the verified JWT `sub` claim. It is **never** accepted from query parameters, path variables, or request bodies.
3. **Unified Error Envelope**:
   ```json
   {
     "error": {
       "code": "VALIDATION_ERROR | UNAUTHORIZED | FORBIDDEN | NOT_FOUND | RATE_LIMITED | SAFETY_VIOLATION | INTERNAL_ERROR",
       "message": "Human-readable diagnostic message.",
       "details": [
         { "field": "time_availability_mins", "issue": "Value must be between 10 and 180" }
       ],
       "timestamp": "2026-11-21T15:30:00Z"
     }
   }
   ```
4. **Idempotency Keys**: Mutating endpoints (e.g., logging sets, finishing workouts) accept an optional `Idempotency-Key: <uuid>` header to prevent duplicate execution during network retries.

---

## 2. Endpoint Catalog

### 2.1 Health & Diagnostics
- `GET /api/v1/health`
  - **Auth**: None
  - **Response 200**:
    ```json
    { "status": "healthy", "version": "1.0.0", "database": "connected", "timestamp": "2026-11-21T15:30:00Z" }
    ```

---

### 2.2 Profile & Onboarding

#### `GET /api/v1/profile`
- **Auth**: Required
- **Response 200**:
  ```json
  {
    "id": "c1f7a4e2-...",
    "email": "athlete@example.com",
    "full_name": "Jordan Vance",
    "role": "user",
    "has_completed_onboarding": true,
    "created_at": "2026-11-20T10:00:00Z"
  }
  ```

#### `GET /api/v1/onboarding`
- **Auth**: Required
- **Description**: Retrieves current onboarding preferences or draft.
- **Response 200**: Returns preferences object or `null` if untouched.

#### `POST /api/v1/onboarding`
- **Auth**: Required
- **Description**: Saves or finalizes onboarding configuration. Enforces age group and safety acceptance.
- **Request Body**:
  ```json
  {
    "age_group": "adult_18_64",
    "experience_level": "intermediate",
    "fitness_goals": ["hypertrophy", "mobility"],
    "workout_location": "commercial_gym",
    "available_equipment": ["barbell", "dumbbells", "cable_machine", "bench"],
    "preferred_activities": ["strength", "rowing"],
    "time_availability_mins": 45,
    "preferred_days": [1, 3, 5],
    "disclaimer_accepted": true
  }
  ```
- **Response 201**: Saved preferences object with `completed_at` timestamp.

---

### 2.3 Exercise Library

#### `GET /api/v1/exercises`
- **Auth**: Optional / Authenticated
- **Query Params**:
  - `category` (string, optional: `strength`, `cardio`, `mobility`)
  - `difficulty` (string, optional: `beginner`, `intermediate`, `advanced`)
  - `muscle` (string, optional: `chest`, `quadriceps`, `lats`)
  - `equipment` (string, optional: `barbell`, `bodyweight`, `dumbbells`)
  - `search` (string, optional: search query on name and tips)
  - `page` (int, default: 1)
  - `page_size` (int, default: 20, max: 100)
- **Response 200**:
  ```json
  {
    "data": [
      {
        "id": "e4a1b2c3-...",
        "slug": "barbell-romanian-deadlift",
        "name": "Barbell Romanian Deadlift",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["hamstrings", "glutes"],
        "secondary_muscles": ["erector_spinae", "forearms"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64", "senior_65_plus"],
        "media": [
          {
            "media_type": "image",
            "url": "https://images.unsplash.com/...",
            "license_type": "Unsplash",
            "attribution_text": "Photo by Victor Freitas on Unsplash"
          }
        ]
      }
    ],
    "pagination": { "page": 1, "page_size": 20, "total_records": 84, "total_pages": 5 }
  }
  ```

#### `GET /api/v1/exercises/{slug}`
- **Auth**: Optional / Authenticated
- **Response 200**: Detailed exercise data including step-by-step instructions, setup tips, contraindications, and video/GIF links.

---

### 2.4 Workouts & Session Management

#### `POST /api/v1/workouts/generate`
- **Auth**: Required
- **Description**: Generates a tailored weekly plan based on the user's active profile and onboarding data.
- **Request Body**:
  ```json
  {
    "cycle_type": "weekly",
    "override_focus": null
  }
  ```
- **Response 201**: Newly generated `workout_plan` containing nested daily `workout_sessions`.

#### `GET /api/v1/workouts/today`
- **Auth**: Required
- **Description**: Retrieves today's active workout session and associated exercise sequence.
- **Response 200**:
  ```json
  {
    "session_id": "s8d2e1-...",
    "title": "Lower Body Posterior Chain & Core",
    "focus_area": "Hamstrings & Glutes",
    "planned_duration_mins": 45,
    "status": "scheduled",
    "exercises": [
      {
        "session_exercise_id": "se-01-...",
        "exercise_order": 1,
        "exercise": {
          "id": "e4a1b2c3-...",
          "name": "Barbell Romanian Deadlift",
          "slug": "barbell-romanian-deadlift"
        },
        "target_sets": 4,
        "target_reps": 10,
        "target_rest_secs": 90,
        "is_completed": false,
        "logs": []
      }
    ]
  }
  ```

#### `POST /api/v1/workouts/sessions/{id}/start`
- **Auth**: Required
- **Description**: Transitions session status to `in_progress`.

#### `POST /api/v1/workouts/sessions/{id}/log-exercise`
- **Auth**: Required
- **Request Body**:
  ```json
  {
    "session_exercise_id": "se-01-...",
    "set_number": 1,
    "weight_kg": 80.0,
    "reps_performed": 10,
    "rpe": 8
  }
  ```
- **Response 201**: Persisted `exercise_log` entry.

#### `POST /api/v1/workouts/sessions/{id}/complete`
- **Auth**: Required
- **Headers**: `Idempotency-Key` (UUID)
- **Request Body**:
  ```json
  {
    "perceived_exertion": 8,
    "notes": "Hamstrings felt engaged. Increased load on 3rd set.",
    "feedback": {
      "energy_rating": 4,
      "difficulty_rating": 4,
      "soreness_level": "moderate"
    }
  }
  ```
- **Response 200**: Updated session object with summary stats.

#### `POST /api/v1/workouts/sessions/{id}/exercises/{exercise_id}/swap`
- **Auth**: Required
- **Description**: Replaces an exercise in the session with an age- and equipment-compatible alternative.
- **Request Body**:
  ```json
  {
    "reason": "equipment_unavailable | joint_discomfort | preference"
  }
  ```
- **Response 200**: Returns replacement exercise and updated session plan.

---

### 2.5 Schedule & Calendar

#### `GET /api/v1/schedule`
- **Auth**: Required
- **Query Params**: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD)
- **Response 200**: List of scheduled workout days, rest days, and completion flags.

#### `PATCH /api/v1/schedule/{id}/reschedule`
- **Auth**: Required
- **Request Body**:
  ```json
  { "new_date": "2026-11-25" }
  ```
- **Response 200**: Updated schedule entry.

---

### 2.6 AI Assistant & RAG Chat

#### `POST /api/v1/chat/conversations`
- **Auth**: Required
- **Request Body**: `{ "title": "Knee-friendly quad alternatives" }`
- **Response 201**: Created conversation entity.

#### `GET /api/v1/chat/conversations`
- **Auth**: Required
- **Response 200**: List of recent conversation threads with timestamps.

#### `POST /api/v1/chat/conversations/{id}/messages`
- **Auth**: Required
- **Rate Limit**: 15 requests / minute per user
- **Request Body**:
  ```json
  {
    "content": "Can I replace back squats today? My lower back is slightly fatigued."
  }
  ```
- **Response (Server-Sent Events streaming `text/event-stream` or JSON)**:
  - Event `meta`: Intent classification & safety status.
  - Event `token`: Incremental response tokens.
  - Event `citations`: Knowledge base sources retrieved via RAG.
  - Event `done`: Full persisted message payload with token usage.

---

### 2.7 Progress, Analytics & Reports

#### `GET /api/v1/progress/summary`
- **Auth**: Required
- **Query Params**: `timeframe` (`7d`, `30d`, `90d`)
- **Response 200**:
  ```json
  {
    "timeframe": "30d",
    "consistency_percentage": 88.5,
    "completed_workouts": 14,
    "total_volume_kg": 42500,
    "total_active_mins": 630,
    "streak_days": 4,
    "muscle_group_distribution": {
      "quadriceps": 28,
      "hamstrings": 24,
      "chest": 20,
      "back": 28
    }
  }
  ```

#### `GET /api/v1/progress/report/pdf`
- **Auth**: Required
- **Description**: Generates and streams an authentic, cleanly formatted PDF activity report.
- **Response 200**: `application/pdf` binary stream.

---

### 2.8 Account Privacy & GDPR

#### `GET /api/v1/profile/export`
- **Auth**: Required
- **Response 200**: Complete JSON bundle of all user profile, onboarding, logs, feedback, and chat messages.

#### `DELETE /api/v1/profile`
- **Auth**: Required
- **Request Body**: `{ "confirm_email": "athlete@example.com" }`
- **Response 204**: Cascade deletes all user data from Supabase and terminates session.
