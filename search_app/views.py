from django.shortcuts import render
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .import search
from CLOTH import settings


def results(request, template_name="search_app/results.html"):
    """ template for displaying settings.PRODUCTS_PER_PAGE paginated product results """
    # get current search phrase
    q = request.GET.get('q', '')
    # get current page number. Set to 1 is missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    matching = search.products(q).get('products', [])
    # generate the pagintor object
    paginator = Paginator(matching,
                          settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list

    page_title = 'Search Results for: ' + q
    return render(request, template_name, locals())