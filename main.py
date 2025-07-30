from data import create_all_tables
from services import app
from services import log_forever

# run main script
def main():
	print("Program started")	
	create_all_tables
	app.run(host='0.0.0.0', port=5000, debug=True)
	log_forever()
	
	
if __name__ == "__main__":
	main()
	
