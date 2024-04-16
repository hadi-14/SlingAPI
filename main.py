from datetime import datetime
from __utils__ import *
import pandas as pd
from api import sling

BASE_DIR = "data"

api = sling('<email>', '<password>')

api.getOrganization()

users = pd.DataFrame(api.getusers())
users.to_csv(f"{BASE_DIR}/users.csv", index=False)
    
shedule = pd.DataFrame(api.getCalendersUsers(datetime(2024, 3, 1), datetime(2024, 4, 15)))
shedule['user'] = shedule['user'].apply(lambda x: x if pd.isna(x) else x['id'])
shedule['user'] = shedule['user'].map({id: name for _, (id, name) in users[['id', 'name']].iterrows()})
shedule = clean_df(shedule)
shedule.to_csv(f"{BASE_DIR}/shedule.csv", index=False)
     