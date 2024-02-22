from prettytable import PrettyTable
import time

class Menu:
    def __init__(self, options, header): #add header
        self.options = options
        self.header = header
    
    
    def menu(self, options=None, header=None):
        if options is None:
            options = self.options
            header = self.header
        while True:
            self.display(options, header)
            choice = input('\nEnter the number corresponding to your choice: ')
            time.sleep(0.1)
            
            try:
                choice = int(choice)
                if 0 <= choice <= len(options):
                    pass
            except Exception:
                print("\nInvalid choice. Please enter a valid option.")

            if choice == 0:
                break

            selected_option = options[choice - 1][0]
            selected_action = options[choice - 1][1]
            
            try:
                selected_action()
            except TypeError:
                try:
                    header = [selected_option]
                    self.menu(selected_action, header)
                
                except Exception as e: # need thinkup what to do here
                    print(e, 'vaaaaaaaa')


                self.menu(selected_option)


    
    def display(self, options, header): #header can be =True
        # print(options) #test
        table = PrettyTable()
        table.align = 'l'
        # table.field_names = ['menu']
        table.field_names = header
        for num, (option, _) in enumerate(options, start=1): #add enumarate
            table.add_row([f'{num}. {option}'])
        if options == self.options:
            table.add_row(['0. Exit'])
        else:
            table.add_row(['0. Main Exit'])
        
        print('')
        print(table.get_string())
        print('')
