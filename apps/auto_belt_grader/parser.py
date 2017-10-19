from bs4 import BeautifulSoup
import re

def parser(url):
    with open(url) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        for line in fp:
            print line

    results = []

    ### getting all the ids
    tags = soup.find_all(id=re.compile("^"))
    ids = []
    for tag in tags:
        ids.append(tag.attrs['id'])

    ### getting all the class
    tags = soup.find_all(class_=re.compile("^"))
    classes = []
    for tag in tags:
        for c in tag.attrs['class']:
            classes.append(c)

    ### getting all the unique classes (remove duplicates in an array)
    def UC(seq):
        return [x for x in seq if seq.count(x) == 1]
    unique_classes = UC(classes)

    ### results
    # print "unique classes: ", len(unique_classes)
    # print "ids:", len(ids)
    ### list the classes and ids
    # print unique_classes
    # print ids
    results.append("{} unique classes. And they are {}".format(len(unique_classes), unique_classes))
    results.append("{} ids. And they are {}".format(len(ids), ids))

    ### check to see if width, height, style, or align attributes are used inside of the HTML
    width_tags = soup.find_all(width=re.compile("^"))
    height_tags = soup.find_all(height=re.compile("^"))
    style_tags = soup.find_all(style=re.compile("^"))
    align_tags = soup.find_all(align=re.compile("^"))

    tags = width_tags + height_tags + style_tags + align_tags
    # print len(tags)
    results.append("{} of width, height, style, or align attributes are used inside of the HTML.".format(len(tags)))

    ### count the number of times you encounter a div with only a single child (even if that child has grand-children)
    tags = soup.find_all("div")
    # print len(tags)
    count = 0
    divs = []
    for tag in tags:
        # print tag.contents   
        # print len(list(tag.children)) - 2
        if len(list(tag.children)) == 3:
            # print tag
            count += 1
            divs.append(tag)
            # print divs
        
    results.append("{} div(s) that has only a single child. And they are{}".format(count, divs))

    return results

