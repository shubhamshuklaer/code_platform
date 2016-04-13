from utils import *
import pickle
from math import *


USER_LOCAL_DATABASE = "local_db"
USER_TAG_DATABASE = "tag_db"
USER_PROBLEM_HEAP = "heap_db"

user_problem_db_1 = {}

def return_problem_db_dict():
	global user_problem_db_1
	return user_problem_db_1

def reopen_problem_db_dict():
	global user_problem_db_1
	with open(get_add_dir()+"/"+PROBLEM_DATABASE_NAME,"r") as f:
		user_problem_db_1 = pickle.load(f)
	return user_problem_db_1

reopen_problem_db_dict()

def return_tag_list():
	with open(get_add_dir()+"/"+TAGS_DATABASE_NAME,"r") as f:
		tag_problem_db = pickle.load(f)
	return tag_problem_db


def return_considerable_tags():
	problem_tag_considerable = []
	tag_problem_db = return_tag_list()
	for t in tag_problem_db.keys():
		if(len(tag_problem_db[t])!=0):
			problem_tag_considerable.append(t)
	return problem_tag_considerable

def weight_accuracy(problem_db,problem):
	Max = float("inf")*-1
	for t in problem_db:
		if Max < float(problem_db[t]['users']):
			Max = float(problem_db[t]['users'])
	return int(problem_db[problem]['users'])/float(Max)

def problem_conceptual_difficulty(problem_db,problem):
	return float(problem_db[problem]["conceptual_diffi"])

def problem_implementation_difficulty(problem_db,problem):
	return float(problem_db[problem]["implementation_diffi"])



def add_number_of_tries(problem):
	try:
		with open(get_add_dir()+"/"+USER_LOCAL_DATABASE,"r") as f:
			user_problem_db = pickle.load(f)
		if(problem in user_problem_db.keys()):
			user_problem_db[problem] += 1
		else:
			user_problem_db[problem] = 0
		f = open(get_add_dir()+"/"+USER_LOCAL_DATABASE,"wb")
		pickle.dump(user_problem_db,f)
		f.close()
	except:
		user_problem_db = dict()
		user_problem_db[problem] = 1
		f = open(get_add_dir()+"/"+USER_LOCAL_DATABASE,"wb")
		pickle.dump(user_problem_db,f)
		f.close()

def get_number_of_tries(problem):
	try:
		with open(get_add_dir()+"/"+USER_LOCAL_DATABASE,"r") as f:
				user_problem_db = pickle.load(f)
		return user_problem_db[problem]
	except:
		return 0

def return_weight_Avg_Score(problem):
	tries = get_number_of_tries(problem)
	#print tries
	exp_value = 0.42*exp(-1*float(tries))
	return (1/(1+exp_value))

def return_weight_accuracy(problem):
	d = return_problem_db_dict()
	users = float(d[problem]["users"])
	exp_value = exp(-1*users/60)
	exp_value = 2 / (1+exp_value)
	exp_value = exp_value - 1
	return exp_value

def return_all_tags(problem):
	d = return_problem_db_dict()
	try:
		return d[problem]['tags']
	except:
		return []

def return_tag_score(tag):
	try:
		with open(get_add_dir()+"/"+USER_TAG_DATABASE,"r") as f:
			user_problem_db = pickle.load(f)
		if(tag in user_problem_db.keys()):
			return user_problem_db[tag]
		return 0
	except:
		return 0

def update_tag_score(tag,score):
	try:
		with open(get_add_dir()+"/"+USER_TAG_DATABASE,"r") as f:
			user_problem_db = pickle.load(f)
		user_problem_db[tag] = score
		f = open(get_add_dir()+"/"+USER_TAG_DATABASE,"wb")
		pickle.dump(user_problem_db,f)
		f.close()
	except:
		user_problem_db = {}
		user_problem_db[tag] = score
		f = open(get_add_dir()+"/"+USER_TAG_DATABASE,"wb")
		pickle.dump(user_problem_db,f)
		f.close()

def computeImplementationScore(problem):
	d = return_problem_db_dict()
	hardness = float(d[problem]['implementation_diffi'])
	score = return_tag_score('implementation')
	return (float(score-hardness)/2)+(float(1)/2)

def computeConceptScore(problem,score):
	d = return_problem_db_dict()
	hardness = float(d[problem]['conceptual_diffi'])
	return (float(score-hardness)/2)+(float(1)/2)

def computeAvgScore(problem,score):
	impl = computeImplementationScore(problem)
	cnpt = computeConceptScore(problem,score)
	return float(impl + cnpt)/2

def return_accuracy(problem):
	d = return_problem_db_dict()
	return float(d[problem]["accuracy"])

def compute_expected_score(problem,score):
	first_half = 0.5 * return_weight_Avg_Score(problem) * computeAvgScore(problem,score)
	#print first_half
	second_half = 0.5 * return_weight_accuracy(problem) * (return_accuracy(problem)/100)
	#print second_half
	return first_half+second_half

def update_score_solved(problem):
	avgtagscore = 0
	s = return_all_tags(problem)
	s.append("implementation")
	for t in s:
		avgtagscore += return_tag_score(t)
	avgtagscore = avgtagscore / len(s)

	score = compute_expected_score(problem,avgtagscore)
	#print score
	l = return_all_tags(problem)
	l.append("implementation")

	for t in l:
		tag_score = return_tag_score(t)
		increment = 1 - score
		tag_score += ((1-tag_score)*increment)
		update_tag_score(t,tag_score)




def update_score_unsolved(problem):
	avgtagscore =  0
	s = return_all_tags(problem)
	s.append("implementation")
	for t in s:
		avgtagscore += return_tag_score(t)
	avgtagscore = avgtagscore / len(s)

	score = compute_expected_score(problem,avgtagscore)

	l = return_all_tags(problem)
	l.append("implementation")

	for t in l:
		tag_score = return_tag_score(t)
		print tag_score
		increment = 0 - score
		tag_score += ((tag_score)*increment)
		update_tag_score(t,tag_score)
	
	add_number_of_tries(problem)


def update_score(problem,solved):
	if(solved == True):
		update_score_solved(problem)
	else:
		update_score_unsolved(problem)


def return_tags_dict_problem(problems):
	d = return_problem_db_dict()
	answer = {}
	for p in problems:
		try:
			answer[p] = (d[problem]['tags'])
			answer[p].append("implementation")
		except:
			answer[p] = ["implementation"]
	return answer

def update_score_solved_dummy(problem):
	avgtagscore = 0
	s = return_all_tags(problem)
	s.append("implementation")
	for t in s:
		avgtagscore += return_tag_score(t)
	avgtagscore = avgtagscore / len(s)

	score = compute_expected_score(problem,avgtagscore)
	#print score
	l = return_all_tags(problem)
	l.append("implementation")

	answer = retrieve_all_tag_score()

	for t in l:
		tag_score = return_tag_score(t)
		increment = 1 - score
		tag_score += ((1-tag_score)*increment)
		answer[t] = tag_score
	
	return answer

def retrieve_all_tag_score():
	t = return_considerable_tags()
	l = {}
	for tag in t:
		l[tag] = return_tag_score(tag)
	return l


def ComputeAvgScoreSolvingProblem(problem):
	computeSum = 0
	for tag,score in update_score_solved_dummy(problem).items():
		computeSum += float(score)
	computeSum/=len(update_score_solved_dummy(problem))
	return computeSum

def get_l_rate():
	return 0.2



def recommendProblem(learning_rate):
	Problem = []
	flag = True
	l = return_problem_db_dict()
	for p in l.keys():
		if(l[p]["solved"]==False):
			Problem.append((ComputeAvgScoreSolvingProblem(p),p))
			if(flag == False):
				sys.stdout.write("\033[F")
			print "processing problem " + p
			flag = False

 	Problem.sort(reverse=True)

 	factor = learning_rate

 	k = 0

 	total_ps = len(Problem)

 	prev_problem = Problem[0][1]

 	for p in Problem:
 		k=k+1
 		if((k/float(total_ps)) < float(factor)):
 			prev_problem = p[1]

 	print prev_problem