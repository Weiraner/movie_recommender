def load_movie_titles(filepath):
    movie_dict = {}
    with open(filepath, encoding='ISO-8859-1') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) > 1:
                movie_id = int(fields[0])
                movie_name = fields[1]
                movie_dict[movie_id] = movie_name
    return movie_dict

