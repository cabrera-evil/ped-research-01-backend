# Hash Table Design (Assignment c)

## Selected Structure

- **Hash Table with separate chaining**
- Located at `app/core/hash_table.py`

Separate chaining means each bucket can hold multiple elements in a list when collisions happen.

## Hash Function

```python
sum(ord(c) for c in str(key)) % self.size
```

This transforms each key into a fixed bucket index from `0` to `size-1`.

## Operations

- `insert(key, value)`: adds or updates by key
- `search(key)`: returns value or `None`
- `delete(key)`: removes key and returns `True/False`
- `list_all()`: returns all `(key, value)` pairs
- `stats()`: returns table metrics

## Collision Handling

When two keys map to the same index, both are kept in the same bucket list.

Example seeded by startup logic:

- `P001` and `P010` -> same bucket
- `P002` and `P020` -> same bucket

## Why This Proves the Requirement

The backend is a small inventory application using the hash table as the only in-memory storage:

- Product code is the hash key
- API exposes CRUD + stats to observe behavior
- Deliberate seeded collisions show real collision resolution in action

## Useful Endpoint for Evidence

`GET /api/v1/inventory/stats/hash`

Returns:

- `table_size`
- `total_elements`
- `used_cells`
- `cells_with_collision`
- `load_factor`
- `distribution`
