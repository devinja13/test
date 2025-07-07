import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import re


# penalize open shift THRS, FRI, and SAT nights
#   binary vector -- high demand nights
# balance # of night and day shifts


data = pd.read_csv('march_data.csv')

month = "March"

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
hd = np.array([1 if pattern.search(col) else 0 for col in data.columns])

avail = np.nan_to_num(avail, nan=0).astype(int)



num_people = avail.shape[0]
num_shifts = avail.shape[1]



model = gp.Model("REMS")







#Decision Variables
x = model.addVars(num_people, num_shifts, vtype=GRB.BINARY, name="x")

# buffer for no more than three people are assigned to a shift 
b = model.addVars(num_shifts, vtype=GRB.INTEGER, lb=0, name="b")

# buffer for if people are not assigned to 2 shifts 
m = model.addVars(num_people, vtype=GRB.INTEGER, lb=0, name="m")


#Objective Function


#High demand nights (THR, FRI, SAT)
#hd = [0,1,0,1,0,1,0,0,0,0,0,0,0,0,0] * 4

#is night shift
isnight = [-1,1] * int(num_shifts / 2)

under_ulitilized_penalty = sum(m[i] for i in range(num_people))
under_staffed_penalty = 1 * sum(b[j] * hd[j] for j in range(num_shifts)) + .2 * sum(b[j] * (1 - hd[j]) for j in range(num_shifts))
balanced_times_penalty = sum((sum(x[i,j] * isnight[j] for j in range(num_shifts))) ** 2 for i in range(num_people))
model.setObjective(5 * under_ulitilized_penalty + 10 * under_staffed_penalty + balanced_times_penalty , GRB.MINIMIZE)

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


#Optional constraint for now    
# ensure every shift has at least one person
#for shift in range(num_shifts):
#    model.addConstr(sum(x[i, shift] for i in range(num_people)) >= 1)


model.optimize()

all_vars = model.getVars()
values = model.getAttr("X", all_vars)
#names = model.getAttr("VarName", all_vars)

#for name, val in zip(names, values):
#    print(f"{name} = {val}")

x_values = np.zeros((num_people, num_shifts))

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# Create an empty NumPy array to store values
x_values = np.zeros((num_people, num_shifts))

# Fill the array with optimized values
for i in range(num_people):
    for j in range(num_shifts):
        
        if avail[i,j] == 1:
             x_values[i, j] = x[i, j].X  # Get the value of the decision variable
             if x_values[i,j] == 0:
                 x_values[i,j] = 2

shifts_this_month = [f"{month} {i} {shift}" for i in range(1, 32) for shift in ["Morning", "Evening"]]
df = pd.DataFrame(x_values, columns = shifts_this_month)
df = df.set_index(pd.Index(tuple(zip(names,emails))))
df.to_csv("sample_output.csv")
print(df.head())

    
# Print the full matrix
# Number of people assigned to eachs shift         
print(np.sum(x_values, axis=0))
#Number of shifts assigned to each person
print(np.sum(x_values, axis=1))

