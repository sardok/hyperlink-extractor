import pytest
import hyperlink_extractor
from lxml import html as lxml_html


@pytest.fixture
def html_frag():
    return '''
    <div>
        <a href='link1.html'><a/>
        <div id="block_1">
            <a href="link2.html"></a> 
        </div>
        <a href="link3.html"></a>
        <div id="block_2">
            <a href="link4.html"></a>
        </div>
        <a href="link5.html"></a>
    </div>
    '''


@pytest.fixture
def html(html_frag):
    return '''
    <html>
        <body>
        {body}
        </body>
    </html>
    '''.format(body=html_frag)


@pytest.fixture
def html_doc_frag(html_frag):
    return lxml_html.fragment_fromstring(html_frag)


def test_basic(html_doc_frag):
    links = hyperlink_extractor.extract_from_doc(html_doc_frag)
    assert len(links) == 5
    for index, link in enumerate(links, start=1):
        assert 'link{}.html'.format(index) in link.path


def test_restrict_xpaths_1(html_doc_frag):
    restrict_xpaths = ['//*[contains(@id, "block_")]']
    links = hyperlink_extractor.extract_from_doc(html_doc_frag, restrict_xpaths)
    assert len(links) == 2
    assert 'link2.html' in links[0].path
    assert 'link4.html' in links[1].path


def test_restrict_xpaths_2(html_doc_frag):
    restrict_xpaths = ['//div[@id="block_1"]', '//div[@id="block_2"]']
    links = hyperlink_extractor.extract_from_doc(html_doc_frag, restrict_xpaths)
    assert len(links) == 2
    assert 'link2.html' in links[0].path
    assert 'link4.html' in links[1].path
