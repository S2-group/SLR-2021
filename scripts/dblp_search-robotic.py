from lxml import etree

DBLP_XML = './dblp-2021-02-01.xml'
YEAR_MIN = 2007
YEAR_MAX = 2020
KEYWORDS = ['ROS','software']
VENUES = tuple([
	'conf/icra',
    'journals/ral',
    'journals/scirobotics',
    'conf/iros',
    'journals/ram',
    'journals/ijrr',
    'journals/rcim',
    'conf/rss',
    'conf/ras',
    'conf/hri',
    'journals/arobots',
    'journals/jfr',
    'journals/jirs',
    'journals/firai',
    'journals/corr'

])

# Iterate over a large-sized xml file without the need to store it in memory in
# full. Yields every next element. Source:
# https://stackoverflow.com/questions/9856163/using-lxml-and-iterparse-to-parse-a-big-1gb-xml-file
def iterate_xml(xmlfile):
    doc = etree.iterparse(xmlfile, events=('start', 'end'), load_dtd=True)
    _, root = next(doc)
    start_tag = None
    for event, element in doc:
        if event == 'start' and start_tag is None:
            start_tag = element.tag
        if event == 'end' and element.tag == start_tag:
            yield element
            start_tag = None
            root.clear()

if __name__ == "__main__":
    hits = 0

    # Parse all entries in the DBLP database.
    for dblp_entry in iterate_xml(DBLP_XML):
        key = dblp_entry.get('key')

        # The db key should start with any of the venues we are interested in,
        # as well as be within the desired year range.
        if (key.startswith(VENUES) and
            int(dblp_entry.find('year').text) >= YEAR_MIN and
            int(dblp_entry.find('year').text) <= YEAR_MAX):
            # Remove any potential HTML content (such as <i>) from the title.
            title = ''.join(dblp_entry.find('title').itertext())

            # If the title contains any of the keywords (case-sensitive) add to
            # result.
            if any(keyword in title for keyword in KEYWORDS):
                # Merge the names of all authors of the work.
                authors = ' & '.join(''.join(author.itertext()) for author in
                    dblp_entry.findall('author'))

                # Obtain the source (usually in the form of a DOI link).
                ee = dblp_entry.find('ee')
                if ee is not None:
                    ee = ee.text

                # Print the current result to stdout as a csv line.
                print(hits,
                      title.replace(',', ';'),
                      dblp_entry.find('year').text,
                      authors,
                      key,
                      ee,
                      sep=', ')

                hits += 1
