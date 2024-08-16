import csv

# Load the CSV file and store the data in memory
file_path = 'insurance.csv'  # Update with your actual file path if needed

with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    # Extract the header
    header = next(reader)
    print("Header:", header)
    # Store all rows in a list for further processing
    rows = [row for row in reader]
# Inspect the first few rows
for i in range(5):  # Adjust this number to inspect more rows if needed
    print(rows[i])

#-----------------------------------------------------------------------Descriptive Analysisis (Average, Min, Max)
# Initialize variables for descriptive statistics
total_age = 0
total_bmi = 0
total_charges = 0
min_age = float('inf')
min_bmi = float('inf')
min_charges = float('inf')
max_age = float('-inf')
max_bmi = float('-inf')
max_charges = float('-inf')
count = len(rows)  # Total number of rows
# Iterate through the stored rows to calculate statistics
for row in rows:
    age = int(row[0])
    bmi = float(row[2])
    charges = float(row[6])
    
    total_age += age
    total_bmi += bmi
    total_charges += charges
    
    min_age = min(min_age, age)
    min_bmi = min(min_bmi, bmi)
    min_charges = min(min_charges, charges)

    max_age = max(max_age, age)
    max_bmi = max(max_bmi, bmi)
    max_charges = max(max_charges, charges)
# Calculate averages
avg_age = total_age / count
avg_bmi = total_bmi / count
avg_charges = total_charges / count
# Print the results
print(f"Age: Avg = {avg_age:.2f}, Min = {min_age}, Max = {max_age}")
print(f"BMI: Avg = {avg_bmi:.2f}, Min = {min_bmi:.2f}, Max = {max_bmi:.2f}")
print(f"Charges: Avg = {avg_charges:.2f}, Min = {min_charges:.2f}, Max = {max_charges:.2f}")


#-----------------------------------------------------------------------Average Cost by Demographics
# Initialize dictionaries for demographic groups
sex_costs = {}
smoker_costs = {}
region_costs = {}

# Function to update demographic dictionaries
def update_costs(demo_dict, key, charge):
    if key in demo_dict:
        demo_dict[key][0] += charge
        demo_dict[key][1] += 1
    else:
        demo_dict[key] = [charge, 1]
# Iterate through the stored rows to calculate costs by demographics
for row in rows:
    sex = row[1]
    smoker = row[4]
    region = row[5]
    charges = float(row[6])
    # Update each demographic dictionary
    update_costs(sex_costs, sex, charges)
    update_costs(smoker_costs, smoker, charges)
    update_costs(region_costs, region, charges)
# Function to calculate averages
def calculate_averages(demo_dict):
    averages = {}
    for key, (total_charges, count) in demo_dict.items():
        averages[key] = total_charges / count
    return averages
# Calculate average costs by demographics
avg_sex_costs = calculate_averages(sex_costs)
avg_smoker_costs = calculate_averages(smoker_costs)
avg_region_costs = calculate_averages(region_costs)
# Print the results
print("Average Costs by Sex:", avg_sex_costs)
print("Average Costs by Smoker Status:", avg_smoker_costs)
print("Average Costs by Region:", avg_region_costs)


#-----------------------------------------------------------------------Distribution of Charges
# Define bins (you can adjust the ranges as needed)
bins = [0, 5000, 10000, 20000, 30000, 40000, 50000, 60000, float('inf')]
bin_counts = [0] * (len(bins) - 1)
# Function to categorize charges into bins
def categorize_charge(charge):
    for i in range(1, len(bins)):
        if charge <= bins[i]:
            return i - 1
    return len(bins) - 2  # Last bin
# Count the charges in each bin
for row in rows:
    charges = float(row[6])
    bin_index = categorize_charge(charges)
    bin_counts[bin_index] += 1
# Print the distribution
print("Distribution of Charges:")
for i in range(len(bin_counts)):
    print(f"{bins[i]} - {bins[i+1]}: {bin_counts[i]} charges")

#-----------------------------------------------------------------------AgesVSCharges
# Define age groups
age_groups = {
    '0-20': [0, 0],
    '21-40': [0, 0],
    '41-60': [0, 0],
    '61+': [0, 0]}
# Function to categorize age into groups
def categorize_age(age):
    if age <= 20:
        return '0-20'
    elif age <= 40:
        return '21-40'
    elif age <= 60:
        return '41-60'
    else:
        return '61+'
# Iterate through the rows and categorize by age groups
for row in rows:
    age = int(row[0])
    charges = float(row[6])
    age_group = categorize_age(age)
    
    # Update the age group totals
    age_groups[age_group][0] += charges
    age_groups[age_group][1] += 1
# Calculate the average charges for each age group
avg_age_group_costs = {group: total_charges / count for group, (total_charges, count) in age_groups.items()}
# Print the results
print("Average Costs by Age Group:", avg_age_group_costs)


#-----------------------------------------------------------------------SmokerVSnon-Smoker cost
# Initialize variables for smoker and non-smoker costs
smoker_costs = [0, 0]  # [total_charges, count]
non_smoker_costs = [0, 0]  # [total_charges, count]
# Iterate through the rows and update costs by smoking status
for row in rows:
    smoker = row[4]
    charges = float(row[6])
    if smoker == 'yes':
        smoker_costs[0] += charges
        smoker_costs[1] += 1
    else:
        non_smoker_costs[0] += charges
        non_smoker_costs[1] += 1
# Calculate average costs
avg_smoker_cost = smoker_costs[0] / smoker_costs[1]
avg_non_smoker_cost = non_smoker_costs[0] / non_smoker_costs[1]
# Calculate the percentage increase
percentage_increase = ((avg_smoker_cost - avg_non_smoker_cost) / avg_non_smoker_cost) * 100
# Print the results
print(f"Average Cost for Smokers: ${avg_smoker_cost:.2f}")
print(f"Average Cost for Non-Smokers: ${avg_non_smoker_cost:.2f}")
print(f"Percentage Increase for Smokers: {percentage_increase:.2f}%")


#-----------------------------------------------------------------------Smoking and Region Correlation
# Initialize dictionaries for costs by smoking status and region
region_smoker_costs = {}
region_non_smoker_costs = {}
# Function to update costs by region and smoking status
def update_region_costs(region, smoker, charge):
    if smoker == 'yes':
        if region in region_smoker_costs:
            region_smoker_costs[region][0] += charge
            region_smoker_costs[region][1] += 1
        else:
            region_smoker_costs[region] = [charge, 1]
    else:
        if region in region_non_smoker_costs:
            region_non_smoker_costs[region][0] += charge
            region_non_smoker_costs[region][1] += 1
        else:
            region_non_smoker_costs[region] = [charge, 1]
# Iterate through the rows and update region costs
for row in rows:
    region = row[5]
    smoker = row[4]
    charges = float(row[6])
    update_region_costs(region, smoker, charges)
# Calculate average costs for each region
avg_region_smoker_costs = {region: total_charges / count for region, (total_charges, count) in region_smoker_costs.items()}
avg_region_non_smoker_costs = {region: total_charges / count for region, (total_charges, count) in region_non_smoker_costs.items()}
# Print the results
print("\nAverage Costs by Smoking Status and Region:")
print("Smokers:")
for region, avg_cost in avg_region_smoker_costs.items():
    print(f"Region: {region}, Average Cost: ${avg_cost:.2f}")
print("\nNon-Smokers:")
for region, avg_cost in avg_region_non_smoker_costs.items():
    print(f"Region: {region}, Average Cost: ${avg_cost:.2f}")


#-----------------------------------------------------------------------BMIvsCharges(1=positive, -1=negative, 0=no cerelation)
def calculate_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x_squared = sum(xi ** 2 for xi in x)
    sum_y_squared = sum(yi ** 2 for yi in y)
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2)) ** 0.5
    if denominator == 0:
        return 0
    return numerator / denominator
# Extract BMI and charges from rows
bmi_values = [float(row[2]) for row in rows]
charges_values = [float(row[6]) for row in rows]
# Calculate correlation
correlation = calculate_correlation(bmi_values, charges_values)
print(f"Correlation between BMI and Charges: {correlation:.2f}")


#-----------------------------------------------------------------------BMI Categories
# Initialize dictionaries for costs by BMI categories
bmi_categories = {
    'Underweight': [0, 0],
    'Normal': [0, 0],
    'Overweight': [0, 0],
    'Obese': [0, 0]}
# Function to categorize BMI
def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'
# Iterate through rows and categorize by BMI
for row in rows:
    bmi = float(row[2])
    charges = float(row[6])
    bmi_category = categorize_bmi(bmi)
    # Update the BMI category costs
    bmi_categories[bmi_category][0] += charges
    bmi_categories[bmi_category][1] += 1
# Calculate average costs for each BMI category
avg_bmi_category_costs = {category: total_charges / count for category, (total_charges, count) in bmi_categories.items()}
# Print the results
print("\nAverage Costs by BMI Category:")
for category, avg_cost in avg_bmi_category_costs.items():
    print(f"BMI Category: {category}, Average Cost: ${avg_cost:.2f}")


#-----------------------------------------------------------------------Gender and Smoking
# Initialize dictionaries for costs by gender and smoking status
gender_smoker_costs = {}
# Update costs by gender and smoking status
for row in rows:
    gender = row[1]
    smoker = row[4]
    charges = float(row[6])
    key = (gender, smoker)
    if key in gender_smoker_costs:
        gender_smoker_costs[key][0] += charges
        gender_smoker_costs[key][1] += 1
    else:
        gender_smoker_costs[key] = [charges, 1]
# Calculate average costs by gender and smoking status
avg_gender_smoker_costs = {key: total_charges / count for key, (total_charges, count) in gender_smoker_costs.items()}
# Print results
print("\nAverage Costs by Gender and Smoking Status:")
for key, avg_cost in avg_gender_smoker_costs.items():
    gender, smoker = key
    print(f"Gender: {gender}, Smoker: {smoker}, Average Cost: ${avg_cost:.2f}")
