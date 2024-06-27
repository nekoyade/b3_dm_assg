import datetime
import random


_addresses = [
    "A 県 X 市 XA 地区",
    "A 県 X 市 XB 地区",
    "A 県 X 市 XC 地区",
    "A 県 X 市 XD 地区",
    "A 県 X 市本町",
    "A 県 Y 町 YA 郡",
    "A 県 Y 町 YB 郡",
    "A 県 Y 町 YC 郡",
    "A 県 Z 市 ZA 区",
    "A 県 Z 市 ZB 区",
    "B 都 X 区 XA",
    "B 都 X 区 XB",
    "B 都 X 区 XC",
    "B 都 Y 区 YA",
    "C 県 X 市 XA 地区",
    "C 県 X 市 XB 地区",
]

def generate_address():
    return random.choice(_addresses)


_phone_count = 0

def generate_phones(n):
    global _phone_count
    result = []
    for _ in range(n):
        major = f"{_phone_count // 10000:03d}"
        minor = f"{_phone_count % 10000:04d}"
        result.append(major + "-" + minor)
        _phone_count += 1
    return result


_person_id_count = 0

def generate_person_id():
    global _person_id_count
    _person_id_count += 1
    result = f"PS{_person_id_count:06d}"
    return result


_kansuji_map = {
    "0": "零",
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
}

def convert_numbers_to_kansuji(numbers):
    global _kansuji_map
    result = ""
    for number in numbers:
        result += _kansuji_map[number]
    return result


_person_first_name_count = 0
_person_last_name_count = 0

def generate_person_name():
    global _person_first_name_count
    global _person_last_name_count
    if _person_last_name_count >= 100:
        _person_first_name_count += 1
        _person_last_name_count = 0
    first_name = convert_numbers_to_kansuji(
            f"{_person_first_name_count:02d}")
    last_name = convert_numbers_to_kansuji(
            f"{_person_last_name_count:02d}")
    _person_last_name_count += 1
    return first_name + " " + last_name


_date_minor_sup = datetime.datetime(2018, 12, 31, 23, 59, 59)
_date_minor_inf = datetime.datetime(2006,  1,  1,  0,  0,  0)
_date_adult_sup = datetime.datetime(2005, 12, 31, 23, 59, 59)
_date_adult_inf = datetime.datetime(1944,  1,  1,  0,  0,  0)
_date_student_sup = datetime.datetime(2005, 12, 31, 23, 59, 59)
_date_student_inf = datetime.datetime(2000,  1,  1,  0,  0,  0)

def generate_person_birth_date(is_adult, is_student):
    date_sup = ...
    date_inf = ...
    if is_student:
        global _date_student_sup
        global _date_student_inf
        date_sup = _date_student_sup
        date_inf = _date_student_inf
    elif is_adult:
        global _date_adult_sup
        global _date_adult_inf
        date_sup = _date_adult_sup
        date_inf = _date_adult_inf
    else:
        global _date_minor_sup
        global _date_minor_inf
        date_sup = _date_minor_sup
        date_inf = _date_minor_inf
    delta_sec = int((date_sup - date_inf).total_seconds())
    birth_date = \
        date_inf + datetime.timedelta(seconds=random.randint(0, delta_sec))
    return birth_date.strftime("%Y-%m-%d")


def generate_person_address(performs):
    if not performs:
        if random.random() < 0.25:
            return ""
    return generate_address()


def generate_person_emails(person_id, n):
    result = []
    for i in range(n):
        person_id_int = int(person_id[2:])
        result.append(f"ps{person_id_int:06d}_{i:02d}@example.com")
    return result


_roles = ["dance", "music"]

def generate_person_roles(performs):
    global _roles
    k = 1 if performs else 0
    l = 2 if performs else 0
    result = random.sample(_roles, random.randint(k, l))
    return result


_instruments = [
    "鉦",
    "締太鼓",
    "大太鼓",
    "笛",
    "三味線",
    "竹太鼓",
    "鼓",
]

def generate_person_instruments(roles, performs):
    if not performs:
        return []
    global _instruments
    l = 1 if "music" in roles else 0
    result = random.sample(_instruments, random.randint(l, 3))
    return result


class Person:
    def __init__(self, is_adult=True, is_student=False, performs=True):
        self.id = generate_person_id()
        self.name = generate_person_name()
        self.birth_date = generate_person_birth_date(is_adult, is_student)
        self.address = generate_person_address(performs)

        if is_adult:
            self.phones = generate_phones(random.randint(1, 2))
            self.emails = generate_person_emails(self.id, random.randint(0, 2))
            self.roles = generate_person_roles(performs)
            self.instruments = generate_person_instruments(
                self.roles, performs)
        else:
            self.phones = generate_phones(random.randint(0, 1))
            self.emails = generate_person_emails(self.id, random.randint(0, 1))
            self.roles = ["dance"] if performs else []
            self.instruments = generate_person_instruments(
                self.roles, performs)

    def to_code(self):
        return (
            "INSERT INTO persons VALUES "
            f"('{self.id}', '{self.name}', '{self.birth_date}', "
            f"'{self.address}');"
        )

    def generate_childs(self, households, n):
        childs = []
        for _ in range(n):
            child = Person(is_adult=False, performs=True)
            childs.append(child)
            households.append((self.id, child.id))
        return childs


def generate_performances(groups):
    performances = []
    dates = [
        "2022-08-20", "2022-08-21",
        "2023-08-20", "2023-08-21",
        "2024-08-20", "2024-08-21",
    ]
    time_slots = [
        "10:00", "11:00", "12:00",
        "15:00", "16:00", "17:00", "18:00",
    ]
    section_id_outside = [
        "SC001", "SC002", "SC003", "SC004",
    ]
    section_id_inside = [
        "SC005", "SC006", "SC007", "SC008",
        "SC009", "SC010", "SC011",
    ]
    _performance_id = 1
    for date in dates:
        for time_slot in time_slots:
            is_outside = ...
            section_ids = ...
            if "-08-20" in date:
                is_outside = True
                section_ids = section_id_outside
            else:
                is_outside = False
                section_ids = section_id_inside
            for section_id in section_ids:
                k = 3 if is_outside else 1
                for group_id in random.sample(groups, random.randint(1, k)):
                    performance_id = f"PF{_performance_id:06d}"
                    performances.append(
                        (performance_id, date, time_slot, group_id, section_id)
                    )
                    _performance_id += 1
    return performances


def generate_reservations(spectators, performances):
    reservations = []
    for performance in performances:
        performance_id, date, _, _, _ = performance
        if "-08-21" not in date:
            continue
        for spectator in random.sample(spectators, random.randint(1, 5)):
            _date = datetime.datetime.strptime(date, "%Y-%m-%d")
            secs = random.randint(24*60*60, 30*24*60*60)
            res_datetime = _date - datetime.timedelta(seconds=secs)
            res_date = res_datetime.strftime("%Y-%m-%d")
            res_time = res_datetime.strftime("%H:%M:%S")
            reservations.append(
                (spectator.id, performance_id, res_date, res_time)
            )
    return reservations


if __name__ == "__main__":
    random.seed(1)


    # Generation

    persons = []

    represented_by = []

    households = []
    persons_groups = []

    for _group_id in range(1, 6 + 1):
        n = random.randint(15, 20)
        tmp_persons = []
        for _ in range(n):
            person = Person(is_adult=True, is_student=False, performs=True)
            tmp_persons.append(person)
        adults = tmp_persons.copy()
        parents = random.sample(tmp_persons, random.randint(1, n//5))
        for parent in parents:
            childs = parent.generate_childs(households, random.randint(1, 3))
            tmp_persons.extend(childs)
        persons.extend(tmp_persons)

        group_id = f"GP{_group_id:03d}"
        for person in tmp_persons:
            persons_groups.append((person.id, group_id))

        representative = random.choice(adults)
        represented_by.append((group_id, representative.id))

    for _group_id in range(7, 8 + 1):
        n = random.randint(15, 20)
        tmp_persons = []
        for _ in range(n):
            person = Person(is_adult=True, is_student=True, performs=True)
            tmp_persons.append(person)
        persons.extend(tmp_persons)

        group_id = f"GP{_group_id:03d}"
        for person in tmp_persons:
            persons_groups.append((person.id, group_id))

        representative = random.choice(tmp_persons)
        represented_by.append((group_id, representative.id))

    for person in random.sample(persons, len(persons)//5):
        for _group_id in random.sample(range(1, 8 + 1), random.randint(1, 2)):
            group_id = f"GP{_group_id:03d}"
            tmp = (person.id, group_id)
            if tmp not in persons_groups:
                persons_groups.append((person.id, group_id))

    groups = [f"GP{i:03d}" for i in range(1, 8 + 1)]
    performances = generate_performances(groups)

    spectators = []
    for _ in range(100):
        is_adult = random.choice([True, True, True, False])
        spectator = Person(is_adult=is_adult, performs=False)
        spectators.append(spectator)

    reservations = generate_reservations(spectators, performances)

    persons.extend(spectators)

    phones = []
    emails = []
    roles = []
    instruments = []
    for person in persons:
        for phone in person.phones:
            phones.append((person.id, phone))
        for email in person.emails:
            emails.append((person.id, email))
        for role in person.roles:
            roles.append((person.id, role))
        for instrument in person.instruments:
            instruments.append((person.id, instrument))


    # Outputs

    persons_str = ""
    for person in persons:
        persons_str += person.to_code()
        persons_str += "\n"
    with open("persons.txt", "w", encoding="utf-8") as f:
        f.write(persons_str)

    phones_str = ""
    for person_id, phone in phones:
        tmp = (
            f"INSERT INTO phones VALUES ('{person_id}', '{phone}');"
        )
        phones_str += tmp
        phones_str += "\n"
    with open("phones.txt", "w", encoding="utf-8") as f:
        f.write(phones_str)

    emails_str = ""
    for person_id, email in emails:
        tmp = (
            f"INSERT INTO emails VALUES ('{person_id}', '{email}');"
        )
        emails_str += tmp
        emails_str += "\n"
    with open("emails.txt", "w", encoding="utf-8") as f:
        f.write(emails_str)

    roles_str = ""
    for person_id, role in roles:
        tmp = (
            f"INSERT INTO roles VALUES ('{person_id}', '{role}');"
        )
        roles_str += tmp
        roles_str += "\n"
    with open("roles.txt", "w", encoding="utf-8") as f:
        f.write(roles_str)

    instruments_str = ""
    for person_id, instrument in instruments:
        tmp = (
            f"INSERT INTO instruments VALUES ('{person_id}', '{instrument}');"
        )
        instruments_str += tmp
        instruments_str += "\n"
    with open("instruments.txt", "w", encoding="utf-8") as f:
        f.write(instruments_str)

    represented_by_str = ""
    for group_id, representative in represented_by:
        represented_by_str += f"{group_id} {representative}\n"
    with open("represented_by.txt", "w", encoding="utf-8") as f:
        f.write(represented_by_str)

    performances_str = ""
    for performance in performances:
        performance_id, date, time_slot, group_id, section_id = performance
        tmp = (
            "INSERT INTO performances VALUES "
            f"('{performance_id}', '{date}', '{time_slot}', '{group_id}', "
            f"'{section_id}');"
        )
        performances_str += tmp
        performances_str += "\n"
    with open("performances.txt", "w", encoding="utf-8") as f:
        f.write(performances_str)

    reservations_str = ""
    for reservation in reservations:
        reserved_by, performance_id, date, time = reservation
        tmp = (
            "INSERT INTO reservations VALUES "
            f"('{reserved_by}', '{performance_id}', '{date}', '{time}');"
        )
        reservations_str += tmp
        reservations_str += "\n"
    with open("reservations.txt", "w", encoding="utf-8") as f:
        f.write(reservations_str)

    households_str = ""
    for parent_id, child_id in households:
        tmp = (
            "INSERT INTO households VALUES ("
            f"'{parent_id}', '{child_id}');"
        )
        households_str += tmp
        households_str += "\n"
    with open("households.txt", "w", encoding="utf-8") as f:
        f.write(households_str)

    persons_groups_str = ""
    for person_id, group_id in persons_groups:
        tmp = (
            "INSERT INTO persons_groups VALUES ("
            f"'{person_id}', '{group_id}');"
        )
        persons_groups_str += tmp
        persons_groups_str += "\n"
    with open("persons_groups.txt", "w", encoding="utf-8") as f:
        f.write(persons_groups_str)
