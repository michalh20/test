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
