from db import supabase

def test_db_connection():
    if supabase is None:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env")
    response = supabase.table("summarizations").select("*").limit(1).execute()
    
    if response.data:
        print (response.data[0])
    else:
        print ("No rows found in summarizations table")

test_db_connection()