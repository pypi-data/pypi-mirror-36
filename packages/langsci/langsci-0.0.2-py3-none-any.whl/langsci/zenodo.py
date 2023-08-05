"""
A bridge between the LangSci LaTeX skeleton and the Zenodo API

Atttributes:
    INCLUDEPAPERP: a regex for finding all \include'd papers in a fiel
    BOOKAUTHORP: a regex for finding the authors of books in a tex file
    LASTAND: a regex to find "\lastand" or "\and", used by LaTeX to join author names
    CHAPTERAUTHORP: a regex to find authors and affiliations of chapter authors
    TITLEP: a regex to find a title 
    ISBNP: a regex to retrieve the digital ISBN 
    CHAPTERKEYWORDSP: a regex to retrieve the keywords
    ABSTRACTP: a regex to retrieve the abstract 
    BACKBODYP: a regex to retrieve the blurb 
    KEYWORDSEPARATOR:  a regex for symbols people use to separate keywords 
    PAGERANGEP: a regex for retrieving page ranges 
    BIBAUTHORP: a regex to retrieve the author field from a BibTeX file
    BIBTITLEP: a regex to retrieve the author field from a BibTeX file
    
"""

import requests
import json
import pprint   
import re
import sys

INCLUDEPAPERP = re.compile(r"\n[\t ]*\\includepaper\{chapters/(.*?)\}")#only papers on new lines, ignoring % comments
BOOKAUTHORP = re.compile(r"\\author{(.*?)}")
LASTAND = re.compile(r"(\\lastand|\\and)")
CHAPTERAUTHORP = re.compile(r"\\author{(.*?) *\\affiliation{(.*)}")
TITLEP = re.compile(r"\\title{(.*?)}")
ISBNP = re.compile(r"\\lsISBNdigital}{(.*)}") 
CHAPTERKEYWORDSP = re.compile(r"\\keywords{(.*?)}")
ABSTRACTP = re.compile(r"\\abstract{(.*?)[}\n]")
BACKBODYP = re.compile(r"\\BackBody{(.*?)[}\n]")
KEYWORDSEPARATOR = re.compile("[,;-]")
PAGERANGEP = re.compile("{([0-9ivx]+--[0-9ivx]+)}")
BIBAUTHORP = re.compile(r"author={([^}]+)") #current setup adds space after author
BIBTITLEP = re.compile(r"title={{([^}]+)}}")

class Publication():
  """
  A Publication holds all the metadata which are 
  generic for books and papers
  """
  
  def __init__(self):
    self.metadata={'upload_type': 'publication',
            'access_right':'open',
            'license':'cc-by',
            'imprint_publisher':'Language Science Press',
            'imprint_place':'Berlin',
            'communities': [{'identifier':'langscipress'}],
            'prereserve_doi': True, 
            'language':'eng' 
        } 
    
  def register(self,token):
    """
    register the publication with Zenodo
    """
    
    data={ 
      'metadata': self.metadata
        } 
    pprint.pprint(json.dumps(data))        
              
    r = requests.post('https://zenodo.org/api/deposit/depositions', 
                      params={'access_token': token},  
                      headers = {"Content-Type": "application/json"},
                      data=json.dumps(data)
                      )
    pprint.pprint(r.json())
    try:
      return r.json()['metadata']["prereserve_doi"]["doi"]
    except KeyError:
      print(r.json()['errors'])
      raise

    
class Book(Publication): 
  """ 
  A full-length publication, either a monograph or an edited volume 
  """
  def __init__(self):
    Publication.__init__(self)
    self.title=None
    self.authors=[]
    self.abstract="Abstract could not be found"
    self.keywords=[]
    self.digitalisbn=None
    self.getBookMetadata()
    self.chapter = []
    self.getChapters()
    self.metadata['publication_type'] = 'book'
    #self.metadata['related_identifiers'] = [{'isAlternateIdentifier':self.digitalisbn}]    #currently not working on Zenodo
    self.metadata['title']=self.title
    self.metadata['description']=self.abstract
    self.metadata['creators']=[{'name':au} for au in self.authors]      
    self.metadata['keywords']=self.keywords
    
  def getBookMetadata(self):
    """
    Parse the file localmetadata.tex and retrieve the metadata
    """
    
    localmetadataf = open('localmetadata.tex')
    localmetadata = localmetadataf.read()
    localmetadataf.close()
    self.title = TITLEP.search(localmetadata).group(1)
    authorstring = BOOKAUTHORP.search(localmetadata).group(1)
    authors = []
    for i, au in enumerate(LASTAND.split(authorstring)):
        if i%2 == 0:#get rid of splitters, i.e. "and" and "lastand" at odd positions
          authors.append(au.strip())
    self.authors = authors
    self.abstract = BACKBODYP.search(localmetadata).group(1)
    try:
      self.keywords = [x.strip() for x in KEYWORDSEPARATOR.split(CHAPTERKEYWORDSP.search(localmetadata).group(1))]
    except:
      pass
    self.digitalisbn = ISBNP.search(localmetadata).group(1) 
    
  def getChapters(self):
    """
    find all chapters in edited volumes which are referenced in main.tex 
    """
      
    mainf = open('main.tex')
    main = mainf.read()
    mainf.close()
    chapterpaths = INCLUDEPAPERP.findall(main) 
    self.chapters = [Chapter(cp,booktitle=self.title,isbn=self.digitalisbn) for cp in chapterpaths]
    

class Chapter(Publication):  
  """
  A chapter in an edited volume
  """
    
  def __init__ (self,path,booktitle='',isbn=False):
    print("reading",path)
    Publication.__init__(self)
    chapterf = open('chapters/%s.tex'%path)
    chapter = chapterf.read()
    chapterf.close()
    preamble = chapter.split('\\begin{document}')[0]
    abstract = ABSTRACTP.search(preamble).group(1)
    if "noabstract" in abstract: 
      abstract = "replace this dummy abstract in Zenodo"
    keywords = []
    try:
      keywords = [x.strip() for x in CHAPTERKEYWORDSP.search(preamble).group(1).split(',')]    
    except:
      pass
    self.path = path.strip()  
    self.abstract = abstract 
    self.keywords = keywords
    self.pagerange = ''
    for l in open('collection_tmp.bib').readlines():  
      if l.startswith("@incollection{chapters/%s,"%path):
        #print(path)
        self.pagerange = PAGERANGEP.search(l).group(1)  
        self.authors = [au.strip() for au in BIBAUTHORP.search(l).group(1).split(' and ')]
        self.title = BIBTITLEP.search(l).group(1)
        break #we have found the entry we are interested in
    self.booktitle = booktitle
    if isbn:
      self.bookisbn = isbn    
    self.metadata['publication_type'] = 'section'   
    self.metadata['imprint_isbn'] = self.bookisbn
    self.metadata['partof_title'] = self.booktitle        
    self.metadata['title']=self.title
    self.metadata['description']=self.abstract
    self.metadata['creators']=[{'name':au} for au in self.authors]  
    self.metadata['keywords']=self.keywords
    #TODO needs affiliation
    #'creators': [{'name': 'Doe, John',
            #'affiliation': 'Zenodo'}],
    #self.metadata['partof_pages'] = chapter.pagerange
    #self.metadata['related_identifiers'] = [{'hasPart':self.bookisbn}] #unintuitive directionality of hasPart and isPart


      

if __name__ == "__main__":
  """
  usage: > python3 zenodo.py 7
  The script looks for all include'd files from the folder chapters/ in main.tex
  It will ignore the first n files, where n is the argument of the script
  If no argument is given, processing will start with the first file. 
  For each file, the script will extract metadata from the file itself 
  and from the file collection_tmp.bib generated by biber. 
  The metadata is collected and a corresponding entry is created on Zenodo. 
  The DOI assigned by Zenodo is collected and inserted into the file. 
  """
  
  book = Book()  
  #for c in book.chapters:
    #pprint.pprint(c.metadata) 
  tokenfile = open('zenodo.token')
  token = open('zenodo.token').read().strip()
  tokenfile.close()
  #print(token) 
  #bookdoi = book.register(token)
  #print("BookDOI{%s}"%bookdoi)
  offset = 0
  try:
    offset = sys.argv[1]
  except IndexError:
    pass
  for i, ch in enumerate(book.chapters[offset:]):    #for continuation if program stops in the middle of a book
    chapterf = open('chapters/%s.tex'%ch.path)
    chapterlines = chapterf.readlines()
    chapterf.close()
    for line in chapterlines:
      if "ChapterDOI" in line:
        print("DOI already present in %s"%ch.path)
        raise IOError
    try:  
      chapterDOI = ch.register(token)  
    except:
      print("%s at position %i from offset %i could not be registered"%(ch.path,i,offset))
    insertstring = "\\ChapterDOI{%s}\n"%chapterDOI  
    chapterf = open('chapters/%s.tex'%ch.path,'w')
    chapterf.write(chapterlines[0]) 
    chapterf.write(insertstring) 
    chapterf.write("".join(chapterlines[1:])) 
    chapterf.close() 
 
