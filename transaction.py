"""This portion of the menu was largely implemented by Rue and Eugenio"""

import sqlite3
import os
import platform

def toDict(t):
    if len(t) == 1:
        return t[0]
    elif len(t) == 5:
        todo = {'item #':t[0], 'amount':t[1], 'category':t[2], 'date':t[3], 'description':t[4]}
        return todo


class TodoList():
    def __init__(self):
        self.runQuery('''CREATE TABLE IF NOT EXISTS todo
                    ("item #" text, amount real, category text, date text, description text)''',())
        self.runQuery('''CREATE TABLE IF NOT EXISTS categories
                (category text)''',())
        
    def selectAll(self):
        ''' return all of the tasks as a list of dicts.'''
        return self.runQuery('SELECT "item #", amount, category, date, description FROM todo', ())

    def add(self, item):
        '''Create a todo item and add it to the todo table. If it is a new category, add the category too'''
        category = item['category']
        self.add_category(category)
        return self.runQuery("INSERT INTO todo VALUES(?,?,?,?,?)",
                             (item['item #'], item['amount'], category, item['date'], item['description']))

    def add_category(self, category):
        category_exists = self.runQuery("SELECT * FROM categories WHERE category=?", (category,))
        if not category_exists:
            self.runQuery("INSERT INTO categories(category) VALUES(?)", (category,))
            return False
        else:
            return True
            
    def selectCategories(self):
        ''' return all unique categories as a set.'''
        return self.runQuery("SELECT DISTINCT category FROM categories", (), True)
    
    def delete(self, item_num):
        ''' delete a todo item '''
        return self.runQuery("DELETE FROM todo WHERE [item #] = ?", (item_num,))

    def update_category(self, old_category, new_category):
        cursor = self.runQuery("UPDATE todo SET category=? WHERE category=?", (new_category, old_category))
        cursor = self.runQuery("UPDATE categories SET category=? WHERE category=?", (new_category, old_category), True)
        categories = self.selectCategories()

    def destroy_all(self):
        self.runQuery('DELETE FROM todo', ())
        self.runQuery('DELETE FROM categories', ())

    def get_year(self):
        '''Return a list of all dates in the database.
        By Aby
        '''
        return self.runQuery('SELECT "item #", amount, category, date, description FROM todo ORDER BY date', ())

    def get_dates(self):
        '''Return a list of all dates in the database.
            By Aby
        '''
        res = self.get_year()
        my_set = []
        for x in res:
            my_set.append(x['date'])
        return my_set

    def my_years(self):
        '''Return a set of all years in the database.
        By Aby
        '''
        dates = self.get_dates()
        my_set = []
        for date in dates:
            my_set.append(date[:4]) # append first four characters of the date string
        d = set(my_set)
        return d
    
    def get_month(self):
        ''' Return a set of all months in the database.
        By Aby
        '''
        dates = self.get_dates()
        my_set = set()
        for date in dates:
            my_set.add(date[5:7])
        return my_set
    
    def get_day(self):
        ''' Return a set of all days in the database.
        By Aby
        '''
        dates = self.get_dates()
        my_set = set()
        for date in dates:
            my_set.add(date[8:])
        return my_set
    
    def get_date(self, date):
        ''' Return a list of all items on a given date.
        By Aby
        '''
        return len(self.runQuery('SELECT * FROM todo WHERE date = ?', (date,)))

    def runQuery(self, query, tuple, category_query=False):
        '''Return results of query as a list of dicts.'''
        home_directory = None
        if platform.system() == 'Windows':
            home_directory = os.getenv('USERPROFILE')
        else:
            home_directory = os.getenv('HOME')
        con = sqlite3.connect(home_directory + '/todo.db')
        # con= sqlite3.connect(os.getenv('USERPROFILE')+'/todo.db')
        cur = con.cursor() 
        cur.execute(query, tuple)
        if category_query:
            results = cur.fetchall()
        else:
            results = cur.fetchall()
            results = [toDict(t) for t in results]
        con.commit()
        con.close()
        return results
