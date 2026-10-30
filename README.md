# OperatingSystem_MemoryAllocationSimulator

## Files
- `app.py`: Flask web server and form handling
- `memory_algorithms.py`: all seven allocation algorithms
- `templates/index.html`: frontend form and results
- `static/style.css`: page styling
- `static/script.js`: shows relevant input fields for each algorithm

## Setup
Use Python 3.10+.

```bash
pip install flask
python app.py
```

Open the local URL printed in the terminal, usually `http://127.0.0.1:5000`.

## How to use
1. Choose one of the seven algorithms.
2. Enter process sizes as comma-separated values, such as `212, 417, 112, 426`.
3. For Equal, Proportional, or Priority, enter total available memory.
4. For First Fit, Best Fit, Worst Fit, or Next Fit, enter block sizes, e.g. `100, 500, 200, 300, 600`.
5. For Priority, optionally enter one priority per process, e.g. `1, 2, 3, 1`. Smaller number means higher priority.
6. Click Run Simulation.

No database or separate JavaScript API server is required. Flask receives the form submission and runs the Python functions.

## Assumptions
- Equal: each process is offered an equal share, capped at its request; unused shares are not redistributed.
- Proportional: when total demand exceeds memory, memory is shared in proportion to requested sizes.
- Priority: lower numeric priority is considered first; processes get their full request or zero.
- Contiguous placement: each block is a free hole; allocating a process reduces that hole by the process size.
- Next Fit resumes searching from the last successful allocation's block and searches circularly.
