import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import re


#Given Data


#Parsin
'''
data = pd.read_csv('march_data.csv')

emails = data['Email Address'].tolist()

names = data["First Name Last Name"].tolist()

O = (data["Are you an Observer or DC Member?"] != "Observer").astype(int).tolist()
#print(Observer)

#print(data.columns)

OC = (data["Are you Off Campus (needed for Duncan Room Scheduling) "] == "Yes").astype(int).tolist()
#print(campus)

month_map = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December"
}

def extract_and_format_shift(col):
    # Extract text within square brackets
    match = re.search(r'\[(.*?)\]', col)
    if match:
        shift = match.group(1)
        shift = shift.strip()  # Remove leading/trailing whitespace
        # Remove any trailing parenthetical information (including trailing whitespace)
        shift = re.sub(r'\s*\(.*?\)\s*$', '', shift)
        # Replace abbreviated month names with full names
        for abbr, full in month_map.items():
            shift = re.sub(r'\b' + re.escape(abbr) + r'\b', full, shift)
        return shift
    else:
        # Return the original column if no brackets are found
        return col


# Apply the function to all column names
data.columns = [extract_and_format_shift(col) for col in data.columns]

avail = data.iloc[:, 5:].values

dates = data.columns[5:]
print(dates)

pattern = re.compile(r'\b(Thu|Fri|Sat)\b.*8PM')

# Apply regex to each column name and build a binary array
dates_vector = np.array([1 if pattern.search(col) else 0 for col in data.columns])
print(dates_vector)

avail = np.nan_to_num(avail, nan=0).astype(int)



num_people = avail.shape[0]
num_shifts = avail.shape[1]
'''

'''
# Set random seed for reproducibility
#random.seed(42)
#np.random.seed(42)

# Create fake names and emails
first_names = ["Alex", "Jamie", "Taylor", "Jordan", "Morgan", "Casey", "Riley", "Avery", "Peyton", "Quinn",
               "Drew", "Cameron", "Skyler", "Logan", "Charlie", "Reese", "Emerson", "Rowan", "Dakota", "Elliot"]
last_names = ["Smith", "Johnson", "Lee", "Brown", "Jones", "Garcia", "Davis", "Miller", "Wilson", "Anderson",
              "Thomas", "Moore", "Jackson", "Martin", "Clark", "Lewis", "Walker", "Young", "Allen", "King"]

names = [f"{first} {last}" for first, last in zip(first_names, last_names)]
emails = [f"{name.lower().replace(' ', '.')}@rice.edu" for name in names]

# Most people are DCs (1), some are Observers (0)
O = np.random.choice([1, 0], size=20, p=[0.85, 0.15]).tolist()

# Most people are on campus (0), some are off-campus (1)
OC = np.random.choice([0, 1], size=20, p=[0.8, 0.2]).tolist()

# Generate availability: 4 shifts per person
num_people = 20
num_shifts = 25
avail = np.zeros((num_people, num_shifts), dtype=int)

for i in range(num_people):
    available_shifts = np.random.choice(num_shifts, size=4, replace=False)
    avail[i, available_shifts] = 1

# Create shift names
dates = [f"March {i+1} (Day {random.choice(['Thu', 'Fri', 'Sat'])}) 8PM" for i in range(num_shifts)]

# Prepare synthetic data summary
import ace_tools as tools; tools.display_dataframe_to_user(name="Synthetic REMS Data", dataframe=pd.DataFrame(avail, columns=dates))

# Package up all parts to return
synthetic_data_summary = {
    "emails": emails,
    "names": names,
    "O": O,
    "OC": OC,
    "dates": dates,
    "avail_matrix_shape": avail.shape,
}
'''
model = gp.Model("REMS")
#Decision Variables
x = model.addVars(num_people, num_shifts, vtype=GRB.BINARY, name="x")

# buffer for no more than three people are assigned to a shift 
b = model.addVars(num_shifts, vtype=GRB.INTEGER, lb=0, name="b")

# buffer for if people are not assigned to 2 shifts 
m = model.addVars(num_people, vtype=GRB.INTEGER, lb=0, name="m")


#Objective Function

model.setObjective(sum(m[i] for i in range(num_people)) + sum(b[j] for j in range(num_shifts)), 
GRB.MINIMIZE)

#Constraints

#making sure no one is given a shift they didn't sign up for
for shift in range(num_shifts):
    for per in range(num_people):
        model.addConstr(x[per, shift] <= avail[per, shift])
    


#making sure that no more than 2 Duty Crew are assigned to a shift
for shift in range(num_shifts):
    model.addConstr(sum(x[i, shift]*O[i]  for i in range(num_people)) + b[shift] == 2)

#making sure that no more than 3 people are assigned to a shift
for shift in range(num_shifts):
    model.addConstr(sum(x[i, shift] for i in range(num_people))+ b[shift] <= 3)

#ensure that no one is assigned to more than 2 shifts
for per in range(num_people):
    model.addConstr(sum(x[per, shift] for shift in range(num_shifts)) + m[per] == 2)

#no more than 2 OC are assigned to a shift
for shift in range(num_shifts):
    model.addConstr(sum(x[per, shift]*OC[per] for per in range(num_people)) <= 2)


model.optimize()

all_vars = model.getVars()
values = model.getAttr("X", all_vars)
names = model.getAttr("VarName", all_vars)

for name, val in zip(names, values):
    print(f"{name} = {val}")

x_values = np.zeros((num_people, num_shifts))

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# Create an empty NumPy array to store values
x_values = np.zeros((num_people, num_shifts))

# Fill the array with optimized values
for i in range(num_people):
    for j in range(num_shifts):
        x_values[i, j] = x[i, j].X  # Get the value of the decision variable

# Print the full matrix
print(x_values)

