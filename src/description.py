#!/usr/bin/env python3
#coding 'utf-8'

'''
src/description.py
Generates desription of Kaggle H1-B dataset.
- Elvis Yu
- Luke Duane
- Will Badart
created: MAR 2018
'''

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#from mpl_toolkits.basemap import Basemap

h1bdat = pd.read_csv(sys.argv[1])
h1bdat = h1bdat.drop(["Unnamed: 0"], axis=1)


print('Number of entries:', h1bdat.shape[0])
print('Number of missing data in each column:')
print(h1bdat.isnull().sum())

ax1 = h1bdat['EMPLOYER_NAME'][h1bdat['YEAR'] == 2011].groupby(h1bdat['EMPLOYER_NAME']).count().sort_values(ascending=False).head(10).plot(kind='barh', title="Top 10 Applicants, 2011")
ax1.set_ylabel("")
plt.show()
ax2 = h1bdat['EMPLOYER_NAME'][h1bdat['YEAR'] == 2016].groupby(h1bdat['EMPLOYER_NAME']).count().sort_values(ascending=False).head(10).plot(kind='barh', title="Top 10 Applicant, 2016")
ax2.set_ylabel("")
plt.show()
ax3 = h1bdat['EMPLOYER_NAME'].groupby([h1bdat['EMPLOYER_NAME']]).count().sort_values(ascending=False).head(10).plot(kind='barh', title="Top 10 Applicant over 2011 to 2016")
ax3.set_ylabel("")
plt.show()


topEmp = list(h1bdat['EMPLOYER_NAME']
[h1bdat['YEAR'] >= 2015].groupby(h1bdat['EMPLOYER_NAME']).count().sort_values(ascending=False).head(10).index)
byEmpYear = h1bdat[['EMPLOYER_NAME', 'YEAR', 'PREVAILING_WAGE']][h1bdat['EMPLOYER_NAME'].isin(topEmp)]
byEmpYear = byEmpYear.groupby([h1bdat['EMPLOYER_NAME'],h1bdat['YEAR']])
markers=['o','v','^','<','>','d','s','p','*','h','x','D','o','v','^','<','>','d','s','p','*','h','x','D']
fig = plt.figure(figsize=(12,7))
for company in topEmp:
    tmp = byEmpYear.count().loc[company]
    plt.plot(tmp.index.values, tmp["PREVAILING_WAGE"].values, label=company, linewidth=2,marker=markers[topEmp.index(company)])
plt.xlabel("Year")
plt.ylabel("Number of Applications")
plt.legend()
plt.title('Number of Applications of Top 10 Applicants')
plt.show()

columnname = 'PREVAILING_WAGE'
column = h1bdat[columnname]
print("Description of salary:")
print(column.describe())
fig = plt.figure(figsize=(10,7))
for company in topEmp:
    tmp = byEmpYear.mean().loc[company]
    plt.plot(tmp.index.values, tmp["PREVAILING_WAGE"].values, label=company, linewidth=2,  marker=markers[topEmp.index(company)])

plt.xlabel("Year")
plt.ylabel("Average Salary Offer (USD)")
plt.legend()
plt.title("Average Salary of Top 10 Applicants")
plt.show()

PopJobs = h1bdat[['JOB_TITLE', 'EMPLOYER_NAME', 'PREVAILING_WAGE']][h1bdat['EMPLOYER_NAME'].isin(topEmp)].groupby(['JOB_TITLE'])
topJobs = list(PopJobs.count().sort_values(by='EMPLOYER_NAME', ascending=False).head(30).index)
df = PopJobs.count().loc[topJobs].assign(mean_wage=PopJobs.mean().loc[topJobs])
fig = plt.figure(figsize=(10,12))
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
width = 0.35
df.EMPLOYER_NAME.plot(kind='barh', ax=ax1, color='C0', width=0.4, position=0, label='# of Applications')
df.mean_wage.plot(kind='barh', ax=ax2, color='C7', width=0.4, position=1, label='Mean Salary')
ax1.set_xlabel('Number of Applications')
ax1.set_ylabel('')
ax1.legend(loc=(0.75,0.55))
ax2.set_xlabel('Mean Salary')
ax2.set_ylabel('Job Title')
ax2.legend(loc=(0.75,0.50))
plt.show()

ax = h1bdat[['JOB_TITLE', 'EMPLOYER_NAME', 'PREVAILING_WAGE']][h1bdat['EMPLOYER_NAME'].isin(topEmp)  & h1bdat['JOB_TITLE'].isin(topJobs)]['PREVAILING_WAGE'].hist(bins=100)
ax.set_ylabel('Offering Wage (USD/year)')
plt.title('Offering Salary Distribution of Popular Jobs from Top Applicants')
plt.show()

PopJobsAll = h1bdat[['JOB_TITLE', 'EMPLOYER_NAME', 'PREVAILING_WAGE']].groupby(['JOB_TITLE'])
topJobsAll = list(PopJobsAll.count().sort_values(by='EMPLOYER_NAME', ascending=False).head(30).index)
dfAll = PopJobsAll.count().loc[topJobsAll].assign(mean_wage=PopJobsAll.mean().loc[topJobsAll])
fig = plt.figure(figsize=(10,12))
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
width = 0.35
dfAll.EMPLOYER_NAME.plot(kind='barh', ax=ax1, color='C0', width=0.4, position=0, label='# of Applications')
dfAll.mean_wage.plot(kind='barh', ax=ax2, color='C7', width=0.4, position=1, label='Mean Salary')
ax1.set_xlabel('# of Applications')
ax1.set_ylabel('')
ax1.legend(loc=(0.75,0.55))
ax2.set_xlabel('Mean wage')
ax2.set_ylabel('Job Title')
ax2.legend(loc=(0.75,0.50))
plt.show()
