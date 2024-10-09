# Examples: Generate fake profiles for testing
def variable_name_to_text (variable):
    for name, value in globals().items():
        if id(value) == id(variable):
            return name
    return None
def display_results(variable):
    print(f"{variable_name_to_text (variable)} = {variable}")


def generate_random_integer(bound_upper, bound_lower):
    return random.randint(bound_lower, bound_upper)

def generate_random_integer(bound_upper, bound_lower):
    return random.randint(bound_lower, bound_upper)
    
def generate_random_float(bound_upper, bound_lower):
    return random.uniform(bound_lower, bound_upper)


import datetime
import random
from dateutil.relativedelta import relativedelta

# [Sample Usage]
# Generate a random date
year = random.randint(2000, 2023)
month = random.randint(1, 12)
day = random.randint(1, 28)
date = datetime.date(year, month, day)
duration_hours = random.randint(1, 24)
time_start = datetime.datetime.now()
time_end = time_start + datetime.timedelta(hours=duration_hours)
# Define the start and end dates
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2023, 4, 15)

# Calculate the time delta in years and months
delta = relativedelta(end_date, start_date)
years = delta.years
months = delta.months
end_date = start_date + relativedelta(months=6, years=2)

print("Start date:", start_date)
print("End date:", end_date)
print("Time elapsed: {} years and {} months".format(years, months))
print("Start time:", time_start)
print("End time:", time_end)
print("Duration (in hours):", duration_hours)
#print("Time elapsed:", time_elapsed)

#!pip install faker
from faker import Faker
fake = Faker() # create a Faker object

name = fake.name()
address = fake.address() # generate a random address
country_code = fake.country_code(representation="alpha-3") # generate a random country code in ISO 3166-1 alpha-3 format
phone_number = fake.phone_number() # generate a random phone number
credit_card_number = fake.credit_card_number()
company = fake.company()
job = fake.job()
profile = [name, address, country_code, phone_number, credit_card_number, company, job]

for i in range(len(profile)):
    display_results(globals()[variable_name_to_text(profile[i])])

age = generate_random_integer(bound_upper = 124, bound_lower = 0)
weight_in_kgs = generate_random_integer(bound_upper = 100, bound_lower = 2)
profile = [age, weight_in_kgs]

username = fake.user_name()
random_word = fake.word()
random_sentence = fake.sentence()
profile = [username, random_word, random_sentence]

for i in range(len(profile)):
    display_results(globals()[variable_name_to_text(profile[i])])
"""
Start date: 2020-01-01
End date: 2022-07-01
Time elapsed: 3 years and 3 months
Start time: 2024-10-09 16:20:32.331772
End time: 2024-10-10 10:20:32.331772
Duration (in hours): 18
name = Michael Murphy
address = 6170 Michelle Motorway Suite 853
Armstrongfurt, IN 58838
country_code = PHL
phone_number = +1-882-444-4528x924
credit_card_number = 372138467440184
company = Drake Ltd
job = Insurance risk surveyor
username = diazdeborah
random_word = professional
random_sentence = Look environmental quite meet cause society.
"""
""" This can be written to a csv file (or format to json) as:
id;date;age;age_range;sex;job_title;marital_status;education;height;weight;location;BMI;health_record;opt-in;
m00001;20160919;19;18-29;female;student;unmarried;masters;155;43;USA;h89802289;yes;
"""