#%%
from serpapi import GoogleSearch
from utils.config import SERPAPI_KEY
import pandas as pd
from keywords import keywords_platforms_set, keywords_skills_set

def get_jobs():
    jobs = []

    ## Helper function to grab jobs one page at a time (10 results per page)
    def get_jobs_page(job_bucket, location, start):
        params = {
            'engine': 'google_jobs',
            'q': job_bucket,
            'location' : location,
            'gl': 'ca',
            'start': start,
            'api_key': SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for job in results['jobs_results']:
            # Extract posted_at and schedule_type, if available
            try:
                job['posted_at'] = job['detected_extensions']['posted_at']
            except:
                job['posted_at'] = None
            
            try:
                job['schedule_type'] = job['detected_extensions']['schedule_type']
            except:
                job['schedule_type'] = None
            
            # Extract keywords for skills & programming
            job_description_words = job['description'].split()

            job['keywords_platforms'] = set()
            job['keyword_skills'] = set()
            for word in job_description_words:
                word = word.replace(',', '')
                if word.lower() in keywords_platforms_set:
                    job['keywords_platforms'].add(word)
                if word.lower() in keywords_skills_set:
                    job['keyword_skills'].add(word)
            
            job['job_bucket'] = job_bucket
            
            jobs.append(job)

    # job_buckets = ['data analyst', 'data engineer', 'data scientist', 'data consultant', 'product manager', 'data architect']
    # locations = ['toronto', 'montreal', 'calgary', 'vancouver', 'halifax']

    job_buckets = ['data analyst']
    locations = ['toronto']
    start = 0
    
    for location in locations:
        for job_bucket in job_buckets:
            while True:
                try:
                    get_jobs_page(job_bucket, location, start)
                    start += 10
                except:
                    break
    
    ## Prepare job results
    df_jobs = pd.DataFrame(jobs)
    df_jobs.rename(
        columns={
            'title': 'job_title'
        },
        inplace=True
    )
    df_jobs['query_date'] = pd.to_datetime('today').date()

    ## Return final solution
    return df_jobs
# %%
