import patoolib
from selenium import webdriver
import glob
import os
from . import parser

### upzip all the zip file
### extract if it is a compressed file, otherwise flash errors
def unzip(name, upload_id):
    try:
        patoolib.extract_archive("media/" + name, outdir="media/documents/{}".format(upload_id))
    except patoolib.util.PatoolError:
        print belt.upload, "is not a compressed file"


def analyze(shortName, upload_id):
    
    #using headless Chrome
    options  = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x1800')
    driver = webdriver.Chrome(chrome_options=options)
    messages = []

    #using PhantomJS
    # driver = webdriver.PhantomJS()
    # driver.set_window_size(1620, 1080)
    # driver.get('https://google.com')

    ### getting html files path
    file = glob.glob('media/documents/{}/{}/*.html'.format(upload_id, shortName))
    cssFile = glob.glob('media/documents/{}/{}/*.css'.format(upload_id, shortName))

    if file:
        filePath = 'file://' + os.getcwd() + "/" +file[0]
        driver.get(filePath)
        print "making screenshot of the html"
        driver.save_screenshot('apps/auto_belt_grader/static/screen.png'.format(upload_id))
        
        ### parsing the html files
        par = parser.parser(file[0])
        for p in par:
            messages.append(p)

        messages.append('----')
        
        ### - count the number of unique html errors: http://validator.w3.org/
        driver.get('https://validator.w3.org/#validate_by_upload')
        driver.find_element_by_id('uploaded_file').send_keys(os.getcwd() + "/" +file[0])
        element = driver.find_element_by_css_selector('#validate-by-upload form')
        element.submit()
        # driver.implicitly_wait(2)
        elements = driver.find_elements_by_css_selector('li.error')
        if len(elements) == 0:
            # success
            messages.append("No errors on HTML validator.")
        else:
            # failed
            # len(elements) number of errors in html validator
            messages.append("Has {} error(s) on HTML validator.".format(len(elements)))
        
    if cssFile:
        ### - count the number of unique css errors: https://jigsaw.w3.org/css-validator/
        driver.get('https://jigsaw.w3.org/css-validator/#validate_by_upload')
        driver.find_element_by_id('file').send_keys(os.getcwd() + "/" + cssFile[0])
        element = driver.find_element_by_css_selector('#validate-by-upload form')
        element.submit()

        elements = driver.find_elements_by_css_selector('tr.error')
        if len(elements) == 0:
            # success
            messages.append("No errors on CSS validator.")
        else:
            # failed
            # len(elements) number of errors in html validator
            messages.append("Has {} error(s) on CSS validator.".format(len(elements)))
        
    # driver.save_screenshot('media/documents/{}/test.png'.format(upload_id)) 
    driver.quit()
    return messages



    