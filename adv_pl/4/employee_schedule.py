"""Interactive employee shift scheduler.

Each shift has two scheduled positions.  This is deliberately a capacity as
well as a coverage target: it makes a preferred shift capable of becoming
full, so conflicts can be reassigned to another open shift that day.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
SHIFTS = ("morning", "afternoon", "evening")
MINIMUM_PER_SHIFT = 2
MAX_DAYS_PER_EMPLOYEE = 5


@dataclass(frozen=True)
class Employee:
    name: str
    preferences: dict[str, str]


def read_shift(prompt: str) -> str:
    while True:
        shift = input(prompt).strip().lower()
        if shift in SHIFTS:
            return shift
        print("Please enter morning, afternoon, or evening.")


def read_employees() -> list[Employee]:
    minimum_people = (len(DAYS) * len(SHIFTS) * MINIMUM_PER_SHIFT + MAX_DAYS_PER_EMPLOYEE - 1) // MAX_DAYS_PER_EMPLOYEE
    while True:
        try:
            count = int(input(f"How many employees? (at least {minimum_people}): "))
            if count >= minimum_people:
                break
        except ValueError:
            pass
        print(f"At least {minimum_people} employees are required to cover 42 weekly positions without anyone working over 5 days.")

    employees: list[Employee] = []
    names: set[str] = set()
    for number in range(1, count + 1):
        while True:
            name = input(f"Employee {number} name: ").strip()
            if name and name.casefold() not in names:
                names.add(name.casefold())
                break
            print("Enter a non-empty name that has not already been used.")
        preferences = {day: read_shift(f"  {day} preference: ") for day in DAYS}
        employees.append(Employee(name, preferences))
    return employees


def build_schedule(employees: list[Employee], rng: random.Random | None = None) -> tuple[dict[str, dict[str, list[str]]], list[str]]:
    """Return a valid schedule and notes about preference conflicts.

    The least-scheduled employees are chosen for each day first.  Six people
    are selected, one for each required position; selecting the lowest weekly
    totals prevents anyone from reaching five days before later days can be
    filled.  Preferred shifts are then filled before random fallback choices.
    """
    if len(employees) < 9:
        raise ValueError("At least 9 employees are needed for the weekly coverage requirement.")
    rng = rng or random.Random()
    totals = {employee.name: 0 for employee in employees}
    schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
    conflicts: list[str] = []

    for day in DAYS:
        # Randomize only ties, then choose the six lightest workloads.
        shuffled = employees[:]
        rng.shuffle(shuffled)
        selected = sorted(shuffled, key=lambda employee: totals[employee.name])[: len(SHIFTS) * MINIMUM_PER_SHIFT]
        remaining = selected[:]

        for shift in SHIFTS:
            for _ in range(MINIMUM_PER_SHIFT):
                preferred = [employee for employee in remaining if employee.preferences[day] == shift]
                if preferred:
                    employee = min(preferred, key=lambda person: totals[person.name])
                else:
                    # Nobody remaining prefers this shift, so this is a random additional assignment.
                    employee = rng.choice(remaining)
                remaining.remove(employee)
                schedule[day][shift].append(employee.name)
                totals[employee.name] += 1
                if employee.preferences[day] != shift:
                    preferred_shift = employee.preferences[day]
                    reason = "was full" if len(schedule[day][preferred_shift]) == MINIMUM_PER_SHIFT else "was unavailable for balanced coverage"
                    conflicts.append(f"{employee.name}: {day} preference ({preferred_shift}) {reason}; assigned {shift}.")

    if any(total > MAX_DAYS_PER_EMPLOYEE for total in totals.values()):
        raise RuntimeError("Scheduler invariant failed: an employee exceeded the weekly limit.")
    return schedule, conflicts


def print_schedule(schedule: dict[str, dict[str, list[str]]], conflicts: list[str]) -> None:
    print("\nFINAL WEEKLY SCHEDULE")
    print("=" * 48)
    for day in DAYS:
        print(f"\n{day}")
        for shift in SHIFTS:
            print(f"  {shift.title():<10}: {', '.join(schedule[day][shift])}")
    print("\nPreference conflicts resolved:")
    if conflicts:
        for conflict in conflicts:
            print(f"  - {conflict}")
    else:
        print("  None")


def main() -> None:
    print("Employee Schedule Manager")
    print("Each shift is staffed by two employees; no one is scheduled more than five days.\n")
    schedule, conflicts = build_schedule(read_employees())
    print_schedule(schedule, conflicts)


if __name__ == "__main__":
    main()
