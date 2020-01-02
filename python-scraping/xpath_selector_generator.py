import re
import lxml
from textblob import TextBlob

def return_selectors(html, keyword, _filter=['img'], ignore_case=True):
    '''
    Receive an html file's contents and string and return the corresponding xpath selector
    args:
        html (str): html content downloaded from a network or opened from a file stream
        keyword (str): string in focus from the webpage whose xpath selector is needed
        _filter (list): list of tags to filter out of result
        ignore_case (bool): determines whether exact case should be matched when looking for expression
    returns:
        if found: list of selectors like ['//div[@id="wanem"]'] will be returned
        if not found: '//error', '//Missing'
    NB: regex only works on str not bytes in case file is read in 'rb' mode
        case 3 does not pose a problem as long as another attribute aside class|id is defined properly
    '''
    parent_tag = 'Undefined'
    try:
        html = str(html)
        
        #regex below selects collection of whole strings up to keyword
        if ignore_case:
            keyline = re.compile(r'(.*?)\s*%s'%keyword, re.IGNORECASE).findall(html)#[0]
        else:
            keyline = re.compile(r'(.*?)\s*%s'%keyword).findall(html)
        #regex below selects parent tag of keyword
        keyline += [html[(html.index(keyword)-100):html.index(keyword)]] #also consider tag before tag appearing to have content because of e.g <a href='link'><i id="g"></i>Content   :if you do not do this, only i is considered which is actually empty
        parent_tags = []
        if len(keyline) > 0:
            for line in keyline:
                #print('On line:',line)
                if ignore_case:
                    parent_tags += re.compile(r'<[^/].*?\".*?\"', re.IGNORECASE).findall(line)
                    #parent_tags += re.compile(r'<[^/].*?\".*?\"', re.IGNORECASE).findall(line)#[-1] #[-1] avoids case 1 by forcing it to use the last match from the top of the document, which will be keyword's parent tag
                else:
                    parent_tags += re.compile(r'<[^/].*?\".*?\"').findall(line)
                    #parent_tags += re.compile(r'<[^/].*?\".*?\"').findall(line)
        selectors = []
        #print('parent_tags:',' '.join(parent_tags),sep='\n')
        for parent_tag in parent_tags:
            try:
                discard = False
                if len(parent_tag) > 0:
                    #.split('>')[-1] removes risk of case 2 using h5 in selector
                    ind = -1
                    if len(parent_tag.split('>')[ind]) > 0:
                        parent_tag = parent_tag.split('>')[ind]
                    else:
                        ind -= 1
                        while not len(parent_tag.split('>')[ind]) > 0:
                            ind -= 1
                        parent_tag = parent_tag.split('>')[ind]
                    #parent_tag = parent_tag.split('>')[-1] if len(parent_tag.split('>')[-1]) > 0 else parent_tag.split('>')[-2]
                    #the next 3 lines solve problem of attribute value containing spaces by extracting the attribute value(the pattern) seperately from the tag and ref (WordList)
                    pattern = (parent_tag.split('"')[-1] if len(parent_tag.split('"')[-1]) > 0 else parent_tag.split('"')[-2]) #extract pattern from string
                    parent_tag = parent_tag[:parent_tag.index('=')] #only consider part of string with tag and ref
                    if len(TextBlob(parent_tag).words) == 2:
                        tag, ref = TextBlob(parent_tag).words
                        for t in _filter:
                            if tag == t:
                                print('Discarding',tag)
                                discard = True
                                break
                        if discard == True:
                            continue
                        selectors += [f'//{tag}[@{ref}="{pattern}"]']
                    else:
                        print('Discarding',parent_tag[:10],'for being too long')
                    #print(selectors[-1])
            except Exception as e:
                print(e,'for',parent_tag[:10])
        return list(set(selectors))
    except Exception as e:
        print(e)
        return '//error'
    return "//Missing"
def get_info_from_page(html,selectors, display=False):
    tree = fromstring(html)
    info = []
    for selector in selectors:
        info += tree.xpath(selector)
    info_list = []
    for data in info:
        if display:
            print(data.text_content())
        info_list += [data.text_content()]
    return info_list
if __name__ == '__main__':
    '''
    To filter out multispaces:
        ' '.join(str.split())
        ' '.join(' '.join(list).split())
    '''
    print('Opening file')
    with open('samplepage.html','rb') as file:
        keyword = 'PENCIL'
        print('Generating selectors for',keyword)
        selectors = return_selectors(file.read(), keyword, ignore_case=False)
        print(len(selectors),'selectors generated for',keyword)
        for selector in selectors:
            try:
                file.seek(0)
                content = get_info_from_page(file.read(), [selector])
                if any((x.isalpha() for x in ' '.join(content))):
                    print(selector,'content:',' '.join(' '.join(content).split()))
                else:
                    print(selector,'is empty')
            except lxml.etree.ParserError as e:
                print('For',selector,e)
