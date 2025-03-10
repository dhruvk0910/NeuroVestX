# Setting Up Supabase for NeuroVestX

## 📌 Prerequisites
- A **Supabase** account ([Sign up here](https://supabase.com/))
- A **new Supabase project**
- Python installed on your system

---

## 🛠️ Step 1: Create a New Supabase Project
1. Go to [Supabase](https://supabase.com/).
2. Sign in and **create a new project**.
3. Note down your **Supabase URL** and **API Key** from the **Project Settings → API** section.

---

## 📂 Step 2: Set Up the `stock_data` Table
1. In the **Supabase Dashboard**, navigate to **Database → Tables**.
2. Click **Create a new table** and set the table name as **`stock_data`**.
3. Add the following columns:

| Column Name | Data Type  | Constraints               |
|------------|-----------|--------------------------|
| `symbol`   | TEXT      | PRIMARY KEY, NOT NULL   |
| `date`     | TIMESTAMP | NOT NULL                |
| `open`     | FLOAT8    | NOT NULL                |
| `high`     | FLOAT8    | NOT NULL                |
| `low`      | FLOAT8    | NOT NULL                |
| `close`    | FLOAT8    | NOT NULL                |
| `volume`   | NUMERIC   | DEFAULT: `0`            |

4. Click **Save** to create the table.

---

## 🔑 Step 3: Configure Supabase Authentication
1. Go to **Authentication → Policies**.
2. Add a policy to allow **INSERT and SELECT** for your application.
3. Ensure your API key is set up for database access.

---

## ⚡ Step 4: Connect Supabase to Your Python Code
1. Install the Supabase client:
   ```sh
   pip install supabase
   ```
2. Add your **Supabase credentials** in your Python script:
   ```python
   from supabase import create_client
   
   SUPABASE_URL = "your-supabase-url"
   SUPABASE_KEY = "your-api-key"
   supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
   ```
3. Test the connection by running:
   ```python
   response = supabase.table("stock_data").select("*").execute()
   print(response)
   ```

✅ **Your Supabase database is now set up and ready to use!** 🎉

