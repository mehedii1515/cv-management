# def GetOutputFormat() -> str:
#     with open(Config.PROMPT_FILE,'r') as stream:
#         try:
#             prompt_data = yaml.safe_load(stream)
#             return prompt_data[0]
#         except Exception as ex:
#             print("{0} error occured. Arguments: {1}".format(type(ex).__name__), ex.args)

'''def PerformForFilesInFolders(Folder : str):
    for (root,dirs,files) in os.walk(Folder, topdown=True):
        for file in files:
            if ".doc" in file:
                filetocheck = os.path.join(root, file)
                if IsResume(filetocheck): print(f"{file} is a resume.")
                else: print(f"{file} is not a resume.")'''
                