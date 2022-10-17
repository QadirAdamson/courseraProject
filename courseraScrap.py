#Author=Emin Resul Tolu
from django.http import HttpResponse

#At first, lets list "subjects" of Coursera(There is 11 subjects)
def home(request):
    return HttpResponse('''
        <strong><p>Warning! Please wait a few seconds after clicking. When scraping is finished, you can download CSV file</strong>
        <ul>
            <li><a href='/data-science'>Data Science</a></li>
            <li><a href='/business'>Business</a></li>
            <li><a href='/computer-science'>Computer Science</a></li>
            <li><a href='/information-technology'>Information Technology</a></li>
            <li><a href='/language-learning'>Language Learning</a></li>
            <li><a href='/health'>Health</a></li>
            <li><a href='/personal-development'>Personal Development</a></li>
            <li><a href='/physical-science-and-engineering'>Physical Science and Engineering</a></li>
            <li><a href='/social-sciences'>Social Sciences</a></li>
            <li><a href='/arts-and-humanities'>Arts and Humanities</a></li>
            <li><a href='/math-and-logic'>Math and Logic</a></li>
        </ul>
    ''')

# ------------- GET DATA FUNCTION ---------------

import requests
from bs4 import BeautifulSoup

#Get target_url and parse it's html
def get_data_from_url(target_url):
    response_data = requests.get(target_url)
    return BeautifulSoup(response_data.text, 'html.parser')

def get_data(request, category):

# Naming csv file and adding required info
    csv = open('static/' + category + '.csv', 'w', encoding="utf-8")
    csv.write('"Course Name", ' + \
        '"Course Provider", ' + \
        '"Course Description", ' + \
        '"Students Enrolled", ' + \
        '"Ratings" \n'
    )

# Get data from /browse + category
    courses = get_data_from_url('https://www.coursera.org/browse/' + category)
    for url in courses.find_all('a', attrs={'class':'CardText-link'}):
        # To select courses, find urls starts with "learn"
        if url['href'].startswith('/learn'):
        # In Courses:
            course_data = get_data_from_url('https://www.coursera.org' + url['href'])
            # Scrap required data from courses
            csv.write('"' + \
                # Course Name:
                course_data.find('h1', attrs={'class':'banner-title banner-title-without--subtitle m-b-0'}).text + '","' + \
                # Course Provider:
                course_data.find('h3', attrs={'class':'headline-4-text bold rc-Partner__title'}).text + '"," ' + \
                # Course Description:
                course_data.find('div', attrs={'class':'content-inner'}).find('p').text + '"," ' + \
                # Students Enrolled:
                course_data.find('div', attrs={'class':'_1fpiay2'}).find('span').text + '"," ' + \
                # Ratings:
                course_data.find('span', attrs={'data-test':'number-star-rating'}).text + '" \n'
            )

    csv.close()
    # CSV file download link is ready
    return HttpResponse(f'''
        You can download your CSV File here => <a href="/static/{category}.csv"> {category}.csv</a>
    ''')