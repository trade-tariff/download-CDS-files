# Python
#
# This file implements an example.
#
# This file is part of mdutils. https://github.com/didix21/mdutils
#
# MIT License: (C) 2018 Dídac Coll


from mdutils.mdutils import MdUtils
from mdutils import Html

md_file = MdUtils(file_name='Example_Markdown', title='Markdown File Example')

md_file.new_header(level=1, title='Overview')  # style is set 'atx' format by default.

md_file.new_paragraph("This is an example of markdown file created using mdutils python package. In this example you "
                     "are going to see how to create a markdown file using this library. Moreover, you're "
                     "finding the available features which makes easy the creation of this type of files while you "
                     "are running Python code.")
md_file.new_paragraph("**IMPORTANT:** some features available on this library have no effect with the GitHub Markdown "
                     "CSS. Some of them are: coloring text, centering text...")
md_file.new_paragraph()

# Available Features
md_file.new_header(level=1, title="This is what you can do")

# ********************************************************************************************************************
# ***************************************************** Markdown *****************************************************
# ********************************************************************************************************************
md_file.new_header(level=2, title="Create Markdown files")
md_file.new_paragraph("``create_md_file()`` is the last command that has to be called.")
md_file.insert_code("import Mdutils\n"
                   "\n"
                   "\n"
                   "md_file = MdUtils(file_name=\'Example_Markdown\',title=\'Markdown File Example\')\n"
                   "md_file.create_md_file()", language='python')

# ********************************************************************************************************************
# ***************************************************** Headers ******************************************************
# ********************************************************************************************************************
md_file.new_header(level=2, title="Create Headers")
md_file.new_paragraph("Using ``new_header`` method you can create headers of different levels depending on the style. "
                     "There are two available styles: 'atx' and 'setext'. The first one has til 6 different header "
                     "levels. Atx's levels 1 and 2 are automatically added to the table of contents unless the "
                     "parameter ``add_table_of_contents`` is set to 'n'. The 'setext' style only has two levels"
                     "of headers.")

md_file.insert_code("md_file.new_header(level=1, title='Atx Header 1')\n"
                   "md_file.new_header(level=2, title='Atx Header 2')\n"
                   "md_file.new_header(level=3, title='Atx Header 3')\n"
                   "md_file.new_header(level=4, title='Atx Header 4')\n"
                   "md_file.new_header(level=5, title='Atx Header 5')\n"
                   "md_file.new_header(level=6, title='Atx Header 6')", language='python')

md_file.new_header(level=1, title='Atx Header 1', add_table_of_contents='n')
md_file.new_header(level=2, title='Atx Header 2', add_table_of_contents='n')
md_file.new_header(level=3, title='Atx Header 3')
md_file.new_header(level=4, title='Atx Header 4')
md_file.new_header(level=5, title='Atx Header 5')
md_file.new_header(level=6, title='Atx Header 6')

md_file.insert_code("md_file.new_header(level=1, title='Setext Header 1', style='setext')\n"
                   "md_file.new_header(level=2, title='Setext Header 2', style='setext')", language='python')

md_file.new_header(level=1, title='Setext Header 1', style='setext', add_table_of_contents='n')
md_file.new_header(level=2, title='Setext Header 2', style='setext', add_table_of_contents='n')
md_file.new_paragraph()  # Add two jump lines

# ********************************************************************************************************************
# ******************************************** Create a table of contents ********************************************
# ********************************************************************************************************************
md_file.new_header(level=2, title='Table of Contents')
md_file.new_paragraph("If you have defined some headers of level 1 and 2, you can create a table of contents invoking "
                     "the following command (Normally, the method will be called at the end of the code before calling "
                     "``create_md_file()``)")
md_file.insert_code("md_file.new_table_of_contents(table_title='Contents', depth=2)", language='python')

# ********************************************************************************************************************
# ******************************************** Paragraph and Text format *********************************************
# ********************************************************************************************************************
md_file.new_header(level=2, title="Paragraph and Text Format")
md_file.new_paragraph("mdutils allows you to create paragraph, line breaks or simply write text:")
# *************************************************** Paragraph ******************************************************
md_file.new_header(3, "New Paragraph Method")

md_file.insert_code("md_file.new_paragraph(\"Using ``new_paragraph`` method you can very easily add a new paragraph\" \n"
                   "\t\t\t\t\t \" This example of paragraph has been added using this method. Moreover,\"\n"
                   "\t\t\t\t\t \"``new_paragraph`` method make your live easy because it can give format\" \n"
                   "\t\t\t\t\t \" to the text. Lets see an example:\")", language='python')

md_file.new_paragraph("Using ``new_paragraph`` method you can very easily add a new paragraph on your markdown file. "
                     "This example of paragraph has been added using this method. Moreover, ``new_paragraph`` method "
                     "make your live easy because it can give format to the text. Lets see an example:")

md_file.insert_code("md_file.new_paragraph(\"This is an example of text in which has been added color, "
                   "bold and italics text.\", bold_italics_code='bi', color='purple')", language='python')

md_file.new_paragraph("This is an example of text in which has been added color, bold and italics text.",
                     bold_italics_code='bi', color='purple')
# ************************************************* New Line *********************************************************
md_file.new_header(3, "New Line Method")

md_file.new_paragraph("``mdutils`` has a method which can create new line breaks. Lets see it.")
md_file.insert_code("md_file.new_line(\"This is an example of line break which has been created with ``new_line`` "
                   "method.\")", language='python')
md_file.new_line("This is an example of line break which has been created with ``new_line`` method.")
md_file.new_paragraph("As ``new_paragraph``, ``new_line`` allows users to give format to text using "
                     "``bold_italics_code`` and ``color`` parameters:")

md_file.insert_code("md_file.new_line(\"This is an inline code which contains bold and italics text and it is centered\","
                   " bold_italics_code='cib', align='center')", language='python')

md_file.new_line("This is an inline code which contains bold and italics text and it is centered",
                bold_italics_code='cib', align='center')
# ************************************************** write **********************************************************
md_file.new_header(3, "Write Method")
md_file.new_paragraph("``write`` method writes text in a markdown file without jump lines ``'\\n'`` and as "
                     "``new_paragraph`` and ``new_line``, you can give format to text using the arguments "
                     "``bold_italics_code``, ``color`` and ``align``: ")

md_file.insert_code("md_file.write(\"The following text has been written with ``write`` method. You can use markdown "
                   "directives to write:\"\n"
                   "\t\t\t \"**bold**, _italics_, ``inline_code``... or \")\n"
                   "md_file.write(\"use the following available parameters:  \\n\")", language='python')

md_file.write("\n\nThe following text has been written with ``write`` method. You can use markdown directives to write: "
             "**bold**, _italics_, ``inline_code``... or ")
md_file.write("use the following available parameters:  \n")

md_file.insert_code("md_file.write('  \\n')\n"
                   "md_file.write('bold_italics_code', bold_italics_code='bic')\n"
                   "md_file.write('  \\n')\n"
                   "md_file.write('Text color', color='green')\n"
                   "md_file.write('  \\n')\n"
                   "md_file.write('Align Text to center', align='center')", language='python')

md_file.write('  \n')
md_file.write('bold_italics_code', bold_italics_code='bic')
md_file.write('  \n')
md_file.write('Text color', color='green')
md_file.write('  \n')
md_file.write('Align Text to center', align='center')
md_file.write('  \n')

# ********************************************************************************************************************
# ************************************************* Create a Table ***************************************************
# ********************************************************************************************************************
md_file.new_header(2, "Create a Table")
md_file.new_paragraph("The library implements a method called ``new_table`` that can create tables using a list of "
                     "strings. This method only needs: the number of rows and columns that your table must have. "
                     "Optionally you can align the content of the table using the parameter ``text_align``")

md_file.insert_code("list_of_strings = [\"Items\", \"Descriptions\", \"Data\"]\n"
                   "for x in range(5):\n"
                   "\tlist_of_strings.extend([\"Item \" + str(x), \"Description Item \" + str(x), str(x)])\n"
                   "md_file.new_line()\n"
                   "md_file.new_table(columns=3, rows=6, text=list_of_strings, text_align='center')", language='python')

list_of_strings = ["Items", "Descriptions", "Data"]
for x in range(5):
    list_of_strings.extend(["Item " + str(x), "Description Item " + str(x), str(x)])
md_file.new_line()
md_file.new_table(columns=3, rows=6, text=list_of_strings, text_align='center')

# ********************************************************************************************************************
# ************************************************** Create Link *****************************************************
# ********************************************************************************************************************

md_file.new_header(2, "Create Links")

# *********************************************** Inline link ********************************************************

md_file.new_header(3, "Create inline links")

link = "https://github.com/didix21/mdutils"
text = "mdutils"

md_file.new_paragraph("``new_inline_link`` method allows you to create a link of the style: "
                     "``[mdutils](https://github.com/didix21/mdutils)``.\n")
md_file.new_paragraph("Moreover, you can add bold, italics or code in the link text. Check the following examples: \n")

md_file.insert_code("md_file.new_line('  - Inline link: '"
                   " + md_file.new_inline_link(link='{}', text='{}')) \n".format(link, text) +
                   "md_file.new_line('  - Bold inline link: ' "
                   "+ md_file.new_inline_link(link='{}', text='{}', bold_italics_code='b') \n".format(link, text) +
                   "md_file.new_line('  - Italics inline link: ' "
                   "+ md_file.new_inline_link(link='{}', text='{}', bold_italics_code='i') \n".format(link, text) +
                   "md_file.new_line('  - Code inline link: ' "
                   "+ md_file.new_inline_link(link='{}', text='{}', bold_italics_code='i') \n".format(link, text) +
                   "md_file.new_line('  - Bold italics code inline link: ' "
                   "+ md_file.new_inline_link(link='{}', text='{}', bold_italics_code='cbi') \n".format(link, text) +
                   "md_file.new_line('  - Another inline link: ' + md_file.new_inline_link(link='{}') \n".format(link),
                   language='python')

md_file.new_line('  - Inline link: ' + md_file.new_inline_link(link=link, text=text))
md_file.new_line('  - Bold inline link: ' + md_file.new_inline_link(link=link, text=text, bold_italics_code='b'))
md_file.new_line('  - Italics inline link: ' + md_file.new_inline_link(link=link, text=text, bold_italics_code='i'))
md_file.new_line('  - Code inline link: ' + md_file.new_inline_link(link=link, text=text, bold_italics_code='c'))
md_file.new_line(
    '  - Bold italics code inline link: ' + md_file.new_inline_link(link=link, text=text, bold_italics_code='cbi'))
md_file.new_line('  - Another inline link: ' + md_file.new_inline_link(link=link))

# *********************************************** Reference link ******************************************************
md_file.new_header(3, "Create reference links")

md_file.new_paragraph("``new_reference_link`` method allows you to create a link of the style: "
                     "``[mdutils][1]``. All references will be added at the end of the markdown file automatically as: \n")

md_file.insert_code("[1]: https://github.com/didix21/mdutils", language="python")
md_file.new_paragraph("Lets check some examples: \n")

link = "https://github.com/didix21/mdutils"

md_file.insert_code("md_file.write('\\n  - Reference link: ' "
                   "+ md_file.new_reference_link(link='{}', text='mdutils', reference_tag='1')\n".format(link) +
                   "md_file.write('\\n  - Reference link: ' "
                   "+ md_file.new_reference_link(link='{}', text='another reference', reference_tag='md')\n".format(
                       link) +
                   "md_file.write('\\n  - Bold link: ' "
                   "+ md_file.new_reference_link(link='{}', text='Bold reference', reference_tag='bold', bold_italics_code='b')\n".format(
                       link) +
                   "md_file.write('\\n  - Italics link: ' "
                   "+ md_file.new_reference_link(link='{}', text='Bold reference', reference_tag='italics', bold_italics_code='i')\n".format(
                       link),
                   language="python")

md_file.write("\n  - Reference link: " + md_file.new_reference_link(link=link, text='mdutils', reference_tag='1'))
md_file.write(
    "\n  - Reference link: " + md_file.new_reference_link(link=link, text='another reference', reference_tag='md'))
md_file.write("\n  - Bold link: " + md_file.new_reference_link(link=link, text='Bold reference', reference_tag='bold',
                                                             bold_italics_code='b'))
md_file.write(
    "\n  - Italics link: " + md_file.new_reference_link(link=link, text='Italics reference', reference_tag='italics',
                                                       bold_italics_code='i'))

# ********************************************************************************************************************
# ************************************************** Create Lists *****************************************************
# ********************************************************************************************************************
md_file.new_header(2, "Create Lists")
# *********************************************** Unordered Lists ******************************************************
md_file.new_header(3, "Create unordered lists")
md_file.new_paragraph(
    "You can add Mark down unordered list using ``md_file.new_list(items, marked_with)``. Lets check an example: ")
items = ["Item 1", "Item 2", "Item 3", "Item 4", ["Item 4.1", "Item 4.2", ["Item 4.2.1", "Item 4.2.2"],
                                                  "Item 4.3", ["Item 4.3.1"]], "Item 5"]
md_file.insert_code(f'items = {items}\n'
                   f'md_file.new_list(items)\n')
md_file.new_list(items=items)

# *********************************************** Ordered Lists ******************************************************
md_file.new_header(3, "Create ordered lists")
md_file.new_paragraph("You can add ordered ones easily, too: ``md_file.new_list(items, marked_with='1')``")
md_file.new_list(items=items, marked_with='1')

md_file.new_paragraph("Moreover, you can add mixed list, for example: ")
items = ["Item 1", "Item 2", ["1. Item 2.1", "2. Item 2.2"], "Item 3"]
md_file.insert_code(f'items = {items}\n'
                   f'md_file.new_list(items)\n')
md_file.new_list(items)
md_file.new_paragraph("Maybe you want to replace the default hyphen ``-`` by a ``+`` or ``*`` then you can do: "
                     "``md_file.new_list(items, marked_with='*')``.")

# ********************************************************************************************************************
# ************************************************** Add Images ******************************************************
# ********************************************************************************************************************

md_file.new_header(2, "Add images")

# *********************************************** Inline Image *******************************************************

image_text = "snow trees"
path = "./doc/source/images/photo-of-snow-covered-trees.jpg"

md_file.new_header(3, "Inline Images")

md_file.new_paragraph("You can add inline images using ``new_inline_image`` method. Method will return: "
                     "``[image](../path/to/your/image.png)``. Check the following example: ")
md_file.insert_code("md_file.new_line(md_file.new_inline_image(text='{}', path='{}'))".format(image_text, path))
md_file.new_line(md_file.new_inline_image(text=image_text, path=path))

# *********************************************** Reference Image *****************************************************
md_file.new_header(3, "Reference Images")
md_file.new_paragraph("You can add inline images using ``new_reference_image`` method. Method will return: "
                     "``[image][im]``. Check the following example: ")
md_file.insert_code(
    "md_file.new_line(md_file.new_reference_image(text='{}', path='{}', reference_tag='im'))".format(image_text, path))
md_file.new_line(md_file.new_reference_image(text=image_text, path=path, reference_tag='im'))

# ************************************************* Html Image *******************************************************

md_file.new_header(2, "Add HTML images")

# *********************************************** Size Image *******************************************************

md_file.new_header(3, "Change size to images")
path = "./doc/source/images/sunset.jpg"

md_file.new_paragraph("With ``Html.image`` you can change size of images in a markdown file. For example you can do"
                     "the following for changing width: ``md_file.new_paragraph(Html.image(path=path, size='200'))``")

md_file.new_paragraph(Html.image(path=path, size='200'))

md_file.new_paragraph(
    "Or maybe only want to change height: ``md_file.new_paragraph(Html.image(path=path, size='x300'))``")
md_file.new_paragraph(Html.image(path=path, size='x300'))

md_file.new_paragraph("Or change width and height: ``md_file.new_paragraph(Html.image(path=path, size='300x300'))``")
md_file.new_paragraph(Html.image(path=path, size='300x300'))
md_file.write('\n')

# *********************************************** Align Image *******************************************************

md_file.new_header(3, "Align images")
md_file.new_paragraph("Html.image allow to align images, too. For example you can run: "
                     "``md_file.new_paragraph(Html.image(path=path, size='300x200', align='center'))``")

md_file.new_paragraph(Html.image(path=path, size='300x200', align='center'))

# Create a table of contents
md_file.new_table_of_contents(table_title='Contents', depth=2)
md_file.create_md_file()