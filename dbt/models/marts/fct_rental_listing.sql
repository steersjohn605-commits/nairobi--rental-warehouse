select s.listing_id,n.neighbourhood,p.property_type,s.bedrooms,s.monthly_rent_kes,s.listed_on,s.is_synthetic
from {{ ref('stg_listings') }} s
join {{ ref('dim_neighbourhood') }} n using(neighbourhood)
join {{ ref('dim_property_type') }} p using(property_type)
