"""
@author: Divyanshu Kakwani <divkakwani@gmail.com>
License: MIT

Given a questionnaire in json form, this module generates its corresponding html
"""

import json
import jinja2

# a generic template for a question
generic_template = """
        <div class="field">
        <div class="ui blue segment" id="question-section">
            <div class="ui label">Question %s</div>
            <br>
            %s
            <br>
            %s
        </div>
        </div>
""" 

def gen_input_code(question, id):
    """
    Returns the html code for rendering the appropriate input
    field for the given question.
    Each question is identified by name=id
    """
    qtype = question['type']
    if qtype == 'text':
        return """<input type="text" class="ui text" name="{0}"
                         placeholder="your answer..." />""".format(id)
    elif qtype == 'code':
        return '<textarea class="ui text" name="{0}"></textarea>'.format(id)
    else:
        button_template = '<input type="radio" name="{0}" value="{1}"> {1}<br>'
        code = '' 
        for choice in question['choices']:
            code = code + button_template.format(id, choice)
        return code
    

questionnaire = json.load(open('questionnaire.json'))
questions = questionnaire['questions']
title = questionnaire['title']
total_questions = len(questions)
time = questionnaire['time']
fields_html = ''

for (sno, question) in enumerate(questions):
    input_html = gen_input_code(question, sno)
    question_html = generic_template % (sno, question['statement'], input_html)
    fields_html = fields_html + question_html


form = """
    <div class="ui  grid container" style="margin-top: 2%;">
        <div class="ui row">
            <h1 class="ui blue header">{0}</h1>
        </div>
        <div class="ui row">
            <form class="ui form" method="post" style="width: 100%; font-size: 18px;">
                {1}
                <input type="submit" value="Submit your response" class="ui blue button" />
            </form> 
        </div>
    </div>
    """.format(title, fields_html)


if __name__ == '__main__':
    outfile = open('templates/form.html', 'w')
    outfile.write(form)

