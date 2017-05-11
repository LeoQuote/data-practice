import csv
import sqlalchemy as sqlal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import time
import codecs


Base = declarative_base()
class Novel(Base):
    __tablename__ = 'novel'
    id = Column(Integer, primary_key=True,unique=True)
    book_id = Column(Integer)
    type = Column(String(64)) 
    style = Column(String(64)) 
    name = Column(String(256)) 
    url = Column(String(64)) 
    status = Column(String(64)) 
    character_count = Column(String(64)) 
    is_published = Column(String(64)) 
    is_signed = Column(String(64)) 
    download_count = Column(Integer) 
    click_count = Column(Integer) 
    comment_count = Column(Integer) 
    like_count = Column(Integer) 
    chapter_count = Column(Integer) 
    update_time = Column(String(64)) 
    author_name = Column(String(64)) 
    author_url = Column(String(64)) 
    capture_date = Column(String(64))

    def __repr__(self):
        return "<novel(name='[]', author=='[]')>".format(self.name,self.author_name)
    
def clean_row(row):
    row = [x if x !='null' else None for x in row]
    row = [x if x !='' else None for x in row]
    for i in range(9,14):
        try :
            int(row[i])
        except ValueError:
            row[i] = None
        except TypeError:
            row[i] = None
    try:
        int(row[3])
    except ValueError:
        return None
    return row 

if __name__ =='__main__':
    now = time.time()
    csv_title = ['类型','风格','书名','书Id','书Url','状态','总字数','出版','签约','总下载','非V章节总点击数','总评论','总收藏','章节','更新时间','作者','作者Url','capturedate']
    sql_title = ['type','style','name','book_id','url','status','character_count','is_published','is_signed','download_count','click_count','comment_count','like_count','chapter_count','update_time','author_name','author_url','capture_date']
    title_dict = dict(zip(csv_title,sql_title))
    engine = sqlal.create_engine('mysql://root:my-secret-pw@mysql/practice_data?charset=utf8mb4')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    novel_session = Session()
    csvfile = codecs.open('jinjiang_2017-05-09.csv', 'r', 'utf-8')
    stop_num = 10000
    i = 0
    for line in csvfile:
        if i ==0:
            i += 1
            continue
        i += 1
        try:
            row = line.split(',')
        except:
            continue
        row = clean_row(row)
        if row==None:
            continue
        ed_novel = Novel(**dict(zip(sql_title,row)))
        novel_session.add(ed_novel)
        if i > stop_num:
            print('{}行过去了'.format(stop_num))
            print('花费时间 {} s'.format(time.time()-now))
            i = 1
            novel_session.commit()
    print('总时间 {} s'.format(time.time()-now))
