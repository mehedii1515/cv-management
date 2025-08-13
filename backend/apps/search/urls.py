"""
Search app URL configuration
"""
from django.urls import path, include
from . import views
from . import file_views

app_name = 'search'

# File-only search endpoints
file_urlpatterns = [
    path('search', file_views.search_files_only, name='file_search_only'),
    path('suggestions', file_views.file_suggestions, name='file_suggestions'),
    path('index/directory', file_views.index_directory, name='index_directory'),
    path('index/file', file_views.index_single_file, name='index_single_file'),
    path('index/delete', file_views.delete_file_from_index, name='delete_file_from_index'),
    path('index/create', file_views.create_file_index, name='create_file_index'),
    path('upload', file_views.upload_and_index_file, name='upload_and_index_file'),
    path('directories', file_views.get_indexed_directories, name='indexed_directories'),
    path('status', file_views.file_search_status, name='file_search_status'),
    path('view', file_views.view_file, name='view_file'),
]

urlpatterns = [
    # Main search endpoints (resume database)
    path('', views.search_cvs, name='search_cvs'),
    path('boolean/', views.boolean_search, name='boolean_search'),
    path('boolean', views.boolean_search, name='boolean_search_no_slash'),  # Support URL without trailing slash
    path('suggest/', views.search_suggestions, name='search_suggestions'),
    path('suggest', views.search_suggestions, name='search_suggestions_no_slash'),  # Support URL without trailing slash
    path('database-files/', views.file_search, name='file_search'),  # Database-linked file search (renamed to avoid conflict)
    path('database-files', views.file_search, name='file_search_no_slash'),  # Support URL without trailing slash
    
    # Pure file search endpoints
    path('files/', include(file_urlpatterns)),
    
    # Admin endpoints
    path('status/', views.search_status, name='search_status'),
    path('status', views.search_status, name='search_status_no_slash'),  # Support URL without trailing slash
    path('create-index/', views.create_index, name='create_index'),
    path('create-index', views.create_index, name='create_index_no_slash'),  # Support URL without trailing slash
    path('help/', views.search_help, name='search_help'),
    path('help', views.search_help, name='search_help_no_slash'),  # Support URL without trailing slash
]
