import config as conf
import re
import os

class TailsData:
    def __init__(self):
        self.tails = []
        self.path_to_tail = conf.tail_folder_path
        self.read_all_tails()

    def read_all_tails(self):
        files = os.listdir(self.path_to_tail)
        images = filter(lambda x: x.endswith('.png'), files)
        for img in images:
            tail_dictionary = self.create_tail_dictionary(str(img))
            self.tails.append(tail_dictionary)

    def create_tail_dictionary(self, name):
        name = name[:-4]
        tail_dictionary = {'number': name[0], 'top': name[2], 'right': name[4], 'bot': name[6], 'left': name[8], 'monastery': False, 'name': name}
        if len(name) > 10:
            tail_dictionary['monastery'] = True
        return tail_dictionary
            
