import pypyodbc as pyodbc
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#TODO: Create function for db connection
#TODO: Create function for db query by survey name/id
#TODO: Checkin to Git
#TODO: Should I be dealing with data set in a different/better fashion?
#TODO: SQL Error handling, capture errors in table vs. stop processing

def cleanStopWords(comment):
    #TODO: Add variations of st lukes to stopword list (st st. luke luke's)
    #TODO: check for plurals, and lemmatize
    #TODO: use join vs. concatenation in final_string
    stopWords = set(stopwords.words('english'))
    wordsFiltered = set(TextBlob(str(comment)).words.lower()) - stopWords
#join
    final_string = ''
    for word in wordsFiltered:
        final_string = final_string+word+' '
    # print('final_string',final_string)
    # print('wordsFiltered:',wordsFiltered)
    return final_string

def wordCount(comment):
    #TODO: make more generic,
    word_count = TextBlob(cleanStopWords(str(comment))).lower().word_counts
    # print('word_count:',word_count)
    return word_count

def nounPhraseCount(comment):
    noun_count = TextBlob(cleanStopWords(str(comment))).lower().np_counts
    # print('noun_count:',noun_count)
    return noun_count

def sentimentAnalysis(comment):

    """
    Capture the sentiment of a comment
    """
    commentSentiment = TextBlob(cleanStopWords(str(comment)), analyzer=NaiveBayesAnalyzer())
    # print('Inside function commentSentiment:',commentSentiment, '\nsentiment', commentSentiment.sentiment, '\npolarity', commentSentiment.polarity,
    #        '\nsubjectivity',
    #        commentSentiment.subjectivity, '\n=============')
    return commentSentiment

def insertSentiment(key,comment):
    try:
        # connect to db
        db_host = 'localhost\sqlexpress'
        db_name = 'EEComments'
        db_user = 'esnider1'
        db_password = 'Ilove1daho'
        connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
        db = pyodbc.connect(connection_string)
        cursor = db.cursor()


        SQL = """\
                exec InsertSentiment @pResponseCommentKey=?
                    ,@pClassification=?
                    ,@pp_pos=?
                    ,@pp_neg=?
                    ,@pPolarity=?
                    ,@pSubjectivity=? 
                """
        args = [key, comment.sentiment[0], comment.sentiment[1], comment.sentiment[2], comment.polarity, comment.subjectivity]
        # print(args)
        cursor.execute(SQL, args)


    except Error as e:
        print(e)

    finally:
        cursor.commit()
        cursor.close()
        db.close()

def insertWordCount(key,comment):
    try:
        # connect to db
        db_host = 'localhost\sqlexpress'
        db_name = 'EEComments'
        db_user = 'esnider1'
        db_password = 'Ilove1daho'
        connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
        db = pyodbc.connect(connection_string)
        cursor = db.cursor()


        SQL = """\
                exec InsertWordCount @pResponseCommentKey=?
                    ,@pKeyWord=?
                    ,@pCount=? 
                """
        args = [key, comment.sentiment[0], comment.sentiment[1], comment.sentiment[2], comment.polarity, comment.subjectivity]
        # print(args)
        cursor.execute(SQL, args)


    except Error as e:
        print(e)

    finally:
        cursor.commit()
        cursor.close()
        db.close()

#main
#connect to db
db_host = 'localhost\sqlexpress'
db_name = 'EEComments'
db_user = 'esnider1'
db_password = 'Ilove1daho'
connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'

db = pyodbc.connect(connection_string)
cursor = db.cursor()
#get question
# SQL = "Select questiontext from dim.Questions where questionkey = 40"
# cursor.execute(SQL)
# result = cursor.fetchone()
# print("Question:",result)


#select data and return all results
SQL = "select responseCommentKey, Comments from dbo.ResponseComments where responseCommentKey = 29"
cursor.execute(SQL)
result = cursor.fetchall()

for r in result:
    sentimentResult = sentimentAnalysis(r[1])
    insertSentiment(r[0], sentimentResult)
    print('wordCount',wordCount(r[1]))
    #print('sentiment',sentimentResult, sentimentResult.sentiment[0], sentimentResult.sentiment[1], sentimentResult.sentiment[2])
    # print('Polarity & subjectivity:', sentimentResult.polarity, sentimentResult.subjectivity)




cursor.close()
db.close()