# AIPackGenerator

A python module for generating AI generated Minecraft resource packs. It utilizes the [Craiyon](https://www.craiyon.com/) image generating AI through the [Craiyon.py]() API wrapper.

## Getting started
Create an instance of the `PackGenerator` class:

```py
from pathlib import Path
from AIPackGenerator import PackGenerator, PackDecorator

pack_gen = PackGenerator(Path(Path.cwd() / 'source/textures'), 1000, 'output/pack_output', False)
```

This class takes 4 parameters:
1. ___The path to the source textures folder.___ The PackGenerator will use this to figure out the file names for all the textures, as well as the correct directories to place the textures in. This documentation will not go over how to get the base Minecraft textures; please refer to [this](https://minecraft.fandom.com/wiki/Tutorials/Creating_a_resource_pack#:~:text=packs%20are%20loaded.-,Accessing%20the%20vanilla%20resources,open%20.jar%20files%20simply%20change%20the%20extension%20from%20.jar%20to%20.zip.,-Modifying%20an%20entity%27s) article in the Minecraft wiki in order to firgure out how to extract the game's base textures. 
2. ___The request amount limit.___ This defines how many requests to the Craiyon API can be active at one time.
3. ___The output folder.___ This defines the directory that the AI generated resource pack will output to. **You do not have to define the current working directory as it automatically outputs there. Only define the folder name that you want it to output to.**
4. ___Whether or not it will output to the console when generating.___ This defines whether or not the generator will output what it's currently generating to the console. Since it generates a lot of files at once, it is recommended to set this to `False` so that it doesn't spam the console.

### Generating the images
In order to generate the pack, you need to call the `generate()` function:

```py
pack_gen.generate('prefix', 0.25)
```

This function takes 2 parameters:
1. ___The prefix used when generating the pack.___ This means that the generator will attach the prefix before each prompt that is submitted to Craiyon (i.e. a prompt for a grass block, "grass block," becomes "prefix grass block," with prefix being whatever was input into the prefix parameter). 
2. ___The time delay in seconds between each request.___

## Making the output a usable resource pack

Finally, to create a usable resource pack and add resource pack files such as the `pack.mcmeta` or `pack.png` files, an instance of `PackDecorator` needs to be created.

```py
decorator = PackDecorator(Path(Path.cwd() / 'output/pack_output/')
```

The `PackDecorator` class only takes one parameter: the directory where the `PackGenerator` output all of its files.

###### Resizing images
Since Craiyon generates images that are 1024x1024, we need to resize them in order for Minecraft to recognize the pack as a valid pack. To do this, we can call the `resize_images` function in `PackDecorator`.

```py
decorator.resize_images(128)
```

This function takes one parameter, which is the new image size. It is recommended that multiples of 2 (i.e. 16x, 32x, 64x, etc.) be used.

### Adding relevant pack files
In order to add the `pack.mcmeta` and `pack.png` files to the resource pack, we need to call the `gen_pack_files()` function.

```py
decorator.gen_pack_files("prefix", 12)
```

This function takes 2 parameters: 
1. ___A prefix for generating `pack.png`.___ When the image is generated, Craiyon is prompted with "pack.png." If you choose to add a prefix, it will add that prefix before the "pack.png" in the prompt. 
2. ___The resource pack format that will be set in the `pack.mcmeta` file.___ Mojang increases the format number when they make drastic changes to the resource pack format that would break compatability with previous game versions. Please refer to the [Minecraft wiki](https://minecraft.fandom.com/wiki/Pack_format) in order to figure out which format number to use for your version.
