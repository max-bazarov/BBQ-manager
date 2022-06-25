# Endpoints

### `employees/`

| method |     description      | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all employees | <pre>[<br />  {<br />    "id": 1,<br />    "name": "Yakov Varnaev"<br />  }<br />]</pre>|
| [POST] | create an employee | <pre>{<br />  "id": 1,<br />  "name": "Yakov Varnaev"<br />}</pre> |

### `employees/{id}/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET] | detail data for employee | <pre>{<br />  "id": 1,<br />  "name": "Yakov Varnaev"<br />  "procedures": [<br />    {<br />      "id": 1,<br />      "name": "Hair Coloring"<br />    }<br />  ]</pre><br />}</pre> |
| [PUT/PATCH] | update employee data | <pre>{<br />  "id": 1,<br />  "name": "Yakov Varnaev"<br />}</pre> |

### `employees/{id}/procedures/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all employees procedures | <pre>[<br />  {<br />    "id": 1,<br />    "name": "Hair Coloring"<br />  }<br />]</pre> |

### `materials/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all materials | <pre>[<br />  {<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />  }<br />]</pre>
| [POST] | create a material | <pre>{<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />}</pre> |

### `materials/{id}/`

| method |     description       | example response |
|--------|-----------------------|------------------|
| [GET] | detail data for material | <pre>{<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />}</pre> |
| [PUT/PATCH] | update material data <br />[price must not be <br />updated if this was used already] | <pre>{<br />    "name": "Ginger Hair Color",<br />    "unit": "g",<br />    "price": 4<br />}</pre> |

### `procedures/`

| method |     description      | example response |
|--------|-----------------------|------------------|
| [GET]  | list of all procedures | <pre>[<br />  {<br />    "id": 1,<br />    "name": "Hair Coloring"<br />  }<br />]</pre>|
| [POST] | create a procedure | <pre>{<br />  "id": 1,<br />  "name": "Hair Coloring"<br />}</pre> |

### `procedures/{id}/`

| method |     description      | example response |
|--------|-----------------------|------------------|
| [GET]  | get procedure detail | <pre>{<br />  "id": 1,<br />  "name": "Hair Coloring"<br />}</pre>|
| [PUT/PATCH] | update a procedure | <pre>{<br />  "id": 1,<br />  "name": "Hair Coloring"<br />}</pre> 

### `purchaces/`
| method |     description      | example response |
|--------|-----------------------|------------------|
| [GET] | list of all purchaces | <pre>[<br />  {<br />    "date": "2022-06-25T11:57:02+0000",<br />    "is_paid_by_card": false,<br />    "procedure": {<br />      "name": "Haircut",<br />      "price": 1100, <br />      "id": 1<br />    },<br />    "master": {<br />      "id": 1,<br />      "name": "Yakov Varnaev" <br />    }<br />  }<br />]</pre> |
| [POST] | create a purchase |<pre>{<br />  "date": "2022-06-25T11:57:02+0000",<br />  "is_paid_by_card": false,<br />  "procedure": {<br />    "name": "Haircut",<br />    "price": 1100, <br />    "id": 1<br />  },<br />  "master": {<br />    "id": 1,<br />    "name": "Yakov Varnaev" <br />  }<br />}</pre> |

### `purchaces/{id}/`
| method |     description      | example response |
|--------|-----------------------|------------------|
| [GET] | get purchase detail |<pre>{<br />  "date": "2022-06-25T11:57:02+0000",<br />  "is_paid_by_card": false,<br />  "procedure": {<br />    "name": "Haircut",<br />    "price": 1100, <br />    "id": 1<br />  },<br />  "master": {<br />    "id": 1,<br />    "name": "Yakov Varnaev" <br />  }<br />}</pre> |
| [PUT/PATCH] | update purchace detail |<pre>{<br />  "date": "2022-06-25T11:57:02+0000",<br />  "is_paid_by_card": false,<br />  "procedure": {<br />    "name": "Haircut",<br />    "price": 1100, <br />    "id": 1<br />  },<br />  "master": {<br />    "id": 1,<br />    "name": "Yakov Varnaev" <br />  }<br />}</pre> |
| [DELETE] | delete purchace | <pre>{"id": 1}</pre> |

### `stats/?year={year}&month={month}&day={day}`
[GET] : get stats for a certain day/month/year
