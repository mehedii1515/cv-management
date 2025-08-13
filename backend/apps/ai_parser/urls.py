from django.urls import path
from . import views

app_name = 'ai_parser'
 
urlpatterns = [
    path('test/', views.test_openai_connection, name='test_openai'),
    path('test-gemini/', views.test_gemini_connection, name='test_gemini'),
    path('test-unstructured/', views.test_unstructured, name='test_unstructured'),
    path('ai-providers/status/', views.get_ai_provider_status, name='ai_provider_status'),
    path('ai-providers/compare/', views.compare_ai_providers, name='compare_ai_providers'),
    path('ai-providers/switch/', views.switch_ai_provider, name='switch_ai_provider'),
    path('expertise/format/', views.get_formatted_expertise_details, name='format_expertise_details'),
    path('expertise/example/', views.get_expertise_display_example, name='expertise_display_example'),
] 