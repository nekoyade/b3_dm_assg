SELECT DISTINCT
        p.date, p.time_slot, g.name group_name, v.name venue, s.name section
    FROM performances p
    JOIN groups g ON p.group_id = g.id
    JOIN sections s ON p.section_id = s.id
    JOIN venues v ON s.venue_id = v.id
    WHERE g.name = '山谷連' and v.name like '%ホール'
        and p.time_slot = '12:00';
