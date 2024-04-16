from datetime import datetime
import requests
import json

class sling:
    url = "https://api.getsling.com/v1"
    apiKey = ""
    org = ""

    def __init__(self, email, password):
        self.auth(email, password)

                 
    def auth(self, email, password):
        """Authorazes Api based on email and password given"""
        
        headers = {
            # 'Accept': '*/*',
            'Content-Type': 'application/json'
        }

        data = {
            'email': email,
            'password': password,
        }

        response = requests.post(self.url + "/account/login", data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            self.apiKey = response.headers['Authorization']
        else:
            print(f"Error: {response.status_code} - {response.text}")        
            
    def getOrganization(self) -> int:
        """Gets Organization of the loged in user"""
        headers = {
            'Authorization': self.apiKey,
            'accept': 'application/json'
        }
        
        response = requests.get(self.url + "/account/session", headers=headers)
        
        if response.status_code == 200:
            self.org = response.json()['org']['id']
            self.userID = response.json()['user']['id']
            return self.org
        else:
            raise Exception(response.text)
    
    def getusers(self) -> dict:
        """Gets the users"""        
        
        headers = {
            'Authorization': self.apiKey,
            'accept': 'application/json'
        }
        
        response = requests.get(self.url + "/users", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.text)
        
    def getCalendersUsers(self, dateStart: datetime, dateEnd: datetime) -> dict:
        
        headers = {
            'Authorization': self.apiKey,
            'accept': 'application/json',
        }
        response = requests.get(self.url + f"/calendar/{self.org}/users/{self.userID}?dates={dateStart.strftime('%Y-%m-%dT%H:%M:%SZ')}/{dateEnd.strftime('%Y-%m-%dT%H:%M:%SZ')}", headers=headers)
        
        return response.json()
        
    def get(self, requestUrl) -> dict:
        
        headers = {
            'Authorization': self.apiKey,
            'accept': 'application/json'
        }
        
        response = requests.get(self.url + "/" + requestUrl, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.text)
        