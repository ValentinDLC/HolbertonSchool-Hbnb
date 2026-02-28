# HBnB Part 2 — Testing Report

## Overview

This report documents the validation logic and test cases implemented for all
five REST API endpoints of the HBnB Part 2 project.

**Stack:** Python 3 · Flask · flask-restx · unittest  
**Test runner:** `python -m pytest tests/ -v` or `python -m unittest discover tests/`

---

## How to Run the Tests

```bash
# From the project root (hbnb/)
pip install flask flask-restx pytest

# Run all tests with verbose output
python -m pytest tests/ -v

# Or with unittest
python -m unittest discover tests/
```

---

## 1. Users — `/api/v1/users/`

### Validation rules implemented

| Field | Rule |
|---|---|
| `first_name` | Required, 1–50 characters |
| `last_name` | Required, 1–50 characters |
| `email` | Required, valid format (`x@x.x`), must be unique |

### Test cases

| # | Test | Input | Expected | Description |
|---|---|---|---|---|
| U1 | `test_create_user_success` | Valid payload | 201 | Happy path — user created |
| U2 | `test_create_user_duplicate_email` | Same email twice | 400 | Email uniqueness enforced |
| U3 | `test_create_user_invalid_email` | `"not-an-email"` | 400 | Regex validation fails |
| U4 | `test_create_user_empty_first_name` | `first_name: ""` | 400 | Empty string rejected |
| U5 | `test_create_user_first_name_too_long` | 51-char string | 400 | Length limit enforced |
| U6 | `test_create_user_missing_fields` | Empty JSON `{}` | 400 | Required fields enforced by flask-restx |
| U7 | `test_get_all_users` | GET `/` | 200 + list | Returns list |
| U8 | `test_get_user_by_id_success` | Valid UUID | 200 | Found |
| U9 | `test_get_user_by_id_not_found` | `"nonexistent-id"` | 404 | Not found |
| U10 | `test_update_user_success` | Valid update | 200 | Fields updated |
| U11 | `test_update_user_not_found` | Fake UUID | 404 | Not found |

---

## 2. Amenities — `/api/v1/amenities/`

### Validation rules implemented

| Field | Rule |
|---|---|
| `name` | Required, 1–50 characters |

### Test cases

| # | Test | Input | Expected | Description |
|---|---|---|---|---|
| A1 | `test_create_amenity_success` | `{"name": "WiFi"}` | 201 | Happy path |
| A2 | `test_create_amenity_empty_name` | `{"name": ""}` | 400 | Empty name rejected |
| A3 | `test_create_amenity_name_too_long` | 51-char name | 400 | Length limit |
| A4 | `test_create_amenity_missing_name` | `{}` | 400 | Required field |
| A5 | `test_get_all_amenities` | GET `/` | 200 + list | Returns list |
| A6 | `test_get_amenity_by_id_success` | Valid UUID | 200 | Found |
| A7 | `test_get_amenity_not_found` | Fake UUID | 404 | Not found |
| A8 | `test_update_amenity_success` | Valid update | 200 | Updated |
| A9 | `test_update_amenity_not_found` | Fake UUID | 404 | Not found |

---

## 3. Places — `/api/v1/places/`

### Validation rules implemented

| Field | Rule |
|---|---|
| `title` | Required, 1–100 characters |
| `price` | ≥ 0 |
| `latitude` | −90 ≤ value ≤ 90 |
| `longitude` | −180 ≤ value ≤ 180 |
| `owner_id` | Must reference an existing User |

### Test cases

| # | Test | Input | Expected | Description |
|---|---|---|---|---|
| P1 | `test_create_place_success` | Full valid payload | 201 | Happy path |
| P2 | `test_create_place_empty_title` | `title: ""` | 400 | Empty title rejected |
| P3 | `test_create_place_negative_price` | `price: -10` | 400 | Negative price rejected |
| P4 | `test_create_place_zero_price_allowed` | `price: 0` | 201 | Free listings allowed |
| P5 | `test_create_place_latitude_out_of_range` | `latitude: 91` | 400 | Out-of-range latitude |
| P6 | `test_create_place_latitude_negative_boundary` | `latitude: -91` | 400 | Out-of-range latitude (negative) |
| P7 | `test_create_place_longitude_out_of_range` | `longitude: 181` | 400 | Out-of-range longitude |
| P8 | `test_create_place_longitude_negative_boundary` | `longitude: -181` | 400 | Out-of-range longitude (negative) |
| P9 | `test_create_place_invalid_owner` | Fake `owner_id` | 404 | Owner not found |
| P10 | `test_create_place_boundary_latitude_valid` | `latitude: 90` | 201 | Exact boundary valid |
| P11 | `test_get_all_places` | GET `/` | 200 + list | Returns list |
| P12 | `test_get_place_by_id_success` | Valid UUID | 200 + `owner` embedded | Enriched response |
| P13 | `test_get_place_not_found` | Fake UUID | 404 | Not found |
| P14 | `test_update_place_success` | Valid update | 200 | Updated |
| P15 | `test_update_place_not_found` | Fake UUID | 404 | Not found |

---

## 4. Reviews — `/api/v1/reviews/`

### Validation rules implemented

| Field | Rule |
|---|---|
| `text` | Required, non-empty |
| `rating` | Integer, 1–5 |
| `user_id` | Must reference an existing User |
| `place_id` | Must reference an existing Place |

### Test cases

| # | Test | Input | Expected | Description |
|---|---|---|---|---|
| R1 | `test_create_review_success` | Full valid payload | 201 | Happy path |
| R2 | `test_create_review_empty_text` | `text: ""` | 400 | Empty text rejected |
| R3 | `test_create_review_rating_too_low` | `rating: 0` | 400 | Below minimum |
| R4 | `test_create_review_rating_too_high` | `rating: 6` | 400 | Above maximum |
| R5 | `test_create_review_invalid_user` | Fake `user_id` | 404 | User not found |
| R6 | `test_create_review_invalid_place` | Fake `place_id` | 404 | Place not found |
| R7 | `test_create_review_boundary_rating_1` | `rating: 1` | 201 | Lower boundary valid |
| R8 | `test_get_all_reviews` | GET `/` | 200 + list | Returns list |
| R9 | `test_get_review_by_id_success` | Valid UUID | 200 | Found |
| R10 | `test_get_review_not_found` | Fake UUID | 404 | Not found |
| R11 | `test_get_reviews_by_place` | Valid place UUID | 200 + list | Filtered list |
| R12 | `test_get_reviews_by_place_not_found` | Fake place UUID | 404 | Not found |
| R13 | `test_update_review_success` | Valid update | 200 | Updated |
| R14 | `test_update_review_not_found` | Fake UUID | 404 | Not found |
| R15 | `test_delete_review_success` | Valid UUID | 200 | Deleted |
| R16 | `test_delete_review_not_found` | Fake UUID | 404 | Not found |
| R17 | `test_deleted_review_no_longer_accessible` | Deleted UUID | 404 | Confirmed deleted |

---

## 5. Bookings — `/api/v1/bookings/`

### Validation rules implemented

| Field | Rule |
|---|---|
| `check_in` | Date format `YYYY-MM-DD`, not in the past |
| `check_out` | Strictly after `check_in` |
| `guests` | ≥ 1 |
| `place_id` | Must reference an existing Place |
| `user_id` | Must reference an existing User |
| Overlap | No two active bookings on same place can share dates |

### Test cases

| # | Test | Input | Expected | Description |
|---|---|---|---|---|
| B1 | `test_create_booking_success` | Full valid payload | 201 + `status: pending` | Happy path |
| B2 | `test_create_booking_invalid_place` | Fake `place_id` | 404 | Place not found |
| B3 | `test_create_booking_invalid_user` | Fake `user_id` | 404 | User not found |
| B4 | `test_create_booking_checkout_before_checkin` | `check_out < check_in` | 400 | Invalid date range |
| B5 | `test_create_booking_guests_zero` | `guests: 0` | 400 | Min guests not met |
| B6 | `test_create_booking_overlap` | Overlapping dates | 409 | Conflict detected |
| B7 | `test_create_booking_adjacent_dates_no_overlap` | Back-to-back dates | 201 | No conflict |
| B8 | `test_get_all_bookings` | GET `/` | 200 + list | Returns list |
| B9 | `test_get_booking_by_id_success` | Valid UUID | 200 + enriched fields | `place_title`, `guest_name` present |
| B10 | `test_get_booking_not_found` | Fake UUID | 404 | Not found |
| B11 | `test_update_booking_success` | `guests: 4` | 200 | Updated |
| B12 | `test_update_booking_not_found` | Fake UUID | 404 | Not found |
| B13 | `test_confirm_booking` | `action: confirm` | 200 + `confirmed` | State transition |
| B14 | `test_cancel_booking` | `action: cancel` | 200 + `cancelled` | State transition |
| B15 | `test_cancel_already_cancelled` | Cancel twice | 400 | Invalid transition |
| B16 | `test_delete_booking_success` | Valid UUID | 200 | Deleted |
| B17 | `test_delete_booking_not_found` | Fake UUID | 404 | Not found |
| B18 | `test_get_bookings_by_user` | Valid user UUID | 200 + list | Filtered by user |
| B19 | `test_get_bookings_by_place` | Valid place UUID | 200 + list | Filtered by place |

---

## cURL Quick Reference

```bash
# Create user
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'

# Create place (replace OWNER_ID)
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title":"My Flat","description":"Nice","price":80,"latitude":48.8,"longitude":2.3,"owner_id":"OWNER_ID"}'

# Create review (replace USER_ID and PLACE_ID)
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text":"Amazing!","rating":5,"user_id":"USER_ID","place_id":"PLACE_ID"}'

# Create booking (replace USER_ID and PLACE_ID)
curl -X POST http://127.0.0.1:5000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"place_id":"PLACE_ID","user_id":"USER_ID","check_in":"2027-06-01","check_out":"2027-06-05","guests":2}'

# Confirm a booking (replace BOOKING_ID)
curl -X PATCH http://127.0.0.1:5000/api/v1/bookings/BOOKING_ID/status \
  -H "Content-Type: application/json" \
  -d '{"action":"confirm"}'

# Test invalid email
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"","last_name":"","email":"not-valid"}'
# → 400 Bad Request

# Test latitude out of range
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title":"X","description":"X","price":10,"latitude":999,"longitude":0,"owner_id":"OWNER_ID"}'
# → 400 Bad Request
```

---

## Summary

| Entity | Tests | Pass criteria |
|---|---|---|
| Users | 11 | Validation, uniqueness, CRUD |
| Amenities | 9 | Validation, CRUD |
| Places | 15 | Boundary testing, owner ref, CRUD |
| Reviews | 17 | Rating range, entity refs, delete |
| Bookings | 19 | Date logic, overlap, status cycle |
| **Total** | **71** | |
