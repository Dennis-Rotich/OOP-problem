import sqlite3

CONN = sqlite3.connect('Judge.db')
CURSOR = CONN.cursor()

class Judge:
    all = {}

    def __init__(self,name,chickenwings,hamburgers,hotdogs):
        total = (chickenwings*5)+(hamburgers*3)+(hotdogs*2)
        self.name = name
        self.score = total

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        if isinstance(value,str) and len(value):
            self._name = value
        else:
            raise ValueError('Invalid name')

    @property
    def score(self):
        return self._score
    @score.setter
    def score(self,value):
        if isinstance(value,int):
            self._score = value
        else:
            raise ValueError('Invalid points, should be integers')    

    def save(self):
        sql="""
            INSERT INTO points (name,score) 
                        VALUES (?,?);
        """
        CURSOR.execute(sql,(self.name,self.score))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def instance_from_db(cls,row):
        contestant = cls.all.get(row[0])
        if contestant:
            contestant.name = row[1]
            contestant.score = row[2]
        else:
            contestant = cls(row[1],row[2],row[3],row[4])
            contestant.id = row[0]
            cls.all[contestant.id] = contestant
        return contestant

    @classmethod
    def score_points(cls):
        sql="""
            SELECT * FROM points ORDER BY score DESC, name ;
        """
        rows = CURSOR.execute(sql).fetchall()
        contestants = []
        for row in rows:
            contestants.append(cls.instance_from_db(row))
        return [{"name":contestant.name,'score':contestant.score} for contestant in contestants]            

    @classmethod
    def reset(cls):
        sql ="""
            DROP TABLE points;
        """
        CURSOR.execute(sql)
        sql="""
            CREATE TABLE points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(20),
                score INTEGER
            );
        """
        CURSOR.execute(sql)        