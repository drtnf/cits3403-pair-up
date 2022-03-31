from app import app
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
import time, random


update_delta = 120
words = []
with open('./app/wordle/fives.txt','r') as word_file:
    for word in word_file:
        words.append(word[:-1])


'''
Renews the selected word every update delta seconds
'''
def check_time():
  f = open('./app/wordle/last_update.txt','r')
  last_update = int(f.read())
  f.close()
  now = int(time.time())
  if (now-last_update) > update_delta:
      last_update = now
      secret = words[random.randrange(len(words))]
      f = open('./app/wordle/answer.txt','w')
      f.write(secret)
      f.close
      f = open('./app/wordle/last_update.txt','w')
      f.write(str(last_update));
      f.close
  return update_delta-(now-last_update)   

'''
Gives time remaining for the current puzzle
'''
@app.route('/wordle_time_left', methods=['GET'])
def wordle_time_left():
  response = jsonify({'time_left':check_time()})
  response.status_code = 201
  return response

'''
route for handling wordle guesses
'''
@app.route('/wordle_guess',methods=['POST','GET'])
def wordle_guess():
  check_time()  
  data = request.args or {}
  if 'guess' not in data or not data['guess'].isalpha() or len(data['guess']) != 5:
    return bad_request('Guess must be a five letter word')
  f = open('./app/wordle/answer.txt','r')
  secret = f.read()
  f.close()
  response = jsonify({'outcome':wordle(data['guess'].upper(), secret.upper())})
  response.status_code = 201
  return response

'''
Wordle guess array
'''
def wordle(guess, target):
    answer = [0]*5 #to return to user                  
    target_free = [True]*5  #for handling multiple letters
    for i in range(5):
        if guess[i]==target[i]:
            answer[i] = 2
            target_free[i] = False
    for i, c in enumerate(guess):
        for j, d in enumerate(target):
            if c==d and target_free[j] and answer[i]==0:
                answer[i] = 1
                target_free[j] = False
    return answer            


