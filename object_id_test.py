from bson.objectid import ObjectId

the_id = ObjectId()
as_str = str(the_id)
print("object ID as string is", as_str)