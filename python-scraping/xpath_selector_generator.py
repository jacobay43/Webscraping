import re
from lxml.html import fromstring
from textblob import TextBlob
import time
'''
Drawback: Extremely slow for complex site like Eventbrite
		  Considerably slow for multiple word keyword arguments
'''
def return_selectors(html, keyword):
    '''
    Receive an html file's contents and string and return the corresponding xpath selector
    args:
        html (str): html content downloaded from a network or opened from a file stream
        keyword (str): string in focus from the webpage whose xpath selector is needed
    returns:
        if found: list of selectors like '//div[@id="wanem"]' will be returned
        if not found: '//error', '//Missing'
    NB: regex only works on str not bytes in case file is read in 'rb' mode
        case 3 does not pose a problem as long as another attribute aside class|id is defined properly
    '''
    parent_tag = 'Undefined'
    try:
        html = str(html)
        
        #regex below selects collection of whole strings up to keyword
        keyline = re.compile(r'(.*?)%s'%keyword, re.IGNORECASE).findall(html)#[0]
        #regex below selects parent tag of keyword
        parent_tags = []
        if len(keyline) > 0:
            for line in keyline:
                parent_tags += re.compile(r'<[^/].*?\".*?\"', re.IGNORECASE).findall(line)#[-1] #[-1] avoids case 1 by forcing it to use the last match from the top of the document, which will be keyword's parent tag
        selectors = []
    
        for parent_tag in parent_tags:
            if len(parent_tag) > 0:
                #.split('>')[-1] removes risk of case 2 using h5 in selector
                parent_tag = parent_tag.split('>')[-1] if len(parent_tag.split('>')[-1]) > 0 else parent_tag.split('>')[-2]
                #the next 3 lines solve problem of attribute value containing spaces by extracting the attribute value(the pattern) seperately from the tag and ref (WordList)
                pattern = (parent_tag.split('"')[-1] if len(parent_tag.split('"')[-1]) > 0 else parent_tag.split('"')[-2]) #extract pattern from string
                parent_tag = parent_tag[:parent_tag.index('=')] #only consider part of string with tag and ref
                tag, ref = TextBlob(parent_tag).words
                selectors += [f'//{tag}[@{ref}="{pattern}"]']
                #print(selectors[-1])
        return selectors
    except Exception as e:
        print(e)
        print(parent_tag)
        return '//error'
    return "//Missing"
    
if __name__ == '__main__':
	with open('webpage.txt','r') as file:
		print('\n'.join(return_selectors(file.read(), 'Upcoming Events')))
    startTime = time.time()        
    case_1 = '''<h5>
                                              <div class="layer-unwrap">Hello
                                              </div>
                             </h5>'''
    case_2 = '''<h5><div class="layer-rap">Hello</div>
                             </h5>'''
    case_3 = '''<p text-font = "12px" class = ".nodec">Greet your friend for me</p>'''

    print('Selector:',return_selectors(case_1, 'Hello'))
    print(f'Time Elapsed: {time.time()-startTime:.2f} s')
    startTime = time.time()
    print('Selector:',return_selectors(case_2, 'Hello'))
    print(f'Time Elapsed: {time.time()-startTime:.2f} s')
    startTime = time.time()
    print('Selector:',return_selectors(case_3, 'Greet'))
    print(f'Time Elapsed: {time.time()-startTime:.2f} s')
    print(fromstring(case_3).xpath(return_selectors(case_3,'Greet')[0])[0].text_content())


