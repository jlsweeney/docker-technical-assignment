import psycopg2

with psycopg2.connect("dbname='postgres' user='postgres' host='db' password='example' port='5432'") as conn:
    print("Connected to database")

    with conn.cursor() as cur:

        cur.execute("""CREATE TABLE IF NOT EXISTS loans (
                            Repayment_Date DATE,
                            Loans INT,
                            Defaults INT,
                            Liquidations INT,
                            Created_at TIMESTAMP DEFAULT NOW()
                        );""")
        
        print("Created table")

        with open('loans.csv') as f:
            cur.copy_expert("COPY loans (Repayment_Date, Loans, Defaults, Liquidations) FROM STDIN DELIMITER ',' CSV HEADER;", f)
            cur.execute("UPDATE loans SET created_at = CURRENT_TIMESTAMP where created_at is null;")

        print("Loaded data")
conn.close()

