# Sectors OR Filter Feature Implementation

## Overview
Implemented OR logic for sectors filtering in the resume parser application. Users can now select multiple sectors and the system will return resumes that have ANY of the selected sectors, rather than requiring all of them.

## Problem Statement
Previously, when users selected multiple sectors in the filter, the system would only use the last selected value due to Django-filter's default behavior. This made it impossible to find resumes with experience in any of several different sectors.

## Solution
Modified the `filter_sectors` method in `ResumeFilter` to:
1. Capture all selected sector values from the request
2. Build an OR query using Django's Q objects
3. Return resumes that match ANY of the selected sectors

## Implementation Details

### Backend Changes
**File:** `backend/apps/resumes/views.py`

```python
def filter_sectors(self, queryset, name, value):
    """Filter by sectors with OR logic for multiple values"""
    if not value:
        return queryset
    
    # Get all sector values from the request
    sector_values = self.data.getlist('sectors')
    
    if not sector_values:
        return queryset
    
    # Build OR query for multiple sectors
    from django.db.models import Q
    sector_queries = Q()
    
    for sector in sector_values:
        if sector and sector.strip():
            # Filter resumes where the sectors JSON field contains the value
            sector_queries |= Q(sectors__icontains=f'"{sector.strip()}"')
    
    return queryset.filter(sector_queries) if sector_queries else queryset
```

### Key Features
1. **Multiple Selection Support**: Uses `getlist()` to capture all selected sectors
2. **OR Logic**: Uses Django Q objects with `|=` operator for OR queries
3. **JSON Field Filtering**: Searches within JSON array fields using `icontains`
4. **Empty Value Handling**: Gracefully handles empty or whitespace-only values
5. **Case Insensitive**: Matching is case insensitive

## Testing Results

### Test Cases
1. **Single Selection**: 
   - Technology: 9 results ✅
   - Education: 7 results ✅
   - Finance: 4 results ✅
   - Healthcare: 6 results ✅

2. **Multiple Selection (OR Logic)**:
   - Technology OR Education: 11 results ✅
   - Finance OR Healthcare: 7 results ✅
   - Technology OR Education OR Healthcare: 11 results ✅

3. **Edge Cases**:
   - Non-existent + valid sector: Returns only valid results ✅
   - Empty values: Handled gracefully ✅
   - Case insensitive matching: Works correctly ✅

### Database Statistics
Available sectors in the database:
- Technology: 9 resumes
- Education: 7 resumes
- Healthcare: 6 resumes
- Finance: 4 resumes
- International Development: 3 resumes
- Government: 2 resumes
- Research: 2 resumes
- Insurance: 2 resumes
- Non-profit: 1 resume
- Recruitment: 1 resume
- E-commerce: 1 resume
- Construction: 1 resume
- Legal: 1 resume
- Science: 1 resume
- (+10 more sectors with 1 resume each)

### Overlap Analysis
For Technology + Education test:
- Resumes with Technology: 9
- Resumes with Education: 7
- Resumes with BOTH: 5 (significant overlap)
- Unique total (OR logic): 11

This demonstrates the OR logic is working correctly - there's substantial overlap between Technology and Education sectors, which is common for technical roles in educational institutions.

## Usage
Users can now:
1. Select multiple sectors in the filter interface
2. Get results that match ANY of the selected sectors
3. Find candidates with experience across diverse industry sectors

## API Usage
```
GET /api/resumes/?sectors=Technology&sectors=Education&sectors=Healthcare
```

This will return resumes that have experience in any combination of "Technology", "Education", or "Healthcare" sectors.

## Benefits
- **Improved Search Flexibility**: Users can find candidates with experience in any of several relevant sectors
- **Better Cross-Industry Searches**: Ideal for roles that span multiple industries
- **Broader Results**: Helps find qualified candidates who might be missed with AND logic
- **Consistent Behavior**: Maintains consistent OR logic across all multi-select filters

## Real-World Use Cases
1. **Cross-Industry Recruitment**: Find candidates with experience in Technology, Finance, or Healthcare
2. **Diverse Sector Experience**: Search for consultants with experience across multiple sectors
3. **Industry Transitions**: Find candidates transitioning between related sectors
4. **Government/Non-profit**: Find candidates with experience in Government, Non-profit, or International Development

## Completion Status
With sectors OR logic implemented, the consistent OR filtering pattern is now complete:
- ✅ Location filtering (OR logic)
- ✅ Expertise areas filtering (OR logic)
- ✅ Skills filtering (OR logic)
- ✅ Sectors filtering (OR logic)
- 🔄 Experience levels (single-select by design)

## Impact on Cross-Filter Logic
The cross-filter logic now benefits from complete OR support:
- **Within Categories**: OR logic for all multi-select filters
- **Between Categories**: AND logic for combining different filter types
- **Example**: (Technology OR Education) AND (JavaScript OR Python) AND (Bangladesh OR Kenya)

This implementation completes the comprehensive OR filtering system across all multi-select filter categories in the application, providing users with maximum flexibility in candidate search and filtering. 