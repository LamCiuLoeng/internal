#coding=utf8
import datetime
from datetime import datetime as dt

def format_today(_to_format='%Y-%m-%d'):
    return dt.strftime(dt.today(), _to_format)

def over_days(comp_dt, dt_now=dt.now()):
	if comp_dt and dt_now:
		return (dt_now.date() - comp_dt.date()).days
	return None
