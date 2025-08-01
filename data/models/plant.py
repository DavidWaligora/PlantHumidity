from data import get_connection
import sqlite3

class Plant:
	def __init__(self, id, name):
		self.id = id
		self.name = name
	
	#add plant
	@staticmethod
	def add(name):
		conn = get_connection()
		cursor = conn.cursor()
		try:
			cursor.execute("INSERT INTO plants (name) VALUES (?)", (name,))
			conn.commit()
			new_id = cursor.lastrowid
			conn.close()
			return Plant (new_id, name)
		except sqlite3.IntegrityError:
			conn.close()
			return None
	
	#get by id
	@staticmethod
	def get_by_id(plant_id):
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT id, name FROM plants WHERE id = ?", (plant_id,))
		row = cursor.fetchone()
		conn.close()
		if row:
			return Plant(id=row[0], name=row[1])
		return None
		
		
	#get all plants
	@staticmethod
	def get_all():
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT id, name FROM plants")
		rows = cursor.fetchall()
		conn.close()
		return [Plant(id=row[0], name=row[1]) for row in rows]
	
	#delete a plant
	@staticmethod
	def delete(plant_id):
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
		rows_affected = cursor.rowcount
		conn.commit()
		conn.close()
		return rows_affected > 0
	
	@staticmethod
	def update(plant_id, plant_name):
		conn = get_connection()
		cursor = conn.cursor()
		try:
			cursor.execute("UPDATE plants SET name = ? WHERE id = ?", (plant_name, plant_id))
			conn.commit
			conn.close()
			return Plant (plant_id, plant_name)
		except:
			conn.close()
			return None
	
	#check if plant exists
	@staticmethod
	def exists(plant_id):
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT 1 FROM plants WHERE id = ?", (plant_id,))
		exists = cursor.fetchone() is not None
		conn.close()
		return exists
