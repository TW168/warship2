import datetime
import pytz


def get_current_datetime(timezone='America/Chicago'):
    """
    Get the current time in the specified time zone.

    Parameters:
        timezone (str): The name of the time zone to convert to. Default is 'America/Chicago'.

    Returns:
        datetime: The current time in the specified time zone.
    """
    # Get the current datetime in UTC timezone
    current_datetime_utc = datetime.datetime.now(pytz.utc)
    # Convert UTC datetime to the specified time zone
    target_timezone = pytz.timezone(timezone)
    current_datetime_target = current_datetime_utc.astimezone(target_timezone)
    return current_datetime_target