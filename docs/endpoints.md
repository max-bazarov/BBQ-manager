# Endpoints

### `employees/`

| method |     description      | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all employees | <pre>[<br />  {<br />    "id": 1,<br />    "name": "Yakov Varnaev"<br />  }<br />]</pre>|
| [POST] | create an employee | <pre>{<br />  "id": 1,<br />  "name": "Yakov Varnaev"<br />}</pre> |

### `employees/{id}/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET] | detail data for employee | <pre>{<br />  "id": 1,<br />  "name": "Yakov Varnaev"<br />  "procedures": []<br />}</pre> |
| [PUT/PATCH] | update employee data | <pre>{<br />  "id": 1,<br />  "name": "Yakov Varnaev"<br />}</pre> |

### `employees/{id}/procedures/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all employees procedures | <pre>[]</pre> |

### `materials/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all materials | <pre>[<br />  {<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />  }<br />]</pre>
| [POST] | create a material | <pre>{<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />}</pre> |

### `materials/{id}/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET] | detail data for material | <pre>{<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />}</pre> |
| [PUT<br />PATCH] | update material data <br />[price must not be <br />updated if this was used already] | <pre>{<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />}</pre> |

### `procedures/`
[GET] : list of all procedures

[POST] : create a procedure

### `procedures/{id}/`
[GET] : detail data for procedure

[PUT/PATCH] : update procedure data

### `purchaces/`
[GET] : list of all purchaces

[POST] : create a purchace

### `purchaces/{id}/`
[GET] : detail data for puchace

[PUT/PATCH] : update purchace data

[DELETE] : delete purchace

### `stats/?year={year}&month={month}&day={day}`
[GET] : get stats for a certain day/month/year
