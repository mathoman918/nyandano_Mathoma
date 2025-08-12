import math

# show the user the calculation they can do
print ("Investment - to calculate the amount of interest you'll earn on your investment.")
print ("Bond - to calculate the amount you'll have to pay on a home loan.")
print ("Enter either “investment” or “bond” from the menu above to proceed:")
calculation = input("enter the calculation you want to do: ").lower()

# investment calculation
if calculation == "investment":
# ask for the deposit amount, interest rate and number of years they plan on investing.
#ask the user to input if they want “simple” or “compound” interest
 p = float(input("enter the amount you want to deposit: "))
 rate = float(input("Enter the interest rate (without % sign): "))
 t = int(input("enter the number of years you plan on investing: "))
 interest = input("do you want simple or compound interest: ").lower()
 r = rate/100

 if interest == "simple":
  a = p * (1 + r*t)
  print (f"total amount after {t} years with simple interest is: {a:.2f}")

 elif interest == "compound":
  a = p *math.pow((1+r),t)
  print (f"total amount after {t} years with compound interest is: {a:.2f}")
 else:
  print("Invalid interest type. Please enter 'simple' or 'compound'.")

# bond calculation
elif calculation == "bond":

#present value of the property ,interest rate, number of months they plan to repay the bond
 p = float(input("enter the current value of the house: "))
 r = float(input("enter the interest rate(without % sign): "))
 n = int(input("enter the number of months you plan to repay the bond: "))

 i = (r/100)/12
 repayment = (i * p)/(1 - (1 + i)**(-n))

 print(f"Your monthly repayment will be: {repayment:.2f}")

else:
 print ("your entry is invalid, please enter investment or bond: ")