import click
from tabulate import tabulate
from db import dbconn
import random


conn = None
word_id = None
TOTAL_QUESTIONS = 10


def conn():
    """ returns the connection object from the db module """

    global conn # using the global conn variable so all other functions can use it

    conn = dbconn()
    return conn

def get_categories():
    """ return the categories and store them in a dict """

    global conn  # using the global conn as it has the connection object alread

    cur = conn.cursor()
    query = "select id, name from category order by 1"
    try:
        cur.execute(query)
        data = cur.fetchall()
        categories = {k: v for k, v in data}
        return categories

    except Exception as e:
        print("couldn't fetch data from category: ", e)
        conn.close()
        print("database connection closed")


def setResult(object_type=str, object_id=int, attempts=1):
    """ 
    takes three keyword args, object_type which determines if the object is the word or sentence.
    the second one is the object_id which is the word_id or sentence_id.
    the last one is the attempts, which takes a default value of 1.
    """

    # based on the object_type I determine the query.
    global conn
    
    
    if object_type == 'word':

        query = "INSERT INTO result (word, attempts) VALUES (%s, %s)"

    elif object_type == 'sentence':

        query = "INSERT INTO result (sentence, attempts) VALUES (%s, %s)"

    else:

        exit("Unknown object_type")


    cursor = conn.cursor()

    try:
        cursor.execute(query, (object_id, attempts))
        conn.commit()

        print("result inserted .. ")

    except Exception as e:
        conn.rollback()
        conn.close()

        print("result couldn't be inserted: ", e)


def show_result(quiz_object='word'):
    """
    this function takes one parameter, the object_type to determine the 
    query and data to pull from the database. It will pull all the data 
    for the object (word or sentence) for the last 7 days from the result
    table. Also it generates a list of strings (header) that will be used
    as header in the viewed table. The table will be generated from the
    fetched data using the tabulate module.
    """
    global conn

    if quiz_object == 'word':

        query = "select w.word, attempts, date(r.created) from result as r join word as w on (r.word = w.id) where r.word is not NULL and r.created >= (CURRENT_DATE - interval '7 DAY') order by date(r.created) ASC"
        header = ['word', 'attempts', 'created']

    else:

        query = "select s.sentence, attempts, date(r.created) from result as r join sentence as s on(r.sentence = s.id) where r.sentence is not NULL and r.created >= (CURRENT_DATE - interval '7 DAY') order by date(r.created) ASC"
        header = ['sentence', 'attempts', 'created']

    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()

        # the tabulate function takes three params. result which is the
        # data to be presented in the table. the headers which is a list
        # of strings to used in the header of the table. tablefmt which
        # is the format of the table. for this one I chose psql.

        print(tabulate(result, headers=header, tablefmt="psql"))

    except Exception as e:
        conn.close()
        print("result couldn't be inserted and connection is closed: ", e)



def quiz_verb(word_id=int, word='str', word_attempts=1):
    """
    takes words from the verb table and has one language which is Spanish.
    """

    global conn
    
    query = "select yo, tu, usted, nosotros, vosotros, ustedes from verb where word = %s"
    cursor = conn.cursor()

    cursor.execute(query, (word_id,))
    verb = cursor.fetchone()
    subject_pronouns = ('yo', 'tu', 'él/ella/Usted', 'nosotros', 'vosotros', 'ellos/ellas/Ustedes')
    
    options = get_options(quiz_object='verb', object_id=word_id, limit=3)
    options.append(verb)
    
    total_attempts = word_attempts
    print("word_attempts to start with = {}".format(word_attempts))
    
    for x in (range(0, len(verb))):
        print("Question number .....",(x + 1), ' from ', (len(verb)))
        correct_answer = 0
        attempts = 0
        new_options = list(map(lambda a: a[x], options))
 
        while correct_answer == 0:

            question = "what is the subject_pronouns '" + subject_pronouns[x] + "' in Spanish for the word " + word + " ? "

            # if the numbe rof attempts exceeds 3, multiple choice answers will be printed

            if attempts > 3:
                i = 0
                for a in random.sample(new_options, len(new_options)): # randomly shuffle the words
                    i += 1
                    print(i,"- ",a)

            answer = input(question)
            if str(verb[x]).lower() == str(answer).lower():
                correct_answer = 1
                print("Correct Answer")
                

            else:
                attempts = attempts + 1
                print("Wrong Answer. Attempt number ".__add__(str(attempts)))

                total_attempts += attempts

                
    result = {'object_type': 'word', 'object_id' : word_id, 'attempts' : total_attempts}
    print("total attempts at the end: ", total_attempts)
    setResult(**result)
     
    

@click.command()
@click.option('--language', type=click.Choice(['ES', 'EN']), default='ES', prompt='Do you want the questions about [ES] or [EN] words/sentences ?')
@click.option('--quiz', type=click.Choice(['W', 'S']), default='W', prompt='Quiz type [W]ords or [S]entences [W/S] ?')
def quiz(language, quiz):
    """ 
    expect two parameters, language and quiz. The language option tells me if the answers should be in english or spanish.
    The quiz option determines the questions if they are about words or sentences.
    the third option here follows is the category. That is optional. It determines the category of the words and sentences.
    """

    global conn
   
    quiz_type = 'word' if quiz == 'W' else 'sentence'
    categoryId = None   # set the deault value for the categoryId
    categories = get_categories()

    # print the catgoryid and the categoryname 

    for k, v in categories.items():
        print("[", k, "] - ", v)

    # wait for an input. it the categoryId is true and the type is int (categoryId) use it in the queries
    # selecting words or sentences.
        
    category = input("select the category number you want the questions to be from. Default all categories. : ")

    if category:
        try:
            categoryId = int(category)

        except Exception as e:
            exit("ERROR: CategoryId has to be a number")
    else:
        print("no category has been selected")
        

    ############## queries section #########
    if quiz_type == 'word':

        query = "select w.id, word, word_en, category, name from word as w join category as c on (w.category = c.id) where w.id not in (select word from result where word is not null and DATE(created) = CURRENT_DATE and attempts = 1 )"

    else:

        query = "select s.id, sentence, sentence_en, category, name from sentence as s join category as c on (s.category = c.id) where s.id not in (select sentence from result where sentence is not null and DATE(created) = CURRENT_DATE and attempts = 1 )"

    # final query to append the category if the category was selected, otherwise just append the order by random limit 1
    # query += " and category = %s order by random() limit 1" if categoryId else "  order by random() limit 1"
    query += " and category = %s order by 1 ASC offset 1 limit 10" if categoryId else "order by 1 ASC offset 1 limit 10"

    ###########################
    
    available_total_questions = get_total_available_questions(quiz_object=quiz_type, categoryId=categoryId)

    quiz_limit = TOTAL_QUESTIONS if available_total_questions > TOTAL_QUESTIONS else available_total_questions
    if quiz_limit == 0:
        exit("There are no questions available today")

    print("total available questions: ", available_total_questions)

    lan1 = [2, 'english']
    lan2 = [1, 'spanish']
    if language == 'EN':
        lan1 = [1, 'spanish']
        lan2 = [2,'english']

    
    cursor = conn.cursor()

    for x in (range(0, int(quiz_limit))):
        print("Question number .....",(x + 1), ' from ', (quiz_limit))
        correct_answer = 0
        attempts = 1
        cursor.execute(query, (categoryId,))
        data = cursor.fetchone()
      
        options = get_options(quiz_object=quiz_type, object_id=data[0])
        options.append(data)


        while correct_answer == 0:

            question = "what is the meaning of the " + lan1[1] + " " + quiz_type + " '" +  data[lan1[0]] + "' in " + lan2[1] + " and category is " + data[4] + " ? "

            # if the number of attempts exceeds 3, multiple choice answers will be printed
            if attempts > 3:
                i = 0
                for a in random.sample(options, len(options)): # randomly shuffle the words options:
                    i += 1
                    print(i,"- ",a[lan2[0]])

            answer = input(question)

            if str(data[lan2[0]]).lower() == answer.lower():
                correct_answer = 1
                print("Correct Answer")
                if data[3] == 1 and quiz_type == 'word':
                    print("it's a verb")
                    quiz_verb(word_id=data[0], word=data[1], word_attempts=attempts )
                else:
                    result = {'object_type': quiz_type, 'object_id': data[0], 'attempts' : attempts}
                    setResult(**result)
            else:
                attempts = attempts + 1
                print("Wrong Answer. Attempt number ".__add__(str(attempts)))

    show_result(quiz_object=quiz_type)
    
    

def get_options(quiz_object=str, object_id=int, category=str, limit=0):
    """
    takes two params, the quiz_object which is either sentence or word. Object_id is the
    word_id or sentence_id, depends on the quiz_object.
    It will return 3 options, one is the given id, and two random options.
    """
    global conn

    options = limit if limit > 0 else 2
    
    if quiz_object == 'sentence':

        query = "select id, sentence, sentence_en from sentence where id != %s order by random() limit %s"

    elif quiz_object == 'word':

        query = "select id, word, word_en from word where id != %s order by random() limit %s"

    elif quiz_object == 'verb':

        query = "select yo, tu, usted, nosotros, vosotros, usted from verb where word != %s order by random() limit %s"

    else:

        exit("no valid quiz_object provided") 

    cursor = conn.cursor()

    try:
        cursor.execute(query, (object_id, options))
        result = cursor.fetchall()
        return result

    except Exception as e:
        print("result couldn't be fetched: ", e)
        conn.close()
        print("connection closed")


def get_total_available_questions(quiz_object=str, categoryId=None):
    """
    check the database to see the total number of available questions for the current day.
    based on the quiz_object and the categoryId if provided. It will return an int for the number of available questions.
    """
    global conn
   
    if quiz_object=='word':

        query = "select Count(*) from word where id not in (select word from result where word is not null and DATE(created) = CURRENT_DATE and attempts = 1)"

    else:

        query = "select Count(*) from sentence where id not in (select sentence from result where sentence is not null and DATE(created) = CURRENT_DATE and attempts = 1) "

    # check if the categoryId is set, append the category where clause to the query.
    if categoryId:
        query += " and category = %s"


    cursor = conn.cursor()

    try:
        cursor.execute(query, (categoryId,))
        total = cursor.fetchone()
        return int(total[0])

    except Exception as e:
        print("result couldn't be fetched: ", e)
        conn.close()
        print("connection closed")


if __name__ == '__main__':
    conn()
    quiz()
    conn.close()
