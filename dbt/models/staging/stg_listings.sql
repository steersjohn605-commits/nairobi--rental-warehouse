with ranked as (
 select *, row_number() over(partition by listing_id order by listed_on desc) rn
 from raw.rental_listings
)
select listing_id,trim(neighbourhood) neighbourhood,lower(property_type) property_type,
 bedrooms,monthly_rent_kes,listed_on,source,is_synthetic
from ranked where rn=1 and monthly_rent_kes>0
