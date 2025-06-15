from flask import Flask, jsonify, request
import threading
from scheduler import scrape_task
import schedule
import time

app = Flask(__name__)

# Store the scheduler thread
scheduler_thread = None

def run_scheduler():
    """Run the scheduler in a separate thread"""
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/start', methods=['POST'])
def start_scheduler():
    """Start the scheduler"""
    global scheduler_thread
    if not scheduler_thread or not scheduler_thread.is_alive():
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        return jsonify({"status": "success", "message": "Scheduler started"})
    return jsonify({"status": "warning", "message": "Scheduler is already running"})

@app.route('/stop', methods=['POST'])
def stop_scheduler():
    """Stop the scheduler"""
    global scheduler_thread
    if scheduler_thread and scheduler_thread.is_alive():
        schedule.clear()
        scheduler_thread = None
        return jsonify({"status": "success", "message": "Scheduler stopped"})
    return jsonify({"status": "warning", "message": "Scheduler is not running"})

@app.route('/run-now', methods=['POST'])
def run_now():
    """Run scraping task immediately"""
    try:
        scrape_task()
        return jsonify({"status": "success", "message": "Scraping task completed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)