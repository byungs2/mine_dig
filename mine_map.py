#TODO : add Wall class, Flag class, The case of when the map has no block but only mines 
import random

def color_print(string, type, color_str):
	if(type == '*'):
		string = '\033[' + color_str[0] + 'm' + string + '\033[0m'
		print(string, end='')
	elif(type == '#'):
		string = '\033[' + color_str[1] + 'm' + string + '\033[0m'
		print(string, end='')
	else:
		string = '\033[' + color_str[2] + 'm' + string + '\033[0m'
		print(string, end='')

class Element:
	def __init__(self, x, y, shape_of_element, type):
		self.x = x
		self.y = y
		self.type = type
		self.shape = shape_of_element
		self.surface_block = "#"
		self.is_visited = 0

# game_result : 1 (win) :: 2 (lose) :: 0 (neutral) 
class Mine_Map:
	def __init__(self, m, n):
		self.color_list = ['31', '35', '34']
		self.elements_cnt = m*n
		self.mine_cnt = 0
		self.m = m
		self.n = n
		self.map = []
		for i in range(m+2):
			self.tmp = []
			for j in range(n+2):
				self.tmp.append(None)
			self.map.append(self.tmp)
		self.game_result = 0 		
		self.padding_x = n + 2
		self.padding_y = m + 2
		for i in (0, m+1):
			for j in range(n+2):
				self.map[i][j] = '@'
		for i in (0, n+1):
			for j in range(m+2):
				self.map[j][i] = '@'

	def set_elements(self, x, y, element):
		self.map[x][y] = element
		if(element.shape == '*'):
			self.find_and_add(x, y, element)
				
	def find_and_add(self, x, y, element):
		offset = (-1 ,0, 1)
		for i in offset:
			for j in offset:
				if(self.map[x+i][y+j] == '@' or (i == 0 and j == 0)):
					continue
				elif(self.map[x+i][y+j] == None):
					self.map[x+i][y+j] = Block(x+i, y+j, 1, "block")
				elif(self.map[x+i][y+j].type == "block"):
					if(self.map[x+i][y+j].shape == 'B'):	
						self.map[x+i][y+j].shape = 1
					else: 
						self.map[x+i][y+j].shape += 1

	def interaction_with_element(self, x, y):
		self.map[x][y].interaction(self)
		self.show_neutral_map()		

	def show_init_map(self):
		for i in range(1, self.m+1):
			for j in range(1, self.n+1):
				color_print(' '+str(self.map[i][j].surface())+' ', self.map[i][j].surface_block, self.color_list)
			print('')

	def show_lose_map(self):
		for i in range(1, self.m+1):
			for j in range(1, self.n+1):
				color_print(' '+str(self.map[i][j].digging())+' ', self.map[i][j].shape, self.color_list)
			print('')
		print("You Lose\n")

	def show_win_map(self):
		for i in range(1, self.m+1):
			for j in range(1, self.n+1):
				color_print(' '+str(self.map[i][j].digging())+' ', self.map[i][j].shape, self.color_list)
			print('')
		print("You Win\n") 

	def show_neutral_map(self):
		for i in range(1, self.m+1):
			for j in range(1, self.n+1):
				color_print(' '+str(self.map[i][j].surface())+' ', self.map[i][j].surface_block, self.color_list)
			print('')

	def game_setting(self, level):
		for i in range(1, self.m+1):
			for j in range(1, self.n+1):
				if(random.random() <= level):
					mine = Mine(i, j, '*', "mine")
					self.set_elements(mine.x, mine.y, mine)
					self.mine_cnt += 1
				elif(self.map[i][j] != None):
					continue
				else:
					block = Block(i, j, 'B', "block")
					self.set_elements(block.x, block.y, block)


class Mine(Element):
	def interaction(self, mine_map):
		mine_map.game_result = 2
		self.surface_block = self.shape		
		mine_map.show_lose_map()

	def digging(self):
		return self.shape
		
	def surface(self):
		return self.surface_block

class Block(Element):
	def interaction(self, mine_map):
		if(self.is_visited == 0):
			self.is_visited = 1
			mine_map.elements_cnt -= 1
			if(self.shape == 'B'):
				self.auto_interaction(mine_map)
			else:
				self.surface_block = self.shape	
		else:
			print("You already has been visited here before")

	def auto_interaction(self, mine_map):
		mine_map.map[self.x][self.y] = Discoverd_Block(self.x, self.y, 'C', 'Discover')
		offset = (-1, 0, 1)
		for i in offset:
			for j in offset:
				if(mine_map.map[self.x+i][self.y+j] == '@' or (i == 0 and j == 0)):
					continue
				elif(mine_map.map[self.x+i][self.y+j].type == "block" and mine_map.map[self.x+i][self.y+j].is_visited == 0): 
					mine_map.map[self.x+i][self.y+j].interaction(mine_map)

	def digging(self):
		return self.shape
		
	def surface(self):
		return self.surface_block

#TODO	
#class Mine_Flag(Element):
#class Wall(Element):

class Discoverd_Block(Element):
	def __init__(self, x, y, shape_of_element, type):
		self.x = x
		self.y = y
		self.type = type
		self.shape = shape_of_element
		self.surface_block = shape_of_element

	def interaction(self, mine_map):
		print("This block already has been found")

	def digging(self):
		return self.shape

	def surface(self):
		return self.surface_block	

if __name__ == '__main__':
	map_size = [int(i) for i in input("Input column and row length (ex : 5 5) :: ").split(' ')]
	level = float(input("Input the level of game in range 0 to 1. (ex : 0.2) :: "))
	Map = Mine_Map(map_size[0], map_size[1])
	Map.game_setting(level)
	Map.show_init_map()

	#game loop
	while Map.game_result == 0:
		coordinate_instruction = [int(i) for i in input("Input coordinate of the map :: (eg 3 4) :: ").split(' ')]
		Map.interaction_with_element(coordinate_instruction[0], coordinate_instruction[1])	
		if(Map.mine_cnt == Map.elements_cnt):
			print("###########################")
			print("###########################")
			print("###########################")
			Map.show_win_map()
			break













