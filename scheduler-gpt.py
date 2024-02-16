import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.start_time = None
        self.end_time = None
        self.waiting_time = 0
        self.response_time = None

def scheduler_fcfs(processes):
    current_time = 0
    for process in processes:
        if process.arrival > current_time:
            current_time = process.arrival
        process.start_time = current_time
        process.end_time = current_time + process.burst
        process.waiting_time = current_time - process.arrival
        process.response_time = process.waiting_time
        current_time = process.end_time

def scheduler_sjf(processes):
    processes.sort(key=lambda x: (x.arrival, x.burst))
    current_time = 0
    for process in processes:
        if process.arrival > current_time:
            current_time = process.arrival
        process.start_time = current_time
        process.end_time = current_time + process.burst
        process.waiting_time = current_time - process.arrival
        process.response_time = process.waiting_time
        current_time = process.end_time

def scheduler_rr(processes, quantum):
    current_time = 0
    queue = processes.copy()
    while queue:
        process = queue.pop(0)
        if process.arrival > current_time:
            current_time = process.arrival
        process.start_time = current_time
        if process.remaining_burst <= quantum:
            current_time += process.remaining_burst
            process.end_time = current_time
            process.remaining_burst = 0
        else:
            current_time += quantum
            process.remaining_burst -= quantum
            queue.append(process)
        process.waiting_time += current_time - process.start_time
        if process.response_time is None:
            process.response_time = process.waiting_time

def calculate_metrics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0
    for process in processes:
        process.turnaround_time = process.end_time - process.arrival
        total_turnaround_time += process.turnaround_time
        total_waiting_time += process.waiting_time
        total_response_time += process.response_time
    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_response_time = total_response_time / len(processes)
    return avg_turnaround_time, avg_waiting_time, avg_response_time

def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)

    directives = {}
    processes = []

    for line in lines:
        parts = line.strip().split()
        if parts[0] == "end":
            break
        elif parts[0] == "use":
            directives[parts[0]] = parts[1]
            if parts[1] == "rr" and "quantum" not in directives:
                print("Error: Missing quantum parameter when use is 'rr'")
                sys.exit(1)
        elif parts[0] == "quantum":
            directives[parts[0]] = int(parts[1])
        elif parts[0] == "process":
            process_info = {}
            for i in range(1, len(parts), 2):
                process_info[parts[i]] = parts[i+1]
            try:
                process = Process(process_info['name'], int(process_info['arrival']), int(process_info['burst']))
                processes.append(process)
            except KeyError as e:
                print(f"Error: Missing parameter {e}.")
                sys.exit(1)
        else:
            try:
                directives[parts[0]] = int(parts[1])
            except ValueError:
                print("Error: Invalid parameter value.")
                sys.exit(1)

    if "processcount" not in directives:
        print("Error: Missing parameter processcount.")
        sys.exit(1)

    process_count = directives["processcount"]
    algorithm = directives["use"]
    quantum = directives.get("quantum")

    if len(processes) != process_count:
        print("Error: Number of processes provided does not match processcount.")
        sys.exit(1)

    if algorithm == "fcfs":
        scheduler_fcfs(processes)
    elif algorithm == "sjf":
        scheduler_sjf(processes)
    elif algorithm == "rr":
        if quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            sys.exit(1)
        scheduler_rr(processes, quantum)
    else:
        print("Error: Invalid scheduling algorithm.")
        sys.exit(1)

    avg_turnaround_time, avg_waiting_time, avg_response_time = calculate_metrics(processes)

    print(f"{process_count} processes")
    print(f"Using {algorithm.upper()}")

    for process in processes:
        print(f"P{process.name} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.response_time}")

    print(f"\nAverage Turnaround Time: {avg_turnaround_time}")
    print(f"Average Waiting Time: {avg_waiting_time}")
    print(f"Average Response Time: {avg_response_time}")

if __name__ == "__main__":
    main()
