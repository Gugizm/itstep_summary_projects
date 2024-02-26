from prettytable import PrettyTable
import sys
import time
# from sxva import Display

class Menu:
    def __init__(self, options, header, display): #add header
        self.options = options
        self.header = header
        self.display = display
    
    
    def menu(self, options=None, header=None):
        if options is None:
            options = self.options
            header = self.header

        while True:
            if self.options == options:
                self.display.menu(options, header, main=True)
            else:
                self.display.menu(options, header)

            try:
                choice = input('\nEnter the number corresponding to your choice: ')
                time.sleep(0.1)
                
                try:
                    choice = int(choice)
                    if 0 <= choice <= len(options):
                        pass
                    else:
                        raise ValueError
                except Exception:
                    print("\nInvalid choice. Please enter a valid option.")
                    continue

                if choice == 0:
                    break

                else:
                    selected_option, selected_action  = options[choice - 1]
                        
                    try:
                        selected_action()
                    except Exception:
                        try:
                            header = selected_option
                            self.menu(selected_action, header)
                        
                        except Exception as e:
                            print(f"Unexpected characters were entered {e}")
                            print(f"Try enter again")
            
            except EOFError:
                print('Received EOF (End of File) signal.')
                print("Exiting the program.")
                print('Goodbye.....')
                sys.exit()
                    # print(selected_option, 'what is that!!!!!!!!!')
                    # self.menu(selected_option)

            except KeyboardInterrupt:
                print("Received KeyboardInterrupt (Ctrl+C)")
                print("Exiting the program.")
                print('Goodbye.....')
                sys.exit()

            except Exception as e:
                print(f"Unexpected characters were entered {e}")
            
                

    
    # def display(self, options, header): #header can be =True
    #     table = PrettyTable()
    #     table.align = 'l'
    #     table.field_names = [header]
    #     for num, (option, _) in enumerate(options, start=1): #add enumarate
    #         table.add_row([f'{num}. {option}'])
    #     if options == self.options:
    #         table.add_row(['0. Exit'])
    #     else:
    #         table.add_row(['0. Back'])
        
    #     print('')
    #     print(table.get_string())
    #     print('')
