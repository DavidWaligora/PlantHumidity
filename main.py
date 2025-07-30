from data import create_all_tables
from services import app
from services import log_forever
import threading

# run main script
def main():
	print("Program started")	
	create_all_tables

	# Start log_forever in a separate thread
	log_thread = threading.Thread(target=log_forever, daemon=True)
	log_thread.start()

	# Run the Flask app (main thread)
	app.run(host='0.0.0.0', port=5000, debug=True)
	
	
if __name__ == "__main__":
	main()

