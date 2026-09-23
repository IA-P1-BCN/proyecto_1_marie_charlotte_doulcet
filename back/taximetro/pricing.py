def calculate_segment(state, duration_seconds, rates):
    if state == "stopped":
        rate = rates["stopped_rate"]
    elif state == "moving":
        rate = rates["moving_rate"]
    else:
        raise ValueError(f"Unknown state: {state}")
    return duration_seconds * rate 

def format_amount(amount):
    return f"{amount:.2f}"