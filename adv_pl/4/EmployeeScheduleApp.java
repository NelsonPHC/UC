import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;

/** Console implementation of the employee scheduling assignment. */
public class EmployeeScheduleApp {
    private static final List<String> DAYS = Arrays.asList(
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday");
    private static final List<String> SHIFTS = Arrays.asList("morning", "afternoon", "evening");
    private static final int MINIMUM_PER_SHIFT = 2;
    private static final int MAX_DAYS_PER_EMPLOYEE = 5;

    private static class Employee {
        final String name;
        final Map<String, String> preferences;

        Employee(String name, Map<String, String> preferences) {
            this.name = name;
            this.preferences = preferences;
        }
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Employee Schedule Manager");
        System.out.println("Each shift is staffed by two employees; no one is scheduled more than five days.\n");
        List<Employee> employees = readEmployees(input);
        ScheduleResult result = buildSchedule(employees, new Random());
        printSchedule(result);
    }

    private static List<Employee> readEmployees(Scanner input) {
        int minimumPeople = (DAYS.size() * SHIFTS.size() * MINIMUM_PER_SHIFT + MAX_DAYS_PER_EMPLOYEE - 1)
                / MAX_DAYS_PER_EMPLOYEE;
        int count;
        while (true) {
            System.out.print("How many employees? (at least " + minimumPeople + "): ");
            try {
                count = Integer.parseInt(input.nextLine().trim());
                if (count >= minimumPeople) break;
            } catch (NumberFormatException ignored) { }
            System.out.println("At least " + minimumPeople + " employees are required to cover 42 weekly positions without anyone working over 5 days.");
        }

        List<Employee> employees = new ArrayList<>();
        Set<String> names = new HashSet<>();
        for (int number = 1; number <= count; number++) {
            String name;
            while (true) {
                System.out.print("Employee " + number + " name: ");
                name = input.nextLine().trim();
                if (!name.isEmpty() && names.add(name.toLowerCase())) break;
                System.out.println("Enter a non-empty name that has not already been used.");
            }
            Map<String, String> preferences = new LinkedHashMap<>();
            for (String day : DAYS) preferences.put(day, readShift(input, "  " + day + " preference: "));
            employees.add(new Employee(name, preferences));
        }
        return employees;
    }

    private static String readShift(Scanner input, String prompt) {
        while (true) {
            System.out.print(prompt);
            String shift = input.nextLine().trim().toLowerCase();
            if (SHIFTS.contains(shift)) return shift;
            System.out.println("Please enter morning, afternoon, or evening.");
        }
    }

    private static ScheduleResult buildSchedule(List<Employee> employees, Random random) {
        if (employees.size() < 9) throw new IllegalArgumentException("At least 9 employees are required.");
        Map<String, Integer> totals = new HashMap<>();
        for (Employee employee : employees) totals.put(employee.name, 0);
        Map<String, Map<String, List<String>>> schedule = new LinkedHashMap<>();
        List<String> conflicts = new ArrayList<>();

        for (String day : DAYS) {
            List<Employee> candidates = new ArrayList<>(employees);
            Collections.shuffle(candidates, random); // makes equal workloads fair
            candidates.sort((a, b) -> Integer.compare(totals.get(a.name), totals.get(b.name)));
            List<Employee> remaining = new ArrayList<>(candidates.subList(0, SHIFTS.size() * MINIMUM_PER_SHIFT));
            Map<String, List<String>> dailySchedule = new LinkedHashMap<>();

            for (String shift : SHIFTS) {
                List<String> assigned = new ArrayList<>();
                for (int slot = 0; slot < MINIMUM_PER_SHIFT; slot++) {
                    Employee employee = null;
                    for (Employee candidate : remaining) {
                        if (candidate.preferences.get(day).equals(shift)) {
                            employee = candidate;
                            break;
                        }
                    }
                    if (employee == null) employee = remaining.get(random.nextInt(remaining.size()));
                    remaining.remove(employee);
                    assigned.add(employee.name);
                    totals.put(employee.name, totals.get(employee.name) + 1);
                    if (!employee.preferences.get(day).equals(shift)) {
                        String preferredShift = employee.preferences.get(day);
                        String reason = dailySchedule.containsKey(preferredShift)
                                && dailySchedule.get(preferredShift).size() == MINIMUM_PER_SHIFT
                                ? "was full" : "was unavailable for balanced coverage";
                        conflicts.add(employee.name + ": " + day + " preference (" + preferredShift
                                + ") " + reason + "; assigned " + shift + ".");
                    }
                }
                dailySchedule.put(shift, assigned);
            }
            schedule.put(day, dailySchedule);
        }
        for (int total : totals.values()) {
            if (total > MAX_DAYS_PER_EMPLOYEE) throw new IllegalStateException("Weekly limit was exceeded.");
        }
        return new ScheduleResult(schedule, conflicts);
    }

    private static void printSchedule(ScheduleResult result) {
        System.out.println("\nFINAL WEEKLY SCHEDULE\n================================================");
        for (String day : DAYS) {
            System.out.println("\n" + day);
            for (String shift : SHIFTS) {
                System.out.printf("  %-10s: %s%n", capitalize(shift), String.join(", ", result.schedule.get(day).get(shift)));
            }
        }
        System.out.println("\nPreference conflicts resolved:");
        if (result.conflicts.isEmpty()) System.out.println("  None");
        else for (String conflict : result.conflicts) System.out.println("  - " + conflict);
    }

    private static String capitalize(String value) {
        return Character.toUpperCase(value.charAt(0)) + value.substring(1);
    }

    private static class ScheduleResult {
        final Map<String, Map<String, List<String>>> schedule;
        final List<String> conflicts;

        ScheduleResult(Map<String, Map<String, List<String>>> schedule, List<String> conflicts) {
            this.schedule = schedule;
            this.conflicts = conflicts;
        }
    }
}
