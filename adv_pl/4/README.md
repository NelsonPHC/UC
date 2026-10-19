# Employee Schedule Manager

Two equivalent console applications are included:

- `employee_schedule.py` (Python 3)
- `EmployeeScheduleApp.java` (Java 8+)

Both ask for each employee's name and preferred shift for every day, then create a seven-day schedule. A shift has two positions, which satisfies the required minimum of two employees and provides a meaningful definition of a “full” preferred shift. When a preferred shift is full, the scheduler places the employee in another available shift that day and records the resolution.

The program requires at least nine employees: 42 weekly positions are required (7 days × 3 shifts × 2 employees), and each employee can work at most five days. Each daily assignment chooses six employees with the lowest current weekly workload, ensuring one shift per person per day and preserving capacity for the entire week.

## Run

```bash
python3 employee_schedule.py
```

```bash
javac EmployeeScheduleApp.java
java EmployeeScheduleApp
```

## Example interaction

Run either program, then answer the prompts with the number of employees,
each employee's name, and one preferred shift for every day. Shift responses
must be `morning`, `afternoon`, or `evening` (case does not matter).

```text
$ python3 employee_schedule.py
Employee Schedule Manager
Each shift is staffed by two employees; no one is scheduled more than five days.

How many employees? (at least 9): 9
Employee 1 name: Ada
  Monday preference: morning
  Tuesday preference: morning
  Wednesday preference: afternoon
  Thursday preference: morning
  Friday preference: evening
  Saturday preference: afternoon
  Sunday preference: morning
Employee 2 name: Ben
  Monday preference: evening
  Tuesday preference: afternoon
  Wednesday preference: morning
  Thursday preference: evening
  Friday preference: morning
  Saturday preference: evening
  Sunday preference: afternoon
Employee 3 name: Carla
  Monday preference: afternoon
  Tuesday preference: afternoon
  Wednesday preference: evening
  Thursday preference: morning
  Friday preference: afternoon
  Saturday preference: morning
  Sunday preference: evening
...
Employee 9 name: Ivan
  Monday preference: evening
  Tuesday preference: morning
  Wednesday preference: afternoon
  Thursday preference: evening
  Friday preference: morning
  Saturday preference: afternoon
  Sunday preference: evening
```

Continue in the same format for employees 4 through 8. Once all nine entries
have been entered, the program prints `FINAL WEEKLY SCHEDULE`, with two names
under each morning, afternoon, and evening shift for every day. It then lists
any preferences that needed to be reassigned to maintain coverage.

If an invalid shift is entered, the program keeps the current prompt and asks
again:

```text
  Monday preference: night
Please enter morning, afternoon, or evening.
  Monday preference: evening
```
