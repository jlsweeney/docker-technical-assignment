import psycopg2

with psycopg2.connect("dbname='postgres' user='postgres' host='db' password='example'") as conn:
    print("Connected to database")
    
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS default_liquidation_rolling_avg_hist (
                            Repayment_Date DATE,
                            Liquidation_to_Default_Ratio FLOAT,
                            LTD_Ratio_Rolling_Average FLOAT,
                            Created_At TIMESTAMP
                        );""")
        
        cur.execute("""INSERT INTO default_liquidation_rolling_avg_hist
                            select  
                                repayment_date, 
                                cast(liquidations as float)/NULLIF(defaults, 0) as Liquidation_to_Default_Ratio,
                                avg(cast(liquidations as float)/NULLIF(defaults, 0)) over (partition by created_at order by repayment_date rows between 6 preceding and current row) AS LTD_Ratio_Rolling_Average,
                                CURRENT_TIMESTAMP as Created_At
                            from loans l
                            where l.created_at in (select max(created_at) from loans);""")
        
        print("Data inserted")

conn.close()