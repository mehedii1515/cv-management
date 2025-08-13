import os
import sys
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reparse_resume(resume_id):
    """
    Reparse a specific resume to update its expertise details
    """
    try:
        # Set up API endpoint
        base_url = "http://localhost:8000"  # Change if your server is on a different port
        endpoint = f"{base_url}/api/resumes/{resume_id}/reparse/"
        
        logger.info(f"Reparsing resume ID: {resume_id}")
        
        # Make API request
        response = requests.post(endpoint)
        
        # Check response
        if response.status_code == 200:
            logger.info("Resume reparsed successfully")
            result = response.json()
            
            # Save result to file for inspection
            with open('reparse_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
                
            logger.info(f"Result saved to reparse_result.json")
            
            # Check expertise details
            if 'data' in result and 'expertise_details' in result['data']:
                expertise_details = result['data']['expertise_details']
                logger.info(f"Found {len(expertise_details)} expertise areas")
                
                # Check if any expertise areas still have "No information found"
                no_info_count = 0
                for area, details in expertise_details.items():
                    if 'work_experience' in details and details['work_experience'] == "No information found":
                        no_info_count += 1
                        
                if no_info_count > 0:
                    logger.warning(f"{no_info_count} expertise areas still have 'No information found'")
                else:
                    logger.info("All expertise areas now have details!")
            
            return True
        else:
            logger.error(f"Failed to reparse resume. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error reparsing resume: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reparse_resume.py <resume_id>")
        sys.exit(1)
        
    resume_id = sys.argv[1]
    reparse_resume(resume_id) 