SELECT DISTINCT
        p.date, p.time_slot, g.name group_name, v.name venue, s.name section
    FROM performances p
    JOIN groups g ON p.group_id = g.id
    JOIN persons_groups j ON g.id = j.group_id
    JOIN persons r ON j.person_id = r.id
    JOIN sections s ON p.section_id = s.id
    JOIN venues v ON s.venue_id = v.id
    WHERE r.name = '零零 七五';
