import pytest
import hyperlink_extractor


@pytest.fixture
def html():
    return '''
    <html>
        <body>
            <a id="a_1" href="link1.html"></a>
            <a id="a_2"></a>
            <a id="a_3" href="link3.html"></a>
            <div id="div_1">
                <a href="link4.html"></a>
                <a href="link5.html"></a>
            </div>
        </body>
    </html> 
    '''


def test_id_1(html):
    restrict_xpaths = ['//a[@id="a_1"]']
    links = hyperlink_extractor.extract(html, restrict_xpaths)
    assert len(links) == 1
    assert 'link1.html' in links[0].path


def test_id_2(html):
    restrict_xpaths = ['//*[@id="div_1"]']
    links = hyperlink_extractor.extract(html, restrict_xpaths)
    assert len(links) == 2
    assert 'link4.html' in links[0].path
    assert 'link5.html' in links[1].path


def test_ignore_invalid(html):
    links = hyperlink_extractor.extract(html)
    assert len(links) == 4


def test_base_url_1(html):
    links = hyperlink_extractor.extract(html, base_url='http://test.com')
    assert links[0].to_text() == 'http://test.com/link1.html'


def test_base_url_2(html):
    links = hyperlink_extractor.extract(html)
    assert links[0].to_text() == 'link1.html'
