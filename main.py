# import matplotlib.pyplot as plt
#
# # Data for highest enrollment programs
# programs = ['Nursing', 'Psychology', 'Kinesiology', 'Computer Science', 'Health Studies',
#             'Biology', 'Communication', 'Elementary Education', 'Construction Management',
#             'Business Administration']
#
# enrollment_numbers = [899, 859, 753, 666, 654, 625, 456, 402, 357, 345]
#
# # Plotting the bar chart
# plt.figure(figsize=(10, 6))
# plt.bar(programs, enrollment_numbers, color='skyblue')
# plt.xlabel('Programs')
# plt.ylabel('Enrollment Numbers')
# plt.title('Highest Enrollment Programs')
# plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
# plt.tight_layout()
#
# # Display the plot
# plt.show()

import matplotlib.pyplot as plt

# Student Population by Degree Level
labels = ['Undergraduate', 'Graduate']
sizes = [17085, 2813]

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
plt.title('Student Population by Degree Level')
plt.show()

# Age Distribution of Undergraduate Students
age_groups = ['18 or younger', '19-20', '21-24', '25-34', '35-49', '50 and older']
undergrad_percentages = [26, 37, 22, 10, 5, 1]

plt.figure(figsize=(10, 6))
plt.bar(age_groups, undergrad_percentages, color='lightgreen')
plt.xlabel('Age Groups')
plt.ylabel('Percentage')
plt.title('Age Distribution of Undergraduate Students')
plt.show()

# Tuition Costs Comparison
tuition_labels = ['In State', 'Out of State']
undergrad_tuition = [8782, 27976]
grad_tuition = [10486, 28605]

fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
bar1 = ax.bar(tuition_labels, undergrad_tuition, bar_width, label='Undergraduate')
bar2 = ax.bar([x + bar_width for x in tuition_labels], grad_tuition, bar_width, label='Graduate')

ax.set_xlabel('Tuition Type')
ax.set_ylabel('Tuition Cost (Per Year)')
ax.set_title('Tuition Costs Comparison')
ax.legend()

plt.show()
