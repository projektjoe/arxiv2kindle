import os.path
from datetime import datetime, timezone


def get_chapter_content(title):
    return \
        f"""<?xml version="1.0" encoding="utf-8"?>
<html xml:lang="en-us" lang="en-us" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="utf-8"/> 
        <link rel="stylesheet" type="text/css" href="../css/commonltr.css"/>
        <title>{title}</title>
        <link type="text/css" rel="stylesheet" href="../css/epub.css"/>
    </head>
    <body>
    </body>
</html>"""

def get_title_page(title, author):
    return \
            f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <meta charset="utf-8" />
        <title>Title page</title>
        <link rel="stylesheet" type="text/css" href="../css/epub.css" />
    </head>
    <body id="titlepage" epub:type="frontmatter titlepage">
        <h1>{title}</h1>
        <p>{author}</p>
    </body>
</html>"""


def table_of_contents(sections):
    items = "\n".join([
        f'                <li>\n'
        f'                    <a href="{(section["title_raw"])}.xhtml">{section["title"]}</a>\n'
        f'                </li>'
        for section in sections
    ])
    return \
        f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <meta charset="utf-8"/>
    	<title>Navigation</title>
        <link rel="stylesheet" type="text/css" href="../css/epub.css"/>
    </head>
    <body epub:type="frontmatter">
        <nav epub:type="toc" id="toc">
            <h1>Table of Contents</h1>
            <ol>
                {items}
            </ol>
        </nav>
    </body>
</html>
"""

def get_mimetype():
    return 'application/epub+zip'

def get_container_xml():
    return """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
   <rootfiles>
      <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""

def get_package_opf(title, creator, sections, images):
    section_list = '\n        '.join([
        f'<item id="c{i + 1}" media-type="application/xhtml+xml" href="xhtml/{(section["title_raw"])}.xhtml"' + (
            ' properties="nav" ' if section["title"] == "nav" else '') + (' properties="mathml" ' if section["needs_math"] else '') + '/>'
        for i, section in enumerate(sections)
    ])
    item_ref_list = '\n        '.join([f'<itemref idref="c{i+1}"/>' for i in range(len(sections))])

    image_list = '\n        '.join([f'<item id="image{i}" href="images/{os.path.basename(image_url)}" media-type="image/png"/>' for i, (image_url, image_content) in enumerate(images.items())])
    return \
        f"""<?xml version="1.0" encoding="utf-8"?>
<package version="3.0" xml:lang="en" unique-identifier="uid" prefix="cc: http://creativecommons.org/ns#" xmlns="http://www.idpf.org/2007/opf">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title id="title">{title}</dc:title>
        <dc:identifier id="uid">code.google.com.epub-samples.linear-algebra</dc:identifier>
        <dc:language>en</dc:language>
        <dc:creator>{creator}</dc:creator>
        <meta property="dcterms:modified">{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
        <dc:rights>This work is shared with the public using the MIT Free Documentation License, Version 1.2.</dc:rights>
        <dc:rights>© 2024 By {creator}.</dc:rights>
        <link rel="cc:license" href="http://www.gnu.org/copyleft/fdl.xhtml"/>
        <meta property="dcterms:source">http://linear.ups.edu</meta>
    </metadata>
    <manifest>
        <item id="css0" href="css/epub.css" media-type="text/css"/>
        <item id="css7" href="css/commonltr.css" media-type="text/css"/>
        {image_list}
        {section_list}
    </manifest>
    <spine>
        {item_ref_list}
    </spine>
</package>"""

def get_epub_css():
    return \
        """body {
    margin: 5em 5em 5em 5em;
    background-color: rgb(255,253,249);
    font-family: arial, verdana, sans-serif;
    color:black;
}

nav#toc ol {
    list-style-type: none;
}

nav#toc ol li a {
    text-decoration : none;
    color:black;
}

body#titlepage {
    text-align : center;
}"""

def get_common_itr_css():
    return \
        """/*
 | This file is part of the DITA Open Toolkit project hosted on 
 | Sourceforge.net. See the accompanying license.txt file for 
 | applicable licenses.
*/

/*
 | (c) Copyright IBM Corp. 2004, 2005 All Rights Reserved.
 */
 
.unresolved { background-color: skyblue; }
.noTemplate { background-color: yellow; }

.base { background-color: #ffffff; }

/* Add space for top level topics */
.nested0 { margin-top : 1em;}

/* div with class=p is used for paragraphs that contain blocks, to keep the XHTML valid */
.p {margin-top: 1em}

/* Default of italics to set apart figure captions */
.figcap { font-style: italic }
.figdesc { font-style: normal }

/* Use @frame to create frames on figures */
.figborder { border-style: solid; padding-left : 3px; border-width : 2px; padding-right : 3px; margin-top: 1em; border-color : Silver;}
.figsides { border-left : 2px solid; padding-left : 3px; border-right : 2px solid; padding-right : 3px; margin-top: 1em; border-color : Silver;}
.figtop { border-top : 2px solid; margin-top: 1em; border-color : Silver;}
.figbottom { border-bottom : 2px solid; border-color : Silver;}
.figtopbot { border-top : 2px solid; border-bottom : 2px solid; margin-top: 1em; border-color : Silver;}

/* Most link groups are created with <div>. Ensure they have space before and after. */
.ullinks { list-style-type: none }
.ulchildlink { margin-top: 1em; margin-bottom: 1em }
.olchildlink { margin-top: 1em; margin-bottom: 1em }
.linklist { margin-bottom: 1em }
.linklistwithchild { margin-left: 1.5em; margin-bottom: 1em  }
.sublinklist { margin-left: 1.5em; margin-bottom: 1em  }
.relconcepts { margin-top: 1em; margin-bottom: 1em }
.reltasks { margin-top: 1em; margin-bottom: 1em }
.relref { margin-top: 1em; margin-bottom: 1em }
.relinfo { margin-top: 1em; margin-bottom: 1em }
.breadcrumb { font-size : smaller; margin-bottom: 1em }
dt.prereq { margin-left : 20px;}

/* Set heading sizes, getting smaller for deeper nesting */
.topictitle1 { margin-top: 0pc; margin-bottom: .1em; font-size: 1.34em; }
.topictitle2 { margin-top: 1pc; margin-bottom: .45em; font-size: 1.17em; }
.topictitle3 { margin-top: 1pc; margin-bottom: .17em; font-size: 1.17em; font-weight: bold; }
.topictitle4 { margin-top: .83em; font-size: 1.17em; font-weight: bold; }
.topictitle5 { font-size: 1.17em; font-weight: bold; }
.topictitle6 { font-size: 1.17em; font-style: italic; }
.sectiontitle { margin-top: 1em; margin-bottom: 0em; color: black; font-size: 1.17em; font-weight: bold;}
.section { margin-top: 1em; margin-bottom: 1em }
.example { margin-top: 1em; margin-bottom: 1em }
div.tasklabel { margin-top: 1em; margin-bottom: 1em; }
h2.tasklabel, h3.tasklabel, h4.tasklabel, h5.tasklabel, h6.tasklabel { font-size: 100%; }

/* All note formats have the same default presentation */
.note { margin-top: 1em; margin-bottom : 1em;}
.notetitle { font-weight: bold }
.notelisttitle { font-weight: bold }
.tip { margin-top: 1em; margin-bottom : 1em;}
.tiptitle { font-weight: bold }
.fastpath { margin-top: 1em; margin-bottom : 1em;}
.fastpathtitle { font-weight: bold }
.important { margin-top: 1em; margin-bottom : 1em;}
.importanttitle { font-weight: bold }
.remember { margin-top: 1em; margin-bottom : 1em;}
.remembertitle { font-weight: bold }
.restriction { margin-top: 1em; margin-bottom : 1em;}
.restrictiontitle { font-weight: bold }
.attention { margin-top: 1em; margin-bottom : 1em;}
.attentiontitle { font-weight: bold }
.dangertitle { font-weight: bold }
.danger { margin-top: 1em; margin-bottom : 1em;}
.cautiontitle { font-weight: bold }
.caution { font-weight: bold; margin-bottom : 1em; }
.warning { margin-top: 1em; margin-bottom : 1em;}
.warningtitle { font-weight: bold }

/* Simple lists do not get a bullet */
ul.simple { list-style-type: none }

/* Used on the first column of a table, when rowheader="firstcol" is used */
.firstcol { font-weight : bold;}

/* Various basic phrase styles */
.bold { font-weight: bold; }
.boldItalic { font-weight: bold; font-style: italic; }
.italic { font-style: italic; }
.underlined { text-decoration: underline; }
.uicontrol { font-weight: bold; }
.parmname { font-weight: bold; }
.kwd { font-weight: bold; }
.defkwd { font-weight: bold; text-decoration: underline; }
.var { font-style : italic;}
.shortcut { text-decoration: underline; }

/* Default of bold for definition list terms */
.dlterm { font-weight: bold; }

/* Use CSS to expand lists with @compact="no" */
.dltermexpand { font-weight: bold; margin-top: 1em; }
*[compact="yes"]>li { margin-top: 0em;}
*[compact="no"]>li { margin-top: .53em;}	
.liexpand { margin-top: 1em; margin-bottom: 1em }
.sliexpand { margin-top: 1em; margin-bottom: 1em }
.dlexpand { margin-top: 1em; margin-bottom: 1em }
.ddexpand { margin-top: 1em; margin-bottom: 1em }
.stepexpand { margin-top: 1em; margin-bottom: 1em }
.substepexpand { margin-top: 1em; margin-bottom: 1em }

/* Align images based on @align on topic/image */
div.imageleft { text-align: left }
div.imagecenter { text-align: center }
div.imageright { text-align: right }
div.imagejustify { text-align: justify }

/* The cell border can be turned on with
   {border-right:solid}
   This value creates a very thick border in Firefox (does not match other tables)

   Firefox works with 
   {border-right:solid 1pt}
   but this causes a barely visible line in IE */
.cellrowborder { border-left:none; border-top:none; border-right:solid 1px; border-bottom:solid 1px }
.row-nocellborder { border-left:none; border-right:none; border-top:none; border-right: hidden; border-bottom:solid 1px}
.cell-norowborder { border-top:none; border-bottom:none; border-left:none; border-bottom: hidden; border-right:solid 1px}
.nocellnorowborder { border:none; border-right: hidden;border-bottom: hidden }

pre.screen { padding: 5px 5px 5px 5px; border: outset; background-color: #CCCCCC; margin-top: 2px; margin-bottom : 2px; white-space: pre}

span.filepath { font-family:monospace }

/* OXYGEN PATCH START - EXM-18359 */
body {
  margin-left: 1em;
  margin-top: 1em;
}
/* OXYGEN PATCH END - EXM-18359 */

/* OXYGEN PATCH START - EXM-18138 */
span.uicontrol > img {
  padding-right: 5px;
}
/* OXYGEN PATCH END - EXM-18138 */

/* OXYGEN PATCH START EXM-17248 - Center figure captions. */
div.fignone p.figcap {
  display:block;
  text-align:left;
  font-weight:bold;
  padding:2px 10px 5px 10px;
}

div.fignone p.figcapcenter {
  display:block;
  text-align:center;
  font-weight:bold;
  padding:2px 10px 5px 10px;
}

div.fignone p.figcapright {
  display:block;
  text-align:right;
  font-weight:bold;
  padding:2px 10px 5px 10px;
}

div.fignone p.figcapjustify {
  display:block;
  text-align:justify;
  font-weight:bold;
  padding:2px 10px 5px 10px;
}

div.fignone img {
  padding-top: 5px;
  padding-left: 10px;
  padding-right: 10px;
}
/* OXYGEN PATCH END EXM-17248 */"""