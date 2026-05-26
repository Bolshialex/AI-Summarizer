from backend.db import supabase

def test_db_connection():
    response = supabase.table("summarizations").select("*").limit(1).execute()
    
    if response.data:
        print (response.data[0])
    else:
        print ("No rows found in summarizations table")

test_db_connection()