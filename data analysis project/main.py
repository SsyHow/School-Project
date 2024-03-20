#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Third-party libraries
# NOTE: You may **only** use the following third-party libraries:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from thefuzz import fuzz
from thefuzz import process
# NOTE: It isn't necessary to use all of these to complete the assignment, 
# but you are free to do so, should you choose.

# Standard libraries
# NOTE: You may use **any** of the Python 3.11 or Python 3.12 standard libraries:
# https://docs.python.org/3.11/library/index.html
# https://docs.python.org/3.12/library/index.html
from pathlib import Path
# ... import your standard libraries here ...


######################################################
# NOTE: DO NOT MODIFY THE LINE BELOW ...
######################################################
studentid = Path(__file__).stem

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION BELOW ...
######################################################
def log(question, output_df, other):
    print(f"--------------- {question}----------------")

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


######################################################
# NOTE: YOU MAY ADD ANY HELPER FUNCTIONS BELOW ...
######################################################



######################################################
# QUESTIONS TO COMPLETE BELOW ...
######################################################

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_1(jobs_csv):
    """Read the data science jobs CSV file into a DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_csv (str): Path to the jobs CSV file.

    Returns:
        DataFrame: The jobs DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    df = pd.read_csv('ds_jobs.csv')

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 1", output_df=df, other=df.shape)
    return df



######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_2(cost_csv, cost_url):
    """Read the cost of living CSV into a DataFrame.  If the CSV file does not 
    exist, scrape it from the specified URL and save it to the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the cost of living CSV file.
        cost_url (str): URL of the cost of living page.

    Returns:
        DataFrame: The cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    csvFile = Path(cost_csv)
    if csvFile.exists():
        df = pd.read_csv(cost_csv)
    else:
        df = pd.read_html(cost_url)[0]
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df.to_csv(cost_csv, index=False)
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 2", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_3(currency_csv, currency_url):
    """Read the currency conversion rates CSV into a DataFrame.  If the CSV 
    file does not exist, scrape it from the specified URL and save it to 
    the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the currency conversion rates CSV file.
        cost_url (str): URL of the currency conversion rates page.

    Returns:
        DataFrame: The currency conversion rates DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    csvFile = Path(currency_csv)
    if csvFile.exists():
        df = pd.read_csv(currency_csv)
    else:
        df = pd.read_html(currency_url)[0]
        df = df.drop('Nearest actual exchange rate', axis = 1, level = 0)
        df.columns = df.columns.get_level_values(1)
        df.columns = [col.replace('\xa0', ' ') for col in df.columns]
        df = df.replace('\u00A0', ' ',regex=True)
        # for i in range(18):
        #     for j in range(4):
        #         if '\u00a0' in df.iat[i,j]:
        #             print(df.iat[i,j])                    
        df = df.drop('30 Jun 23', axis=1)
        df = df.rename(columns={'31 Dec 23': 'rate'})
        df.reset_index(drop=True, inplace=True)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df.to_csv(currency_csv, index=False)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    # ######################################################
    log("QUESTION 3", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_4(country_csv, country_url):
    """Read the country codes CSV into a DataFrame.  If the CSV file does not 
    exist, it will be scrape the data from the specified URL and save it to the 
    CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the country codes CSV file.
        cost_url (str): URL of the country codes page.

    Returns:
        DataFrame: The country codes DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    csvFile = Path(country_csv)
    if csvFile.exists():
        df = pd.read_csv(country_csv)
    else:
        df = pd.read_html(country_url)[0]
        df = df.drop(['Year', 'ccTLD', 'Notes'], axis = 1)
        df = df.rename(columns={'Country name (using title case)': 'country', 'Code': 'code'})
        df.to_csv(country_csv, index=False)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 4", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_5(jobs_df):
    """Summarise some dimensions of the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The summary DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = pd.DataFrame(index=jobs_df.columns, columns=['observations', 'distinct', 'missing'])
    for column in jobs_df.columns:
        df.at[column, 'observations'] = jobs_df[column].count()
        df.at[column, 'distinct'] = jobs_df[column].nunique()
        df.at[column, 'missing'] = jobs_df[column].isnull().sum()

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 5", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_6(jobs_df):
    """Add an experience rating column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The jobs DataFrame with the experience rating column added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    rating = {'EN': 1, 'MI': 2, 'SE': 3, 'EX': 4}
    jobs_df['experience_rating'] = jobs_df['experience_level'].map(rating)
    df = jobs_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 6", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_7(jobs_df, country_df):
    """Merge the jobs and country codes DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 6.
        country_df (DataFrame): The country codes DataFrame returned in 
                                question 4.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    # print(jobs_df, country_df)
    country_df.set_index('code', inplace=True)
    jobs_df['country'] = jobs_df['employee_residence'].map(country_df['country'])
    df = jobs_df

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 7", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_8(jobs_df, currency_df):
    """Add an Australian dollar salary column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 7.
        currency_df (DataFrame): The currency conversion rates DataFrame 
                                 returned in question 3.

    Returns:
        DataFrame: The jobs DataFrame with the Australian dollar salary column
                   added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    
    jobs_df = jobs_df[jobs_df['work_year'] == 2023]
    rate = float(currency_df.loc[currency_df['country'] == 'United States', 'rate'].iloc[0])
    
    jobs_df['salary_in_aud'] = jobs_df['salary_in_usd'] * rate
    jobs_df['salary_in_aud'] = jobs_df['salary_in_aud'].astype('int') 
    # print(df)
    df = jobs_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 8", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_9(cost_df):
    """Re-scale the cost of living DataFrame to be relative to Australia.

    See the assignment spec for more details.

    Args:
        cost_df (DataFrame): The cost of living DataFrame returned in question 2.

    Returns:
        DataFrame: The re-scaled cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    
    cost_df = cost_df[['country', 'cost_of_living_plus_rent_index']]
    index = cost_df.loc[cost_df['country'] == 'Australia', 'cost_of_living_plus_rent_index'].iloc[0]
    cost_df['cost_of_living_plus_rent_index'] = ((cost_df['cost_of_living_plus_rent_index'] / index) * 100).round(1)
    cost_df = cost_df.sort_values(by='cost_of_living_plus_rent_index')
    df = cost_df
    # print(df)
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 9", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_10(jobs_df, cost_df):
    """Merge the jobs and cost of living DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 8.
        cost_df (DataFrame): The cost of living DataFrame returned in question 9.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=1):
        """
        :param df_1: the left table to join
        :param df_2: the right table to join
        :param key1: key column of the left table
        :param key2: key column of the right table
        :param threshold: how close the matches should be to return a match, based on Levenshtein distance
        :param limit: the amount of matches that will get returned, these are sorted high to low
        :return: dataframe with boths keys and matches
        """
        s = df_2[key2].tolist()
        
        m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
        df_1['matches'] = m
        
        m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
        df_1['matches'] = m2
        
        return df_1
    
    fuzzy_merge(jobs_df, cost_df, 'country', 'country', 90)
    jobs_df = jobs_df[jobs_df['matches'] != '']
    jobs_df = pd.merge(jobs_df, cost_df, left_on='matches', right_on='country', how='left')
    jobs_df = jobs_df.drop(columns=['matches','country_y'])
    jobs_df = jobs_df.rename(columns={'country_x': 'country'})
    df = jobs_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 10", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_11(jobs_df):
    """Create a pivot table of the average salary in AUD by country and 
    experience rating.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.

    Returns:
        DataFrame: The pivot table.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    jobs_df = jobs_df.pivot_table(values='salary_in_aud', 
                             index='country', 
                             columns='experience_rating', 
                             aggfunc='mean')
    jobs_df = jobs_df.fillna(0).astype(int)
    jobs_df.columns = pd.MultiIndex.from_tuples([('salary_in_aud', i) for i in jobs_df.columns])
    jobs_df = jobs_df.sort_values(by=[('salary_in_aud', i[1]) for i in jobs_df.columns], ascending=False)
    df = jobs_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 11", output_df=None, other=df)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_12(jobs_df):
    """Create a visualisation of data science jobs to help inform a decision
    about where to live, based (minimally) on salary and cost of living.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
 
    # I want to only consider the FT jobs and senior level only. 
    ft_df = jobs_df[jobs_df['employment_type'] == 'FT']
    ft_df = ft_df[ft_df['experience_level'] == 'SE']
    # ft_df = ft_df[ft_df['country'] != 'Israel']
    average_salary = ft_df.groupby(['country'])['salary_in_aud'].mean().reset_index()
    average_salary['salary_in_aud'] = average_salary['salary_in_aud'].round(0).astype(int)
    average_salary = average_salary.sort_values(by='salary_in_aud', ascending=True)
    # print(average_salary.columns, average_salary.shape)
    selected_columns = jobs_df[['country', 'cost_of_living_plus_rent_index', 'employee_residence']]
    selected_columns = selected_columns.drop_duplicates()
    # print(selected_columns)

    average_salary = pd.merge(average_salary, selected_columns, on='country', how='left')
   
    _, axs1 = plt.subplots()
    axs1.bar(average_salary['employee_residence'], average_salary['salary_in_aud'], color='skyblue', label='Average Salary')
    # axs[0].set_title('Full Time Senior Level Average Salary by Country')
    axs1.set_xlabel('Country')
    axs1.set_ylabel('Average Salary(in AUD)')
    axs1.tick_params('y', color='b')
    axs2 = axs1.twinx()
    axs2.plot(average_salary['employee_residence'], average_salary['cost_of_living_plus_rent_index'], color='red',label='Cost of Living')
    # axs[1].set_title('Full Time Senior Level Average Salary vs. Cost of Living by Country')
    axs2.set_ylabel('Cost of Living plus rent (AU index = 100)')
    axs2.tick_params('y', color='r')
    # plt.xticks(rotation=45)
    line1, label1 = axs1.get_legend_handles_labels()
    line2, label2 = axs2.get_legend_handles_labels()
    axs2.legend(line1+line2, label1+label2, loc='upper left')
    plt.title("Full Time Senior Average Salary and Cost of Living by Country")


    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    plt.savefig(f"{studentid}-Q12.png")


######################################################
# NOTE: DO NOT MODIFY THE MAIN FUNCTION BELOW ...
######################################################
if __name__ == "__main__":
    # data ingestion and cleaning
    df1 = question_1("ds_jobs.csv")
    df2 = question_2("cost_of_living.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/cost_of_living.html")
    df3 = question_3("exchange_rates.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/exchange_rates.html")
    df4 = question_4("country_codes.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/country_codes.html")

    # data exploration
    df5 = question_5(df1.copy(True))

    # data manipulation
    df6 = question_6(df1.copy(True))
    df7 = question_7(df6.copy(True), df4.copy(True))
    df8 = question_8(df7.copy(True), df3.copy(True))
    df9 = question_9(df2.copy(True))
    df10 = question_10(df8.copy(True), df9.copy(True))
    df11 = question_11(df10.copy(True))

    # data visualisation
    question_12(df10.copy(True))
