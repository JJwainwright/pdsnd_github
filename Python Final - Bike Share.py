import time
import pandas as pd
import numpy as np

CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }
Cities = ["chicago", "new york city", "washington"]

Months = ["january", "february", "march", "april", "may", "june"]

Days = ["sunday", "monday", "tuesday", "wednesday", 
        "thursday", "friday", "saturday" ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Welcome! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True: 
        city = input("Which city would you like to learn more about Chicago, New York City or Washington? \n> ").lower()
        if city in Cities:
            break 
        else: 
            print("\n\t ERROR: " + city + " is not valid, please enter a valid city.")

    # get user input for month (all, january, february, ... , june)
    while True: 
        month = input("Please provide us a month name or type 'all' to apply no month filter.\n (Choices: all, january, february, march, april, may or june)\n>").lower().replace(" ","")
        if month in Months or month == "all":
            break     
        else:
            print("\n\t ERROR: " + month + " is not valid, please enter a month or 'all'.")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: 
        day = input("Please provide us a day of the week or type 'all' to apply no day filter.\n Once entered we will start our analysis!\n (Choices: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday)\n>").lower().replace(" ","")
        if day in Days or day =="all":
            break 
        else:
            print("\n\t ERROR: " + day + " is not valid, please enter a week day name or 'all'.")
        
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Statistics for the most common times of travel."""
    print("\nThe Most Common Times of Travel:\n")
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].value_counts().idxmax()
    most_common_month_name = Months[most_common_month - 1].title()
    print(most_common_month_name + "is the most common month.")

    # display the most common day of week
    most_common_day_of_week = df["day_of_week"].value_counts().idxmax()
    print(most_common_day_of_week, "is the most common day of week." )

    # display the most common start hour

    most_common_start_hour = df["Start Time"].dt.hour.value_counts().idxmax()
    print(most_common_start_hour, "is most common start hour.")

    print("\nThis took {:.6f} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Statistics for the most popular stations and trip."""
    print("\nThe Most Popular Stations & Trip information:\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].value_counts().idxmax()
    print(most_common_start_station, "is most commonly used start station." )

    # display most commonly used end station
    most_common_end_station = df["End Station"].value_counts().idxmax()
    print(most_common_end_station, "is most commonly used end station.")

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[["Start Station", "End Station"]].mode().loc[0]
    print("The most commonly used combinations of start station and end station is {} and {}."\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took {:.6f} seconds.".format((time.time() - start_time)))
    print("-"*40)


def trip_duration_stats(df):
    """Statistics on the total and average trip duration."""
    print("\nTrip Duration analytics:\n")
    start_time = time.time()

    # display total travel time
    total_travel = df["Trip Duration"].sum()
    print("{:.2f} seconds is the total travel time.".format(total_travel))

    # display mean travel time
    mean_travel = df["Trip Duration"].mean()
    print("{:.2f} seconds is the mean travel time.".format(mean_travel))

    print("\nThis took {:.6f} seconds.".format((time.time() - start_time)))
    print("-"*40)


def user_stats(df):
    """Statistics for bikeshare user base."""
    print("\nUser Statistics:\n")
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types:\n")
    user_counts = df["User Type"].value_counts()
    # printing out the total numbers of user types 
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    """Displays Statistics on bikeshare users gender & birth year if available."""
    # Display counts of gender
    print("\nCounts of Gender:\n")
  
    found_gender = False
    found_birthyear = False
  
    for column in df:
        if column == "Gender":
            found_gender = True
            gender_counts = df["Gender"].value_counts()
            # printing out the total numbers of genders
            for index, gender_count in enumerate(gender_counts):
                print("  {}: {}".format(gender_counts.index[index], gender_count))
        if column == "Birth Year":
            found_birthyear = True
            print("\n Birth Year Statistics:")
            # Display earliest, most recent, and most common year of birth
            birth_year = df["Birth Year"]
            # earliest birth year
            earliest_year = birth_year.min()
            print(int(earliest_year), "is the earliest birth year.")
            # most recent birth year
            most_recent = birth_year.max()
            print(int(most_recent), "is the most recent birth year.")
            # most common birth year
            most_common_year = birth_year.value_counts().idxmax()
            print(int(most_common_year), "is the most common birth year.")        
    if found_gender == False and found_birthyear == False:
        print("Neither Gender nor Birth Year found.") 
    elif found_gender == False:
        print("Gender not found.")
    elif found_birthyear == False:
        print("Birth Year not found.")
    

    print("\nThis took {:.6f} seconds.".format((time.time() - start_time)))
    print('-'*40)
    
   
def display_data(df):
    """
    Displays raw CSV file data based on the selections above upon request. 
    Displays only five rows of the data at a time.
    """ 
    show_raw_data = input("\nDo you want to see the raw data for the Statistics above?" " Type: \"yes\" or \'no\".\n").lower().replace(" ","")
    if show_raw_data == "yes":
        # Number of rows to increment by.
        increment_value = 5
        # Starting indices
        low_index = 0
        high_index = increment_value

        while True:            
            print(df.iloc[low_index:high_index])
            low_index += increment_value
            high_index += increment_value
            print("Press Enter to continue...")
            stop = input("Type stop to end.\n")
            if stop == 'stop':
                return
            else:
                continue        
    if show_raw_data == "no":
            return
    else:
        print("\nError: Not a valid answer.")
        return display_data(df, line)        
    

def main():
    """ The order the calls will be made in to display the statistics, the anchor. """    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        #The call to restart the program or leave
        restart = input("\nWould you like to restart? Enter yes or no.\n").lower().replace(" ","")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()