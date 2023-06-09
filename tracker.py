"""This portion of the menu was implemented as a team and was done primarily on Aaron's computer. We met as a group and collaborated behind
Aaron's computer."""
from transaction import TodoList
import sys
import datetime #used for date comprehension 

# here are some helper functions ...
p_states = ["quit", "show categories", "add category", "modify category", "show transactions", "add transaction", "delete transaction", "summarize transactions by date", "summarize transactions by month", "summarize transactions by year", "summarize transactions by category", "print this menu"]

class IllegalDateField(Exception):
    """Raise when backend attempts to go down an out of bounds flow path for date, may only be 0, 1 or 2"""

def get_valid_category():
    """Checks if a category is valid, by Rue"""
    while True:
        category = input("Please enter a category name: ").strip()
        if not category:
            print("Category cannot be empty or just whitespace. Please try again.")
        else:
            return category

def valid_num(message):
    """Checks if a numeric argument is numeric, by Aaron"""
    num = ""
    while type(num) != int:
        try:
            num = int(num)
        except ValueError:
            num = input(message)
    return num

def validate_date(flow_path:int):
    """Written by rue, validates the dates passed"""
    while True:
        try:
            print("Please enter a valid ",end = "")
            if flow_path == 0:
                mydate = input("day")
                datetime.date(year=2022, month=1, day=int(mydate))
                return mydate
            elif flow_path == 1:
                my_date = input("month")
                datetime.date(year=2022, month=int(my_date), day=1)
                return my_date
            elif flow_path == 2:
                my_date = input("year")
                datetime.date(year = int(my_date), month = 1, day = 1)
                return my_date
            else:
                raise IllegalDateField("Cannot have date that is not part of day, month, year")
        except ValueError:
            print("Please correct the date field")

            
def print_usage():
    ''' print an explanation of how to use this command, by Aby '''
    count  = 0
    for x in p_states:
        print(str(count) + ". "+ x)
        count += 1
        
def print_todos(todos):
    ''' print the todo items, by Eugenio '''
    if len(todos)==0:
        print('no tasks to print')
        return
    print('\n')
    print("%-10s %-10s %-20s %-12s %-30s" % ('item #', 'amount', 'category', 'date', 'description'))
    print('-' * 80)
    for item in todos:
        values = tuple(item.values()) 
        print("%-10s %-10s %-20s %-12s %-30s" % values)



def print_categories(categories):
    """Function print_categories prints categories, by Rue"""
    if len(categories) == 0:
        print("No categories entered")
    else:
        print("Categories")
        print('-' * 10)
        for x in categories:
            print(x[0])
    print('-' * 10)


def process_args(arglist, todolist):
    ''' examine args and make appropriate calls to TodoList, by Eugenio and Rue'''
    arg = arglist
    if arglist == None:
        print_usage()

    elif arg == p_states[0]:
        print("goodbye")
    elif arg == p_states[9]:
        my_years = todolist.my_years()
        my_years = list(my_years)
        if(my_years is not None):
            my_list = todolist.selectAll()
            year_list = []
            for year in my_years:
                count = sum(1 for item in my_list if item['date'].startswith(year))
                year_list.append(count)
            print("Items by year:")
            for x in range(len(year_list)):
                print(f'{my_years[x]}:   {year_list[x]}')
        else:
            print("There are no items in the list to account for by year.")
    elif arg == p_states[1]:
        #vanilla 
        print_categories(todolist.selectCategories())
    elif arg == p_states[2]:
        catbool = todolist.add_category(get_valid_category())
        if catbool is True:
            print("This category already exists, will not be duplicated in the category set")
        else:
            print("Category added")
    elif arg == p_states[5]:
        #add transaction
        task = {}
        task['item #'] = valid_num("Please enter a valid item # ")
        task['amount'] = valid_num("Please enter the amount ")
        task['category'] = input("Please enter a category ").lstrip()
        day = validate_date(0)
        month = validate_date(1)
        year = validate_date(2)
        task['date'] = datetime.date(year=int(year), month=int(month), day=int(day))
        task['description'] = get_valid_category()
        todolist.add(task)
        
    # Test date, get date (test types needed)
    elif arg == p_states[7]:
        day = validate_date(0)
        month = validate_date(1)
        year = validate_date(2)
        my_date = datetime.date(year=int(year), month=int(month), day=int(day))
        print(f'There were {todolist.get_date(my_date)} transactions on {my_date}.')
        
    elif arg == p_states[4]:
        print_todos(todolist.selectAll())
    #deletion
    elif arg.startswith(p_states[6]):
        arg = arg.lstrip(p_states[6])
        todolist.delete(arg)
    elif arg == p_states[10]:
        my_categories = [category[0] for category in todolist.selectCategories()]
        my_list = todolist.selectAll()
        category_list = []
        for category in my_categories:
            count = sum(1 for item in my_list if item['category'] == category)
            category_list.append(count)
        print("Items by category:")
        for x in range(len(category_list)):
            print(f'{my_categories[x]}:   {category_list[x]}')
    elif arg == p_states[11]:
        print_usage()

    elif arg == p_states[8]:
        # get all transactions and group them by month
        transactions = todolist.selectAll()
        transactions_by_month = {}
        for transaction in transactions:
            date_obj = datetime.datetime.strptime(transaction['date'], "%Y-%m-%d")
            month = date_obj.month
            year = date_obj.year
            key = f"{year}-{month:02d}"
            if key in transactions_by_month:
                transactions_by_month[key].append(transaction)
            else:
                transactions_by_month[key] = [transaction]

        # print the transactions by month
        if len(transactions_by_month) == 0:
            print("No transactions found.")
        else:
            for key in sorted(transactions_by_month.keys()):
                print(f"Transactions for {key}:")
                print_todos(transactions_by_month[key])
        
    elif arg.startswith(p_states[3]):
        arg = arg[len(p_states[3]):]
        arg = arg.lstrip()
        while True:
            my_input = input("What should the new category be?")
            if(my_input.strip() == ""):
                continue
            else:
                todolist.update_category(arg, my_input)
                break      
    
def main():
    """This main method written as a team on Aaron's computer."""
    todolist = TodoList()
    if len(sys.argv) == 1:
        print_usage()
        args = ""
        while args != 'quit':
            args = input("Enter a choice ")            
            process_args(args,todolist)
            print('-'*40+'\n')
    else:
        # read the args and process them
        args = sys.argv[1:]
        process_args(args, todolist)
        print('-'*40+'\n'*3)

if __name__ == "__main__":
    main()

