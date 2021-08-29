def words(data):
    with open(data) as data:
        data = [word.strip() for word in data.readlines()]
        return data
