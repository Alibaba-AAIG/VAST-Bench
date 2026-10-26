# Customer directory query contract

`search_customers(connection, name_fragment, region)` returns Customer objects with
customer_id, display_name, email, and region. Only active records are included.
The name filter is a case-insensitive literal substring, including punctuation;
the region is an exact string match. Results are ordered by display_name and
customer_id. `connection` is a normal SQLite connection.
