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

        tail_dictionary = {'number': int(name[:2]), 'top': name[3], 'right': name[5], 'bot': name[7], 'left': name[9], 'name': name, 
        'monastery': False, 'city_mark': False, 'city': False, 'end_point': False, 'road': False}

        special_signs = {'m': 'monastery', 'k': 'city_mark', 'g': 'long_city', 'l': 'corner_long_city', 'x': 'cross_road'}
        check_side_loop_list = ['top', 'right', 'bot', 'left']

        for key, value in special_signs.items():
            if name.find(key) > 0:
                if value == 'long_city':
                    tail_dictionary['city'] = ['left', 'right']
                elif value == 'cross_road':
                    tail_dictionary['end_point'] = True
                elif value == 'monastery':
                    tail_dictionary[value] = True
                    if tail_dictionary["bot"] == 'r':
                        tail_dictionary['end_point'] = True
                        tail_dictionary['road'] = ['bot']
                elif value == 'corner_long_city':
                    tail_dictionary['city'] = True
                else:
                    tail_dictionary[value] = True
            
        # Full city case
        if tail_dictionary["top"] == tail_dictionary["bot"] == tail_dictionary["left"] == tail_dictionary["right"] == 'c':         
            tail_dictionary["city"] = ['left', 'top', 'right', 'bot']
            return tail_dictionary

        if tail_dictionary["left"] == tail_dictionary["top"] == tail_dictionary["right"] == 'c':         
            tail_dictionary["city"] = ['left', 'top', 'right']
            if tail_dictionary["bot"] == 'r':
                tail_dictionary['end_point'] = True
                tail_dictionary['road'] = ['bot']
            return tail_dictionary

        if tail_dictionary["top"] == tail_dictionary["bot"] == 'r' and not tail_dictionary['end_point']:
            tail_dictionary['road'] = ['top', 'bot']

        if tail_dictionary["left"] == tail_dictionary["right"] == 'r' and not tail_dictionary['end_point']:
            tail_dictionary['road'] = ['left', 'right']

        
        for i in range(len(check_side_loop_list)):
            prev_side = tail_dictionary[check_side_loop_list[i-1]]
            current_side = tail_dictionary[check_side_loop_list[i]]
        
            if current_side == prev_side == "c":
                tail_dictionary['city'] = [check_side_loop_list[i], check_side_loop_list[i-1]]
            if current_side == prev_side == "r" and not tail_dictionary['end_point']:
                tail_dictionary['road'] = [check_side_loop_list[i-1], check_side_loop_list[i]]
        
        return tail_dictionary


tail_data = TailsData()
print(tail_data.tails)
