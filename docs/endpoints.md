# Endpoints

### `employees/`
[GET] : list of all employees
[POST] : create an employee

## `employees/{id}/`
[GET] : detail data for employee
[PUT/PATCH] : update employee data

## `employees/{id}/procedures/`
[GET] : list of all employees procedures

### `materials/`
[GET] : list of all materials
[POST] : create a material

## `materials/{id}/`
[GET] : detail data for material
[PUT/PATCH] : update material data [price must not be updated if this was used already]

### `procedures/`
[GET] : list of all procedures
[POST] : create a procedure

## `procedures/{id}/`
[GET] : detail data for procedure
[PUT/PATCH] : update procedure data

### `purchaces/`
[GET] : list of all purchaces
[POST] : create a purchace

## `purchaces/{id}/`
[GET] : detail data for puchace
[PUT/PATCH] : update purchace data
[DELETE] : delete purchace

## `stats/?year={year}&month={month}&day={day}`
[GET] : get stats for a certain day/month/year
