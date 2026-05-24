from app.services.dag import topological_sort, execute_workflow

def test_topological_sort_simple():
    steps = {
        "step1": {"name": "Step 1", "type": "http", "depends_on": []},
        "step2": {"name": "Step 2", "type": "http", "depends_on": ["step1"]},
        "step3": {"name": "Step 3", "type": "http", "depends_on": ["step2"]},
    }
    order = topological_sort(steps)
    assert order.index("step1") < order.index("step2")
    assert order.index("step2") < order.index("step3")
    print("✅ test_topological_sort_simple passed")

def test_topological_sort_parallel():
    steps = {
        "step1": {"name": "Step 1", "type": "http", "depends_on": []},
        "step2": {"name": "Step 2", "type": "http", "depends_on": []},
        "step3": {"name": "Step 3", "type": "http", "depends_on": ["step1", "step2"]},
    }
    order = topological_sort(steps)
    assert order.index("step1") < order.index("step3")
    assert order.index("step2") < order.index("step3")
    print("✅ test_topological_sort_parallel passed")

def test_execute_workflow():
    definition = {
        "steps": {
            "step1": {"name": "Cek Stok", "type": "http", "depends_on": []},
            "step2": {"name": "Proses Bayar", "type": "http", "depends_on": ["step1"]},
            "step3": {"name": "Kirim Email", "type": "http", "depends_on": ["step2"]},
        }
    }
    results = execute_workflow(definition)
    assert len(results) == 3
    assert results[0]["status"] == "success"
    print("✅ test_execute_workflow passed")

if __name__ == "__main__":
    test_topological_sort_simple()
    test_topological_sort_parallel()
    test_execute_workflow()
    print("\n✅ Semua test passed!")