# (c) 2018, Roman Miroshnychenko <roman1972@gmail.com>
# License: MIT
from .data import HTML5
from modeltranslation_xliff.parsers.html import parse_content, add_ph_tags, add_t_tags


def test_html_parser_html5():
    cont_list = list(parse_content(HTML5))
    assert len(cont_list) == 18
    assert 'HTML5 test sample' in cont_list
    assert 'html5, sample' in cont_list
    assert 'Image caption' in cont_list
    assert 'Paragraph <span class="foo">with</span><em>inline tags</em>.' in cont_list
    assert 'Second line' in cont_list and 'Third line' in cont_list
    assert 'Paragraph with enclosing inline tags.</strong>' in cont_list
    assert '"Paragraph with entity references."' in cont_list
    assert 'Paragraph with character reference.' in cont_list  # This string contains a non-breaking space
    assert 'Inline image: <img src="http://via.placeholder.com/350x150" />' in cont_list
    assert '.foo { color: blue; }' not in cont_list
    assert 'console.log(\'Hello World!\');' not in cont_list
    assert 'Preserve &lt;invalid XML chars&gt;' in cont_list


def test_html_parser_plain_text():
    content_list = list(parse_content('Some plain text.'))
    assert content_list == ['Some plain text.']


def test_add_ph_tags():
    string = 'Preserve &lt;invalid XML chars&gt;'
    segment = add_ph_tags(string)
    assert segment == 'Preserve <ph id="1">&lt;</ph>invalid XML chars<ph id="2">&gt;</ph>'


def test_add_t_tags():
    string = '<b><i>String with <span>various open</span>,<br>close and isolated tags.</em></b>'
    segment = add_t_tags(string)
    assert segment == '<bpt id="1">&lt;b&gt;</bpt><it id="2">&lt;i&gt;</it>' \
                      'String with <bpt id="3">&lt;span&gt;</bpt>various open' \
                      '<ept id="3">&lt;/span&gt;</ept>,<it id="4">&lt;br&gt;</it>' \
                      'close and isolated tags.<it id="5">&lt;/em&gt;</it>' \
                      '<ept id="1">&lt;/b&gt;</ept>'
