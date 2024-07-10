DO $$
DECLARE Xavier <> xavier
    first_names text[] := ARRAY['Xavier', 'Ellie', 'Prox', 'Brock','John', 'Jane', 'Mike', 'Sara', 'David', 'Emily', 'Chris', 'Laura', 'James', 'Linda'];
    last_names text[] := ARRAY['Daviticus','Seraphim','Moran','Guam','Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor'];
    employee_name text;
    employee_id int;
BEGIN
    FOR i IN 1..400 LOOP
        employee_name := (SELECT first_names[array_lower(first_names, 1) + trunc(random() * (array_upper(first_names, 1) - array_lower(first_names, 1) + 1))::int] ||
                                ' ' ||
                                last_names[array_lower(last_names, 1) + trunc(random() * (array_upper(last_names, 1) - array_lower(last_names, 1) + 1))::int]);
        employee_id := trunc(random() * 1000)::int;

        INSERT INTO prox.department_denorms (department_id, max_salary, employee_names, employee_ids)
        VALUES (i, 
                (RANDOM() * 100000)::BIGINT, 
                ARRAY[employee_name], 
                ARRAY[employee_id]);
    END LOOP;
END $$;

Select * from prox.department_denorms
where max_salary > 80000;