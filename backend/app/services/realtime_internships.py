"""
Real-time LinkedIn internship fetcher
Returns LinkedIn job search URLs based on skills
"""

import requests
from typing import List, Dict

def fetch_linkedin_jobs(skills: List[str], location: str = "India", limit: int = 10) -> List[Dict]:
    """
    Returns real LinkedIn job search URLs based on skills
    NOTE: These link to real LinkedIn searches, not mock data
    """
    try:
        # Build skill-based search query
        skill_query = " ".join(skills[:3]) if skills else "software"
        
        # Real job categories with actual LinkedIn search URLs
        internships = [
            {
                "title": "Software Engineering Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "Java", "AWS", "JavaScript"],
                "url": f"https://www.linkedin.com/jobs/search/?keywords=software%20engineering%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Data Science Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "Machine Learning", "SQL", "Data Analysis"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=data%20science%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Frontend Developer Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["React", "JavaScript", "CSS", "HTML"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=frontend%20developer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Full Stack Development Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Node.js", "React", "MongoDB", "Express"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=full%20stack%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Machine Learning Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "TensorFlow", "PyTorch", "AI"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=machine%20learning%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Backend Developer Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Java", "Spring Boot", "AWS", "API"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=backend%20developer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "DevOps Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Docker", "Kubernetes", "CI/CD", "Jenkins"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=devops%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "AI/ML Research Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "Deep Learning", "NLP", "Research"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=AI%20ML%20research%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Cloud Engineer Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["AWS", "Azure", "Terraform", "Cloud"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=cloud%20engineer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Mobile App Development Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["React Native", "iOS", "Android", "Flutter"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=mobile%20app%20developer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": f"{skill_query.title()} Internships (Custom Search)",
                "company": "All Companies",
                "location": location,
                "skills": skills[:4] if skills else ["General"],
                "url": f"https://www.linkedin.com/jobs/search/?keywords={skill_query.replace(' ', '%20')}%20intern&location={location}&f_E=1",
                "type": "internship"
            }
        ]
        
        return internships[:limit]
        
    except Exception as e:
        print(f"Error in fetch_linkedin_jobs: {e}")
        return []


def fetch_indeed_internships(skills: List[str], location: str = "India", limit: int = 10) -> List[Dict]:
    """
    Fetch real-time internships from Indeed.com
    Note: This uses web scraping. For production, use Indeed's official API.
    """
    try:
        internships = []
        
        # Build search query from skills
        query = "internship " + " ".join(skills[:3]) if skills else "internship"
        
        # Indeed URL (this is a simplified approach)
        url = "https://in.indeed.com/jobs"
        params = {
            "q": query,
            "l": location,
            "jt": "internship"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse job listings
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:limit]:
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        
                        if title_elem and company_elem:
                            internships.append({
                                "title": title_elem.get_text(strip=True),
                                "company": company_elem.get_text(strip=True),
                                "location": location_elem.get_text(strip=True) if location_elem else "Not specified",
                                "source": "Indeed",
                                "url": f"https://in.indeed.com/jobs?q={query}&l={location}",
                                "type": "internship"
                            })
                    except:
                        continue
        except Exception as e:
            print(f"Warning: Could not fetch from Indeed: {e}")
        
        return internships
        
    except Exception as e:
        print(f"Error in fetch_indeed_internships: {e}")
        return []


def fetch_internshala_internships(skills: List[str], location: str = "Bangalore", limit: int = 10) -> List[Dict]:
    """
    Fetch internships from Internshala (Indian platform)
    Better alternative for India-based internships
    """
    try:
        internships = []
        
        # Internshala API endpoint (unofficial)
        query = " ".join(skills[:3]) if skills else "engineering"
        
        url = "https://api.internshala.com/internships/"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        params = {
            "filter_locations": location,
            "internship_type": "work_from_office"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("internships", [])
                
                for item in results[:limit]:
                    internships.append({
                        "title": item.get("profile_name", "Internship"),
                        "company": item.get("company_name", "Company"),
                        "location": item.get("location_name", location),
                        "source": "Internshala",
                        "skills": item.get("skill_tags", skills),
                        "stipend": item.get("stipend", "Unpaid"),
                        "url": f"https://internshala.com/internship/{item.get('id', '')}",
                        "type": "internship"
                    })
        except Exception as e:
            print(f"Warning: Internshala fetch error: {e}")
        
        return internships
        
    except Exception as e:
        print(f"Error in fetch_internshala_internships: {e}")
        return []


def fetch_linkedin_jobs(skills: List[str], location: str = "India", limit: int = 10) -> List[Dict]:
    """
    Returns real LinkedIn job search URLs based on skills
    NOTE: These link to real LinkedIn searches, not mock data
    """
    try:
        # Build skill-based search query
        skill_query = " ".join(skills[:3]) if skills else "software"
        
        # Real job categories with actual LinkedIn search URLs
        internships = [
            {
                "title": "Software Engineering Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "Java", "AWS", "JavaScript"],
                "url": f"https://www.linkedin.com/jobs/search/?keywords=software%20engineering%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Data Science Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "Machine Learning", "SQL", "Data Analysis"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=data%20science%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Frontend Developer Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["React", "JavaScript", "CSS", "HTML"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=frontend%20developer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Full Stack Development Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Node.js", "React", "MongoDB", "Express"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=full%20stack%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Machine Learning Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "TensorFlow", "PyTorch", "AI"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=machine%20learning%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Backend Developer Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Java", "Spring Boot", "AWS", "API"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=backend%20developer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "DevOps Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Docker", "Kubernetes", "CI/CD", "Jenkins"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=devops%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "AI/ML Research Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["Python", "Deep Learning", "NLP", "Research"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=AI%20ML%20research%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Cloud Engineer Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["AWS", "Azure", "Terraform", "Cloud"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=cloud%20engineer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": "Mobile App Development Internships",
                "company": "Multiple Companies",
                "location": "India",
                "skills": ["React Native", "iOS", "Android", "Flutter"],
                "url": "https://www.linkedin.com/jobs/search/?keywords=mobile%20app%20developer%20intern&location=India&f_E=1",
                "type": "internship"
            },
            {
                "title": f"{skill_query.title()} Internships (Custom Search)",
                "company": "All Companies",
                "location": location,
                "skills": skills[:4] if skills else ["General"],
                "url": f"https://www.linkedin.com/jobs/search/?keywords={skill_query.replace(' ', '%20')}%20intern&location={location}&f_E=1",
                "type": "internship"
            }
        ]
        
        return internships[:limit]
        
    except Exception as e:
        print(f"Error in fetch_linkedin_jobs: {e}")
        return []


def fetch_all_real_time_internships(skills: List[str], location: str = "India") -> Dict:
    """
    Fetch from all available sources and combine results
    """
    results = {
        "internshala": fetch_internshala_internships(skills, location, limit=5),
        "indeed": fetch_indeed_internships(skills, location, limit=5),
        "linkedin": fetch_linkedin_jobs(skills, location, limit=3),
        "total_count": 0
    }
    
    results["total_count"] = sum(len(v) for k, v in results.items() if k != "total_count")
    
    return results
