"""Misc helpers."""
from django.db.models import Q
from django.db.models import Count
from bs4 import BeautifulSoup

def get_url_friendly(name):
    """Converts the name to a url friendly string for use in `str_id`"""
    temp = "-".join(name.lower().split())
    return "".join(c for c in temp if c.isalnum() or c == "-")

def query_from_num(request, default_num, queryset):
    """Returns queryset with from and num if the query parameters are valid."""
    # Initialize defaults
    from_i = 0
    num = default_num

    # Set values from query paramters if available and valid
    from_q = request.GET.get('from')
    num_q = request.GET.get('num')
    if from_q is not None and str.isdigit(from_q):
        from_i = int(from_q)
    if num_q is not None and str.isdigit(num_q) and int(num_q) <= 100:
        num = int(num_q)

    return queryset[from_i: from_i + num]

def query_search(request, min_length, queryset, fields):
    """Returns queryset with search filter."""
    search = request.GET.get('query')
    if search is not None and len(search) >= min_length:
        all_queries = Q()
        for field in fields:
            all_queries = all_queries | Q(**{field + '__icontains': search})
        return queryset.filter(all_queries)

    return queryset

def sort_by_field(queryset, field, reverse=False):
    """Return a queryset ordered by a field"""
    queryset = queryset.annotate(field_count=Count(field))
    return queryset.order_by(('-' if reverse else '') + 'field_count')

def table_to_markdown(html):
    # Initialize
    md = ''
    MAX_COLS = 0
    HEADER_SEPARATOR = 'HEADER_SEPARATOR'

    # Parse
    SOUP = BeautifulSoup(html, features='html.parser')

    # Count maximum columns
    for row in SOUP.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        MAX_COLS = max(MAX_COLS, len(cols))

    if MAX_COLS == 0:
        return md

    if MAX_COLS == 1:
        for row in SOUP.find_all('tr'):
            md += row.find(['td', 'th']).text.replace('\n', '') + '\n'
        return md

    # Iterate all rows and columns
    for i, row in enumerate(SOUP.find_all('tr')):
        # Iterate all columns
        cols = row.find_all(['td', 'th'])
        for col in cols:
            txt = col.text.replace('\n', '')
            md += txt + '&zwnj; | '

        if len(cols) < MAX_COLS:
            md += '&zwnj; | ' * (MAX_COLS - len(cols))

        # Insert newline after each row
        md += '\n'

        # Insert header and separator placeholder
        if i == 0:
            md += HEADER_SEPARATOR + '\n'

    # Replace header separator
    md = md.replace(HEADER_SEPARATOR, '---|' * MAX_COLS)

    return md
