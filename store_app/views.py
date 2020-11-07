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

# def about(request, template_name='flatpages/about_page.html'):
# 	page_title = 'About Page'
# 	return render(request,template_name,locals())

def contact(request, template_name='flatpages/contact_page.html'):
	page_title = 'Contact Page'
	return render(request,template_name,locals())

def privacy(request, template_name='flatpages/privacy_policy.html'):
	page_title = 'Privacy Page'
	return render(request,template_name,locals())