from django.shortcuts import render

# this block of code handles the flatpages rendering when in production
def file_not_found_404(request, exception):
    page_title = 'Page Not Found'
    context = {'page_title': page_title}
    response= render(request, "404.html", locals())
    response.status_code=404
    return response

def server_error_500(request):
	page_title = 'Server Error'
	context = {'page_title': page_title}
	return render(request,'500.html',locals())

