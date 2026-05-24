# Code Review

## File: worker.py
## Reviewer: FlowForge Team

---

### Kode yang direview:

```python
def process_jobs(jobs):
    results = []
    for job in jobs:
        db = connect_db()
        result = db.execute("SELECT * FROM tasks WHERE id = " + job['id'])
        results.append(result)
    return results
```

---

### Temuan & Feedback:

#### 1. SQL Injection (Critical)
Query langsung menggabungkan string tanpa parameterisasi:
```python
# Berbahaya
db.execute("SELECT * FROM tasks WHERE id = " + job['id'])

# Seharusnya
db.execute("SELECT * FROM tasks WHERE id = :id", {"id": job['id']})
```

#### 2. Koneksi Database di dalam Loop (Major)
Membuka koneksi baru setiap iterasi sangat tidak efisien dan bisa menyebabkan connection exhaustion.
```python
# Berbahaya
for job in jobs:
    db = connect_db()  # koneksi baru setiap loop

# Seharusnya
db = connect_db()  # buka sekali di luar loop
for job in jobs:
    ...
```

#### 3. Tidak Ada Error Handling (Major)
Jika satu job gagal, seluruh proses berhenti tanpa penjelasan.
```python
# Seharusnya
for job in jobs:
    try:
        result = db.execute(...)
        results.append(result)
    except Exception as e:
        print(f"Job {job['id']} gagal: {e}")
        continue
```

#### 4. Koneksi Tidak Ditutup (Minor)
Setelah selesai, koneksi database tidak ditutup sehingga menyebabkan resource leak.
```python
# Seharusnya
finally:
    db.close()
```

---

### Kesimpulan:
Kode ini memiliki celah keamanan serius (SQL injection) dan masalah performa (koneksi berulang). 
Wajib diperbaiki sebelum merge ke production.