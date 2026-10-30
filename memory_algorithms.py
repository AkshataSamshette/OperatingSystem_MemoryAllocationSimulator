"""Algorithm functions used by the Memory Allocation Simulator web app."""


def equal_allocation(memory, processes):
    """Give every process an equal-sized partition (share = memory / count).

    If a process requests less than its partition, the unused part is internal
    fragmentation. If it requests more than its partition, the excess request
    cannot fit in that partition and is reported as unmet request.
    """
    share = memory / len(processes)
    results = []
    for p in processes:
        allocated = share
        internal = max(0.0, allocated - p["size"])
        unmet = max(0.0, p["size"] - allocated)
        results.append({
            "process": p["id"],
            "requested": p["size"],
            "allocated": allocated,
            "block": None,
            "fragmentation": (f"Internal: {internal:.2f} MB" if internal > 0
                               else (f"Request exceeds partition by {unmet:.2f} MB" if unmet > 0
                                     else "None (0 MB)")),
            "internal_fragmentation": internal,
            "unmet_request": unmet,
        })
    return results


def proportional_allocation(memory, processes):
    total_requested = sum(p["size"] for p in processes)
    results = []

    for p in processes:
        allocated = (
            p["size"]
            if total_requested <= memory
            else memory * p["size"] / total_requested
        )
        results.append({
            "process": p["id"],
            "requested": p["size"],
            "allocated": allocated,
            "block": None,
            "fragmentation": "None (0 MB)",
            "internal_fragmentation": 0.0,
            "unmet_request": max(0.0, p["size"] - allocated),
        })
    return results


def priority_allocation(memory, processes):
    remaining = memory
    allocation_by_id = {}

    # Lower numeric priority means higher priority.
    # Each process gets its full request or zero.
    for p in sorted(processes, key=lambda item: item["priority"]):
        if p["size"] <= remaining:
            allocation_by_id[p["id"]] = p["size"]
            remaining -= p["size"]
        else:
            allocation_by_id[p["id"]] = 0

    return [
        {
            "process": p["id"],
            "requested": p["size"],
            "allocated": allocation_by_id[p["id"]],
            "block": None,
            "fragmentation": "None (0 MB)",
            "internal_fragmentation": 0.0,
            "unmet_request": max(0.0, p["size"] - allocation_by_id[p["id"]]),
        }
        for p in processes
    ]


def contiguous_allocation(block_sizes, processes, algorithm):
    holes = list(block_sizes)
    results = []
    next_position = 0

    for p in processes:
        candidates = [
            i for i, size in enumerate(holes)
            if size >= p["size"]
        ]

        if not candidates:
            results.append({
                "process": p["id"],
                "requested": p["size"],
                "allocated": 0,
                "block": None,
                "remaining_in_block": None,
                "fragmentation": "Not allocated",
            })
            continue

        if algorithm == "first_fit":
            chosen = candidates[0]
        elif algorithm == "best_fit":
            chosen = min(candidates, key=lambda i: holes[i])
        elif algorithm == "worst_fit":
            chosen = max(candidates, key=lambda i: holes[i])
        elif algorithm == "next_fit":
            chosen = None
            for offset in range(len(holes)):
                i = (next_position + offset) % len(holes)
                if holes[i] >= p["size"]:
                    chosen = i
                    break
            if chosen is None:
                results.append({
                    "process": p["id"],
                    "requested": p["size"],
                    "allocated": 0,
                    "block": None,
                    "remaining_in_block": None,
                })
                continue
        else:
            raise ValueError("Unknown allocation algorithm.")

        holes[chosen] -= p["size"]
        results.append({
            "process": p["id"],
            "requested": p["size"],
            "allocated": p["size"],
            "block": chosen + 1,
            "remaining_in_block": holes[chosen],
            "fragmentation": "Pending calculation",
        })

        if algorithm == "next_fit":
            next_position = chosen

    return results, holes
