import MySQLdb
# mysql://root:my-secret-pw@mysql/practice_data
comment_stop=[100,1000,5000,10000]
click_stop = [100000, 1000000, 50000000]
character_stop = [10000,50000,200000,1000000]

comment_per_ton_thounsand_stop = [10,50,200,500]
click_per_ton_thounsand_stop = [100,1000,10000,50000]
def get_sql(name,stops,is_average):
    first_stop = 0
    SQL = 'SELECT'
    titles = []
    for item in stops:
        second_stop = item
        titles += ['{}-{}'.format(first_stop,second_stop)]
        if is_average:
            SQL += """
            COUNT( CASE WHEN `{2}`/`character_count`*10000 BETWEEN {0} AND {1} THEN 1 ELSE NULL END ) AS `{0}-{1}`,""".format(first_stop,second_stop,name)
        else:
            SQL += """
            COUNT( CASE WHEN `{2}` BETWEEN {0} AND {1} THEN 1 ELSE NULL END ) AS `{0}-{1}`,""".format(first_stop,second_stop,name)
        first_stop = item + 1
    titles += ['>{}'.format(first_stop)]
    if is_average:
        SQL +="""
        COUNT( CASE WHEN `{1}`/`character_count` > {0} THEN 1 ELSE NULL END ) AS `>{0}`""".format(first_stop,name)
    else:
        SQL +="""
        COUNT( CASE WHEN `{1}` > {0} THEN 1 ELSE NULL END ) AS `>{0}`""".format(first_stop,name)
    SQL += """
    FROM novel;"""
    return titles,SQL

def query_and_print(title,column_name,stop,is_average):
    db = MySQLdb.connect(host='mysql',passwd='my-secret-pw',db='practice_data')
    c = db.cursor()
    (titles,comment_sql) = get_sql(column_name,stop,is_average)
    result = c.execute(comment_sql)
    result = c.fetchone()
    print(title)
    for keys,items in iter(zip(titles,result)):
        print('{} : {}'.format(keys,items))

query_and_print('总字数','character_count',character_stop,False)
query_and_print('总点击','click_count', click_stop,False)
query_and_print('总评论','comment_count', comment_stop,False)

query_and_print('平均万字点击','click_count',click_per_ton_thounsand_stop,True)
query_and_print('平均万字评论','comment_count', comment_per_ton_thounsand_stop ,True)
