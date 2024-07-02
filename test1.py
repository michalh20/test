from mitmproxy import http
import json

def response(flow: http.HTTPFlow) -> None:
    # Check if the request URL matches the target URL
    if flow.request.pretty_url == "https://courier-api.wolt.com/courier-api/me/cash_balance":
        # Load the response body as JSON
        response_json = json.loads(flow.response.text)
        
        # Check if the response contains the "balance" key
        if "balanceData" in response_json and "balance" in response_json["balanceData"]:
            # Modify the balance number to 99999
            response_json["balanceData"]["balance"] = 99999
            
            # Convert the modified JSON back to a string
            flow.response.text = json.dumps(response_json)
    if flow.request.pretty_url == "https://courier-api.wolt.com/courier-api/poll":
        # Load the response body as JSON
        response_json = json.loads(flow.response.text)
        target_addresses = ["Borova", "Borová", "borova", "borová", "Bratislavská cesta 1"]
        # Function to check if any address matches the target addresses
        def check_addresses(data):
            address_found = False
            if isinstance(data, dict):
                for key, value in data.items():
                    if key == "address":
                        if value in target_addresses:
                            address_found = True
                    elif key == "name" and isinstance(value, dict) and "en" in value:
                        if address_found:
                            value["en"] = "XXXXXX"
                    else:
                        address_found = check_addresses(value) or address_found
            elif isinstance(data, list):
                for item in data:
                    address_found = check_addresses(item) or address_found
            return address_found
        
        # Start checking the addresses in the response JSON
        check_addresses(response_json)
        
        # Convert the modified JSON back to a string
        flow.response.text = json.dumps(response_json)
    
