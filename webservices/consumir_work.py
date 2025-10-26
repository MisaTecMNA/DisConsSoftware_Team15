import requests, json
BASE = "http://localhost:8001/works"

def pp(r): 
    try: print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except: print(r.text)

# CREATE
r = requests.post(BASE, json={"title":"El Principito","theme":"Filosofía infantil"}); print("POST", r.status_code); pp(r)
wid = r.json().get("id")

# LIST
r = requests.get(BASE); print("\nGET ALL", r.status_code); pp(r)

# GET ONE
r = requests.get(f"{BASE}/{wid}"); print("\nGET ONE", r.status_code); pp(r)

# PUT
r = requests.put(f"{BASE}/{wid}", json={"title":"El Principito (ed. revisada)","theme":"Cuento filosófico"}); print("\nPUT", r.status_code); pp(r)

# PATCH
r = requests.patch(f"{BASE}/{wid}", json={"theme":"Clásico universal"}); print("\nPATCH", r.status_code); pp(r)

# DELETE
r = requests.delete(f"{BASE}/{wid}"); print("\nDELETE", r.status_code); pp(r)

# FINAL LIST
r = requests.get(BASE); print("\nGET ALL (final)", r.status_code); pp(r)
