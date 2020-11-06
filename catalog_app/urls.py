from django.urls import path
from.import views
from store_app import views as store


urlpatterns=[
	path('',views.index,name='home-page'),
	
	path('about/',store.about,name='about-page'),
	path('contact/',store.contact,name='contact-page'),
	path('privacy/',store.privacy,name='privacy-page'),

	path('category/<slug:category_slug>/show_category',views.show_category, name='catalog_category'),
    path('product/<slug:product_slug>/show_product', views.show_product,name='catalog_product'),
    path('review/product/add', views.add_review, name='product_add_review'),
    path('tag/product/add', views.add_tag, name='add_tag' ),
    path('tag_cloud/tag_cloud',views.tag_cloud, name='tag_cloud'),
    path('tag/<slug:tag>', views.tag,name='tag'),

]
