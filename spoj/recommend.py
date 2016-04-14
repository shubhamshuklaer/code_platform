import utils
from recsys.datamodel.data import Data
from recsys.algorithm.factorize import SVD, SVDNeighbourhood
import pickle
import os

def parse_data():
	filename = '../data/ml-1m/ratings.dat'
	data = Data()
	format = {'col':0, 'row':1, 'value':2, 'ids': int}
	data.load(filename, sep='::', format=format)
	train, test = data.split_train_test(percent=80) # 80% train, 20% test
	data.save(os.path.join(utils.get_add_dir(), 'ratings'), pickle=True)

def load_data():
	data = Data()
	data.load(os.path.join(utils.get_add_dir(), 'ratings'), pickle=True)
	return data	

def compute_SVD():
	svd = SVD()
	svd.set_data(load_data())

	K=100
	svd.compute(k=K, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile=None)
	svd.save_model(os.path.join(utils.get_add_dir(), 'ratings'))

def compute_SVDNeighbourhood():
	svd = SVDNeighbourhood()
	svd.set_data(load_data())

	K=100
	svd.compute(k=K, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile=None)
	svd.save_model(os.path.join(utils.get_add_dir(), 'ratings_neigh'))

def get_similarity(probID1, probID2, SVDNeighbourhood=False):
	if SVDNeighbourhood:
		svd2 = SVDNeighbourhood()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings_neigh'))
	else:
		svd2 = SVD()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings'))
	return svd2.similarity(probID1, probID2)

def get_similar_problems(probID, SVDNeighbourhood=False):
	if SVDNeighbourhood:
		svd2 = SVDNeighbourhood()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings_neigh'))
	else:
		svd2 = SVD()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings'))
	return svd2.similar(probID)

def predict_rating(probID, userID, MIN_RATING, MAX_RATING, SVDNeighbourhood=False):
	if SVDNeighbourhood:
		svd2 = SVDNeighbourhood()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings_neigh'))
	else:
		svd2 = SVD()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings'))
	return svd2.predict(probID, userID, MIN_RATING, MAX_RATING)

def recommend_problems(userID, SVDNeighbourhood=False):
	if SVDNeighbourhood:
		svd2 = SVDNeighbourhood()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings_neigh'))
	else:
		svd2 = SVD()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings'))
	problems = svd2.recommend(userID, n=20, only_unknowns=False, is_row=False)
	ret = []
	data = load_data()
	for problem in problems:	
		found = False
		for t in data:
			# print t, problem
			if t[1] == problem[0] and t[2] == 45:
				found = True
				break
		if not found:		
			# print problem
			ret.append(problem)

	return ret


def get_recommended_problem_code(userID=45, SVDNeighbourhood=False):
	problems_recsys = pickle.load( open( os.path.join(utils.get_add_dir(), 'problems_recsys'), "rb" ) )
	problem_keys = list(problems_recsys)

	return problem_keys[recommend_problems(userID)[0][0]%3300]

def get_recommended_problem_id(userID=45, SVDNeighbourhood=False):
	problems_recsys = pickle.load( open( os.path.join(utils.get_add_dir(), 'problems_recsys'), "rb" ) )
	problem_keys = list(problems_recsys)

	return recommend_problems(userID)[0][0]%3300

def recommend_users(probID, SVDNeighbourhood=False):
	if SVDNeighbourhood:
		svd2 = SVDNeighbourhood()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings_neigh'))
	else:
		svd2 = SVD()
		svd2.load_model(os.path.join(utils.get_add_dir(), 'ratings'))
	return svd2.recommend(probID)

def set_rating(rating, userID=45, probCode='GSS1', compute=False, SVDNeighbourhood=False):
	problems_recsys = pickle.load( open( os.path.join(utils.get_add_dir(), 'problems_recsys'), "rb" ) )
	problem_keys = list(problems_recsys)
	
	data = Data()
	data.load(os.path.join(utils.get_add_dir(), 'ratings'), pickle=True)

	data.add_tuple((rating, problem_keys.index(probCode), userID))

	data.save(os.path.join(utils.get_add_dir(), 'ratings'), pickle=True)

	if compute:
		if SVDNeighbourhood:
			compute_SVDNeighbourhood()
		else:
			compute_SVD()

# parse_data()
# compute_SVD()
	
# probCode = get_recommended_problem_code()
# probID = get_recommended_problem_id()
# print probCode, probID

# set_rating(1, 45, probCode, compute=False, SVDNeighbourhood=False)

# probCode = get_recommended_problem_code()
# probID = get_recommended_problem_id()
# print probCode, probID

