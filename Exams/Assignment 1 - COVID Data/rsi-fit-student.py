import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
path_to_datafile = "../../data/drop-jump/all_participant_data_rsi.csv"

### YOUR CODE HERE
data = pd.read_csv(path_to_datafile)

accel_rsi = data['accelerometer_rsi'].to_numpy()
force_plate_rsi = data['force_plate_rsi'].to_numpy()

alpha = 0.05

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

### YOUR CODE HERE
##fit accel and forceplt rsi to norm dist
accel_mu, accel_std = norm.fit(accel_rsi)
fp_mu, fp_std = norm.fit(force_plate_rsi)

##report parametetrs
print("Acceleration RSI")
print("mu =", accel_mu)
print("std =", accel_std)

print("Force Plate RSI")
print("mu =", fp_mu)
print("std =", fp_std)

##create pdf for accel
x_accel = np.linspace(min(accel_rsi), max(accel_rsi), 1000)
y_accel = norm.pdf(x_accel, loc=accel_mu, scale=accel_std)

##create and label plot
plt.figure()
plt.plot(x_accel, y_accel, label='Acceleration RSI Normal PDF')
plt.title('Acceleration RSI Normal Distribution')
plt.xlabel('RSI')
plt.ylabel('Probability Density')
plt.legend()
plt.show()

## create pdf for forceplt
x_fp = np.linspace(min(force_plate_rsi), max(force_plate_rsi), 1000)
y_fp = norm.pdf(x_fp, loc=fp_mu, scale=fp_std)

plt.figure()
plt.plot(x_fp, y_fp, label='Force Plate RSI Normal PDF')
plt.title('Force Plate RSI Normal Distribution')
plt.xlabel('RSI')
plt.ylabel('Probability Density')
plt.legend()
plt.show()


"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

"""
Acceleration
"""
### YOUR CODE HERE
##bin setup for even spacing inside
inside_bins = np.linspace(0, 2, 10)

bins = []
##add neg inf to cover pts outside bin range to match infinite distribution norm bin cnt
bins.append(-np.inf)

##add vals in range
for value in inside_bins:
    bins.append(value)

####add pos inf to cover pts outside bin range to match infinite distribution norm bin cnt
bins.append(np.inf)

##make bins an array
bins = np.array(bins)

##parse accel vals in bin range
accel_hist = np.histogram(accel_rsi, bins=bins)
accel_obs = accel_hist[0]

accel_exp_list = []

##use norm dist to estimate expected vals in bin range
for i in range(len(bins) - 1):
    left = bins[i]
    right = bins[i+1]

    prob = norm.cdf(right, accel_mu, accel_std) - norm.cdf(left, accel_mu, accel_std)
    count = prob * len(accel_rsi)

    accel_exp_list.append(count)

##use chitest to compare expected to actual
accel_exp = np.array(accel_exp_list)

chi2_accel, p_accel = chisquare(accel_obs, accel_exp)

print("Acceleration chi2 =", chi2_accel)
print("Acceleration p =", p_accel)

##use pval to check fit
if p_accel < alpha:
    print("Acceleration: Not a good fit")
else:
    print("Acceleration: Good fit")


"""
Force Plate
"""
### YOUR CODE HERE
##same as above for forceplate
fp_hist = np.histogram(force_plate_rsi, bins=bins)
fp_obs = fp_hist[0]

fp_exp_list = []

for i in range(len(bins) - 1):
    left = bins[i]
    right = bins[i+1]

    prob = norm.cdf(right, fp_mu, fp_std) - norm.cdf(left, fp_mu, fp_std)
    count = prob * len(force_plate_rsi)

    fp_exp_list.append(count)

fp_exp = np.array(fp_exp_list)

chi2_fp, p_fp = chisquare(fp_obs, fp_exp)

print("\nForce Plate chi2 =", chi2_fp)
print("Force Plate p =", p_fp)

if p_fp < alpha:
    print("Force Plate: Not a good fit")
else:
    print("Force Plate: Good fit")

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

### YOUR CODE HERE
##perform and store ttest comparing accel to force plate
t_stat, p_val = ttest_ind(accel_rsi, force_plate_rsi)

print("t-stat =", t_stat)
print("p =", p_val)

##compare pval to given alpha
if p_val < alpha:
    print("Means are NOT equal")
else:
    print("Means are equal")

"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

### YOUR CODE HERE
##create array for difference of force and accel
error = force_plate_rsi - accel_rsi

##norm fit error array
error_mu, error_std = norm.fit(error)

print('\n\n-----Question 4-----')
print("Error mu =", error_mu)
print("Error std =", error_std)

##setup plot and display
x_values = np.linspace(min(error), max(error), 1000)
y_values = norm.pdf(x_values, error_mu, error_std)

plt.figure()
plt.hist(error, bins=16, density=True, alpha=0.6, label="Error Histogram")
plt.plot(x_values, y_values, label="Normal Fit")
plt.title("RSI Error Distribution")
plt.xlabel("Error")
plt.ylabel("Density")
plt.legend()
plt.show()