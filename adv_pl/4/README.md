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
