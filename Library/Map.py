from PIL import Image
import csv
from Mash.Tile import *
import pygame

class Map(object):

    map_array = []
    tile_set_height = 0
    tile_set_width = 0
    pixels = 0
    map_total_width = 0
    map_total_height = 0


    def __init__(self, tile_set_file, map_data_file):
        map_numbers, data, tiles_used_and_attributes = self.get_map_data(map_data_file)

        self.tile_set_height = data[2]
        self.tile_set_width = data[1]
        self.pixels = data[0]

        tile_list = self.get_tiles(tile_set_file)

        self.map_array = self.get_map_array(map_numbers, tiles_used_and_attributes, tile_list)

        self.map_total_height = len(self.map_array) * self.pixels
        self.map_total_width *= self.pixels
        self.entire_map = self.stitch_map()

    def stitch_map(self):
        cnt = 0
        result = Image.new('RGB', (self.map_total_width, self.map_total_height))
        for row in self.map_array:
            for tile in row:
                print(tile.properties)
                img = Image.open(tile.get_img())
                result.paste(im=img, box=(tile.x_coor, tile.y_coor))
        result.save('fullmap.png')
        return 'fullmap.png'

    # tracker and tracker_2:
    #   ONE: first four iterations in file are all data numbers (pixels, width of tileset, heiht of tileset, how many tiles used)
    #   TWO: tracker 2 loops (how many tiles used by user) times to get all the tiles that are used
    #   THREE: the rest of the data after that is all map data
    # look at the sample input file generated by Ashes java application, will make more sense

    def get_map_data(self, file_name):
        data = []
        tiles_used_and_attributes = []
        map_numbers = []
        tracker = 0
        tracker_2 = 0
        with open(file_name, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                if tracker < 4: # ONE
                    data.append(int(row[0]))
                    tracker += 1
                elif tracker_2 < data[3]: # TWO
                    tiles_used_and_attributes.append(row)
                    tracker_2 += 1
                else: # THREE
                    self.map_total_width = len(row) # this is a dirty way of getting how many tiles are in a row, later scaled by pixel
                    map_numbers.append(row)

        return map_numbers, data, tiles_used_and_attributes

    # this gets the tiles from the tile set


    def get_tiles(self, file_name):
        tiles = []
        i = 0
        img = Image.open(file_name)
        for row in range(self.tile_set_height):
            for column in range(self.tile_set_width):
                stored_name = str(i)+'.png' # stores them as .png files
                i += 1
                cropStats = (self.pixels*column, row*self.pixels, self.pixels*column+self.pixels, row*self.pixels+self.pixels)
                croppedImg = img.crop(cropStats)
                croppedImg.save(stored_name)
                tiles.append(stored_name)
        return tiles

    # this uses the stuff generate from the last 2 functions to produce the final result
    # and array of tile objects, used to draw the map
    # each tile object will get coordinates in reference to the whole mapp

    def get_map_array(self, map_numbers, tiles_used_and_attributes, tile_list):
        row_of_tiles = []
        map_array = []
        x = 0
        y = 0
        for row in map_numbers:
            for num in row:
                for details in tiles_used_and_attributes:
                    if int(details[0]) == int(num):
                        row_of_tiles.append(Tile(tile_list[int(num)], details[1:], x, y, self.pixels))
                        break
                x += self.pixels
            map_array.append(row_of_tiles)
            row_of_tiles = []
            y += self.pixels
            x = 0
        return map_array

    def get_tile(self, x, y):
        print("x:", x)
        sub = x % self.pixels
        print("sub:", sub)
        x -= sub
        print("x-sub:", x)
        x /= self.pixels
        print("x /= pixels:", x)

        print("y:", y)
        sub = y % self.pixels
        print("sub:", sub)
        y -= sub
        print("y-sub:", y)
        y /= self.pixels
        print("y /= pixels:", y)
        return self.map_array[int(y)][int(x)]


    def collide(self, li):
        t = self.get_tile(li[0], li[1])
        for thing in t.properties:
            if "blocked" == thing:
                return True
        return False













