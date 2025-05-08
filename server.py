from flask import Flask, jsonify
import requests
import bs4
from src.utils import generate_headers, handle_x_migration, get_ondemand_file_url
from src import ClientTransaction

app = Flask(__name__)

def get_transaction_generator():
    # Initialize session with required headers
    session = requests.Session()
    session.headers = generate_headers()

    # Get home page response
    home_page_response = handle_x_migration(session=session)

    # Get ondemand.s file response
    ondemand_file_url = get_ondemand_file_url(response=home_page_response)
    ondemand_file = session.get(url=ondemand_file_url)
    ondemand_file_response = bs4.BeautifulSoup(ondemand_file.content, 'html.parser')

    # Create transaction generator
    return ClientTransaction(
        home_page_response=home_page_response,
        ondemand_file_response=ondemand_file_response
    )

@app.route('/tid', methods=['GET'])
def generate_tid():
    try:
        # Default values for demonstration
        method = "GET"
        path = "/i/api/graphql/IOh4aS6UdGWGJUYTqliQ7Q/Followers"
        
        # Generate transaction ID
        ct = get_transaction_generator()
        transaction_id = ct.generate_transaction_id(method=method, path=path)
        
        return jsonify({
            "status": "success",
            "tid": transaction_id
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 