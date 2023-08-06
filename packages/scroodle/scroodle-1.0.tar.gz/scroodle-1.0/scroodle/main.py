import pandas as pd
from robobrowser import RoboBrowser
import webbrowser
from tabulate import tabulate
import getpass
import configparser
import config

# Both are initialized in main, after reading\writing my_creds.ini
CURRENT_SEMESTER = None
PREFERRED_LANG = None


def init_connection(browser, username, password):
    """Initializes connection with Moodle website and
       log ins with given user credentials
    :param: browser: RoboBrowser object
    :param username: The user's given username
    :param password: The user's given password
    """
    browser.open(config.MY_IDC_HOME)
    login_form = browser.get_form(id='auth_form')
    login_form['username'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)


def get_courses_codes(browser):
    """
    :param: browser: RoboBrowser object
    :return: Courses codes for current semester
    """
    browser.open(config.MOODLE_MAIN_PAGE.format(
        config.CURR_YEAR, PREFERRED_LANG))
    semester_form = browser.get_forms()[1]
    semester_form['coc-category'].value = \
        config.SEMESTER_DICT[CURRENT_SEMESTER]
    all_courses_links = [url.get('href') for url in
                         [link.find('a') for link in browser.select(
                             ".coc-category-{}".format(
                                  config.SEMESTER_DICT[CURRENT_SEMESTER]))]]
    return [code_in_link.split('=')[1] for code_in_link in all_courses_links]


def get_course_name(course_code):
    """
    :param course_code: Course code (string)
    :return: Course name (string)
    """
    browser.open(config.COURSE_MAIN_PAGE.format(config.CURR_YEAR, course_code))
    return browser.select('.page-header-headings')[0].h1.string


def add_course_new_info(main_df, course_name, num_last_items=3):
    """
    :param main_df: Either an empty dataframe or a
           dataframe containing previous courses information
    :param course_name: String
    :param num_last_items: Number of last items from each course
    :return: Dataframe with num_last_items information
    """
    browser.open(config.COURSE_NEW_ITEMS_PAGE.format(
                  config.CURR_YEAR, courses_dict[course_name]))
    course_info = pd.read_html(str(browser.find('table')))[0]\
        .head(num_last_items)
    course_info['Course Name'] = course_name
    course_info['View'] = [a_tag.get('href')
                           for a_tag in browser.find('table')
                                .find_all('a')][:num_last_items]
    if len(main_df.index) == 0:  # If the dataframe is empty, initialize it
        main_df = course_info
    else:
        main_df = main_df.append(course_info, ignore_index=True)
    return main_df


def ask_for_username(creds_parser):
    """
    :param creds_parser: Configparser object from main program
    :return: Returns the username as entered by user and the possibly-
             modified configparser object
    """
    username = input('Type username (usually in the format firstname.lastname): ')
    save_flag = input('Should we save your username for next time? y\\n: ') == 'y'
    if save_flag:
        print('Your username is being saved in file my_creds.ini.')
        creds_parser['CREDENTIALS'] = {}
        creds_parser['CREDENTIALS']['USERNAME'] = username
    return username, creds_parser


def download_requested_items(links_series, num_requested):
    """
    :param links_series: Pandas series of just the links
    :param num_requested: How many links requested
    """

    # links_series.iteritems() returns a zip object of (index, link). This
    #  is casted to a list, so we can used list slicing.
    for index, row in list(links_series.iteritems())[:num_requested]:
        webbrowser.open(row)


if __name__ == '__main__':
    creds_parser = configparser.ConfigParser()
    first_time_flag = False

    # If the file is empty, it is th first use!
    if creds_parser.read('my_creds.ini') == []:
        first_time_flag = True
        creds_parser['PREFERENCES'] = {}
        creds_parser['PREFERENCES']['LANGUAGE'] = input('What is your preferred language? he\\en: ')
        creds_parser['PREFERENCES']['CURRENT_SEMESTER'] = input('What is the current semester? 1\\2\\3: ')
        print('Preferred language and current semester are saved in my_creds.ini.')
        username, creds_parser = ask_for_username(creds_parser=creds_parser)

    # If 'CREDENTIALS' section is not in file, then the user asked the program
    # to not save his username last time
    elif 'CREDENTIALS' not in creds_parser:
        username, creds_parser = ask_for_username(creds_parser=creds_parser)

    # Get username, either from file or input
    else:
        username = creds_parser['CREDENTIALS']['USERNAME']

    CURRENT_SEMESTER = creds_parser['PREFERENCES']['CURRENT_SEMESTER']
    PREFERRED_LANG = creds_parser['PREFERENCES']['LANGUAGE']

    # Get user's password
    user_password = getpass.getpass('Password for {}: '.format(username))

    print('Working!')

    # If the username wasn't in file, suggest it
    # if first_time_flag:
    with open('my_creds.ini', 'w') as creds_file:
        creds_parser.write(creds_file)

    df = pd.DataFrame()
    browser = RoboBrowser(parser='html.parser')
    init_connection(browser=browser, username=username, password=user_password)
    course_codes = get_courses_codes(browser=browser)
    courses_dict = dict()

    # Each course has its own unique code
    for code in course_codes:
        courses_dict['{}'.format(get_course_name(code))] = code

    # For each such course, we add its new information to the dataframe
    for course in courses_dict:
        df = add_course_new_info(df, course)

    # Sorting the dataframe by date
    df['Time'] = pd.to_datetime(df['Time']).apply(
        lambda date_index: date_index.strftime('%d/%m/%Y'))
    df['Time'] = pd.to_datetime(df['Time'])
    df.sort_values(by='Time', ascending=False, inplace=True)

    # Reordering the dataframe
    new_col_order = ['Time', 'Course Name', 'Text', 'Activity',
                     'Action', 'View']
    df = df[new_col_order]
    df.set_index(['Time'], inplace=True)
    print(tabulate(df, headers='keys', tablefmt='psql'))

    if input('Should we view the latest updates online? y\\n: ') == 'y':

        # Has to be casted to integer, to be parsed in download_requested_items
        # as slicing index
        num_requested = int(input('How many to view? (from the newest) 1\\2\\3... :\n'
                              'Note that some will be downloaded!'))
        download_requested_items(links_series=df['View'], num_requested=num_requested)
