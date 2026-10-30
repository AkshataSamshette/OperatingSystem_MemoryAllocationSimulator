from flask import Flask, render_template, request
from memory_algorithms import (
    equal_allocation,
    proportional_allocation,
    priority_allocation,
    contiguous_allocation,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        algorithm = request.form.get("algorithm", "").strip()
        process_text = request.form.get("processes", "").strip()
        block_text = request.form.get("blocks", "").strip()
        memory_text = request.form.get("memory", "").strip()

        # Process sizes are comma-separated, e.g. 100, 250, 300
        process_sizes = parse_positive_list(process_text, "process sizes")
        processes = [
            {
                "id": f"P{i + 1}",
                "size": size,
                "priority": int(priority)
            }
            for i, (size, priority) in enumerate(
                zip(process_sizes, parse_priorities(
                    request.form.get("priorities", ""), len(process_sizes)
                ))
            )
        ]

        if algorithm in {"equal", "proportional", "priority"}:
            memory = parse_positive_number(memory_text, "total memory")
            if algorithm == "equal":
                name = "Equal Allocation"
                results = equal_allocation(memory, processes)
                holes = None
            elif algorithm == "proportional":
                name = "Proportional Allocation"
                results = proportional_allocation(memory, processes)
                holes = None
            else:
                name = "Priority-Based Allocation"
                results = priority_allocation(memory, processes)
                holes = None

            total_memory = memory
            external_fragmentation = None
            used_memory = sum(row["allocated"] for row in results)
            free_memory = max(0, total_memory - used_memory)

        elif algorithm in {"first_fit", "best_fit", "worst_fit", "next_fit"}:
            blocks = parse_positive_list(block_text, "memory block sizes")
            names = {
                "first_fit": "First Fit",
                "best_fit": "Best Fit",
                "worst_fit": "Worst Fit",
                "next_fit": "Next Fit",
            }
            name = names[algorithm]
            results, holes = contiguous_allocation(blocks, processes, algorithm)
            total_memory = sum(blocks)
            free_memory = sum(holes)
            used_memory = total_memory - free_memory
            # Simplified external-fragmentation indicator: all free holes except the largest.
            external_fragmentation = max(0.0, free_memory - max(holes, default=0.0))
            for row in results:
                row["fragmentation"] = (
                    f"External: {external_fragmentation:.2f} MB"
                    if external_fragmentation > 0 else "External: 0 MB"
                )
        else:
            raise ValueError("Please select a valid algorithm.")

        return render_template(
            "index.html",
            result_name=name,
            results=results,
            total_memory=round(total_memory, 2),
            used_memory=round(used_memory, 2),
            free_memory=round(free_memory, 2),
            utilization=round(used_memory / total_memory * 100, 2),
            external_fragmentation=round(external_fragmentation, 2) if algorithm in {"first_fit", "best_fit", "worst_fit", "next_fit"} else None,
            holes=holes,
            selected_algorithm=algorithm,
            form_data=request.form,
        )

    except (ValueError, TypeError) as exc:
        return render_template(
            "index.html",
            error=str(exc),
            selected_algorithm=request.form.get("algorithm", ""),
            form_data=request.form,
        ), 400


def parse_positive_number(text, label):
    try:
        value = float(text)
    except (ValueError, TypeError):
        raise ValueError(f"Enter a valid number for {label}.")
    if value <= 0:
        raise ValueError(f"{label.capitalize()} must be greater than zero.")
    return value


def parse_positive_list(text, label):
    if not text:
        raise ValueError(f"Enter {label}, separated by commas.")
    try:
        values = [float(item.strip()) for item in text.split(",")]
    except ValueError:
        raise ValueError(f"Use comma-separated numbers for {label}.")
    if not values or any(value <= 0 for value in values):
        raise ValueError(f"All {label} must be greater than zero.")
    return values


def parse_priorities(text, count):
    if not text:
        return [1] * count
    try:
        values = [int(item.strip()) for item in text.split(",")]
    except ValueError:
        raise ValueError("Priorities must be comma-separated whole numbers.")
    if len(values) != count:
        raise ValueError("Enter exactly one priority per process, or leave priorities blank.")
    return values


if __name__ == "__main__":
    app.run(debug=True)
