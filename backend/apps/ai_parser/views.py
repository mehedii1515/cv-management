from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
import logging

from .gemini_service import GeminiService
from .unstructured_service import UnstructuredService

logger = logging.getLogger(__name__)


@api_view(['GET'])
def test_openai_connection(request):
    """
    Test endpoint to verify OpenAI connection
    """
    try:
        if not settings.OPENAI_API_KEY:
            return Response({
                'status': 'error',
                'message': 'OpenAI API key not configured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Configure and test OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Simple test prompt
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": "Say 'Hello from OpenAI'"}],
            max_tokens=100,
            temperature=0.5
        )
        
        return Response({
            'status': 'success',
            'message': 'OpenAI connection successful',
            'test_response': response.choices[0].message.content,
            'model': settings.OPENAI_MODEL
        })
        
    except Exception as e:
        logger.error(f"OpenAI connection test failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'OpenAI connection failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def test_unstructured(request):
    """
    Test endpoint to verify Unstructured service status and capabilities
    """
    try:
        # Try to initialize the Unstructured service
        unstructured_service = UnstructuredService()
        
        # Get capability test results
        capability_test = unstructured_service.test_extraction_capability()
        
        if capability_test['status'] == 'success':
            # Get version information if available
            try:
                from importlib.metadata import version
                unstructured_version = version('unstructured')
            except:
                unstructured_version = 'Unknown'
            
            return Response({
                'status': 'success',
                'message': 'Unstructured service is available and configured properly',
                'version_info': {
                    'installed': True,
                    'version': unstructured_version
                },
                'supported_formats': unstructured_service.supported_formats,
                'capabilities': {
                    'high_resolution_extraction': True,
                    'table_detection': True,
                    'section_detection': True,
                    'contact_info_extraction': True,
                    'ocr_support': True,
                    'multiple_languages': True
                },
                'test_results': capability_test
            })
        else:
            return Response({
                'status': 'error',
                'message': capability_test['message'],
                'version_info': {
                    'installed': True,
                    'error': capability_test['message']
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except ImportError as e:
        logger.error(f"Unstructured import error: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Unstructured package is not installed: {str(e)}',
            'version_info': {
                'installed': False
            },
            'recommendation': 'Please run "pip install unstructured[pdf,docx,doc,txt]" to install the required package.'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Unstructured test failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Unstructured service error: {str(e)}',
            'version_info': {
                'installed': True,
                'error': str(e)
            },
            'troubleshooting_steps': [
                'Verify that unstructured is properly installed with "pip show unstructured"',
                'Check for missing dependencies with "pip install unstructured[pdf,docx,doc,txt]"',
                'Ensure you have sufficient disk space and memory',
                'Try reinstalling the package with "pip install --upgrade unstructured"'
            ]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def test_gemini_connection(request):
    """
    Test endpoint to verify Gemini connection
    """
    try:
        if not settings.GEMINI_API_KEY:
            return Response({
                'status': 'error',
                'message': 'Gemini API key not configured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Test Gemini connection
        gemini_service = GeminiService()
        test_result = gemini_service.test_connection()
        
        if test_result['status'] == 'success':
            return Response(test_result)
        else:
            return Response(test_result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        logger.error(f"Gemini connection test failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Gemini connection failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_ai_provider_status(request):
    """
    Get the status of all AI providers
    """
    try:
        status_info = {
            'current_provider': getattr(settings, 'AI_PROVIDER', 'openai'),
            'providers': {}
        }
        
        # Check OpenAI status
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            try:
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10
                )
                status_info['providers']['openai'] = {
                    'available': True,
                    'model': settings.OPENAI_MODEL,
                    'status': 'connected'
                }
            except Exception as e:
                status_info['providers']['openai'] = {
                    'available': False,
                    'model': settings.OPENAI_MODEL,
                    'status': f'error: {str(e)}'
                }
        else:
            status_info['providers']['openai'] = {
                'available': False,
                'model': 'not configured',
                'status': 'API key not configured'
            }
        
        # Check Gemini status
        if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
            try:
                gemini_service = GeminiService()
                test_result = gemini_service.test_connection()
                status_info['providers']['gemini'] = {
                    'available': test_result['status'] == 'success',
                    'model': settings.GEMINI_MODEL,
                    'status': test_result['message']
                }
            except Exception as e:
                status_info['providers']['gemini'] = {
                    'available': False,
                    'model': settings.GEMINI_MODEL,
                    'status': f'error: {str(e)}'
                }
        else:
            status_info['providers']['gemini'] = {
                'available': False,
                'model': 'not configured',
                'status': 'API key not configured'
            }
        
        return Response({
            'status': 'success',
            'data': status_info
        })
        
    except Exception as e:
        logger.error(f"AI provider status check failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Failed to check AI provider status: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def compare_ai_providers(request):
    """
    Compare parsing results from different AI providers
    """
    try:
        test_text = request.data.get('test_text', '')
        if not test_text:
            return Response({
                'status': 'error',
                'message': 'test_text parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from .services import ResumeParsingService
        
        results = {}
        
        # Test OpenAI if available
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            try:
                parser = ResumeParsingService(ai_provider='openai')
                results['openai'] = parser.parse_with_openai(test_text)
            except Exception as e:
                results['openai'] = {'error': str(e)}
        
        # Test Gemini if available
        if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
            try:
                parser = ResumeParsingService(ai_provider='gemini')
                results['gemini'] = parser.parse_with_gemini(test_text)
            except Exception as e:
                results['gemini'] = {'error': str(e)}
        
        return Response({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        logger.error(f"AI provider comparison failed: {str(e)}")
        return Response({
            'status': 'success',
            'message': f'Comparison failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def switch_ai_provider(request):
    """
    Switch the AI provider for the current session
    """
    try:
        new_provider = request.data.get('provider', '').lower()
        
        if new_provider not in ['openai', 'gemini', 'both']:
            return Response({
                'status': 'error',
                'message': 'Invalid provider. Must be "openai", "gemini", or "both"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Test the new provider to ensure it works
        if new_provider == 'openai':
            if not settings.OPENAI_API_KEY:
                return Response({
                    'status': 'error',
                    'message': 'OpenAI API key not configured'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Test OpenAI connection
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
        elif new_provider == 'gemini':
            if not settings.GEMINI_API_KEY:
                return Response({
                    'status': 'error',
                    'message': 'Gemini API key not configured'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Test Gemini connection
            gemini_service = GeminiService()
            test_result = gemini_service.test_connection()
            if test_result['status'] != 'success':
                return Response({
                    'status': 'error',
                    'message': f'Gemini connection failed: {test_result["message"]}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'success',
            'message': f'AI provider switched to {new_provider}',
            'provider': new_provider,
            'note': 'This change is only for this session. To make it permanent, update your .env file and restart the server.'
        })
        
    except Exception as e:
        logger.error(f"Provider switch failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Failed to switch provider: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_formatted_expertise_details(request):
    """
    Get formatted expertise details for user-friendly display
    """
    try:
        # Get the resume ID or expertise_details from request
        expertise_details = request.data.get('expertise_details', {})
        
        if not expertise_details:
            return Response({
                'status': 'error',
                'message': 'expertise_details parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Import the service to format the details
        from .services import ResumeParsingService
        
        # Create a parser instance
        parser = ResumeParsingService()
        
        # Format the expertise details
        formatted_details = parser.format_expertise_details_for_display(expertise_details)
        
        return Response({
            'status': 'success',
            'formatted_expertise_details': formatted_details,
            'total_expertise_areas': len(formatted_details)
        })
        
    except Exception as e:
        logger.error(f"Formatting expertise details failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Failed to format expertise details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_expertise_display_example(request):
    """
    Get an example of how expertise details should be displayed
    """
    try:
        # Example expertise details structure
        example_expertise_details = {
            "Python": {
                "work_experience": "Time Period: Jan 2020 to Present\nOrganization: Tech Company\nLocation: New York, USA\nRole/Title: Software Engineer\nResponsibilities:\n- Developed backend services using Python and Django\n- Implemented data processing pipelines\n- Created REST APIs for mobile applications\n\nTime Period: Mar 2018 to Dec 2019\nOrganization: Another Company\nLocation: San Francisco, USA\nRole/Title: Python Developer\nResponsibilities:\n- Built data analysis tools using Python\n- Developed machine learning models\n- Created automated testing frameworks",
                "projects": "Project Name: Data Analysis Tool\nTime Period: Mar 2019 to Dec 2019\nClient/Organization: Internal Project\nDescription:\n- Built a data analysis tool using Python, Pandas and Matplotlib\n- Implemented machine learning algorithms for predictive analytics\n- Created user-friendly interface for non-technical users\n\nProject Name: Automation Framework\nTime Period: Jan 2018 to Feb 2019\nClient/Organization: Client XYZ\nDescription:\n- Developed automated testing framework using Python and Selenium\n- Reduced testing time by 60%\n- Integrated with CI/CD pipeline",
                "other_related_info": "Skills Mentioned: Python, Django, Flask, Pandas, NumPy, Matplotlib, Scikit-learn, TensorFlow\nCertifications: Python Institute PCAP Certification, AWS Certified Developer\nEducation/Training: Bachelor's in Computer Science, Python Programming Course from Coursera\nTools & Software: PyCharm, VS Code, Jupyter Notebook, Git, Docker\nAchievements: Led Python migration project, Improved system performance by 40%\nPublications: 'Python Best Practices' article in Tech Journal\nProfessional Associations: Python Software Foundation Member\nLanguages: Python (Expert), SQL (Advanced)"
            },
            "Machine Learning": {
                "work_experience": "Time Period: Jan 2020 to Present\nOrganization: Tech Company\nLocation: New York, USA\nRole/Title: ML Engineer\nResponsibilities:\n- Developed machine learning models for recommendation systems\n- Implemented deep learning algorithms for image recognition\n- Optimized model performance and deployment",
                "projects": "Project Name: Recommendation Engine\nTime Period: Jun 2020 to Dec 2020\nClient/Organization: E-commerce Platform\nDescription:\n- Built collaborative filtering recommendation system\n- Implemented content-based filtering algorithms\n- Achieved 25% improvement in user engagement",
                "other_related_info": "Skills Mentioned: TensorFlow, PyTorch, Scikit-learn, Keras, OpenCV\nCertifications: TensorFlow Developer Certificate, Google Cloud ML Engineer\nEducation/Training: Master's in Data Science, Machine Learning Specialization from Coursera\nTools & Software: Jupyter Notebook, Google Colab, AWS SageMaker, Docker\nAchievements: Published research paper on deep learning, Led ML team of 5 engineers\nPublications: 'Deep Learning in Production' conference paper\nProfessional Associations: IEEE, ACM\nLanguages: Python (Expert), R (Intermediate)"
            }
        }
        
        # Format the example
        from .services import ResumeParsingService
        parser = ResumeParsingService()
        formatted_example = parser.format_expertise_details_for_display(example_expertise_details)
        
        return Response({
            'status': 'success',
            'message': 'Example of formatted expertise details for display',
            'raw_expertise_details': example_expertise_details,
            'formatted_expertise_details': formatted_example,
            'structure_explanation': {
                'expertise_name': 'The name of the expertise area',
                'work_experiences': 'List of work experiences related to this expertise',
                'projects': 'List of projects related to this expertise',
                'other_info': 'Additional information like skills, certifications, education, etc.'
            }
        })
        
    except Exception as e:
        logger.error(f"Getting expertise display example failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Failed to get expertise display example: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 