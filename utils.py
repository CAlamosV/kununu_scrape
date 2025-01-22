import os
import requests
from bs4 import BeautifulSoup
import re
import json

def soup_from_url(url: str, scrapingbee = True) -> BeautifulSoup:
    """
    Get BeautifulSoup object from a URL
    """
    if scrapingbee:
        response = requests.get(
            url='https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': os.getenv('SCRAPINGBEE_API_KEY'),
                'url':url,
                'render_js': 'false',
            })
    else:
        response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")

def get_all_links_from_div(url: str, div: str = "LinksLevel_container__cGmmL", url_init: str = "https://www.kununu.com/de/") -> list:
    """
    Get all links from a div in the HTML corresponding to a URL
    """
    soup = soup_from_url(url).find(class_ = div)
    return [url_init + x["href"] for x in soup.find_all('a', href=True)]

def camel_to_snake_case(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def convert_keys_to_snake_case(data: dict) -> dict:
    """Recursively convert all dictionary keys to snake_case."""
    if isinstance(data, dict):
        return {camel_to_snake_case(k): convert_keys_to_snake_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data

def replace_null_with_none(json_str):
    # Parse the JSON string into a Python object
    data = json.loads(json_str)
    
    # Replace null with None recursively
    def replace(data):
        if isinstance(data, dict):
            return {k: replace(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [replace(item) for item in data]
        elif data is None:
            return None
        else:
            return data
    
    return replace(data)

def flatten(data, parent_key=''):
    """Flatten a nested dictionary"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}_{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)

column_name_mapping = {
    'firm_name': 'firm_name',
    'url': 'kn_url',
    'uuid': 'uuid',
    'views_num': 'kn_views_num',
    'percent_recommend_overall': 'kn_employee_rec_score',
    'overall_rating': 'kn_overall',
    'total_reviews_num': 'kn_total_reviews_num',
    'salaries_posted_num': 'kn_salaries_posted_num',
    'gehaltsozialleistungen': 'kn_salary_benefits',
    'image': 'kn_image',
    'karriereweiterbildung': 'kn_career_development',
    'arbeitsatmosphare': 'kn_work_atmosphere',
    'kommunikation': 'kn_communication',
    'kollegenzusammenhalt': 'kn_colleague_cohesion',
    'work_life_balance': 'kn_work_life_balance',
    'vorgesetztenverhalten': 'kn_superiors_behavior',
    'interessante_aufgaben': 'kn_interesting_tasks',
    'arbeitsbedingungen': 'kn_working_conditions',
    'umwelt_sozialbewusstsein': 'kn_environment_social_awareness',
    'gleichberechtigung': 'kn_equal_rights',
    'umgang_mit_alteren_kollegen': 'kn_dealing_with_older_colleagues',
    'all_applicants_review_num': 'kn_all_applicants_review_num',
    'all_applicants_review_score': 'kn_all_applicants_review_score',
    'hired_review_num': 'kn_hired_review_num',
    'hired_review_score': 'kn_hired_score',
    'rejected_review_num': 'kn_rejected_review_num',
    'rejected_review_score': 'kn_rejected_score',
    'offerdeclined_review_num': 'kn_offer_declined_review_num',
    'offerdeclined_review_score': 'kn_offer_declined_score',
    'deferred_review_num': 'kn_deferred_review_num',
    'deferred_review_score': 'kn_deferred_score',
    'employees_review_num': 'kn_employees_review_num',
    'employee_review_score': 'kn_employee_review_score',
    'employee_rec_score': 'kn_employee_rec_score',
    'corporate_culture_review_num': 'kn_corporate_culture_review_num',
    'satisfied_salary_pct': 'kn_satisfied_salary_pct',
    'kantine': 'kn_canteen',
    'flexible_arbeitszeiten': 'kn_flexible_working_hours',
    'betriebsarzt': 'kn_company_doctor',
    'betriebliche_altersvorsorge': 'kn_company_retirement_provision',
    'parkplatz': 'kn_parking',
    'homeoffice': 'kn_home_office',
    'gesundheits_maßnahmen': 'kn_health_measures',
    'rabatte': 'kn_discounts',
    'diensthandy': 'kn_company_phone',
    'mitarbeiter_beteiligung': 'kn_employee_participation',
    'internetnutzung': 'kn_internet_usage',
    'gute_verkehrsanbindung': 'kn_good_transport_links',
    'mitarbeiter_events': 'kn_employee_events',
    'essenszulage': 'kn_food_allowance',
    'barrierefrei': 'kn_accessible',
    'coaching': 'kn_coaching',
    'kinderbetreuung': 'kn_childcare',
    'firmenwagen': 'kn_company_car',
    'hund_erlaubt': 'kn_dogs_allowed',
    'sehr_gut_reviews': 'kn_very_good_reviews',
    'gut_reviews': 'kn_good_reviews',
    'befriedigend_reviews': 'kn_satisfactory_reviews',
    'genuegend_reviews': 'kn_insufficient_reviews',
    'name': 'kn_firm_name',
    'simple_name': 'kn_firm_simple_name',
    'canonical_slug': 'kn_canonical_slug',
    'locations_main_country_code': 'kn_country_code',
    'locations_main_city': 'kn_city',
    'locations_main_state': 'kn_state',
    'locations_total': 'kn_locations_total',
    'is_verified': 'kn_is_verified',
    'is_claimed': 'kn_is_claimed',
    'is_top_company_paid': 'kn_is_top_company_paid',
    'industry_id': 'kn_industry_id',
    'total_companies': 'kn_total_companies',
    'reviews_total_published_reviews_last_two_years': 'kn_reviews_published_last_two_years',
    'reviews_total_published_reviews_offline_deleted_last_two_years': 'kn_reviews_offline_deleted_last_two_years',
    'reviews_first_review_year': 'kn_reviews_first_year',
    'reviews_industry_average_score': 'kn_industry_avg_score',
    'reviews_recommendation_rate_percentage': 'kn_recommendation_rate_pct',
    'reviews_recommendation_rate_total_reviews': 'kn_recommendation_total_reviews',
    'reviews_recommendation_rate_recommended_total_reviews': 'kn_recommendation_total_positive_reviews',
    'reviews_recommendation_rate_not_recommended_total_reviews': 'kn_recommendation_total_negative_reviews'
}

required_keys = [
        "name", "simple_name", "canonical_slug", "locations_main_country_code",
        "locations_main_city", "locations_main_state", "locations_total",
        "is_verified", "is_claimed", "is_top_company_paid", "industry_id",
        "total_companies", "reviews_total_published_reviews_last_two_years",
        "reviews_total_published_reviews_offline_deleted_last_two_years",
        "reviews_first_review_year", "reviews_industry_average_score",
        "reviews_recommendation_rate_percentage",
        "reviews_recommendation_rate_total_reviews",
        "reviews_recommendation_rate_recommended_total_reviews",
        "reviews_recommendation_rate_not_recommended_total_reviews"
    ]