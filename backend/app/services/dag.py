from collections import deque

def topological_sort(steps: dict) -> list:
    """Urutkan steps berdasarkan dependency"""
    in_degree = {step_id: 0 for step_id in steps}
    
    for step_id, step in steps.items():
        for dep in step.get("depends_on", []):
            if dep in in_degree:
                in_degree[step_id] += 1

    queue = deque([s for s in in_degree if in_degree[s] == 0])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for step_id, step in steps.items():
            if current in step.get("depends_on", []):
                in_degree[step_id] -= 1
                if in_degree[step_id] == 0:
                    queue.append(step_id)

    if len(order) != len(steps):
        raise ValueError("Workflow memiliki circular dependency!")

    return order

def execute_workflow(definition: dict) -> list:
    """Eksekusi workflow berdasarkan urutan DAG"""
    steps = definition.get("steps", {})
    order = topological_sort(steps)
    results = []

    for step_id in order:
        step = steps[step_id]
        results.append({
            "step_id": step_id,
            "name": step.get("name"),
            "type": step.get("type"),
            "status": "success"
        })

    return results