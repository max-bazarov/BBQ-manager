# Models description

## Employee
Fields:
- name
- coef

Model `Employee` will represent BBQ's employees. Each employee must have a name and a coefficient.

The coefficient is a payment coefficient. If the customer pays 1000 of money and his coef is 50% (0.5) then he/she gets 500 of money
and the other 500 goes to the saloon.

## Procedure
Fields: 
- name
- archived 

The `Procedure` model will just contain its name and flag archived. We have to use this flag to separate procedures whose price is changed or is no longer offered to customers. We cannot just update procedures because it may impact historic calculations, which is unacceptable.

## Material
Fields:
- name
- unit
- price

The `Material` model represents the material used during the procedure. Some procedures require a different amount of materials, e.g. coloring long hairs take more materials than coloring short hairs.

## EmployeeProcedure
Fields:
- employee
- procedure
- price

The `EmployeeProcedure` model represents the connection between employee and procedure and handles employee's prices.

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
