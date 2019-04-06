from bs4 import BeautifulSoup
import requests
import json


def get_course_urls():

    course_list_url = 'http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php'
    page = requests.get(course_list_url).content
    soup = BeautifulSoup(page, "lxml")

    course_urls = []

    a = soup.find_all('option')[1::]
    for i in a:
        course = i.get_text()[:3]
        course_url = 'http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb=' + course
        course_urls.append(course_url)
    return course_urls


def instructor_add(data, new_instructor, new_course, instructor_name):
    if instructor_name != '--':
        if instructor_name in data:
            data[instructor_name].append(new_course)
        else:
            data.update(new_instructor)
    return data


def update_instructor_data():

    course_urls = get_course_urls()

    data = {}

    for course_url in course_urls:

        print(course_url)

        page = requests.get(course_url).content
        soup = BeautifulSoup(page, "lxml")

        soup = soup.find(class_='dersprg')
        for tr in soup.find_all('tr')[2::]:
            tds = tr.find_all('td')
            crn = int(tds[0].get_text())
            course_code = tds[1].get_text()
            course_name = tds[2].get_text()
            instructor_name = tds[3].get_text().replace('  ', ' ')
            buildings = tds[4].get_text()
            days = tds[5].get_text()
            times = tds[6].get_text()
            rooms = tds[7].get_text()


            new_course = [crn, course_code, course_name, buildings, days, times, rooms]
            new_instructor = {instructor_name : [new_course]}


            if ',' in instructor_name:
                multi_instructor = instructor_name.split(', ')
                for ins in multi_instructor:
                    new_instructor = {ins : [new_course]}
                    instructor_add(data, new_instructor, new_course, ins)
            else:
                instructor_add(data, new_instructor, new_course, instructor_name)

    with open('data.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
