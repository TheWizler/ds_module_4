import pandas as pd

# Load data
schools_df = pd.read_csv('PyCitySchools/Resources/schools_complete.csv')
students_df = pd.read_csv('PyCitySchools/Resources/students_complete.csv')

# Merge data sets
merged_df = pd.merge(students_df, schools_df, on="school_name")

# Calculate passing scores
passing_math = merged_df['math_score'] >= 70
passing_read = merged_df['reading_score'] >= 70
passing_both = passing_math & passing_read

# Add columns for passing statuses to the merged DataFrame
merged_df['passing_math'] = passing_math
merged_df['passing_reading'] = passing_read
merged_df['passing_both'] = passing_both

# Group by | metrics
school_group = merged_df.groupby('school_name')
percent_passing_math = school_group['passing_math'].mean() * 100
percent_passing_read = school_group['passing_reading'].mean() * 100
percent_overall_pass = school_group['passing_both'].mean() * 100
school_budget = school_group['budget'].mean()
students_per_school = school_group['Student ID'].nunique()

# Create first DataFrame 
school_summary_df = pd.DataFrame({
    "Total Students": students_per_school,
    "Total School Budget": school_budget,
    "Per Student Budget": school_budget / students_per_school,
    "Average Math Score": school_group['math_score'].mean(),
    "Average Reading Score": school_group['reading_score'].mean(),
    "% Passing Math": percent_passing_math,
    "% Passing Reading": percent_passing_read,
    "% Overall Passing": percent_overall_pass,
    "School Type": school_group['type'].first()
})

# Scores by School Size
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Categorize
school_summary_df['School Size'] = pd.cut(school_summary_df['Total Students'], bins=size_bins, labels=labels)

# Group by school size
grouped_by_size = school_summary_df.groupby('School Size', observed=True).mean(numeric_only=True)

# Select columns
size_summary = grouped_by_size[['Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', '% Overall Passing']]

# Print the results
print("Scores by School Size:")
print(size_summary)

# Scores by School Spending

# Define spending bins and labels
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# Categorize 
school_summary_df['Spending Ranges (Per Student)'] = pd.cut(school_summary_df['Per Student Budget'], bins=spending_bins, labels=labels)

# Group by spending range
grouped_by_spending = school_summary_df.groupby('Spending Ranges (Per Student)', observed=True).mean(numeric_only=True)

# Create DataFrame to hold the above results
spending_summary = pd.DataFrame({
    "Average Math Score": grouped_by_spending["Average Math Score"],
    "Average Reading Score": grouped_by_spending["Average Reading Score"],
    "% Passing Math": grouped_by_spending["% Passing Math"],
    "% Passing Reading": grouped_by_spending["% Passing Reading"],
    "% Overall Passing": grouped_by_spending["% Overall Passing"]
})

# Print output
print("Scores by Spending:")
print(spending_summary)

# Highest-Performing Schools (by % Overall Passing)
# Sort schools using sort_values % 'Overall Passing' | descending | display the top 5
top_schools = school_summary_df.sort_values('% Overall Passing', ascending=False).head(5)
print("\nTop Schools:")
print(top_schools)

# Lowest-Performing Schools (by % Overall Passing) - just ascend instead of descend through the data
# Sort schools using sort_values % 'Overall Passing' | ascending | display the top 5
bottom_schools = school_summary_df.sort_values('% Overall Passing', ascending=True).head(5)

# Math Scores 
# Group by school | name | grade | average math scores - add .head() to pull smaller data set
math_scores = merged_df.pivot_table(index='school_name', columns='grade', values='math_score', aggfunc='mean').head()

# Math Scores by Grade
math_scores = math_scores[['9th', '10th', '11th', '12th']]

# Print the DataFrame
print("\nMath Scores by Grade:")
print(math_scores)

# Reading Scores 
reading_scores = merged_df.pivot_table(index='school_name', columns='grade', values='reading_score', aggfunc='mean').head()

# Sort columns 
reading_scores = reading_scores[['9th', '10th', '11th', '12th']]

# Print the DataFrame - add .head() to pull smaller data set - I then separated the outputs with \n to make it more readable
print("\nReading Scores by Grade:")
print(reading_scores)

# Create type_summary DataFrame
type_summary = school_summary_df.groupby('School Type').mean(numeric_only=True)[[
    "Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"
]]

# Print type_summary
print("\nSummary by School Type:")
print(type_summary)
