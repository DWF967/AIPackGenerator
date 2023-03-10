from craiyon import Craiyon
import base64
from pathlib import Path
import time
from random import randint
from PIL import Image
from os import walk as oswalk

from threading import Thread

class PackGenerator:

    def __init__(self, path, request_limit=75, output_dir='generated', gen_individual_output=False, img_size=256):
        self.path = path
        self.__request_limit = request_limit
        self.__output_dir = output_dir
        self.__gen_individual_output = gen_individual_output

        self.__gen = Craiyon()
        self.__time_taken = []
        self.__dir_list = []

        self.__img_size = img_size

    def __calc_time_remaining(self, start, end, iter_num, list_len):
        curr_time_taken = end-start
        self.__time_taken.append(curr_time_taken)
        est_time = ((sum(self.__time_taken))/len(self.__time_taken)) * ((list_len//self.__request_limit)-iter_num)

        est_hours = est_time//60//60
        est_min = est_time//60 - est_hours*60*60
        est_sec = est_time - est_min*60

        res = f'{est_hours} hours, {est_min} minutes, {round(est_sec)} seconds.'

        return res
    
    def __gen_dir_list(self, directory):
        for root, dirs, files in oswalk(directory):
            for i in dirs:
                self.__dir_list.append(Path(f'{root}/{i}'))
        return

    def __gen_file_list(self, directory):
        file_list = []
        for i in directory.glob("*.png"):
            file_list.append(i.name)
        return file_list

    def __gen_usable_names(self, file_list):
        names_list = []

        for i in file_list:
            str1 = i.split('.')[0]
            str1 = str1.replace('_', ' ')
            names_list.append(str1)

        return names_list

    def __save_image(self, generated_images, curr_directory, file_name):
        path = (Path.cwd() / f'{self.__output_dir}/assets/minecraft/textures/{curr_directory}') 
        path.mkdir(parents=True, exist_ok=True)

        with open(path / f'{file_name}.png', 'wb') as f:
            f.write(base64.decodebytes(generated_images.images[randint(0, 8)].encode('utf-8')))

        with Image.open(Path(path / f'{file_name}.png')) as img:
            resized_img = img.resize((self.__img_size, self.__img_size))
            resized_img.save(Path(path / f'{file_name}.png'))

    def __ai_generation(self, prompt, curr_directory, prompt_prefix):
        if prompt_prefix == '':
            if(self.__gen_individual_output): print(f"Generating: {prompt}")
            ai_res = self.__gen.generate(prompt)
        else:
            prefix = prompt_prefix + ' '
            if(self.__gen_individual_output): print(f"Generating: {prefix}{prompt}")
            ai_res = self.__gen.generate(prefix + prompt)

        file_name = prompt.replace(' ', '_')
        self.__save_image(ai_res, curr_directory, file_name)

        if self.__gen_individual_output:
            if (prompt_prefix != ''): print(f"Finished generating: {prompt}.")
            else: print(f"Finished generating: {prompt_prefix} {prompt}.")

    def generate(self, prompt_prefix=''):
        self.__gen_dir_list(self.path)

        threads = []
        active_threads = []
        counter = 0

        iter_counter = 0

        for i in range(len(self.__dir_list)):
            curr_dir = str(self.__dir_list[i]).split('\\textures\\')[1]

            files = self.__gen_file_list(self.__dir_list[i])
            prompts = self.__gen_usable_names(files)

            for k in range(len(prompts)):
                new_thread = Thread(target = self.__ai_generation, args = (prompts[k], curr_dir, prompt_prefix))
                threads.append(new_thread)

        for i in range(len(threads)):
            threads[i].start()
            active_threads.append(threads[i])
            counter += 1

            if counter == self.__request_limit:
                start_time = time.time()
                iter_counter += 1

                for k in active_threads:
                    k.join()

                end_time = time.time()
                time_remaining = self.__calc_time_remaining(start_time, end_time, iter_counter, len(threads))

                print(f'Time Remaining: {time_remaining}.')

                counter = 0

        return
    
    def set_img_size(self, new_size):
        self.__img_size = new_size
    
    def set_request_limit(self, new_limit):
        self.__request_limit = new_limit

    def set_output_dir(self, new_dir):
        self.__output_dir = new_dir
    

# Testing
pack_gen = PackGenerator(Path(Path.cwd() / 'source/textures'), 75, 'output/faithful_ai', True, 16)

pack_gen.generate('Hatsune Miku')
