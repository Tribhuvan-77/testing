from pathlib import Path



def Directory_Tree(path:str)->str:
    directory_context=""
    root=Path(path)
    for item in root.iterdir():
        if item.is_dir():
            directory_context+="\n"+item.name+"\n"
            for i in item.iterdir():
                directory_context+=i.name+"\n"
        if item.is_file():
            directory_context+=item.name+"\n"
    return directory_context
    
