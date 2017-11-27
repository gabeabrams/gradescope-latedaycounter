# gradescope-latedaycounter

For courses that use late days (students get a set of late days that they can use to submit a day later on an assignment with no penalty) with the following type of policy:

Each student gets `X` late days total per semester. They can use at most `Y` late days on each assignment. Submitting 1 min - 24 hours late costs 1 late day, submitting 24 hours & 1 min late - 48 hours late costs 2 late days, and so on.

The script also supports grace periods. With a 5 min grace period, submitting 6min - 24 hours & 5 min late costs 1 late day, submitting 24 hours & 6 min - 48 hours & 5min late costs 2 late days.

# Usage: 
## 1. Download Grades CSVs from Gradescope

For each assignment that students can use late days on, download the "Grades" CSV file (visit assignment, open "Review Grades" pane, click "Download Grades" and select CSV).

Put all CSVs in the same folder as `calculateLateDays.py`.

## 2. Run the Script

Run `python calculateLateDays.py` and follow instructions, inputting max late days per semester, grace period, etc.

## 3. Interpret Results

A new file: `Late Days.csv` will appear in the current directory. In addition to student information columns, you'll find the following:

*Late Days Used (total)* – The total late days used by each student so far.

*Late days used for _____* – A column added for each assignment (e.g., `Late days used for Homework 1`) indicating the number of late days used by each student on this assignment.

*Exceeded late day max for semester* – TRUE/FALSE column indicating students that used more than the semester max of late days.

*Exceeded late day max for _____* – A column added for each assignment (e.g., `Exceeded late day max for Homework 1`) with TRUE/FALSE indicating whether each student used more than the per-assignment late day max for this assignment.

<hr>

_Thanks to Jonah Feldman, Instructional Technology Intern at Harvard University, for his work on this script_