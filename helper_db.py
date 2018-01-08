import datetime

def _convert_date(data):
  date1 = data.split('-')
  return [int(x) for x in date1]

def create_dates(time_data):
  d1 = _convert_date(time_data.start_date)
  d2 = _convert_date(time_data.end_date)
  day2 = datetime.date(d2[0],d2[1],d2[2])
  day1 = datetime.date(d1[0],d1[1],d1[2]) 
  delta = day2 - day1
  dd = []
  for i in range(delta.days + 1):
      dd.append(day1 + datetime.timedelta(days=i))
  days = []
  day_week = {0: "Monday", 1: 'Tuesday', 2:' Wednesday', 3: 'Thursday', 4:'Friday', 5:"Saturday", 6:'Sunday'}
  for d in dd:
      wd = d.weekday()
      days.append((day_week[wd], d))
  return days

def get_choreographers(db_list):
  return [x for x in db_list if x.choreographer]

