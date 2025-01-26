import FreeCADGui

def list_all_commands():
    commands = FreeCADGui.listCommands()
    for command in commands:
        print(command)

if __name__ == "__main__":
    list_all_commands()



  