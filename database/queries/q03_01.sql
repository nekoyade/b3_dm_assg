SELECT DISTINCT
        p.date, p.time_slot, v.name venue, s.name section, s.capacity,
        g.name group_name
    FROM performances p
    JOIN sections s ON p.section_id = s.id
    JOIN venues v ON s.venue_id = v.id
    JOIN groups g ON p.group_id = g.id
    WHERE p.date like '2023-%' and v.name = 'XB 東演芸ホール';
