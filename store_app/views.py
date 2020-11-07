from django.shortcuts import render
from django.http import Http404

def file_not_found_404(request, exception=Http404):
    page_title = 'Page Not Found'
    context = {'page_title': page_title}
    return render(request, "404.html", context)

def server_error_500(request):
	page_title = 'Server Error'
	context = {'page_title': page_title}
	return render(request,'500.html',context)

