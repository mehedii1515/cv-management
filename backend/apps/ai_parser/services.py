import os
import json
import logging
import re
from openai import OpenAI
from django.conf import settings
from django.core.files.storage import default_storage
from typing import Dict, Any, Optional

from .gemini_service import GeminiService
from .unstructured_service import UnstructuredService

logger = logging.getLogger(__name__)


class ResumeParsingService:
    """
    Service to parse resume content using OpenAI GPT or Google Gemini
    """

    def __init__(self, ai_provider: str = None):
        # Determine AI provider
        self.ai_provider = ai_provider or getattr(settings, 'AI_PROVIDER', 'openai')
        
        # Initialize OpenAI client if needed
        if self.ai_provider in ['openai', 'both']:
            openai_key = os.getenv('OPENAI_API_KEY')
            if not openai_key:
                if self.ai_provider == 'openai':
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                else:
                    logger.warning("OPENAI_API_KEY not found, OpenAI will be disabled")
                    self.openai_client = None
            else:
                self.openai_client = OpenAI(api_key=openai_key)
                self.openai_model = settings.OPENAI_MODEL
        
        # Initialize Gemini client if needed
        if self.ai_provider in ['gemini', 'both']:
            try:
                self.gemini_service = GeminiService()
            except ValueError as e:
                if self.ai_provider == 'gemini':
                    raise e
                else:
                    logger.warning(f"Gemini initialization failed: {str(e)}, Gemini will be disabled")
                    self.gemini_service = None
        
        # Initialize Unstructured service for text extraction
        try:
            self.unstructured_service = UnstructuredService()
            logger.info("Unstructured service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Unstructured service: {str(e)}")
            raise ValueError("Unstructured service initialization failed. This service is required for text extraction. Please ensure Unstructured is properly installed.")

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from resume file using Unstructured library
        """
        logger.info(f"Using Unstructured to extract text from {file_path}")
        
        # Get file info for logging
        try:
            from django.core.files.storage import default_storage
            if not os.path.isabs(file_path):
                full_path = default_storage.path(file_path)
            else:
                full_path = file_path
            
            file_size = os.path.getsize(full_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            logger.info(f"File details: {file_path} | Size: {file_size} bytes | Type: {file_ext}")
        except Exception as e:
            logger.warning(f"Could not get file details: {e}")
        
        # Extract text
        result = self.unstructured_service.extract_text(file_path)
        
        # Log extraction results
        text_length = len(result) if result else 0
        word_count = len(result.split()) if result else 0
        line_count = len(result.split('\n')) if result else 0
        
        logger.info(f"Extraction completed: {text_length} characters, {word_count} words, {line_count} lines")
        
        # Log first and last parts for verification
        if result:
            preview_start = result[:200].replace('\n', ' ').strip()
            preview_end = result[-200:].replace('\n', ' ').strip()
            logger.info(f"Text preview - START: {preview_start}...")
            logger.info(f"Text preview - END: ...{preview_end}")
        else:
            logger.warning("WARNING: No text extracted from file!")
        
        # The UnstructuredService now returns a string directly, not a dictionary
        return result

    def create_parsing_prompt(self, resume_text: str) -> str:
        """
        Create a comprehensive prompt for parsing resume with expertise details
        """
        prompt = f"""
        Please analyze the following resume text and extract structured information in JSON format.

        Extract the following information:
        1. **Basic Information**: first_name, last_name, email, phone_number, location (country only)
        2. **Professional Details**: current_employer, years_of_experience, total_experience_months, availability, preferred_contract_type, preferred_work_arrangement
        3. **Online Presence**: linkedin_profile, website_portfolio
        4. **Personal**: date_of_birth (YYYY-MM-DD format), references, notes
        5. **Skills & Experience**: expertise_areas, sectors, skill_keywords
        6. **Qualifications**: languages_spoken, professional_certifications, professional_associations, publications
        7. **Expertise Details**: For each expertise area found, extract COMPREHENSIVE and DETAILED information about that expertise

        CRITICAL REQUIREMENTS:
        - For location, extract ONLY the country name (e.g., "United States", "Canada", "United Kingdom")
        - For years_of_experience, return as integer (e.g., 5, 10, 15)
        - For total_experience_months, calculate total experience in months (e.g., 60, 120, 180)
        - For expertise_areas, return as array of strings (e.g., ["Python", "Machine Learning", "Data Science"])
        - For expertise_details, extract COMPLETE and DETAILED information for each expertise area found

        EXPERTISE DETAILS FORMAT (EXTREMELY IMPORTANT):
        For each expertise area identified (like Python, JavaScript, Project Management, etc.), you MUST extract ALL information from the resume that could be related to this expertise, even if the connection is indirect.

        1. **Work Experience**: For each job where this expertise MIGHT have been used (based on job title, company, or responsibilities), include:
        ```
        [Time Period]: [Month/Year] to [Month/Year] (or Present)
        [Organization]: [Company Name]
        [Location]: [City, Country]
        [Role/Title]: [Job Title]
        [Responsibilities]:
        - [ALL responsibilities from this job]
        - [Another responsibility]
        ```

        2. **Projects**: For each project that MIGHT involve this expertise, include:
        ```
        [Project Name]: [Name of the project]
        [Time Period]: [Month/Year] to [Month/Year] (or Present)
        [Client/Organization]: [Client or Organization Name]
        [Description]:
        - [COMPLETE project description]
        - [ALL roles and contributions]
        ```

        3. **Other Related Information**: Include ALL other relevant information that demonstrates this expertise:
        ```
        Skills Mentioned: [List all specific skills, tools, technologies mentioned related to this expertise]
        Certifications: [Any certifications related to this expertise area]
        Education/Training: [Relevant educational background, courses, training programs]
        Tools & Software: [Specific tools, software, frameworks, platforms used]
        Achievements: [Awards, recognitions, accomplishments in this expertise area]
        Publications: [Papers, articles, blogs related to this expertise]
        Professional Associations: [Memberships in professional organizations related to this expertise]
        Languages: [Programming languages, spoken languages if relevant to this expertise]
        ```

        EXTREMELY IMPORTANT INSTRUCTIONS FOR EXPERTISE DETAILS:
        - You MUST extract ALL work experiences and projects that could be related to each expertise area
        - DO NOT combine or summarize multiple experiences into one - list each experience separately
        - DO NOT skip any experience or project that might be relevant
        - DO NOT return "No information found" unless absolutely nothing in the resume could relate to the expertise
        - Make reasonable inferences about which experiences might involve each expertise area
        - For technical skills (programming languages, tools, etc.), include ALL software development experience
        - For soft skills or management expertise, include ALL relevant professional experiences
        - Include ALL job experiences that might have used the expertise, even if not explicitly mentioned
        - If specific details are missing, use placeholders like "Time Period: Not specified" rather than omitting the experience
        - Be comprehensive and inclusive rather than restrictive when determining relevance
        - NEVER combine multiple experiences into one entry - each experience should be its own separate entry
        - ALWAYS separate different experiences with a blank line

        Return ONLY valid JSON in this exact format:
        {{
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@email.com",
            "phone_number": "+1234567890",
            "location": "United States",
            "current_employer": "Company Name",
            "years_of_experience": 5,
            "total_experience_months": 60,
            "availability": "Available",
            "preferred_contract_type": "Full-time",
            "preferred_work_arrangement": "Remote",
            "linkedin_profile": "https://linkedin.com/in/johndoe",
            "website_portfolio": "https://johndoe.com",
            "date_of_birth": "1990-01-01",
            "references": "Available upon request",
            "notes": "Additional notes",
            "expertise_areas": ["Python", "Machine Learning"],
            "sectors": ["Technology", "Healthcare"],
            "skill_keywords": ["Python", "TensorFlow", "AWS"],
            "languages_spoken": ["English", "Spanish"],
            "professional_certifications": ["AWS Certified", "PMP"],
            "professional_associations": ["IEEE", "ACM"],
            "publications": ["Paper 1", "Paper 2"],
            "expertise_details": {{
                "Python": {{
                    "work_experience": "Time Period: Jan 2020 to Present\\nOrganization: Tech Company\\nLocation: New York, USA\\nRole/Title: Software Engineer\\nResponsibilities:\\n- Developed backend services using Python and Django\\n- Implemented data processing pipelines\\n- Created REST APIs for mobile applications\\n\\nTime Period: Mar 2018 to Dec 2019\\nOrganization: Another Company\\nLocation: San Francisco, USA\\nRole/Title: Python Developer\\nResponsibilities:\\n- Built data analysis tools using Python\\n- Developed machine learning models\\n- Created automated testing frameworks",
                    "projects": "Project Name: Data Analysis Tool\\nTime Period: Mar 2019 to Dec 2019\\nClient/Organization: Internal Project\\nDescription:\\n- Built a data analysis tool using Python, Pandas and Matplotlib\\n- Implemented machine learning algorithms for predictive analytics\\n- Created user-friendly interface for non-technical users\\n\\nProject Name: Automation Framework\\nTime Period: Jan 2018 to Feb 2019\\nClient/Organization: Client XYZ\\nDescription:\\n- Developed automated testing framework using Python and Selenium\\n- Reduced testing time by 60%\\n- Integrated with CI/CD pipeline",
                    "other_related_info": "Skills Mentioned: Python, Django, Flask, Pandas, NumPy, Matplotlib, Scikit-learn, TensorFlow\\nCertifications: Python Institute PCAP Certification, AWS Certified Developer\\nEducation/Training: Bachelor's in Computer Science, Python Programming Course from Coursera\\nTools & Software: PyCharm, VS Code, Jupyter Notebook, Git, Docker\\nAchievements: Led Python migration project, Improved system performance by 40%\\nPublications: 'Python Best Practices' article in Tech Journal\\nProfessional Associations: Python Software Foundation Member\\nLanguages: Python (Expert), SQL (Advanced)"
                }}
            }}
        }}
        
        Resume text to analyze:
        {resume_text}
        """
        return prompt

    def parse_with_openai(self, resume_text: str) -> Dict[str, Any]:
        """
        Use OpenAI GPT to parse resume text into structured data
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Check if resume text is too large and truncate if necessary
        max_resume_length = 1000000  # Characters
        if len(resume_text) > max_resume_length:
            logger.warning(
                f"Resume text too large ({len(resume_text)} chars). Truncating to {max_resume_length} chars.")
            resume_text = resume_text[:max_resume_length] + "\n\n[Text truncated for processing]"

        # First, get basic parsing
        prompt = self.create_parsing_prompt(resume_text)

        # Make API call to OpenAI
        response = self.openai_client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": "You are a specialized resume parser that extracts detailed and comprehensive information into structured JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Lower temperature for more consistent output
            max_tokens=200000,  # Increased tokens to handle larger resumes
            response_format={"type": "json_object"}
        )

        # Check if response is None or has no content
        if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
            logger.error("OpenAI API returned an invalid response")
            raise ValueError("No valid response from AI service")

        # Extract the content from the response
        response_content = response.choices[0].message.content
        if not response_content or not response_content.strip():
            logger.error("OpenAI API returned empty response content")
            raise ValueError("Empty response content from AI service")

        response_text = response_content.strip()

        # Final check for empty response after cleaning
        if not response_text:
            logger.error("Response became empty after cleaning")
            raise ValueError("Invalid response format from AI service")

        # Try to parse JSON response with better error handling
        try:
            parsed_data = json.loads(response_text)
        except json.JSONDecodeError as json_error:
            logger.error(
                f"JSON decode error: {str(json_error)}, Response: {response_text[:500]}")

            # Try to fix common JSON issues
            if "Unterminated string" in str(json_error):
                # Try to fix by adding closing quotes and braces
                fixed_text = self._attempt_json_repair(response_text)
                if fixed_text:
                    try:
                        parsed_data = json.loads(fixed_text)
                        logger.info("Successfully repaired JSON response")
                    except json.JSONDecodeError:
                        # If repair failed, raise the original error
                        logger.error("Failed to repair JSON response")
                        raise json_error
                else:
                    # If repair failed, raise the original error
                    raise json_error
            else:
                # For other JSON errors, raise the original error
                raise json_error

        # Validate and clean the data
        cleaned_data = self.validate_and_clean_data(parsed_data)

        return cleaned_data

    def _attempt_json_repair(self, broken_json: str) -> str:
        """
        Attempt to repair common JSON issues
        """
        try:
            # Check if we have an opening brace
            if not broken_json.strip().startswith('{'):
                return None

            # Count opening and closing braces
            open_braces = broken_json.count('{')
            close_braces = broken_json.count('}')

            # Add missing closing braces
            if open_braces > close_braces:
                broken_json += '}' * (open_braces - close_braces)

            # Check for unclosed quotes by finding keys with no values
            import re
            # Find patterns like "key": with no value
            unclosed_keys = re.findall(r'"([^"]+)":\s*$', broken_json)
            if unclosed_keys:
                # For each unclosed key, add a placeholder value
                for key in unclosed_keys:
                    broken_json = broken_json.replace(
                        f'"{key}":',
                        f'"{key}": ""'
                    )

            return broken_json
        except Exception as e:
            logger.error(f"Error attempting to repair JSON: {str(e)}")
            return None

    def parse_with_gemini(self, resume_text: str) -> Dict[str, Any]:
        """
        Use Google Gemini to parse resume text into structured data
        """
        if not self.gemini_service:
            raise ValueError("Gemini service not initialized")
        
        # Create parsing prompt
        prompt = self.create_parsing_prompt(resume_text)
        
        # Parse with Gemini
        parsed_data = self.gemini_service.parse_with_gemini(resume_text, prompt)
        
        # Validate and clean the data
        cleaned_data = self.validate_and_clean_data(parsed_data)
        
        return cleaned_data

    def parse_with_ai(self, resume_text: str, preferred_provider: str = None) -> Dict[str, Any]:
        """
        Parse resume with specified AI provider or fallback to alternative
        """
        provider = preferred_provider or self.ai_provider
        
        if provider == 'openai':
            try:
                return self.parse_with_openai(resume_text)
            except Exception as e:
                logger.error(f"OpenAI parsing failed: {str(e)}")
                # Try Gemini as fallback if both are available
                if self.ai_provider == 'both' and self.gemini_service:
                    logger.info("Attempting to parse with Gemini as fallback")
                    return self.parse_with_gemini(resume_text)
                raise e
        
        elif provider == 'gemini':
            try:
                return self.parse_with_gemini(resume_text)
            except Exception as e:
                logger.error(f"Gemini parsing failed: {str(e)}")
                # Try OpenAI as fallback if both are available
                if self.ai_provider == 'both' and self.openai_client:
                    logger.info("Attempting to parse with OpenAI as fallback")
                    return self.parse_with_openai(resume_text)
                raise e
        
        elif provider == 'both':
            # Try both and return the first successful result
            for ai_provider in ['openai', 'gemini']:
                try:
                    if ai_provider == 'openai' and self.openai_client:
                        return self.parse_with_openai(resume_text)
                    elif ai_provider == 'gemini' and self.gemini_service:
                        return self.parse_with_gemini(resume_text)
                except Exception as e:
                    logger.error(f"{ai_provider} parsing failed: {str(e)}")
                    continue
            
            # If both failed, raise the last error
            raise ValueError("Both OpenAI and Gemini parsing failed")
        
        else:
            raise ValueError(f"Unknown AI provider: {provider}")

    # Removed unused methods: needs_expertise_reanalysis and analyze_expertise_experience
    # These were making additional API calls that are no longer needed since the main parsing prompt is comprehensive

    def create_fallback_response(self) -> Dict[str, Any]:
        """
        Create a minimal fallback response when AI parsing fails
        """
        return {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'location': '',
            'date_of_birth': None,
            'current_employer': '',
            'years_of_experience': None,
            'total_experience_months': None,
            'availability': '',
            'preferred_contract_type': '',
            'preferred_work_arrangement': '',
            'expertise_areas': [],
            'expertise_details': {},
            'sectors': [],
            'skill_keywords': [],
            'linkedin_profile': '',
            'website_portfolio': '',
            'languages_spoken': [],
            'references': '',
            'notes': 'AI parsing failed - manual review required',
            'professional_certifications': [],
            'professional_associations': [],
            'publications': []
        }

    def extract_country_only(self, location_string: str) -> str:
        """
        Extract only the country name from a location string that might contain city/state
        """
        if not location_string or not location_string.strip():
            return ""

        location = location_string.strip()

        # Common patterns for extracting country from location strings
        # Handle cases like "City, Country" or "City, State, Country"

        # Split by comma and take the last part (usually country)
        parts = [part.strip() for part in location.split(',')]
        if len(parts) > 1:
            # Last part is likely the country
            potential_country = parts[-1]

            # Common country name mappings
            country_mappings = {
                'USA': 'United States',
                'US': 'United States',
                'UK': 'United Kingdom',
                'UAE': 'United Arab Emirates',
                'BD': 'Bangladesh',
                'IN': 'India',
                'CA': 'Canada',
                'AU': 'Australia',
                'DE': 'Germany',
                'FR': 'France',
                'JP': 'Japan',
                'CN': 'China',
                'SG': 'Singapore',
                'MY': 'Malaysia',
                'TH': 'Thailand',
                'PH': 'Philippines',
                'ID': 'Indonesia',
                'VN': 'Vietnam',
                'KR': 'South Korea',
                'TW': 'Taiwan',
                'HK': 'Hong Kong',
                'NZ': 'New Zealand'
            }

            # Check if it's a country code and expand it
            if potential_country.upper() in country_mappings:
                return country_mappings[potential_country.upper()]

            # List of common country names to validate
            common_countries = {
                'bangladesh', 'india', 'pakistan', 'nepal', 'sri lanka',
                'united states', 'canada', 'mexico', 'brazil', 'argentina',
                'united kingdom', 'germany', 'france', 'italy', 'spain', 'netherlands',
                'china', 'japan', 'south korea', 'singapore', 'malaysia', 'thailand',
                'australia', 'new zealand', 'south africa', 'nigeria', 'egypt',
                'russia', 'ukraine', 'poland', 'sweden', 'norway', 'denmark'
            }

            # Check if the last part looks like a country
            if potential_country.lower() in common_countries:
                return potential_country.title()

            # Return the last part as country (best guess)
            return potential_country

        # If no comma, check if the whole string is a country
        if location.lower() in {
            'bangladesh', 'india', 'pakistan', 'nepal', 'sri lanka',
            'united states', 'usa', 'canada', 'mexico', 'brazil', 'argentina',
            'united kingdom', 'uk', 'germany', 'france', 'italy', 'spain',
            'china', 'japan', 'south korea', 'singapore', 'malaysia', 'thailand',
            'australia', 'new zealand', 'south africa', 'nigeria', 'egypt'
        }:
            # Map common abbreviations
            if location.lower() in ['usa', 'us']:
                return 'United States'
            elif location.lower() in ['uk']:
                return 'United Kingdom'
            else:
                return location.title()

        # If we can't determine the country, return the original string
        # (it might already be just a country name)
        return location

    def normalize_url(self, url: str) -> str:
        """
        Normalize URL by ensuring it has a proper protocol
        """
        if not url or not url.strip():
            return ''

        clean_url = url.strip()

        # Check if URL already has a protocol
        if clean_url.startswith('http://') or clean_url.startswith('https://'):
            return clean_url

        # Check if it starts with '//' (protocol-relative URL)
        if clean_url.startswith('//'):
            return f'https:{clean_url}'

        # For URLs without protocol, add https://
        return f'https://{clean_url}'

    def split_expertise_areas(self, expertise_list: list) -> list:
        """
        Split expertise areas that contain multiple topics separated by common delimiters
        """
        if not expertise_list:
            return []

        # Common separators for expertise areas
        separators = [
            ' and ',
            ' & ',
            ' / ',
            '/',
            ' | ',
            ' + ',
            ', ',
            ';'
        ]

        split_areas = []

        for item in expertise_list:
            if not isinstance(item, str) or not item.strip():
                continue

            current_item = item.strip()

            # Check if the item contains any separators
            found_separator = False
            for separator in separators:
                if separator in current_item:
                    # Split on this separator
                    parts = current_item.split(separator)
                    for part in parts:
                        cleaned_part = part.strip()
                        if cleaned_part and cleaned_part not in split_areas:
                            split_areas.append(cleaned_part)
                    found_separator = True
                    break

            # If no separator found, add the item as-is
            if not found_separator and current_item not in split_areas:
                split_areas.append(current_item)

        return split_areas

    def validate_and_clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean the parsed data
        """
        # Safety check - if data is None, return fallback response
        if data is None:
            logger.error("Received None data for validation")
            return self.create_fallback_response()
        
        cleaned_data = {}

        # String fields
        string_fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'location',
            'current_employer', 'availability', 'preferred_contract_type',
            'preferred_work_arrangement', 'linkedin_profile', 'website_portfolio',
            'references', 'notes'
        ]

        for field in string_fields:
            value = data.get(field)
            if value and isinstance(value, str) and value.strip():
                # Special handling for location to extract only country name
                if field == 'location':
                    cleaned_data[field] = self.extract_country_only(
                        value.strip())
                # Special handling for URL fields to normalize them
                elif field in ['linkedin_profile', 'website_portfolio']:
                    cleaned_data[field] = self.normalize_url(value.strip())
                else:
                    cleaned_data[field] = value.strip()
            else:
                cleaned_data[field] = ''

        # Date of birth field
        dob = data.get('date_of_birth')
        if dob and isinstance(dob, str) and dob.strip():
            # Basic validation for date format (YYYY-MM-DD)
            try:
                from datetime import datetime
                datetime.strptime(dob.strip(), '%Y-%m-%d')
                cleaned_data['date_of_birth'] = dob.strip()
            except ValueError:
                cleaned_data['date_of_birth'] = None
        else:
            cleaned_data['date_of_birth'] = None

        # Integer fields
        years_exp = data.get('years_of_experience')
        if isinstance(years_exp, (int, float)) and years_exp >= 0:
            cleaned_data['years_of_experience'] = int(years_exp)
        else:
            cleaned_data['years_of_experience'] = None

        # Total experience in months
        months_exp = data.get('total_experience_months')
        if isinstance(months_exp, (int, float)) and months_exp >= 0:
            cleaned_data['total_experience_months'] = int(months_exp)
        else:
            cleaned_data['total_experience_months'] = None

        # Handle expertise_areas separately with splitting logic
        expertise_areas = data.get('expertise_areas', [])
        if isinstance(expertise_areas, list):
            # Clean and filter empty strings first
            cleaned_expertise = [item.strip() for item in expertise_areas if isinstance(
                item, str) and item and item.strip()]
            # Apply splitting logic to separate combined expertise areas
            cleaned_data['expertise_areas'] = self.split_expertise_areas(
                cleaned_expertise)
        else:
            cleaned_data['expertise_areas'] = []

        # Other array fields (without splitting)
        other_array_fields = [
            'sectors', 'skill_keywords',
            'professional_certifications', 'professional_associations', 'publications'
        ]

        for field in other_array_fields:
            value = data.get(field, [])
            if isinstance(value, list):
                # Clean and filter empty strings
                cleaned_data[field] = [item.strip() for item in value if isinstance(
                    item, str) and item and item.strip()]
            else:
                cleaned_data[field] = []

        # Languages field (more complex structure)
        languages = data.get('languages_spoken', [])
        if isinstance(languages, list):
            cleaned_languages = []
            for lang in languages:
                if isinstance(lang, dict) and 'language' in lang:
                    language_name = lang.get('language', '')
                    proficiency = lang.get('proficiency', '')
                    cleaned_lang = {
                        'language': language_name.strip() if language_name else '',
                        'proficiency': proficiency.strip() if proficiency else '',
                        'mother_tongue': bool(lang.get('mother_tongue', False))
                    }
                    if cleaned_lang['language']:
                        cleaned_languages.append(cleaned_lang)
            cleaned_data['languages_spoken'] = cleaned_languages
        else:
            cleaned_data['languages_spoken'] = []

        # --- NEW: Normalize and propagate expertise_details ---
        expertise_details = data.get('expertise_details', {})
        if isinstance(expertise_details, dict):
            propagated_details = {}
            for area_key, details_val in expertise_details.items():
                # Ensure we have a dictionary for details (skip if not)
                if not details_val:
                    details_val = {}
                # Split the key in case it contains combined areas like "Python / Django"
                split_keys = self.split_expertise_areas([area_key])
                # If splitting returned nothing, use the original key
                if not split_keys:
                    split_keys = [area_key]
                for single_key in split_keys:
                    # If the same area already exists, try to merge missing fields
                    if single_key in propagated_details and isinstance(propagated_details[single_key], dict) and isinstance(details_val, dict):
                        for k, v in details_val.items():
                            # Fill only empty or missing fields to avoid overwriting richer data
                            if k not in propagated_details[single_key] or not propagated_details[single_key][k]:
                                propagated_details[single_key][k] = v
                    else:
                        propagated_details[single_key] = details_val
            # Ensure every expertise_area has at least an empty dict
            for ea in cleaned_data.get('expertise_areas', []):
                if ea not in propagated_details:
                    propagated_details[ea] = {}
            cleaned_data['expertise_details'] = propagated_details
        # --- END NEW ---

        return cleaned_data

    def check_extraction_quality(self, extracted_text: str, file_path: str) -> Dict[str, Any]:
        """
        Analyze the quality of text extraction and provide diagnostics
        """
        quality_report = {
            'file_path': file_path,
            'extraction_successful': True,
            'issues': [],
            'stats': {},
            'quality_score': 0
        }
        
        if not extracted_text or not extracted_text.strip():
            quality_report['extraction_successful'] = False
            quality_report['issues'].append('No text extracted from file')
            quality_report['quality_score'] = 0
            return quality_report
        
        # Calculate basic stats
        text_length = len(extracted_text)
        word_count = len(extracted_text.split())
        line_count = len(extracted_text.split('\n'))
        
        quality_report['stats'] = {
            'characters': text_length,
            'words': word_count,
            'lines': line_count,
            'avg_words_per_line': round(word_count / max(line_count, 1), 2)
        }
        
        # Quality checks
        quality_score = 100
        
        # Check minimum length
        if text_length < 100:
            quality_report['issues'].append('Text too short (< 100 characters)')
            quality_score -= 30
        elif text_length < 500:
            quality_report['issues'].append('Text may be incomplete (< 500 characters)')
            quality_score -= 15
        
        # Check for typical resume content
        resume_indicators = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'[\+\d\-\(\)\s]{8,}',
            'experience_keywords': ['experience', 'work', 'employment', 'job', 'position', 'role'],
            'education_keywords': ['education', 'degree', 'university', 'college', 'school', 'bachelor', 'master'],
            'skills_keywords': ['skill', 'technical', 'programming', 'software', 'tool', 'technology']
        }
        
        import re
        text_lower = extracted_text.lower()
        
        # Check for email
        if re.search(resume_indicators['email'], extracted_text):
            quality_report['stats']['has_email'] = True
        else:
            quality_report['issues'].append('No email address found')
            quality_score -= 10
        
        # Check for phone
        if re.search(resume_indicators['phone'], extracted_text):
            quality_report['stats']['has_phone'] = True
        else:
            quality_report['issues'].append('No phone number found')
            quality_score -= 5
        
        # Check for resume sections
        sections_found = 0
        for section_type, keywords in [
            ('experience', resume_indicators['experience_keywords']),
            ('education', resume_indicators['education_keywords']),
            ('skills', resume_indicators['skills_keywords'])
        ]:
            if any(keyword in text_lower for keyword in keywords):
                quality_report['stats'][f'has_{section_type}_section'] = True
                sections_found += 1
            else:
                quality_report['issues'].append(f'No {section_type} section indicators found')
        
        if sections_found == 0:
            quality_score -= 25
        elif sections_found < 2:
            quality_score -= 10
        
        # Check for proper capitalization (indicates good extraction)
        upper_count = sum(1 for c in extracted_text if c.isupper())
        upper_ratio = upper_count / text_length if text_length > 0 else 0
        
        if upper_ratio < 0.01:  # Less than 1% uppercase
            quality_report['issues'].append('Very low capitalization - may indicate OCR/extraction issues')
            quality_score -= 15
        elif upper_ratio > 0.5:  # More than 50% uppercase
            quality_report['issues'].append('Too much capitalization - may indicate formatting issues')
            quality_score -= 10
        
        # Check for excessive repeated characters (extraction artifacts)
        repeated_patterns = re.findall(r'(.)\1{5,}', extracted_text)
        if repeated_patterns:
            quality_report['issues'].append(f'Found repeated character patterns: {repeated_patterns[:3]}')
            quality_score -= 5
        
        # Check for common extraction artifacts
        artifacts = ['||||', '____', '===', '---', '...........']
        found_artifacts = [art for art in artifacts if art in extracted_text]
        if found_artifacts:
            quality_report['issues'].append(f'Found potential extraction artifacts: {found_artifacts}')
            quality_score -= 5
        
        quality_report['quality_score'] = max(0, quality_score)
        
        # Overall assessment
        if quality_score >= 80:
            quality_report['assessment'] = 'Excellent extraction'
        elif quality_score >= 60:
            quality_report['assessment'] = 'Good extraction'
        elif quality_score >= 40:
            quality_report['assessment'] = 'Fair extraction - may need review'
        else:
            quality_report['assessment'] = 'Poor extraction - needs attention'
        
        return quality_report

    def validate_expertise_experience(self, expertise_exp: dict, total_years: int) -> dict:
        """
        Validate and adjust expertise experience to ensure realistic values
        """
        if not expertise_exp or not total_years:
            return expertise_exp

        validated_exp = {}

        for area, experience_str in expertise_exp.items():
            # Extract numeric value from experience string
            experience_years = self.extract_years_from_string(experience_str)

            # If experience is unrealistic (e.g., same as total for all areas),
            # we'll keep it but flag for manual review
            if experience_years and experience_years <= total_years + 2:  # Allow some flexibility
                validated_exp[area] = experience_str
            elif experience_years:
                # Cap at total experience if it's way too high
                validated_exp[area] = f"{min(experience_years, total_years)} years"
            else:
                # Keep original string if we can't parse it
                validated_exp[area] = experience_str

        return validated_exp

    def extract_years_from_string(self, experience_str: str) -> float:
        """
        Extract years from experience string like "3 years", "2.5 years", "18 months"
        """
        import re

        if not experience_str:
            return 0

        # Look for patterns like "3 years", "2.5 years", "18 months"
        years_match = re.search(
            r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)', experience_str.lower())
        if years_match:
            return float(years_match.group(1))

        months_match = re.search(
            r'(\d+(?:\.\d+)?)\s*(?:months?|mos?)', experience_str.lower())
        if months_match:
            return float(months_match.group(1)) / 12

        # Try to extract just a number
        number_match = re.search(r'(\d+(?:\.\d+)?)', experience_str)
        if number_match:
            return float(number_match.group(1))

        return 0

    def parse_resume(self, file_path: str, preferred_provider: str = None) -> Dict[str, Any]:
        """
        Main method to parse resume and return structured data
        """
        logger.info(f"Starting to parse resume: {file_path}")

        # Extract text from file
        resume_text = self.extract_text(file_path)

        if not resume_text or not resume_text.strip():
            logger.error(f"No text could be extracted from {file_path}")
            raise ValueError("No text could be extracted from the resume file")

        logger.info(f"Extracted {len(resume_text)} characters from resume")
        
        # Parse with AI - this will handle provider selection and fallback
        try:
            parsed_data = self.parse_with_ai(resume_text, preferred_provider)
        except Exception as e:
            logger.error(f"AI parsing failed: {str(e)}")
            # Return fallback response if AI fails
            return self.create_fallback_response()

        # Check if we got an incomplete response
        if not parsed_data.get('expertise_areas') and not parsed_data.get('skill_keywords'):
            logger.warning(f"Received incomplete response for {file_path}")
            # We'll continue with validation, but log the warning
        else:
            logger.info("Successfully parsed resume with AI")

        # Validate and clean data
        cleaned_data = self.validate_and_clean_data(parsed_data)

        # Ensure expertise_details exists in cleaned_data
        if 'expertise_details' not in cleaned_data:
            cleaned_data['expertise_details'] = {}

        logger.info(f"Successfully completed parsing resume: {file_path}")
        return cleaned_data

    def format_expertise_details_for_display(self, expertise_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format expertise details into a user-friendly structure for display
        """
        formatted_details = {}
        
        for expertise_area, details in expertise_details.items():
            formatted_area = {
                'expertise_name': expertise_area,
                'work_experiences': [],
                'projects': [],
                'other_info': {}
            }
            
            # Parse work experience
            work_exp_text = details.get('work_experience', '')
            if work_exp_text:
                formatted_area['work_experiences'] = self._parse_work_experience_text(work_exp_text)
            
            # Parse projects
            projects_text = details.get('projects', '')
            if projects_text:
                formatted_area['projects'] = self._parse_projects_text(projects_text)
            
            # Parse other related info
            other_info_text = details.get('other_related_info', '')
            if other_info_text:
                formatted_area['other_info'] = self._parse_other_info_text(other_info_text)
            
            formatted_details[expertise_area] = formatted_area
        
        return formatted_details

    def _parse_work_experience_text(self, work_exp_text: str) -> list:
        """
        Parse work experience text into structured format
        """
        experiences = []
        
        # Split by double newlines to separate different experiences
        exp_blocks = work_exp_text.split('\n\n')
        
        for block in exp_blocks:
            if not block.strip():
                continue
                
            exp_data = {
                'time_period': '',
                'organization': '',
                'location': '',
                'role_title': '',
                'responsibilities': []
            }
            
            lines = block.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('Time Period:'):
                    exp_data['time_period'] = line.replace('Time Period:', '').strip()
                elif line.startswith('Organization:'):
                    exp_data['organization'] = line.replace('Organization:', '').strip()
                elif line.startswith('Location:'):
                    exp_data['location'] = line.replace('Location:', '').strip()
                elif line.startswith('Role/Title:'):
                    exp_data['role_title'] = line.replace('Role/Title:', '').strip()
                elif line.startswith('Responsibilities:'):
                    current_section = 'responsibilities'
                elif line.startswith('- ') and current_section == 'responsibilities':
                    exp_data['responsibilities'].append(line[2:].strip())
            
            if exp_data['time_period'] or exp_data['organization'] or exp_data['role_title']:
                experiences.append(exp_data)
        
        return experiences

    def _parse_projects_text(self, projects_text: str) -> list:
        """
        Parse projects text into structured format
        """
        projects = []
        
        # Split by double newlines to separate different projects
        project_blocks = projects_text.split('\n\n')
        
        for block in project_blocks:
            if not block.strip():
                continue
                
            project_data = {
                'project_name': '',
                'time_period': '',
                'client_organization': '',
                'description': []
            }
            
            lines = block.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('Project Name:'):
                    project_data['project_name'] = line.replace('Project Name:', '').strip()
                elif line.startswith('Time Period:'):
                    project_data['time_period'] = line.replace('Time Period:', '').strip()
                elif line.startswith('Client/Organization:'):
                    project_data['client_organization'] = line.replace('Client/Organization:', '').strip()
                elif line.startswith('Description:'):
                    current_section = 'description'
                elif line.startswith('- ') and current_section == 'description':
                    project_data['description'].append(line[2:].strip())
            
            if project_data['project_name'] or project_data['time_period']:
                projects.append(project_data)
        
        return projects

    def _parse_other_info_text(self, other_info_text: str) -> dict:
        """
        Parse other related info text into structured format
        """
        other_info = {
            'skills_mentioned': [],
            'certifications': [],
            'education_training': [],
            'tools_software': [],
            'achievements': [],
            'publications': [],
            'professional_associations': [],
            'languages': []
        }
        
        lines = other_info_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('Skills Mentioned:'):
                skills_text = line.replace('Skills Mentioned:', '').strip()
                if skills_text:
                    other_info['skills_mentioned'] = [skill.strip() for skill in skills_text.split(',')]
            
            elif line.startswith('Certifications:'):
                cert_text = line.replace('Certifications:', '').strip()
                if cert_text:
                    other_info['certifications'] = [cert.strip() for cert in cert_text.split(',')]
            
            elif line.startswith('Education/Training:'):
                edu_text = line.replace('Education/Training:', '').strip()
                if edu_text:
                    other_info['education_training'] = [edu.strip() for edu in edu_text.split(',')]
            
            elif line.startswith('Tools & Software:'):
                tools_text = line.replace('Tools & Software:', '').strip()
                if tools_text:
                    other_info['tools_software'] = [tool.strip() for tool in tools_text.split(',')]
            
            elif line.startswith('Achievements:'):
                achieve_text = line.replace('Achievements:', '').strip()
                if achieve_text:
                    other_info['achievements'] = [achieve.strip() for achieve in achieve_text.split(',')]
            
            elif line.startswith('Publications:'):
                pub_text = line.replace('Publications:', '').strip()
                if pub_text:
                    other_info['publications'] = [pub.strip() for pub in pub_text.split(',')]
            
            elif line.startswith('Professional Associations:'):
                assoc_text = line.replace('Professional Associations:', '').strip()
                if assoc_text:
                    other_info['professional_associations'] = [assoc.strip() for assoc in assoc_text.split(',')]
            
            elif line.startswith('Languages:'):
                lang_text = line.replace('Languages:', '').strip()
                if lang_text:
                    other_info['languages'] = [lang.strip() for lang in lang_text.split(',')]
        
        return other_info

    # Removed redundant methods:
    # - _enrich_expertise_details
    # - _extract_expertise_details_from_text
    # - extract_expertise_details
    # - _create_empty_expertise_response

    # Removed unused method: extract_all_expertise_details
    # This method is no longer needed since expertise details are extracted in the main parsing prompt
 