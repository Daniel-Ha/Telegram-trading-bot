"""
extract_all_info_from_message
Usage: called by handle_notification_creation to extract all the information from the message into variables to use

Terms to clarify:
notification parameters: query parameters, condition
query parameters: parameters used to run the Dune query (not including query_id)
"""

import re

###### EXTRACT_ALL_INFO_FROM_MESSAGE() ######
#function to get all the parameters from  message
def extract_all_info_from_message(message, query_id):
    #get user info
    user_info = get_user_info(message)
    #Split message into the notification parameters and the notification name
    notif_parameters, notif_name = extract_notif_name(message)
    #get query parameters from notification parameters and format them
    query_parameters = extract_and_format_query_parameters(notif_parameters)
    #get condition from notification parameters
    condition = extract_and_format_condition(notif_parameters)
    return user_info, query_id , query_parameters, condition, notif_name

###### EXTRACT_ALL_INFO_FROM_MESSAGE() HELPER FUNCTIONS ##########

# Function to get user info from message
def get_user_info(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    return [user_id, first_name]

# Function to split message into the notification parameters and the notification name
def extract_notif_name(message):
    # Extracting the message text from the provided message structure
    msg_text = message.text
    
    # Splitting the message text by smart quotes to extract the notification name
    parts = msg_text.split('"')
    print(parts)
    if len(parts) < 2:
        print("Error: Notification name not found.")
        return None, None
    
    # Further split the second part by smart quote to isolate the notification name
    notif_name_parts = parts[1].split('”')
    if len(notif_name_parts) < 1:
        print("Error: Incorrect notification name format.")
        return None, None
    
    notif_name = notif_name_parts[0]
    
    # Assuming the parameters are the part of the message before the notification name
    notif_parameters = parts[0].split()[1:]  # Splitting by space and removing the command part
    
    return notif_parameters, notif_name

#function to get and format the query parameters from the notification parameters
def extract_and_format_query_parameters(msg_array):
    parameters = []
    # Loop through everything except for the last bit of message
    if msg_array:
        parameters_in_msg_array = msg_array[:len(msg_array) - 1]
        for parameter in parameters_in_msg_array:
            parameter_info = parameter.split('=', 1)
            parameters.append(tuple(parameter_info))  # Convert to tuple
        if len(parameters) >= 1:
            return parameters
    else:
        return False


#function to get and format the condition from the notification parameters
def extract_and_format_condition(msg_array):
    raw_condition = ''.join(msg_array[len(msg_array) - 1:])  # Join the last element of the array into a single string
    condition = re.split(r'(<=|>=|<|>|=)', raw_condition)  # Split using regular expression
    condition = [c for c in condition if c]  # Remove empty strings from the result
    return condition