# Models description

![alt text](https://github.com/Yakov-Varnaev/BBQ-manager/blob/main/docs/BBQ%20db.png?raw=true)

## Employee
Fields:
- name

Model `Employee` represents BBQ's employees.

## Procedure
Fields: 
- name

The `Procedure` model contains procedure's name.

## Material
Fields:
- name
- unit
- price
- archived

The `Material` model represents the material used during the procedure. Some procedures require a different amount of materials, e.g. coloring long hairs take more materials than coloring short hairs. If price of the material is changed, we should not update material price, because it will affect historic data. So, new material should be created and old one should be archived.

## EmployeeProcedure
Fields:
- employee
- procedure
- price
- coef
- archived

The `EmployeeProcedure` model represents the connection between employee and procedure and handles employee's prices. The coefficient is a payment coefficient. If the customer pays 1000 of money and his coef is 50% (0.5) then he/she gets 500 of money
and the other 500 goes to the saloon. Flag archived shows if procedure is archived. We have to use this flag to separate procedures whose price is changed or is no longer offered to customers. We cannot just update procedures because it may impact historic calculations, which is unacceptable.

## Purchase
Fields:
- time
- procedure
- is_paid_by_card

The `Purchase` model represents a customer visit to the saloon.

## UsedMaterials
Fields:
- material
- purchase
The `UsedMaterials` model represents a connection between purchase and materials used during the procedure.
