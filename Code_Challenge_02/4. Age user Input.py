# Get the user's current age
current_age = int(input("Please enter your current age: "))

# Assuming retirement age is 65
retirement_age = 65

# Calculate the years until retirement
years_until_retirement = 65 - current_age

# Check if the user has already reached or exceeded retirement age
if years_until_retirement > 0:
    print("You have " + str(years_until_retirement) + "years left to retire")
elif years_until_retirement == 0:
    print("Congratulations! You have reached retirement age.")
else:
    print("You are already past your retirement age (65).")
