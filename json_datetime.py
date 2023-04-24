import json
import datetime


# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


# Create a datetime object
dt = datetime.datetime.now()

# Serialize the object using the custom function
json_data = json.dumps(dt, default=serialize_datetime)
print(json_data)
