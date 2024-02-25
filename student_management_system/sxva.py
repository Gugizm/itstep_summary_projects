from prettytable import PrettyTable


class Display:
    def __init__(self, table_fields):
        super().__init__()
        self._table_fields = table_fields

    def menu(self, options, header, main=False): #header can be =True
        table = PrettyTable()
        table.align = 'l'
        vanga = ' ' * 10
        lavanda = vanga + header + vanga
        table.field_names = [lavanda]
        for num, (option, _) in enumerate(options, start=1): #add enumarate
            table.add_row([f'{num}. {option}'])
        if main:
            table.add_row(['0. Exit'])
        else:
            table.add_row(['0. Back'])
        
        print('')
        print(table.get_string())
        print('')


    def table(self, objects):
        table = PrettyTable()
        table.field_names = (self._table_fields)
        if isinstance(objects, list):
            for obj in objects:
                table.add_row(obj.attribute_list())
        else:    
            table.add_row(objects.attribute_list())
        print(table.get_string())


    def prompt(self, header, text):
        table = PrettyTable()
        table.field_names = [header]
        table.add_row([text])
        print(table.get_string())
                    

    
    def error(self, error):
        table = PrettyTable()
        table.field_names = ['ERROR!']
        table.add_row([error])
        print(table.get_string())