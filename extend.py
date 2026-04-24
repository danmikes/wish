import os
import requests
from bs4 import BeautifulSoup

USER = os.environ.get('PA_USER')
PASS = os.environ.get('PA_PASS')

def extend_pythonanywhere():
  session = requests.Session()
    
  # 1. Token from login
  base_url = 'https://eu.pythonanywhere.com/'
  login_page = session.get(f'{base_url}/login/')
  soup = BeautifulSoup(login_page.text, 'html.parser')
  csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
  
  # 2. Login
  login_data = {
    'csrfmiddlewaretoken': csrf_token,
    'auth-username': USER,
    'auth-password': PASS,
    'login_view-current_step': 'auth',
    'next': ''
  }
  response = session.post(f'{base_url}/login/', data=login_data)

  # Check login
  if response.status_code != 200 or 'Invalid login' in response.text:
    print('Login failed')
    return False

  # 3. Webapp data
  webapp_page = session.get(f'{base_url}/user/{USER}/webapps/')
  soup = BeautifulSoup(webapp_page.text, 'html.parser')

  # 4. Button
  extend_form = soup.find('form', action=lambda x:x and 'extend' in x)
  if not extend_form:
    print('Extend button not found')
    print(f'Page snippet: {webapp_page.text[:500]}')
    return False
  
  # 5. Extend
  extend_url = extend_form.get('action')
  if not extend_url.startswith('http'):
    extend_url = base_url + extend_url

  # Token for form
  extend_csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})
  extend_data = {}
  if extend_csrf:
    extend_data['csrfmiddlewaretoken'] = extend_csrf.get('value')
  
  response = session.post(extend_url, data=extend_data)

  print(f'Extend result: {response.status_code}')
  success = response.status_code == 200 and 'extended' in response.text.lower()

  if success:
    print('Webapp extended')
  else:
    print('Webapp not extended: {response.text[:200]}')

  return success

if __name__ == "__main__":
  extend_pythonanywhere()
