import sys


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # your code here
    
    for i in data:
        ##go through every row in list of data
        if i[1] == 'Rockingham' and i[2] == 'Virginia' and i[4]!=0:
            ##check if its rockingham county in va and the covid cases are pos
            firstcaserock = i[0]
            ##return first positive case and break loop
            break
    for i in data:
        ##same as above
        if i[1] == 'Harrisonburg city' and i[2] == 'Virginia' and i[4]!=0:
            firstcaseharris = i[0]
            break
##return print statement
    return print("The first positive COVID case in Rockingham County was on ", str(firstcaserock)," and the first positive case in Harrisonburg was on ",str(firstcaseharris),'\n')

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """

    # your code here
    ##initiate variables for use later
    harrisprevday = 0
    rockprevday = 0
    harrismax = 0
    rockmax = 0
    harrisdate = ""
    rockdate = ""

    for i in data:
        ##go through every row in list of data
        if i[1] == 'Harrisonburg city' and i[2] == 'Virginia':
            ##check if its harrisonburg county in va
            if harrisprevday != 0:
                ##if prev day isnt zero make new daily cases and compare to max
                newcases = i[4] - harrisprevday

                if newcases > harrismax:
                    harrismax = newcases
                    harrisdate = i[0]

            harrisprevday = i[4]
            ##set prev to current 


        if i[1] == 'Rockingham' and i[2] == 'Virginia':
            ##same as above
            if rockprevday != 0:
                newcases = i[4] - rockprevday

                if newcases > rockmax:
                    rockmax = newcases
                    rockdate = i[0]

            rockprevday = i[4]


    return print("The day with greatest number of new COVID cases in Rockingham County was on", rockdate, "with", rockmax, "cases. The day with greatest number of new COVID cases in Harrisonburg was on",harrisdate, "with", harrismax, "cases\n")

def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    
    # your code here
    ##initiate variables for use later
    rocklist = []
    harrislist = []
    rockdaily = []
    harrisdaily = []
    rockmax7 = 0
    rockstart = 0
    harrismax7 = 0
    harrisstart = 0

    for i in data:
        ##go through every row in list of data
        if i[1] == 'Rockingham' and i[2] == 'Virginia':
            ##if data row is right place, store into new list
            rocklist.append(i)
        if i[1] == 'Harrisonburg city' and i[2] == 'Virginia':
            #same above
            harrislist.append(i)

    for i in range(1, len(rocklist)):
        ##go through new list and compute and append daily case numbers to another list
        rockdaily.append(rocklist[i][4] - rocklist[i -1][4])

    for i in range(1, len(harrislist)):
        ##same above
        harrisdaily.append(harrislist[i][4] - harrislist[i - 1][4])

    for i in range(len(rockdaily) - 6):
        ##go thru daily list (not fully to end or error)
        s = sum(rockdaily[i:(i+7)])
        ##create a 7 day sum
        if s > rockmax7:
            #compare sum to max sum and if greater set as max and mark start
            rockmax7 = s
            rockstart = i

    for i in range(len(harrisdaily) -6):
        ##same as above
        s = sum(harrisdaily[i:(i+7)])

        if s > harrismax7:
            harrismax7 = s
            harrisstart = i

    rockstartd = rocklist[rockstart+1][0]
    rockend = rocklist[rockstart+7][0]
    harrisstartd = harrislist[harrisstart+1][0]
    harrisend = harrislist[harrisstart+7][0]
    ##use start variables to find exact date range for both cities and return

    return print("The 7 day period with greatest number of new COVID cases in Rockingham County was from", rockstartd, "to", rockend, "with", rockmax7, "cases. The 7 day period with the most positive cases in Harrisonburg was from",harrisstartd, "to", harrisend, "with", harrismax7, "cases\n")

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

   ## for (date,county, state, fips, cases, deaths) in data:
     ##   print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)


