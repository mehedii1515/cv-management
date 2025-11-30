from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.search'
    verbose_name = 'CV Search Engine'
    
    def ready(self):
        """Import signals and documents when the app is ready"""
        # Import signals for automatic indexing
        import apps.search.signals
        print("✅ Search signals registered for automatic indexing")
        
        # Import document registry to register documents with Elasticsearch
        try:
            from . import documents
            print("✅ Search documents registered with Elasticsearch")
        except ImportError as e:
            print(f"⚠️ Warning: Could not import search documents: {e}")
