import shelve

with shelve.open("crop_database") as db:
    for x in db:
        print(x)