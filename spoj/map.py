from utils import *
from recsys.datamodel.item import Item

from recsys.datamodel.data import Data
from recsys.algorithm.factorize import SVD
import pickle
import os
import operator
import utils

genre_list = ['Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary',
	 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

problems_recsys = {}

problems = pickle.load( open( os.path.join(utils.get_add_dir(), 'problem_database'), "rb" ) )
# print problems
# exit()
tags = pickle.load( open( os.path.join(utils.get_add_dir(), 'tags_database'), "rb" ) )

sorted_tags = sorted(tags.items(), key=lambda x: len(x[1]), reverse=True)
# print sorted_tags

problem_keys = list(problems)
tag_keys = [tag[0] for tag in sorted_tags]
print tag_keys


# exit()

def read_items(filename):
    items = dict()
    for line in open(filename):
        #1::Toy Story (1995)::Animation|Children's|Comedy
        data =  line.strip('\r\n').split('::')
        item_id = int(data[0])
        item_name = data[1]
        genres = data[2].split('|')
        item = Item(item_id)
        item.add_data({'name': item_name, 'genres': genres})
        items[item_id] = item
        tags=[]
        for genre in genres:
        	tags.append(tag_keys[genre_list.index(genre)])
        problems_recsys[problem_keys[item_id%3300+1]] = {'name': problems[problem_keys[item_id%3300+1]]['title'], 'tags': tags}
    return items

# Call it!
filename = '../data/ml-1m/movies.dat'
items = read_items(filename)

pickle.dump( problems_recsys, open( os.path.join(utils.get_add_dir(), 'problems_recsys'), "wb" ) )


print problems_recsys
