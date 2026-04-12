# Normal Forms to Star Schema Example

This note shows how the same `customer orders` dataset can be modeled across normal forms and then reshaped into a warehouse-style star schema.

## Starting Point: Unnormalized Form

This version contains repeating groups like `product_1` and `product_2`, which makes it hard to query and maintain.

```text
customer_orders_raw
----------------------------------------------------------------------------------------------
customer_id | customer_name | customer_city | order_id | order_date | product_1 | product_2
1           | Alice         | Seattle       | 1001     | 2026-04-01 | Laptop    | Mouse
1           | Alice         | Seattle       | 1002     | 2026-04-02 | Keyboard  | null
2           | Bob           | Austin        | 1003     | 2026-04-02 | Monitor   | Cable
```

## First Normal Form (1NF)

In 1NF, each field contains a single atomic value and repeating groups are removed.

```text
customer_orders_1nf
-------------------------------------------------------------------
customer_id | customer_name | customer_city | order_id | order_date | product
1           | Alice         | Seattle       | 1001     | 2026-04-01 | Laptop
1           | Alice         | Seattle       | 1001     | 2026-04-01 | Mouse
1           | Alice         | Seattle       | 1002     | 2026-04-02 | Keyboard
2           | Bob           | Austin        | 1003     | 2026-04-02 | Monitor
2           | Bob           | Austin        | 1003     | 2026-04-02 | Cable
```

## Second Normal Form (2NF)

In 2NF, we remove partial dependencies on a composite key. If the effective key is `(order_id, product)`, then customer and order attributes should not be repeated on every product row.

```text
orders_2nf
-----------------------------------------------
order_id | customer_id | customer_name | customer_city | order_date
1001     | 1           | Alice         | Seattle       | 2026-04-01
1002     | 1           | Alice         | Seattle       | 2026-04-02
1003     | 2           | Bob           | Austin        | 2026-04-02
```

```text
order_items_2nf
-------------------------
order_id | product
1001     | Laptop
1001     | Mouse
1002     | Keyboard
1003     | Monitor
1003     | Cable
```

## Third Normal Form (3NF)

In 3NF, we remove transitive dependencies by separating customer information from order information.

```text
customers_3nf
--------------------------------
customer_id | customer_name | customer_city
1           | Alice         | Seattle
2           | Bob           | Austin
```

```text
orders_3nf
--------------------------------
order_id | customer_id | order_date
1001     | 1           | 2026-04-01
1002     | 1           | 2026-04-02
1003     | 2           | 2026-04-02
```

```text
order_items_3nf
-------------------------
order_id | product
1001     | Laptop
1001     | Mouse
1002     | Keyboard
1003     | Monitor
1003     | Cable
```

## Boyce-Codd Normal Form (BCNF)

BCNF is stricter than 3NF. Every determinant must be a candidate key.

Suppose `zip_code -> customer_city`. In that case, storing both `zip_code` and `customer_city` in the customer table can violate BCNF, so we split them.

```text
customers_bcnf
-------------------------
customer_id | customer_name | zip_code
1           | Alice         | 98101
2           | Bob           | 73301
```

```text
zip_codes_bcnf
-------------------------
zip_code | customer_city
98101    | Seattle
73301    | Austin
```

## Star Schema / Warehouse Model

For analytics, we often move away from highly normalized models and build a star schema that is easier to query.

### Dimension Tables

```text
dim_customer
-----------------------------------------
customer_key | customer_id | customer_name | customer_city
101          | 1           | Alice         | Seattle
102          | 2           | Bob           | Austin
```

```text
dim_product
--------------------------------
product_key | product_name
201         | Laptop
202         | Mouse
203         | Keyboard
204         | Monitor
205         | Cable
```

```text
dim_date
------------------------
date_key | full_date
20260401 | 2026-04-01
20260402 | 2026-04-02
```

### Fact Table

```text
fct_order_items
------------------------------------------------------
order_id | customer_key | product_key | order_date_key
1001     | 101          | 201         | 20260401
1001     | 101          | 202         | 20260401
1002     | 101          | 203         | 20260402
1003     | 102          | 204         | 20260402
1003     | 102          | 205         | 20260402
```

## Key Takeaway

- Normal forms are mainly used to reduce redundancy and preserve consistency in operational systems.
- Star schema is mainly used in analytics systems to simplify joins and support reporting.
- A normalized source model and a dimensional warehouse model can both represent the same business process, but they optimize for different goals.
