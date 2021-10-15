from ebooklib import epub
from bs4 import BeautifulSoup
import requests


# epub data
booktitle = input('Book name: ')
author = input('Author: ')
no_chapters = int(input('Chapters: '))

#setup
book = epub.EpubBook()
book.set_title(booktitle)
book.set_language('en')
book.add_author(author)
chapters = []

# setup initial link + next chapter link & start chapter
src = requests.get(f'https://allnovel.org/otherworldly-evil-monarch/chapter-1-evil-monarch-jun-xie.html').text
nextchaplnk = 'https://allnovel.org/otherworldly-evil-monarch/chapter-2-jun-moxie.html'
start_chp = 1
title = ''
for i in range(start_chp, no_chapters+1):
    # when we are getting the source from the next chapter link
    if i != start_chp:
        src = requests.get(nextchaplnk).text

    # create the soup
    soup = BeautifulSoup(src, 'lxml')

   # get the text and paragraphs from the soup
    rawtext = soup.find('div', id='chapter-content')
    paragraphs = rawtext.find_all('p')

    # to see if title has been found
    titlefound = False
    pagecontents = ''

    title = soup.find('a', class_='chapter-title')['title']
    # add all text to the page content
    for paragraph in paragraphs:
        # # keep looking for the title until its been found
        # if not titlefound and 'Chapter' in paragraph.text:
        #     title = f'Chapter {i}: {paragraph.text}'
        #     titlefound = True
        # # after its been found the rest of the text should be contents
        # else:
        #     pagecontents += str(paragraph)
        pagecontents += str(paragraph)



    # create the chapter object
    chapter = epub.EpubHtml(title=title, file_name=f'chap_{i}.xhtml', lang='en')

    # initialise the variable to hold the chapter's text, add title to it
    chaptertext = f'<h1>{title}</h>' + pagecontents

    # set the contents of the chapter
    chapter.content = chaptertext
    # add chapter to book
    book.add_item(chapter)
    # add chapter to chapters list (which will become table of contents)
    chapters.append(chapter)
    print(f'{title} added.')

    # find next chapter link if not last chap
    if i < no_chapters:
        next_c = soup.find('a', id='next_chap')['href']
        nextchaplnk = f"https://allnovel.org{next_c}"
        # # title = next_c[19:-5].replace('-', ' ')
        # nextchaplnk = f'https://readwebnovels.net/novel/otherworldly-evil-monarch/chapter-{i+1}/'



book.toc = tuple(chapters)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ['nav'] + chapters

# write to the file
epub.write_epub(f'{booktitle}.epub', book, {})
