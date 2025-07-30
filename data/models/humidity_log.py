from data import get_connection
from datetime import datetime, timedelta
from .plant import Plant

class HumidityLog:
	def __init__(self, id, plant_id, timestamp, humidity):
		self.id = id
		self.plant_id = plant_id
		self.timestamp = timestamp
		self.humidity = humidity
		
	#loggen data
	@staticmethod
	def log(plant_id, humidity):
		timestamp = datetime.now().isoformat(timespec='seconds')
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute("""
		INSERT INTO humidity_logs (plant_id, timestamp, humidity)
		VALUES (?, ?, ?)
		""", (plant_id, timestamp, humidity))
		conn.commit()
		new_id = cursor.lastrowid
		conn.close()
		return HumidityLog(new_id, plant_id, timestamp, humidity)
	
	#get latest per plant
	@staticmethod
	def get_latest_for_plant(plant_id, limit=1):
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute("""
		SELECT id, plant_id, timestamp, humidity
		FROM humidity_logs
		WHERE plant_id = ?
		ORDER BY timestamp DESC
		LIMIT ?
		""", (plant_id, limit))
		logs = [HumidityLog(*row) for row in cursor.fetchall()]
		conn.close()
		return logs
		
	#get latest logs grouped by plant
	@staticmethod
	def get_latest_logs_grouped_by_plant(limit=1):
		grouped_logs = []
		plants = Plant.get_all()
		
		for plant in plants:
			logs = HumidityLog.get_latest_for_plant(plant.id,limit)
			grouped_logs.append({
				"plant_id": plant.id,
				"logs": [
					{
						"timestamp": log.timestamp,
						"humidity": log.humidity
					}	for log in logs
				]
			})
		return grouped_logs
	
	#delete older than 2 weeks\
	@staticmethod
	def delete_old_records():
		conn = get_connection()
		cursor = conn.cursor()
		
		two_weeks_ago = datetime.now() - timedelta(weeks=2)
		cutoff_date = two_weeks_ago.strftime('%Y-%m-%d %H:%M:%S')
		
		
		query = f"""
		DELETE FROM humidity_logs
		WHERE timestamp < ?
		"""
		cursor.execute(query, (cutoff_date,))
		conn.commit()
		
		conn.close()
		
		
