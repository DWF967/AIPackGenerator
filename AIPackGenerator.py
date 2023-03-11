from craiyon import Craiyon
import base64
from pathlib import Path
import time
from random import randint
from PIL import Image
from os import walk as oswalk

from threading import Thread

class FileSearcher:
    
    def __init__(self, directory):
        self.__directory = directory    

    def gen_dir_list(self):
        dir_list = []

        for root, dirs, files in oswalk(self.__directory):
            for i in dirs:
                dir_list.append(Path(f'{root}/{i}'))

        return dir_list

    def gen_file_list(self, dir_list):
        file_list = []

        for i in dir_list.glob("*.png"):
            file_list.append(i.name)

        return file_list

    def gen_usable_names(self, file_list):
        names_list = []

        for i in file_list:
            str1 = i.split('.')[0]
            str1 = str1.replace('_', ' ')
            names_list.append(str1)

        return names_list

class PackGenerator:

    def __init__(self, path, request_limit=75, output_dir='generated', gen_individual_output=False):
        self.__request_limit = request_limit
        self.__output_dir = output_dir
        self.__gen_individual_output = gen_individual_output

        self.__gen = Craiyon()
        self.__file_searcher = FileSearcher(path)

        self.__dir_list = self.__file_searcher.gen_dir_list()

        self.__time_taken = []
        self.__failed_list = []

    def __calc_time_remaining(self, start, end, iter_num, list_len):
        curr_time_taken = end-start
        self.__time_taken.append(curr_time_taken)
        est_time = ((sum(self.__time_taken))/len(self.__time_taken)) * ((list_len//self.__request_limit)-iter_num)

        est_hours = est_time//60//60
        est_min = est_time//60 - est_hours*60*60
        est_sec = est_time - est_min*60

        res = f'{est_hours} hours, {est_min} minutes, {round(est_sec)} seconds.'

        return res

    def __save_image(self, generated_images, curr_directory, file_name):
        path = (Path.cwd() / f'{self.__output_dir}/assets/minecraft/textures/{curr_directory}') 
        path.mkdir(parents=True, exist_ok=True)

        with open(path / f'{file_name}.png', 'wb') as f:
            f.write(base64.decodebytes(generated_images.images[randint(0, 8)].encode('utf-8')))

    def __ai_generation(self, prompt, curr_directory, prompt_prefix):
        if prompt_prefix == '':
            if(self.__gen_individual_output): print(f"Generating: {prompt}")

            try:
                ai_res = self.__gen.generate(prompt)
            except:
                if self.__gen_individual_output: print(f'(Too many requests) Failed generating: {prompt}, will try later.')
                self.__failed_list.append((prompt, curr_directory, prompt_prefix))
                return
        else:
            prefix = prompt_prefix + ' '
            if(self.__gen_individual_output): print(f"Generating: {prefix}{prompt}")
            
            try:
                ai_res = self.__gen.generate(prefix + prompt)
            except:
                if self.__gen_individual_output: print(f'(Too many requests) Failed generating: {prompt_prefix} {prompt}, will try later.')
                self.__failed_list.append((prompt, curr_directory, prompt_prefix)) 
                return

        file_name = prompt.replace(' ', '_')
        self.__save_image(ai_res, curr_directory, file_name)

        if self.__gen_individual_output:
            if (prompt_prefix != ''): print(f"Finished generating: {prompt}.")
            else: print(f"Finished generating: {prompt_prefix} {prompt}.")

    def __regenerate(self, request_buffer=5):
        print('Regenerating failed attempts.')
        self.__time_taken.clear()

        failed_list_copy = self.__failed_list[:]

        threads = []
        active_threads = []
        counter = 0

        for i in range(len(failed_list_copy)):
            new_thread = Thread(target = self.__ai_generation, args = failed_list_copy[i])
            threads.append(new_thread)
            self.__failed_list.remove(failed_list_copy[i])

        for i in range(len(threads)):
            threads[i].start()
            active_threads.append(threads[i])
            counter += 1

            if counter == self.__request_limit:
                time.sleep(request_buffer)

                counter = 0

        for k in active_threads:
                k.join()

        if len(self.__failed_list) != 0: self.__regenerate(request_buffer)

        return

    def generate(self, prompt_prefix='', request_buffer=5):
        threads = []
        active_threads = []
        counter = 0

        for i in range(len(self.__dir_list)):
            curr_dir = str(self.__dir_list[i]).split('\\textures\\')[1]

            files = self.__file_searcher.gen_file_list(self.__dir_list[i])
            prompts = self.__file_searcher.gen_usable_names(files)

            for k in range(len(prompts)):
                new_thread = Thread(target = self.__ai_generation, args = (prompts[k], curr_dir, prompt_prefix))
                threads.append(new_thread)

        print(f'Estimated time: {(request_buffer*len(threads))//60//60} hours, {(request_buffer*len(threads))//60-((request_buffer*len(threads))//60//60)*60} minutes, {(request_buffer*len(threads))-((request_buffer*len(threads)//60)*60)} seconds')

        start_time = time.time()

        for i in range(len(threads)):
            threads[i].start()
            time.sleep(request_buffer)
            active_threads.append(threads[i])
            counter += 1

            if counter == self.__request_limit or i == len(threads) - 1:
                for k in active_threads:
                    k.join()
                counter = 0

        if len(self.__failed_list) != 0: self.__regenerate(request_buffer)

        end_time = time.time()
        time_taken = end_time-start_time
        print(f'Generation took {time_taken//60} minutes, {time_taken-((time_taken//60)*60)}')

        return
    
    def set_img_size(self, new_size):
        self.__img_size = new_size
    
    def set_request_limit(self, new_limit):
        self.__request_limit = new_limit

    def set_output_dir(self, new_dir):
        self.__output_dir = new_dir
    
class PackDecorator:
    def __init__(self, path):
        self.__path = path
        self.__file_searcher = FileSearcher(path)

        self.__dir_list = self.__file_searcher.gen_dir_list()
        self.__file_list = []
        for i in self.__dir_list: 
            file_list = self.__file_searcher.gen_file_list(i)
            for k in file_list:
                self.__file_list.append(k)
    
    def gen_pack_files(self, desc):

        return
    
    def __resize_image(self, dir, name, size):

        with Image.open(Path(dir / name)) as img:
            resized_img = img.resize((size, size))
            resized_img.save(Path(dir / name))

        return  

    def resize_images(self, size):
        threads = []
        active_threads = []

        for i in self.__dir_list:
            for k in i.glob('*.png'):
                new_thread = Thread(target = self.__resize_image, args = (i, k.name, size))
                threads.append(new_thread)

        for i in threads:
            i.start()
            active_threads.append(i)

        for i in active_threads:
            i.join()    

        print('finished')    
