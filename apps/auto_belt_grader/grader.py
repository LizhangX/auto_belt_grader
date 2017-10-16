import patoolib
from selenium import webdriver
import glob
import os


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

    #using PhantomJS
    # driver = webdriver.PhantomJS()
    # driver.set_window_size(1620, 1080)
    # driver.get('https://google.com')
    print "making screenshot"
    file =  glob.glob('media/documents/{}/{}/*.html'.format(upload_id, shortName))
    if file[0]:
        filePath = 'file://' + os.getcwd() + "/" +file[0]
        print filePath
        driver.get(filePath)
        driver.save_screenshot('media/documents/{}/screen.png'.format(upload_id))
    driver.quit()



    