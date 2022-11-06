import fpl_functions as fpl

def main_menu(df, mainDF):
    input_val = int(input("What do you want to see: \n 1) Overall Database \n 2) Your Team:\n 3) Exit \n"))
    if input_val == 1:
        main_db_menu(df, mainDF)
    else:
        quit()

def main_db_menu(df, mainDF):
    print(df)
    input_val = int(input("What do you want to do: \n 1) Search Database \n 2) Add/Remove a column \n 3) Sort Database \n 4) Back to previous menu\n"))
    if input_val == 1:
        search_db_menu(df,df, mainDF)
    elif input_val  == 2:
        column_menu(df, mainDF)
    elif input_val == 3:
        sort_menu(df, mainDF)
    else:
        main_menu(df, mainDF)
        

# add further optional columns
def column_menu(df, mainDF):
    input_val = int(input("What column do you want to add or remove\n  1) Bonus Points\n"))
    if input_val == 1:
        val = 'bonus'
    else:
        val = ''
        main_db_menu(df, mainDF)    
    if val in df:
        df = fpl.remove_column(val, df)
    else:
        df = fpl.add_column(val, df, mainDF)
    main_db_menu(df, mainDF)

def sort_menu(df, mainDF):
    input_val = int(input("What column do you want to sort by\n1) Total Points\n2) Name\n"))
    if input_val == 1:
        sorted_db = fpl.sort_db('total_points', df)
        print(sorted_db)

def search_db_menu(df, odf, mainDF):
    print(df)
    input_val = int(input("What do you want to search: \n 1) Name \n 2) Team \n 3) Position \n 4) Reset Database\n 5) Back to previous menu (will reset search) \n"))
    searched_df = df
    if input_val == 1:
        run = True
        while run == True:
            search_input = input("Player Name(Leave empty to return to previous menu): ")
            if search_input =="":
                run == False
                search_db_menu(searched_df, odf, mainDF)
            else:
                searched_df = fpl.filter_name(df, search_input)
                print(searched_df)
    elif input_val == 2:
        run = True
        while run == True:
            search_input = input("Team Name (Leave empty to return to previous menu): ")
            if search_input =="":
                run == False
                search_db_menu(searched_df, odf, mainDF)
            else:
                searched_df = fpl.filter_team(df, search_input)
                print(searched_df)
    elif input_val == 3:
        run = True
        while run == True:
            search_input = int(input("Position:\n 1) GK\n 2) DEF\n 3) MID\n 4) FWD\n 5) Back to previous menu "))
            if search_input == 1:
                search_input = "GK"
            elif search_input == 2:
                search_input = "DEF"
            elif search_input == 3:
                search_input = "MID"
            elif search_input == 4:
                search_input = "FWD"
            else:
                run == False
                search_db_menu(searched_df, odf, mainDF)
            searched_df = fpl.filter_pos(df, search_input)
            print(searched_df)

    elif input_val == 4:
        searched_df = fpl.reset_df(odf)
        search_db_menu(searched_df, odf, mainDF)

    elif input_val == 5:
        main_db_menu(odf, mainDF)