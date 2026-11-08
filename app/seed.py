import os, random
from datetime import date,timedelta
import psycopg
DB=os.getenv("DATABASE_URL","postgresql://portfolio:portfolio@localhost:5434/rentals")
AREAS=["Kilimani","Westlands","Roysambu","Kasarani","South B","Ngara","Langata","Kileleshwa","Embakasi","Lavington"]
TYPES=["bedsitter","apartment","maisonette","studio"]
def main():
    rng=random.Random(42); rows=[]
    for i in range(1,501):
        area=rng.choice(AREAS); typ=rng.choice(TYPES); beds=0 if typ in ("studio","bedsitter") else rng.randint(1,4)
        base={"bedsitter":12000,"studio":18000,"apartment":26000,"maisonette":65000}[typ]
        rent=int(base*rng.uniform(.65,2.5)*(1+max(beds-1,0)*.55))
        rows.append((f"SYN-{i:04d}",area,typ,beds,rent,date.today()-timedelta(days=rng.randint(0,365)),"synthetic-seed",True))
    with psycopg.connect(DB) as c:
        c.execute("CREATE SCHEMA IF NOT EXISTS raw")
        c.execute("""CREATE TABLE IF NOT EXISTS raw.rental_listings(
          listing_id text PRIMARY KEY,neighbourhood text,property_type text,bedrooms int,
          monthly_rent_kes int,listed_on date,source text,is_synthetic boolean)""")
        c.executemany("""INSERT INTO raw.rental_listings VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
          ON CONFLICT(listing_id) DO UPDATE SET monthly_rent_kes=excluded.monthly_rent_kes,
          listed_on=excluded.listed_on""",rows)
    print(f"Seeded {len(rows)} synthetic rows")
if __name__=="__main__": main()
