import aiosqlite

db=None

async def init():
   global db

   db=await aiosqlite.connect("reserv.db")

   await db.execute("PRAGMA foreign_keys=ON")

   await db.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT
    )
   ''')

   await db.execute('''
    CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    service TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
    )
   ''')

   await db.commit()

async def get_user_informaition(user_id):
   async with db.execute('''
   SELECT 
   id,service,date,time,status
   FROM appointments
   WHERE user_id=?
   ''',(user_id,)) as cursor:

      return await cursor.fetchall()



async def add_user(user_id,name,phone):
   await db.execute("INSERT OR IGNORE INTO users (id,name,phone) VALUES(?,?,?)",
    (user_id,name,phone))

   await db.commit()

async def add_appointment(user_id,service,date,time,status,created_at):
   await db.execute("" 
   "INSERT INTO appointments(user_id,service,date,time,status,created_at) " \
   "VALUES(?,?,?,?,?,?)",(user_id,service,date,time,status,created_at))
   await db.commit()
async def is_time_available(date,time):
   async with db.execute('''
    SELECT * FROM appointments
    WHERE date=?
    AND time=?
    AND status='active'
   ''',(date,time)) as cursor:
      appointment=await cursor.fetchone()
      return appointment is None
async def cancel_appointment(appointment_id,user_id):
   cursor=await db.execute('''
   UPDATE appointments 
   SET status='cancelled'
   WHERE id=?
   AND user_id=?
   AND status=?
   ''',(appointment_id,user_id,"active"))

   await db.commit()
   return cursor.rowcount>0
import jdatetime
async def today_status():
   today=jdatetime.date.today().strftime("%Y-%m-%d")
   async with db.execute('''
   SELECT COUNT(*),
   COALESCE(SUM(CASE WHEN status="active" THEN 1 ELSE 0 END),0),
   COALESCE(SUM(CASE WHEN status="cancelled" THEN 1 ELSE 0 END),0) 
   FROM appointments
   WHERE date=?

   ''',(today,)) as cursor:

      return await cursor.fetchone()
async def month_status():
    today = jdatetime.date.today()
    # بازه‌ی ماه شمسی جاری: از اول ماه تا آخر ماه
    first_day = today.replace(day=1).strftime("%Y-%m-%d")

    # آخرین روز ماه
    if today.month <= 6:
        last_day_num = 31
    elif today.month <= 11:
        last_day_num = 30
    else:
        last_day_num = 29  # یا 30 بسته به سال کبیسه

    last_day = today.replace(day=last_day_num).strftime("%Y-%m-%d")

    async with db.execute('''
        SELECT COUNT(*),
               COALESCE(SUM(CASE WHEN status='active' THEN 1 ELSE 0 END),0),
               COALESCE(SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END),0)
        FROM appointments
        WHERE date BETWEEN ? AND ?
    ''', (first_day, last_day)) as cursor:
        return await cursor.fetchone()

async def users_information():
   async with db.execute('''
   SELECT users.id,
   name,phone
   COUNT(appointments.id)
   FROM users
   JOIN apointments ON users.id=appointments.user_id
   GROUP BY users.id
   ''') as cursor:
      return await cursor.fetchall()
