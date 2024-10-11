
userid_to_state_mapping = {}

def should_allow(event:dict)->bool:
    userid = event["userid"]
    current_timestamp = int(event["timestamp"])
    if userid not in userid_to_state_mapping.keys():
        # Add to map
        constructed_state = {"last_timestamp":current_timestamp, "count":1}
        userid_to_state_mapping[userid] = constructed_state
    else:
        existing_state = userid_to_state_mapping[userid]
        last_timestamp = existing_state["last_timestamp"]
        count = existing_state["count"]
        #if timediff_mins(last_timestamp,)