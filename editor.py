import click
from db import dbconn
conn = None
word_id = None

def conn():
    """ returns the connection object from the db class """

    global conn

    conn = dbconn()
    return conn

def get_categories():
    """ return the categories and store them in a dict """

    global conn

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





@click.command()
@click.option('--word', prompt='Spanish word')
@click.option('--word_en', prompt='Translation')
def add_word(word, word_en):
    """
    exptect three parameters, word, word_en and categoryid. It will store them in
    the word table. The category will be taken from the get_category method as it
    will be fetched from the db. The returned word_id will be stored in the global
    word_id variable to be used by the verb method.
    """

    global conn, word_id
    categories = get_categories()
    for k,v in categories.items():
        print(k, " - ", v)

    category = input("Category Number: ")
    cur = conn.cursor()
    query = ''' INSERT INTO word (word, word_en, category) values (%s, %s, %s) RETURNING id '''
    values = (word.lower().title(), word_en.lower().title(), int(category))

    try:
        cur.execute(query, values)
        word_id = cur.fetchone()[0]
        if int(category) == 1:
            print("it's a verb")
            add_verb()
        else:
            conn.commit()
            click.echo("The word %s is successfully inserted: word_id: %s" % (word, word_id), nl=True)

    except Exception as e:
        print("couldn't insert data for word: ", e)
        conn.rollback()
        conn.close()
        print("database connection closed")



@click.command()
@click.option('--yo', prompt='Yo')
@click.option('--tu', prompt='Tu')
@click.option('--usted', prompt='Usted/El/Ella')
@click.option('--nosotros', prompt='Nosotros')
@click.option('--vosotros', prompt='Vosotros')
@click.option('--ustedes', prompt='Ustedes')
@click.option('--tense', type=click.Choice(['Present', 'Preterite', 'Imperfect', 'Conditional', 'Future']), default='Present', prompt='Tense')
def add_verb(yo, tu, usted, nosotros, vosotros, ustedes, tense):

    global conn, word_id
    cur = conn.cursor()
    query = ''' INSERT INTO verb (word, tense, yo, tu, usted, nosotros, vosotros, ustedes) values (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id '''
    values = (word_id, tense, yo.lower().title(), tu.lower().title(), usted.lower().title(), nosotros.lower().title(), vosotros.lower().title(), ustedes.lower().title())

    try:
        cur.execute(query, values)
        verb_id = cur.fetchone()[0]
        print("added verb successfully. VerbID: ", verb_id)
        conn.commit()

    except Exception as e:
        print("couldn't insert data for word: ", e)
        conn.rollback()
        conn.close()
        print("database transaction rolled back and closed")

@click.command()
@click.option('--sentence', prompt='Spanish Sentence')
@click.option('--sentence_en', prompt='English Sentence')
def add_sentence(sentence, sentence_en):

    global conn
    
    categories = get_categories()
    for k,v in categories.items():
        print(k, " - ", v)

    category = input("Category Number: ")
    cur = conn.cursor()
    query = ''' INSERT INTO sentence (sentence, sentence_en, category) values (%s, %s, %s) RETURNING id '''
    values = (sentence.lower().title(), sentence_en.lower().title(), int(category))

    try:
        cur.execute(query, values)
        sentence_id = cur.fetchone()[0]
        conn.commit()
        click.echo("The sentence is successfully inserted with id: %s" % (sentence_id), nl=True)

    except Exception as e:
        print("couldn't insert data for word: ", e)
        conn.rollback()
        conn.close()
        print("database connection closed")


@click.command()
@click.option('--action', type=click.Choice(['W', 'S']), default='W', prompt="select action to add [W: Words/ S:Sentences]")
def run(action):

    conn()
    if action == 'W':
        add_word()
    else:
        add_sentence()


if __name__ == '__main__':
    run()
    conn.close()


