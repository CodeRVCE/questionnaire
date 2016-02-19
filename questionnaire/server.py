from flask import Flask, request, make_response, redirect
from flask import render_template
from genform import total_questions
import json
import shelve 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        response = make_response(redirect('/questionnaire'))
        response.set_cookie('name', request.form.get('name'))
        response.set_cookie('usn', request.form.get('usn'))
        return response
        

@app.route('/questionnaire', methods=['GET', 'POST'])
def get_questionnaire():
    if request.method == 'GET':
        name = request.cookies.get('name')
        usn = request.cookies.get('usn')
        if not name or not usn:
            response = make_response(redirect('/'))
            return response
        return render_template('questionnaire.html')
    elif request.method == 'POST':
        submissions = shelve.open('submissions')
        name = request.cookies.get('name')
        usn = request.cookies.get('usn')
        answers = [request.form.get(str(i)) for i in range(total_questions)]
        # with open(name+'_'+usn, 'w') as outfile:
        #     json.dump([name, usn, responses], outfile)
        submissions[usn] = {'name': name, 'answers': answers}
        submissions.close()
        return 'Finished!'
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



