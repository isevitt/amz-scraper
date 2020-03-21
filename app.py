from flask import Flask, request
import sys
from worker import run
app = Flask(__name__)

@app.route("/start", methods=["GET", "POST"])
def start_scraping():
    try:
        merchant_id = request.args.get("merchant_id")
        num_pages = request.args.get("num_pages")
        print(f"merchant id is {merchant_id}, num_pages is  {num_pages}", file=sys.stdout)
        run(merchant_id, num_pages)
        return f"request was received for merchant id:  {merchant_id}"
    
    except Exception as e:
        return f"Error {e}"

@app.route("/", methods=["GET", "POST"])
def nothing():
    return "Endpoint Not implemented"


if __name__ == '__main__':
    app.run(debug=True)
