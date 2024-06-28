SELECT DISTINCT
        p.name, p.birth_date, p.address, i.instrument, h.phone, e.email
    FROM performers p
    JOIN phones h ON p.id = h.person_id
    JOIN emails e ON p.id = e.person_id
    JOIN instruments i ON p.id = i.person_id
    WHERE i.instrument like '%太鼓'
