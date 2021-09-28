from quick_api.backends.json_file import JsonFile

# Backend type to use.  Only JSON available as of now
BACKEND_TYPE = JsonFile

# File to save/retrieve records from
SOURCE = "data/data.json"

# If using flask to host static content, this would be the html file to load at /
STATIC_ENTRY = "index.html"



class Config:
    BACKEND = BACKEND_TYPE(SOURCE)
    STATIC_ENTRY_POINT = STATIC_ENTRY

