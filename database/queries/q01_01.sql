SELECT DISTINCT
        p.name, p.birth_date, p.address, r.role, h.phone, e.email
    FROM performers p
    JOIN phones h ON p.id = h.person_id
    JOIN emails e ON p.id = e.person_id
    JOIN roles r ON p.id = r.person_id
    WHERE r.role = 'dance'
