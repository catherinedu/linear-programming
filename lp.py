from pulp import *

# Creates a list of the Ingredients
Ingredients = ['TOMATO', 'LETTUCE', 'SPINACH', 'CARROT',  'OIL']

kcal = {'TOMATO': 21, 
         'LETTUCE': 16, 
         'SPINACH': 371, 
         'CARROT': 346, 
         'OIL': 884}

protein = {'TOMATO': 0.85, 
         'LETTUCE': 1.62, 
         'SPINACH': 12.78, 
         'CARROT': 8.39, 
         'OIL': 0}

fat = {'TOMATO': 0.33, 
         'LETTUCE': 0.20, 
         'SPINACH': 1.58, 
         'CARROT': 1.39, 
         'OIL': 100.0}

carbs = {'TOMATO': 4.64, 
         'LETTUCE': 2.37, 
         'SPINACH': 74.69, 
         'CARROT': 80.7, 
         'OIL': 0.0}

sodium = {'TOMATO': 9.0, 
         'LETTUCE': 8.0, 
         'SPINACH': 7.0, 
         'CARROT': 508.2, 
         'OIL': 0.0}



# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Salad Problem", LpMinimize)

# A dictionary called 'ingredient_vars' is created to contain the referenced Variables
ingredient_vars = LpVariable.dicts("Ingr",Ingredients,0)

# The objective function is added to 'prob' first
prob += lpSum([kcal[i]*ingredient_vars[i] for i in Ingredients]), "Total kCal of Ingredients per salad"

# The constraints are added to 'prob'
prob += lpSum([protein[i] * ingredient_vars[i] for i in Ingredients]) >= 15.0, "ProteinRequirement"
prob += 6.0 >= lpSum([fat[i] * ingredient_vars[i] for i in Ingredients]) >= 2.0, "FatRequirement"
prob += lpSum([carbs[i] * ingredient_vars[i] for i in Ingredients]) >= 4.0, "CarbRequirement"
prob += lpSum([sodium[i] * ingredient_vars[i] for i in Ingredients]) <= 100.0, "SodiumRequirement"
#prob += lpSum(prob.variables()[2].varValue + prob.variables()[4].varValue) / lpSum([prob.variables()[i].varValue for i in range(8)]) >= 0.40, "GreensRequirement"
prob += (1 - 0.5) * ingredient_vars['TOMATO'] + (0 - 0.5) * ingredient_vars['LETTUCE'] + \
        (0 - 0.5) * ingredient_vars['SPINACH'] + (1 - 0.5) * ingredient_vars['CARROT'] + \
        (1 - 0.5) * ingredient_vars['OIL'] >= 0.0, 'GreensRequirement'
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total kCal of Ingredients per salad = ", value(prob.objective))